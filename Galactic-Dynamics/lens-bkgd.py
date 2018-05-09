'''
Original use of functions by Adam Bolton, 2009.
http://www.physics.utah.edu/~bolton/python_lens_demo/
'''

# Given a background source, this lenses it and plots both as output.
# The parameters for the lens can be changed but it's a point-like lens source

def lensed(gamp,gsig,gx,gy,gax,gpa,name,lamp=1.5,lsig=0.05,lx=0.,ly=0.,lax=1.,lpa=0.):
	import numpy as np
	import matplotlib.pyplot as plt
	import matplotlib.gridspec as gridspec
	from matplotlib import cm
	import lensdemo_funcs as ldf
	import matplotlib.patheffects as PathEffects

	# Package some image display preferences in a dictionary object, for use below:
	myargs = {'interpolation': 'nearest', 'origin': 'lower', 'cmap': cm.viridis}
	lensargs = {'interpolation': 'nearest', 'origin': 'lower', 'cmap': cm.viridis}

	# Make some x and y coordinate images:
	nx.ny = 501,501
	xhilo,yhilo = [-2.5, 2.5],[-2.5, 2.5]
	x = (xhilo[1] - xhilo[0]) * np.outer(np.ones(ny), np.arange(nx)) / float(nx-1) + xhilo[0]
	y = (yhilo[1] - yhilo[0]) * np.outer(np.arange(ny), np.ones(nx)) / float(ny-1) + yhilo[0]

	# Set some Gaussian blob image parameters and pack them into an array:
	g_amp = gamp	    # peak brightness value
	g_sig = gsig	    # Gaussian "sigma" (i.e., size)
	g_xcen = gx	    # x position of center
	g_ycen = gy	    # y position of center
	g_axrat = gax  	    # minor-to-major axis ratio
	g_pa = gpa	    # major-axis position angle (degrees) c.c.w. from x axis
	gpar = np.asarray([g_amp, g_sig, g_xcen, g_ycen, g_axrat, g_pa])

	# Set some SIE lens-model parameters and pack them into an array:
	l_amp = lamp	    # Einstein radius
	l_xcen = lx	    # x position of center
	l_ycen = ly   	    # y position of center
	l_axrat = lax  	    # minor-to-major axis ratio
	l_pa = lpa	    # major-axis position angle (degrees) c.c.w. from x axis
	lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])
	lenspar = np.asarray([l_amp, lsig, l_xcen, l_ycen, l_axrat, l_pa])

	# The following lines will plot the un-lensed and lensed images side by side:
	g_image = ldf.gauss_2d(x, y, gpar)		# the background source
	(xg, yg) = ldf.sie_grad(x, y, lpar)		# the SIE lens gradient
	g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)	# applying the gradient
	lens_source = ldf.gauss_2d(x, y, lenspar)	# creating lens (visually)
	lens_source[lens_source < 0.6] = np.nan		# threshold for cuts

	plt.figure(figsize=(8,4))
	gs1 = gridspec.GridSpec(1,2)
	gs1.update(wspace=0.03)
	cmap = plt.cm.viridis

	ax1 = plt.subplot(gs1[0])
	im = ax1.imshow(g_image,**myargs,clim=(0.5,2.2)) # set to make the lens the same always
	vmin, vmax = im.get_clim()			 # set to make the lens the same always
	ax1.set_yticklabels([]); ax1.set_xticklabels([])
	ax1.set_yticks([]); ax1.set_xticks([])

	txt = ax1.text(20,457,'Background Source', size=15, color='w')
	txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

	# Listing parameters on ax1
	txt = ax1.text(20,20,'amp:%s, sig:%s,\ncenter:(%s,%s),\naxrat:%s, pa:%s'\
		%(gpar[0],gpar[1],gpar[2],gpar[3],gpar[4],gpar[5]), size=13, color='w')
	txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

	ax2 = plt.subplot(gs1[1])
	ax2.imshow(g_lensimage,**myargs,clim=(vmin,vmax))
	ax2.imshow(lens_source,**lensargs,clim=(vmin,vmax))

	if lax == 1.: cir = plt.Circle((250,250),150,fill=False,ls='--',color='C0')
	if lax == 2.: cir = plt.Circle((250,250),150,fill=False,ls='--',color='C0')
	ax2.add_artist(cir)
	ax2.set_yticklabels([]); ax2.set_xticklabels([])
	ax2.set_yticks([]); ax2.set_xticks([])
	
	txt = ax2.text(20,457,'Lensed Image', size=15, color='w')
	txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

	#plt.savefig('gamp%sgaxrat%sx%sy%s.png'%(g_amp,g_axrat,g_xcen,g_ycen),dpi=200)
	#plt.savefig('test.png',dpi=200) # useful for troubleshooting
	plt.savefig('lens-still%s.pdf'%(name),dpi=200)	
	plt.close('all')

if __name__ == "__main__":
	import sys
	lensed(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),\
		float(sys.argv[5]),float(sys.argv[6]),str(sys.argv[7]))


