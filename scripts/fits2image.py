import numpy as np
import pdb
from taskinit import gentools
ms = gentools(['ms'])[0]
ia = gentools(['ia'])[0]
#qa = gentools(['qa'])[0]
#execfile('fixImage_fixedcoord.py')

emerlin_ost_dir = '/local/scratch/btunbrid/work/im3shape_work/COSMOS/Radio_noise_simulations/output/'

def rescale_image(image_array,new_max):
  image_max = image_array.max()
  factor = float( new_max / image_max)
  image_array = np.multiply(image_array,factor)
  return image_array

def fixImage(datafile,
             centre_freq=1.4, #GHz
             bandwidth=2., # in fits header 2.5e+07 quoted 25000000
#GHz 37.5 MHz for 
             n_channels=7,
             peakvalue='0.024',#'0.0092034321',
             peakunit='Jy',
             pixel_scale=0.2, #pixel/arcmin
		#Central image is positioned at 150.119166668, 2.20573611111#'0h8m49.4s',
             Ra_central='10h02m28.67s',
             Dec_central='+02d38m28.64s',
             ost_template_image=emerlin_ost_dir+'ost_template.image',
             input_casa_image='simulated_VLA_large_casa.image'):
  '''Kludgey function to give an image from GalSim the correct co-ordinate
  system for observation with CASA.
  '''
  ia.open(datafile)
  input_array = ia.getchunk()
  input_array[np.isnan(input_array)] = 0.0
  
  ra_extent = input_array.shape[0]
  dec_extent = input_array.shape[1]

  ia.open(ost_template_image)
  template_csys = ia.coordsys()
  ia.done()
  
  delta_ra=str(pixel_scale)+'arcsec'
  delta_dec=str(pixel_scale)+'arcsec'
  template_csys.setobserver(value='Ben')
  template_csys.setincrement(value=(delta_ra,delta_dec),type='direction')
  
  new_shape = [ra_extent,dec_extent,1,1]
  
  ia.newimagefromshape(outfile=input_casa_image,
                       shape=new_shape,
                       csys=template_csys.torecord())
  
  ia.open(input_casa_image)
  ia.setbrightnessunit(unit='Jy/pixel')
  rescaled_image = rescale_image(input_array,
                                 qa.quantity(qa.convert(peakvalue+
                                                    peakunit,'Jy'))['value'])
  ia.putchunk(rescaled_image)
  ia.done()
  
  min_freq = str((float(centre_freq) - float(bandwidth)/2.0))+'GHz'
  max_freq = str((float(centre_freq) + float(bandwidth)/2.0))+'GHz'
  channel_inc = str(float(bandwidth) / n_channels)+'GHz'
  
  ia.open(input_casa_image)
  image_array = ia.getchunk()
  tmp_csys = ia.coordsys()

  axnames = tmp_csys.names()
  axisindex = 1

  refpix_RA = int(image_array.shape[0] / 2.0)
  refpix_Dec = int(image_array.shape[1] / 2.0)

  ref_RA = qa.convert(qa.unit(Ra_central),'rad')['value']
  ref_Dec = qa.convert(qa.unit(Dec_central),'rad')['value']
  ref_Freq = qa.convert(qa.unit(str(centre_freq)+'GHz'),'Hz')['value']
  ref_chan_inc = qa.convert(qa.unit(channel_inc),'Hz')['value']

  for axis in axnames:
    if axis == 'Right Ascension':
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'crval'+str(axisindex), hdvalue = float(ref_RA))
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'cunit'+str(axisindex), hdvalue = 'rad')
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'crpix'+str(axisindex), hdvalue = refpix_RA)
      ra_extent = str(image_array.shape[axisindex-1] * tmp_csys.increment()['numeric'][axisindex-1])+tmp_csys.units()[axisindex-1]
    print axis
    if axis == 'Declination':
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'crval'+str(axisindex), hdvalue = float(ref_Dec))
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'cunit'+str(axisindex), hdvalue = 'rad')
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'crpix'+str(axisindex), hdvalue = refpix_Dec)
      dec_extent = str(image_array.shape[axisindex-1] * tmp_csys.increment()['numeric'][axisindex-1])+tmp_csys.units()[axisindex-1]

#    if axisindex ==1:
#        sign=-1.
#    else:
#        sign=+1.
    sign=1.
    if axis == 'Frequency':
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'crval'+str(axisindex), hdvalue = float(ref_Freq))
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'cunit'+str(axisindex), hdvalue = 'Hz')
      imhead(imagename = input_casa_image, mode = 'put', hdkey = 'cdelt'+str(axisindex), hdvalue = float(ref_chan_inc)*sign)
    axisindex +=1 

  cdelt1 = imhead(imagename = input_casa_image, mode = 'get', hdkey = 'cdelt1')
  imhead(imagename = input_casa_image, mode = 'put', hdkey = 'cdelt1', hdvalue = -1*float(cdelt1['value']))

  ia.done()

if __name__=='__main__':
  fixImage('./output/simulated_VLA_large_inc_unresolved.fits', input_casa_image='./output/simulated_VLA_large_inc_unresolved.image')
