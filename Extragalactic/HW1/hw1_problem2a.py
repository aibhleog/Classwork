import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.integrate as integrate

plt.close('all')

# ------ defining constants ----- #
# -- using mks for convenience -- #
c = 2.998e8 # m / s
h = 6.626e-34 # m^s * kg / s
k = 1.31e-23 # J / K
b = 2.898e-3 # m * K

# ------ FUNCTIONS ----- #
# ----- Wien's Law ----- #
def wiens(T):
	return b / T # will be in meters

# ---- Planck's Law ---- #
def planck(x,T):
	return (2*h*c**2) / (x**5 * (np.exp((h*c)/(x*k*T))-1))

# ---- Integrate over Bandpass ---- #
def integrated_flux(nu,filt,flux):
    return integrate.trapz(filt * flux / nu, nu) / integrate.trapz(filt / nu, nu)
# ---------------------- #


# reading in bandpass data
filts = np.loadtxt('UBV_ma06.txt',skiprows=17)
ufilt = [filts[:,0],filts[:,1]] # wavelength in A
bfilt = [filts[:,2],filts[:,3]]
vfilt = [filts[:,4],filts[:,5]]


# -- calculating colors for BB -- #
temp = [10000]
lam = np.arange(1e-9,4e-6,1e-9) # in m

flux = []
for filt in [ufilt,bfilt,vfilt]:
	f = interp1d(lam*1e10,planck(lam,temp))
	indx = np.arange(len(filt[0]))
	indx = indx[filt[0] > 0]

	bb_match = f(filt[0][indx])
	flux.append(integrated_flux(2.998e18/filt[0][indx],filt[1][indx],bb_match))
flux = np.asarray(flux)


# plotting integrating example
plt.figure(figsize=(9,3))
plt.plot(lam*1e10,planck(lam,temp)/max(planck(lam,temp)),color='k',lw=2.)
plt.text(0.02,0.86,'Blackbody, T: 10$^4$ K',transform=plt.gca().transAxes,fontsize=15)

x = [3600,4350,5470]
nam = ['$U$','$B$','$V$']
count = 0
for filt in [ufilt,bfilt,vfilt]:
	indx = np.arange(len(filt[0]))
	indx = indx[filt[0] > 0]
	plt.plot(filt[0][indx],filt[1][indx]*1.2,color='k')
	plt.fill_between(filt[0][indx],filt[1][indx]*1.2,alpha=0.3,label=nam[count])
	
	plt.scatter(x[count],flux[count]/max(planck(lam,temp)),s=200,\
		edgecolor='k',color='C%s'%int(count))
	count += 1

plt.legend(frameon=False,fontsize=15)
plt.ylim(0.,1.5)	
plt.xlim(ufilt[0][0]-100,vfilt[0][-1]+100)
plt.ylabel('flux')
plt.xlabel('wavelength [$\AA$]')
plt.gca().set_yticklabels([])

plt.tight_layout()
plt.savefig('plots-data/hw1_prob2a.pdf',dpi=200)
plt.close('all')


