#!/local/scratch/btunbrid/anaconda/bin/python
#


import numpy as np
import galsim
from astropy import units as u
from scipy import random
import sys
import os
import math
import nump_
import logging
import time
import galsim

from astropy.table import Table, Column, MaskedColumn, vstack
import astropy.coordinates as coord
import astropy.units as u
from astropy.io import ascii
from astropy.wcs import WCS
from astropy.io import fits
from astropy import wcs as pywcs
from astropy.coordinates import SkyCoord


rseed = 123456
# Read in galaxy catalog
cat_file_name = 'cosmos_vla_large_catalog_wXY_inc_unresolved_point_sources.fits'
dir = '/home/btunbrid/share/COSMOS/Radio_noise_simulations/catalog/'
VLA_large_resolved_catalog =  Table.read(dir+cat_file_name, format='fits')



# Read in field information
#Field_ID  name  RArad  DECrad  RAdeg  DECdeg
pointing_file = 'Pointing_Information.txt'
dir = '/home/btunbrid/share/COSMOS/Radio_noise_simulations/simulation/'
Pointings =  Table.read(dir+pointing_file, format='ascii')
Field_ID = Pointings['Field_ID']
name = Pointings['name']
RArad = Pointings['RArad']
DECrad = Pointings['DECrad']
RAdeg = Pointings['RAdeg']
DECdeg = Pointings['DECdeg']

