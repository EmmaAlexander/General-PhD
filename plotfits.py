#!/usr/bin/env python
# Script to quickly load up a 2 dimensional .fits image file and save to a .png image (if desired). 

print('Importing modules') # Import modules
import numpy as np
from astropy.wcs import WCS
from astropy.io import fits
from astropy.nddata.utils import Cutout2D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
from optparse import OptionParser
import matplotlib.colors as colors

print('Getting inputs') # Get inputs and options
usage = "usage: %prog [options] -i FileName.fits"
parser = OptionParser(usage=usage)
parser.add_option("-i", "--infile", dest="infile", help="Name of input .fits file", metavar="INFILE")
parser.add_option("-o", "--outfile", dest="outfile", help="Name of output .png file", metavar="OUTFILE")
(options, args) = parser.parse_args()

if options.infile is not None: # Checking to see if input filename has been specified
    fitsfile = options.infile
    print('Reading file')
    #open file and get data
    hdu = fits.open(fitsfile)
    header = hdu[0].header
    #print header
    data = hdu[0].data[0,0,:,:]
    wcs = WCS(header)
    hdu.close()
else: #if no input filename specified, exit with error message
    print('Error: input fits file not specified')
    sys.exit(1)
    
if options.outfile is not None: #check to see if to save a png copy of fitsfile
    save_png = True
    outfile = options.outfile
else
    save_png = False

# Feeling plot, plot, plot! 
print('Plotting')
abs_data = np.absolute(data)
ax=plt.subplot(projection=wcs,slices=('x','y', 0,0))    
cmap= cm.jet
im=ax.imshow(data,origin='lower',cmap=cmap,vmin=np.nanmean(data),vmax=np.nanmax(data))
ra = ax.coords['ra']
dec=ax.coords['dec']
ra.set_major_formatter('hh:mm:ss')
ra.set_axislabel('Right Ascension')
dec.set_axislabel('Declination')
cbar=plt.colorbar(im)
cbar.set_label('Intensity [Jy/beam]')
# add a beam in the corner
width=bmaj/pixsize
height=bmin/pixsize
pad=5.
posx=0.+pad+width/2.
posy=0.+pad+height/2.
ellipse= Ellipse(xy=(posx,posy),width=width,height=height,angle=bpa+90,edgecolor='black',fc='black',lw=2)
ax.add_patch(ellipse)
# Save to a .png file if desired
if save_fig == True:
    plt.savefig(outfile,dpi=300)
plt.show()
