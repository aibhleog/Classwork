'''
Original use of functions by Adam Bolton, 2009.
http://www.physics.utah.edu/~bolton/python_lens_demo/
'''

# Given a background source, this lenses it and plots both as output.
# The parameters for the lens can be changed but for it's a point source

def lensed(gamp,gsig,gx,gy,gax,gpa,filename,lamp=0.1,lsig=0.05,lax=1.,lpa=0.):
	import numpy as np
	import matplotlib.pyplot as plt
	import matplotlib.gridspec as gridspec
	from matplotlib import cm
	import lensdemo_funcs as ldf
	import matplotlib.patheffects as PathEffects
	import matplotlib.animation as animation

	# Package some image display preferences in a dictionary object, for use below:
	myargs = {'interpolation': 'nearest', 'aspect':'auto', 'origin': 'lower', 'cmap': cm.viridis}
	lensargs = {'interpolation': 'nearest', 'aspect':'auto', 'origin': 'lower', 'cmap': cm.viridis}

	# Make some x and y coordinate images:
	nx.ny = 501,501
	xhilo,yhilo = [-2.5, 2.5],[-2.5, 2.5]
	x = (xhilo[1] - xhilo[0]) * np.outer(np.ones(ny), np.arange(nx)) / float(nx-1) + xhilo[0]
	y = (yhilo[1] - yhilo[0]) * np.outer(np.arange(ny), np.ones(nx)) / float(ny-1) + yhilo[0]

	# Set some Gaussian blob image parameters and pack them into an array:
	g_amp = gamp    # peak brightness value
	g_sig = gsig    # Gaussian "sigma" (i.e., size)
	g_xcen = gx     # x position of center
	g_ycen = gy     # y position of center
	g_axrat = gax   # minor-to-major axis ratio
	g_pa = gpa      # major-axis position angle (degrees) c.c.w. from x axis
	gpar = np.asarray([g_amp, g_sig, g_xcen, g_ycen, g_axrat, g_pa])

	fig = plt.figure(figsize=(8,4))
	gs1 = gridspec.GridSpec(1,2)
	gs1.update(wspace=0.035)
	fig.subplots_adjust(left=0.02,bottom=0.03,right=0.98,top=0.97)

	g_image = ldf.gauss_2d(x, y, gpar)
	ax1 = plt.subplot(gs1[0])
	im = ax1.imshow(g_image,**myargs,clim=(0.5,2.2)) # set to make the lens the same always
	vmin, vmax = im.get_clim()
	ax1.set_yticklabels([]); ax1.set_xticklabels([])
	ax1.set_yticks([]); ax1.set_xticks([])

	txt = ax1.text(20,457,'Background Source', size=15, color='w')
	txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

	ax2 = plt.subplot(gs1[1])

	def init():
		# Set some SIE lens-model parameters and pack them into an array:
		l_amp = lamp              # Einstein radius
		l_xcen = -2.5             # x position of center
		l_ycen = 2.5              # y position of center
		l_axrat = lax             # minor-to-major axis ratio
		l_pa = lpa                # major-axis position angle (degrees) c.c.w. from x axis
		lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])
		lenspar = np.asarray([l_amp, lsig, l_xcen, l_ycen, l_axrat, l_pa])

		# The following lines will plot the un-lensed and lensed images side by side:
		(xg, yg) = ldf.sie_grad(x, y, lpar)
		g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)
		lens_source = ldf.gauss_2d(x, y, lenspar)
		lens_source[lens_source < 0.6] = np.nan

		ax2.imshow(g_lensimage,**myargs,clim=(vmin,vmax))
		lens = ax2.imshow(lens_source,**lensargs,clim=(vmin,vmax))
		ax2.set_yticklabels([]); ax2.set_xticklabels([])
		ax2.set_yticks([]); ax2.set_xticks([])
	
		txt = ax2.text(20,457,'Lensed Image', size=15, color='w', zorder=5)
		txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])
		return lens,

	def lense_it(indx):
		moveit = np.arange(-2.5,2.5,0.1)
		# Set some SIE lens-model parameters and pack them into an array:
		l_amp = lamp              # Einstein radius
		l_xcen = moveit[indx]     # x position of center
		l_ycen = moveit[indx]*-1  # y position of center
		l_axrat = lax             # minor-to-major axis ratio
		l_pa = lpa                # major-axis position angle (degrees) c.c.w. from x axis
		lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])
		lenspar = np.asarray([l_amp, lsig, l_xcen, l_ycen, l_axrat, l_pa])

		# The following lines will plot the un-lensed and lensed images side by side:
		(xg, yg) = ldf.sie_grad(x, y, lpar)
		g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)
		lens_source = ldf.gauss_2d(x, y, lenspar)
		lens_source[lens_source < 0.6] = np.nan

		ax2.imshow(g_lensimage,**myargs,clim=(vmin,vmax))
		lens = ax2.imshow(lens_source,**lensargs,clim=(vmin,vmax))
		ax2.set_yticklabels([]); ax2.set_xticklabels([])
		ax2.set_yticks([]); ax2.set_xticks([])
	
		txt = ax2.text(20,457,'Lensed Source', size=15, color='w', zorder=5)
		txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])
		return lens,

	anim = animation.FuncAnimation(fig,lense_it,init_func=init,\
		frames=len(np.arange(-2.5,2.5,0.1)),interval=100,blit=True)
		
	anim.save('%s.gif'%(filename),fps=20,writer='imagemagick',\
		extra_args=['-vcodec','h264','-pix_fmt','yuv420p'])
	plt.close('all')

if __name__ == "__main__":
	import sys
	lensed(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),\
		float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),str(sys.argv[7]))


