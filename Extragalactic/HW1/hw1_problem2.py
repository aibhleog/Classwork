import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.integrate as integrate
from astropy.io import fits
from astropy.table import Table

# ------ defining constants ----- #
# -- using mks for convenience -- #
c = 2.998e8 # m / s
h = 6.626e-34 # m^s * kg / s
k = 1.38e-23 # J / K
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


# -- reading in Kurucz models -- #
modelnames = ['19000[g40]','12000[g40]','9500[g40]','8250[g45]','7250[g45]','6500[g45]','6000[g45]','5750[g45]','5250[g45]','4250[g45]','3750[g45]']
names = ['B3V','B8V','A0V','A5V','F0V','F5V','G0V','G5V','K0V','K5V','M0V']
models = []

own = False
for x in range(len(modelnames)):
    #t = fits.open('/home/aibhleog/Desktop/catalogs/ck04models/ckp00/ckp00_%s.fits'\
    t = fits.open('/home/aibhleog/Documents/Classes/Extragalactic/hw1_files/kp00/kp00_%s.fits'\
                  %(modelnames[x][:-5]))
    t2 = t[1].data
    tab = Table(t2)
    models.append(tab['%s'%(modelnames[x][-4:-1])])
    del t,t2
mwave = tab['WAVELENGTH']
# ---------------------- #

# reading in bandpass data
filts = np.loadtxt('UBV_ma06.txt',skiprows=17)
ufilt = [filts[:,0],filts[:,1]] # wavelength in A
bfilt = [filts[:,2],filts[:,3]]
vfilt = [filts[:,4],filts[:,5]]

# -- calculating colors for BB -- #
temp = [3000,6000,10000,15000]
alltemp = [25,15,10,8,6,5,4,3]
lam = np.arange(1e-9,4e-6,1e-9) # in m

mags = [[],[],[]]
for t in temp:
	count = 0
	#print(t)
	for filt in [ufilt,bfilt,vfilt]:
		f = interp1d(lam*1e10,planck(lam,t))
		indx = np.arange(len(filt[0]))
		indx = indx[filt[0] > 0]

		bb_match = f(filt[0][indx])
		bb_match_nu = bb_match * filt[0][indx]**2 / c
		int_flux = integrated_flux(2.998e18/filt[0][indx],filt[1][indx],bb_match_nu)
		mags[count].append(-2.5*np.log10(int_flux)+48.6)
		count += 1
mags = np.asarray(mags)

# -- ALL TEMPS -- #
oth_mags = [[],[],[]]
for t in alltemp:
	t *= 1e3 # convert to 1000's of K
	count = 0
	for filt in [ufilt,bfilt,vfilt]:
		f = interp1d(lam*1e10,planck(lam,t))
		indx = np.arange(len(filt[0]))
		indx = indx[filt[0] > 0]

		bb_match = f(filt[0][indx])
		bb_match_nu = bb_match * filt[0][indx]**2 / c
		int_flux = integrated_flux(2.998e18/filt[0][indx],filt[1][indx],bb_match_nu)
		oth_mags[count].append(-2.5*np.log10(int_flux)+48.6)
		count += 1
oth_mags = np.asarray(oth_mags)
# ---------------------- #

# -- Kurucz model colors -- #
k_mags = [[],[],[]]
for m in models:
	count = 0
	for filt in [ufilt,bfilt,vfilt]:
		f = interp1d(mwave,m)
		indx = np.arange(len(filt[0]))
		indx = indx[filt[0] > 0]

		bb_match = f(filt[0][indx])
		bb_match_nu = bb_match * filt[0][indx]**2 / c
		int_flux = integrated_flux(2.998e18/filt[0][indx],filt[1][indx],bb_match_nu)
		k_mags[count].append(-2.5*np.log10(int_flux)+48.6)
		count += 1
k_mags = np.asarray(k_mags)

# -- plotting data -- #
plt.figure(figsize=(6.7,8))
ax1 = plt.gca()

cmap = plt.get_cmap('Blues')
colors = cmap(np.linspace(0, 1.0, len(models)))

ax1.plot(k_mags[1]-k_mags[2],k_mags[0]-k_mags[1],color='k',ls=':',zorder=1,alpha=0.6,lw=1.)
for i in range(len(models)):
	ax1.scatter(k_mags[1][i]-k_mags[2][i],k_mags[0][i]-k_mags[1][i],edgecolor='k',\
		s=100,color=colors[i],label=names[i])
	#print('%s & %s & %s'%(names[i],round(k_mags[1][i]-k_mags[2][i],3),round(k_mags[0][i]-k_mags[1][i],3))) # Latex table coding

if own == True:
	ax1.text(0.3,0.9,'Data from personal\n   Kurucz models', transform=ax1.transAxes,fontsize=15)
else:	
	ax1.text(0.3,0.94,'Data from eCampus', transform=ax1.transAxes,fontsize=15)

ax1.set_ylim(2.45,-0.35)
ax1.set_xlim(-0.55,1.9)
ax1.legend(frameon=False,fontsize=15)
ax1.set_ylabel('U $\endash$ B',fontsize=17)
ax1.set_xlabel('B $\endash$ V',fontsize=17)

# plotting 
ylims = ax1.get_ylim()
xlims = ax1.get_xlim()
ax = ax1.twiny()

cmap = plt.get_cmap('inferno')
colors = cmap(np.linspace(0, 1.0, len(alltemp)))
colors = colors[::-1]

ax.plot(oth_mags[1]-oth_mags[2],oth_mags[0]-oth_mags[1],color='k',ls=':',zorder=1,alpha=0.6,lw=1.)
for i in range(len(alltemp)):
	t = alltemp[i]*1e3
	ax.scatter(oth_mags[1][i]-oth_mags[2][i],oth_mags[0][i]-oth_mags[1][i],edgecolor='k',\
		s=100,color=colors[i],label='%s K'%round(t))
	#print('%s & %s & %s'%(t,round(oth_mags[1][i]-oth_mags[2][i],3),round(oth_mags[0][i]-oth_mags[1][i],3))) # Latex table coding
ax.legend(frameon=False,loc=3,fontsize=15)

ax.set_ylim(ylims[0],ylims[1])
ax.set_xlim(xlims[0],xlims[1])
ax.set_xticklabels([])

plt.tight_layout()
if own == True:
	plt.savefig('plots-data/hw1_prob2.pdf',dpi=200)
else:	
	plt.savefig('plots-data/hw1_prob2_check.pdf',dpi=200)
plt.close('all')



