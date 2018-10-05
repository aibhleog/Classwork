import numpy as np
import matplotlib.pyplot as plt

# ------ defining constants ----- #
# -- using mks for convenience -- #
c = 2.998e8 # m / s
h = 6.626e-34 # m^s * kg / s
k = 1.31e-23 # J / K
b = 2.898e-3 # m * K

# ---- Planck's Law ---- #
def planck(x,T,which='lam'):
	if which == 'nu':
		bT = (2*h*x**3) / (c**2 * (np.exp((h*x)/(k*T))-1))
	else:
		bT = (2*h*c**2) / (x**5 * (np.exp((h*c)/(x*k*T))-1))
	return bT

def wiens(T):
	'''
	This function is just to make it easier
	to add the text at the peak of each blackbody
	'''
	return b / T # will be in meters    
# -------------------- #

# --- plotting both versions --- #
plt.figure(figsize=(9,6))

c = 2.998e8 # A / s
lam = np.arange(1e-9,4e-6,1e-9) # in m
nu = c / lam # converting to Hz using c [m/s]
lam_nm = lam * 1e6

ax = plt.gca()
ax.plot(lam_nm-10000,lam*planck(lam,7000)/1e7,lw=2.7,\
	color='k',alpha=0.4,label='using B$_{\lambda}$(T)')
ax.plot(lam_nm,nu*planck(nu,7000,which='nu')/1e7,ls=':',\
	color='g',label=r'using B$_{\nu}$(T)')

for t in [7000,6000,5000,4000,3000]:
	y = lam*planck(lam,t)/1e7; indx = y.tolist().index(max(y))
	ax.plot(lam_nm,lam*planck(lam,t)/1e7,lw=2.7,\
		alpha=0.2)#color='#A7C9DF')
	ax.plot(lam_nm,nu*planck(nu,t,which='nu')/1e7,ls=':',\
	color='k')
	ax.text(wiens(t)*1e6,y[indx]-0.15,'T: %s K'%t) 
	
ax.set_xlim(lam_nm[0],lam_nm[-10])
lims = ax.get_ylim()
ax.set_xlabel('wavelength [microns]')
ax.set_ylabel(r'$\lambda$B$_{\lambda}$(T) / 1e7')

ax2 = ax.twiny()
ax2 = ax2.twinx()
ax2.set_ylim(lims[0],lims[1])
ax2.set_xlim(lam_nm[0],lam_nm[-1])
ax2.set_ylabel(r'$\nu$B$_{\nu}$(T) / 1e7',rotation=270,labelpad=15)
ax2.set_xticklabels([])

ax.legend(frameon=False,fontsize=16)

plt.tight_layout()
plt.savefig('plots-data/hw1_prob1.pdf',dpi=200)
plt.close('all')