f=int(os.environ['PBS_ARRAYID'])-1
#for f in range(len(Field_ID)):
if 'COSMOS' in str(name[f]):
  # image properties
  image_size = 2.0 * galsim.degrees # size of big image in each dimension
  pixel_scale = 0.3   # arcsec / pixel
  base_stamp_size = 120.*(0.35/pixel_scale)  
  stamp_xsize = base_stamp_size
  stamp_ysize = base_stamp_size   # separation of galaxies within image
  image_size = int((image_size / galsim.arcsec) / pixel_scale) # convert to pixels
  im_diff_deg = 2.0/2.
  print 'setup ', name[f]
  #galaxy list in field
  fID = []
  fra = []
  fdec = []
  fe1 = []
  fe2 = []
  fgal_flux = []
  fgal_rms_bg = []
  fgal_r0 = []
  resolved = []
  IDcount = 0
  RAmin , RAmax = (RAdeg[f]-im_diff_deg)*galsim.degrees, (RAdeg[f]+im_diff_deg)*galsim.degrees
  DECmin , DECmax = (DECdeg[f]-im_diff_deg)*galsim.degrees, (DECdeg[f]+im_diff_deg)*galsim.degrees
  for sc in range(len(VLA_large_resolved_catalog)):
    if float(VLA_large_resolved_catalog['ra'][sc])*galsim.degrees < RAmax and float(VLA_large_resolved_catalog['ra'][sc])*galsim.degrees > RAmin:
      if float(VLA_large_resolved_catalog['dec'][sc])*galsim.degrees < DECmax and float(VLA_large_resolved_catalog['dec'][sc])*galsim.degrees > DECmin:
        IDcount = IDcount + 1
        fID.append(VLA_large_resolved_catalog['ID'])
        fra.append(VLA_large_resolved_catalog['ra'][sc])
        fdec.append(VLA_large_resolved_catalog['dec'][sc])
        fe1.append(VLA_large_resolved_catalog['e1'][sc])
        fe2.append(VLA_large_resolved_catalog['e2'][sc])
        fgal_flux.append(VLA_large_resolved_catalog['p_flux'][sc])
        fgal_rms_bg.append(VLA_large_resolved_catalog['rms_bg'][sc])
        #bmajor and minor axis is in arcsecs
        fgal_r0.append(VLA_large_resolved_catalog['gal_r0'][sc])
        resolved.append(VLA_large_resolved_catalog['resolved'][sc])
  print 'read in sources'
  id_list = map(None, numpy.array(fID))

  big_fft_params = galsim.GSParams(maximum_fft_size=10008608)

  nobj = len(fID)
  print 'field', name[f], 'number of objects', nobj
  # Make output directory if not already present.
  if not os.path.isdir('output_point_sources'):
    os.mkdir('output_point_sources')

  gal_file_name = os.path.join('output_point_sources','simulated_VLA_large_'+name[f]+'.fits')
  gal_signal_to_noise = 100

  # intialise the images to be used
  full_image = galsim.ImageF(image_size, image_size, scale=pixel_scale)
  full_image.setOrigin(1,1)

  # set up the pixel grid 
  pix = galsim.Pixel(pixel_scale)

  # initilise an id counter, lists containing catalogue

  e1_list = []
  e2_list = []
  x_list = []
  y_list = []


  #World coordinate system for dull image.
  sky_center = galsim.CelestialCoord(ra=RAdeg[f]*galsim.degrees, dec=DECdeg[f]*galsim.degrees)
  theta = 0. * galsim.degrees
  # ( dudx  dudy ) = ( cos(theta)  -sin(theta) ) * pixel_scale
  # ( dvdx  dvdy )   ( sin(theta)   cos(theta) )
  dudx = math.cos(theta.rad()) * pixel_scale
  dudy = -math.sin(theta.rad()) * pixel_scale
  dvdx = math.sin(theta.rad()) * pixel_scale
  dvdy = math.cos(theta.rad()) * pixel_scale
  image_center = full_image.trueCenter()
  affine = galsim.AffineTransform(dudx, dudy, dvdx, dvdy, origin=full_image.trueCenter())
  wcs = galsim.TanWCS(affine, sky_center, units=galsim.arcsec)
  full_image.wcs = wcs

  gal_list = [ None ] * len(id_list)


  for i in range(nobj):
    index=i
    gal = gal_list[index]
    #Source Position
    cat_ra = fra[i]
    cat_dec = fdec[i]
    sky_coordinate = galsim.CelestialCoord(ra=float(cat_ra)*galsim.degrees, dec=float(cat_dec)*galsim.degrees)
    image_pos = wcs.toImage(sky_coordinate)
    # image_pos = PositionD(x=35999.5, y=35999.5)
    x = float((str(image_pos).split('(', 1)[-1]).rsplit(',', 1)[0])
    y = float((str(image_pos).rsplit(',', 1)[-1]).rsplit(')', 1)[0])
    # Account for the fractional part of the position:
    ix = int(math.floor(x+0.5))
    iy = int(math.floor(y+0.5))
    offset = galsim.PositionD(x-ix, y-iy)
    stampdiff = int(math.floor((stamp_xsize/2)+0.5))

    e1 = fe1[i]
    e2 = fe2[i]
    gal_flux = fgal_flux[i]
    gal_rms_bg = fgal_rms_bg[i]
    #bmajor and minor axis is in arcsecs
    gal_r0 = fgal_r0[i]

  #  print gal_r0, e1,e2
    # create and shear the galaxy
    gal = galsim.Gaussian(half_light_radius=gal_r0, flux=gal_flux)
    #gal = galsim.Exponential(flux=gal_flux, half_light_radius=gal_r0)
    if resolved[i]==1:
      gal.applyShear(g1=e1, g2=e2)

    gal_list[index] = gal

    print i, ix, iy, gal_r0, gal_flux
  
    # Don't convolve with the PSF
    final_gal = galsim.Convolve([pix,gal],gsparams=big_fft_params)
    # draw it onto the correct patch
    this_stamp_size = base_stamp_size
    stamp = galsim.ImageF(this_stamp_size,this_stamp_size)
  #  b = galsim.BoundsI(ix*stamp_xsize+1 , (ix+1)*stamp_xsize-1, 
  #           iy*stamp_ysize+1 , (iy+1)*stamp_ysize-1)
  #  sub_gal_image = full_image[b]

    # Draw the image
    #print 'draw'
    final_gal.drawImage(image=stamp, wcs=wcs.local(image_pos), offset=offset, method='no_pixel')
  #  final_gal.draw(sub_gal_image)
    #print 'drawn'
    # Recenter the stamp at the desired position:
    stamp.setCenter(ix,iy)
    #print 'check1'
    # Find the overlapping bounds:
    bounds = stamp.bounds & full_image.bounds
    #print 'check2', stamp, bounds, image_size, stamp[bounds], full_image[bounds]
    full_image[bounds] += stamp[bounds]
    #print 'check3'
  # write out the galaxy image
  all_gals_fname = gal_file_name
  print 'write to file '+gal_file_name
  full_image.write(gal_file_name)

