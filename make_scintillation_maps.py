import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import subprocess
import numpy as np

font = {'weight' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)

from tqdm import tqdm

dists = [1, 2, 4, 8, 16, 32, 64, 128]
ra = np.linspace(-np.pi, np.pi, 360)
dec= np.linspace(-np.pi/2, np.pi/2, 180)
X,Y = np.meshgrid(ra,dec)

for dist in tqdm(dists):
    
    fig = plt.figure(figsize=(20,8))
#     ax = plt.subplot(111, projection = 'mollweide')
    ax = plt.subplot(111)

    scint = np.empty((len(dec), len(ra)))
    for y in range(len(dec)):
        for x in range(len(ra)):
    #         print(x, y)
            output = subprocess.run(['./run_NE2001.pl', str(ra[x]*180/np.pi), str(dec[y]*180/np.pi), str(dist), '-1', 'SCINTIME'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            scint[y][x] = float(output.split()[2])
            print('Finished dist: %s, (ra, dec): (%s, %s)' % (dist, x, y))
    np.save('scint_array_dist_%s_kpc.npy' % dist, scint)

    plt.grid(color='w', linestyle='--', alpha=0.1)
    # ax.contour(X,Y,np.log(scint),levels=np.arange(-3, 10),colors='k', linewidths=1)
    c = ax.contourf(X,Y,np.log(scint*10),100,cmap='Greys')
    cbar = fig.colorbar(c, ticks=np.arange(-5, 10, step=2.))
    cbar.ax.set_ylabel(r'$\log_{10}[\Delta t_d\mathrm{\ (s)}]$', rotation=90)

    plt.plot([0.6667/180*np.pi], [-0.0362/180*np.pi], '+r', label='Sgr B2')

    plt.title(r'Scintillation Timescale Throughout the Milky Way ($d$=%s kpc, $V$=10 km/s)' % dist)
    plt.xticks(np.arange(-np.pi, np.pi, step=np.pi/6), np.arange(-180, 180, step=180//6))
    plt.yticks(np.arange(-np.pi/2, np.pi/2, step=np.pi/6), np.arange(-90, 90, step=180//6))
    plt.xlabel(r'$l$ (deg)')
    plt.ylabel(r'$b$ (deg)')
    plt.legend()
    
    plt.savefig('dist_%s_kpc.png' % dist)
    
    print('------------------------')

