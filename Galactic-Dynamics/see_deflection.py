'''
Original use of functions by Adam Bolton, 2009.
http://www.physics.utah.edu/~bolton/python_lens_demo/
'''

# This code allows you to view the deflection gradients in both x and y directions.
def deflection(lamp=1.5,laxrat=1.)
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
	nx = 501
	ny = 501
	xhilo = [-2.5, 2.5]
	yhilo = [-2.5, 2.5]
	x = (xhilo[1] - xhilo[0]) * np.outer(np.ones(ny), np.arange(nx)) / float(nx-1) + xhilo[0]
	y = (yhilo[1] - yhilo[0]) * np.outer(np.arange(ny), np.ones(nx)) / float(ny-1) + yhilo[0]

	# Set some SIE lens-model parameters and pack them into an array:
	l_amp = 1.5	    # Einstein radius
	l_xcen = 0.	    # x position of center
	l_ycen = 0.   	    # y position of center
	l_axrat = 1.  	    # minor-to-major axis ratio
	l_pa = 0.	    # major-axis position angle (degrees) c.c.w. from x axis
	lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])
	lenspar = np.asarray([l_amp, 0.05, l_xcen, l_ycen, l_axrat, l_pa])

	# The following lines will plot the un-lensed and lensed images side by side:
	(xg, yg) = ldf.sie_grad(x, y, lpar)

	plt.figure(figsize=(8,4))
	gs1 = gridspec.GridSpec(1,2)
	gs1.update(wspace=0.03)
	cmap = plt.cm.viridis
	cir = plt.Circle((250,250),150,fill=False,ls='--',color='C0')

	ax1 = plt.subplot(gs1[0])
	im = ax1.imshow(xg,**myargs)#,clim=(0.5,2.2)) # set to make the lens the same always
	vmin, vmax = im.get_clim()
	ax1.add_artist(cir)
	ax1.set_yticklabels([]); ax1.set_xticklabels([])
	ax1.set_yticks([]); ax1.set_xticks([])

	txt = ax1.text(20,457,'x deflection', size=15, color='w')
	txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

	cir = plt.Circle((250,250),150,fill=False,ls='--',color='C0')
	ax2 = plt.subplot(gs1[1])
	ax2.imshow(yg,**myargs,clim=(vmin,vmax))
	ax2.add_artist(cir)
	ax2.set_yticklabels([]); ax2.set_xticklabels([])
	ax2.set_yticks([]); ax2.set_xticks([])

	txt = ax2.text(20,457,'y deflection', size=15, color='w')
	txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

	#plt.savefig('test.png',dpi=200) # useful for troubleshooting
	plt.savefig('deflection.pdf',dpi=200)	
	plt.close('all')


if __name__ == "__main__":
	import sys
	try: amp = float(sys.argv[1])
	except IndexError: amp = 1.5
	try: rat = float(sys.argv[2])
	except IndexError: rat = 1.
	
	deflection(amp,rat)

