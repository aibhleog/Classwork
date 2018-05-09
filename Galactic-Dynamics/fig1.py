'''
This script creates Figure 1 in my project report.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc,Ellipse

def angcurve(start,end,w,h):
	x1,y1 = start[0],start[1]
	x2,y2 = end[0],end[1]
	arc = Arc((x1+0.5*(x2-x1),y2+0.5*abs(y2-y1)),w,h,theta1=-40,theta2=60)
	return arc

f,ax = plt.subplots(1,1,figsize=(8,3))
ax.plot([0.85,0.93],[0,0.15],color='k'); ax.plot([0.85,0.93],[0,-0.15],color='k')
ell = Ellipse((0.92,0),0.02,0.21,color='k')
ax.add_patch(ell)

ax.plot([1,3.05],[0,0],ls='--',color='k')
ax.plot([1,2.5],[0,1.5],lw=2.5,color='C0',zorder=4)
ax.plot([1,3],[0,1],ls=':',color='k')

ax.plot([2.5,3],[1.5,2],lw=2.,ls='--',color='k')
ax.plot([2.505,3],[1.5,1],lw=2.5,color='C0')

alpha = angcurve([2.57,1.50],[2.59,1.45],0.1,0.3)
beta = angcurve([1.97,0.65],[2.02,-0.2],0.15,0.65)
theta = angcurve([1.5,0.65],[1.52,-0.2],0.15,0.7)
ax.add_patch(alpha)
ax.add_patch(beta)
ax.add_patch(theta)

ax.scatter(3.05,2.02,marker='*',s=200,facecolors='none',edgecolors='C0')
ax.scatter(3.05,1.05,marker='*',s=200,color='C0',edgecolors='k')
ax.scatter(2.507,0.,marker='o',s=600,color='k')

ax.text(1.605,0.33,r'$\theta$',fontsize=15)
ax.text(2.09,0.2,r'$\beta$',fontsize=15)
ax.text(2.68,1.4,r'$\alpha$',fontsize=15)
ax.text(2.68,1.44,r'^',fontsize=14)

ax.text(3.108,1.95,'(I)',fontsize=14)
ax.text(3.1,0.92,'(S)',fontsize=14)
ax.text(2.55,0.25,'(L)',fontsize=14)

y = -0.5
ax.plot([1,2.5],[y,y],color='k')
ax.plot([1,1],[y+0.12,y-0.12],color='k');plt.plot([2.5,2.5],[y+0.12,y-0.12],color='k')
ax.plot([2.5,3],[y-0.3,y-0.3],color='k')
ax.plot([2.5,2.5],[y-0.3+0.12,y-0.3-0.12],color='k');plt.plot([3,3],[y-0.3+0.12,y-0.3-0.12],color='k')
ax.plot([1,3],[y-0.6,y-0.6],color='k')
ax.plot([1,1],[y-0.6+0.12,y-0.6-0.12],color='k');plt.plot([3,3],[y-0.6+0.12,y-0.6-0.12],color='k')

ax.text(1.7,y-0.37,'D$_{OL}$',fontsize=15)
ax.text(2,y-1.,'D$_{OS}$',fontsize=15)
ax.text(2.7,y-0.15,'D$_{LS}$',fontsize=15)

ax.set_xlim(0.84,3.13)
plt.axis('off')
plt.tight_layout()
#plt.savefig('test.png',dpi=200) # useful for troubleshooting
plt.savefig('fig1.png',dpi=200)
plt.close('all')


