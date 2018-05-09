'''
This script creates Figure 2 in my project report.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc,Ellipse

def angcurve(start,end,w,h):
	x1,y1 = start[0],start[1]
	x2,y2 = end[0],end[1]
	arc = Arc((x1+0.5*(x2-x1),y2+0.5*abs(y2-y1)),w,h,theta1=-40,theta2=60)
	return arc

shift = 0.
f,ax = plt.subplots(1,1,figsize=(8,2.35))
ax.plot([0.85-shift,0.93-shift],[0,0.15],color='k'); ax.plot([0.85-shift,0.93-shift],[0,-0.15],color='k')
ell = Ellipse((0.92-shift,0),0.02,0.21,color='k')
ax.add_patch(ell)

ax.plot([1-shift,3],[0,0],ls=':',color='k')
ax.plot([1-shift,2],[0,0.5],lw=2,color='C0',zorder=4)
ax.plot([1-shift,2],[0,-0.5],lw=2,color='C0',zorder=4)

ax.text(1.69,0.11,r'$\theta_E$',fontsize=15)
theta = angcurve([1.85-shift,0.65],[1.32-shift,-0.4],0.15,0.4)
ax.add_patch(theta)

ax.text(3.0,0.2,'(S)',fontsize=14)
ax.text(2.07,0.15,'(L)',fontsize=14)

ax.plot([2,3.03],[0.5,1],lw=2.,ls='--',color='k')
ax.plot([2,3.03],[-0.5,-1],lw=2.,ls='--',color='k')
ax.plot([2.01,3],[0.5,0],lw=2,color='C0')
ax.plot([2.01,3],[-0.5,0],lw=2,color='C0')

ax.scatter(3.05,0.,marker='*',s=200,color='C0',edgecolors='k')
ax.scatter(2.015,0.,marker='o',s=400,color='k')
ell = Ellipse((3.05,0),0.2,2.,lw=3.,color='C0',fill=False)
ax.add_patch(ell)

ax.set_xlim(0.84,3.23)
plt.axis('off')
plt.tight_layout()
#plt.savefig('test.png',dpi=200) # useful for troubleshooting
plt.savefig('fig2.png',dpi=200)
plt.close('all')





