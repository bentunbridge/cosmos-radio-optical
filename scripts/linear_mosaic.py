# Scripts for linear mosaic VLA COSMOS

import os
import numpy as np
import shutil
import re
from StringIO import StringIO


#Calibration steps
thesteps = [0]
step_title = {0:  'Make Large Auto image'}

try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps


# The Python variable 'mysteps' will control which steps
# are executed when you start the script using
#   execfile('scriptForCalibration.py')
# e.g. setting
#   mysteps = [2,3,4]# before starting the script will make the script execute
# only steps 2, 3, and 4
# Setting mysteps = [] will make it execute all steps.

print 'Write the value for variables -> run the script from the beginning'
#definitions

BASEdir = os.getcwd()

targets=['COSMOS_F01','COSMOS_F02', 'COSMOS_F03', 'COSMOS_F04', 'COSMOS_F05', 'COSMOS_F06','COSMOS_F07', 'COSMOS_F08', 'COSMOS_F09', 'COSMOS_F10', 'COSMOS_F11', 'COSMOS_F12', 'COSMOS_F13', 'COSMOS_F14', 'COSMOS_F15', 'COSMOS_F16', 'COSMOS_F17','COSMOS_F18', 'COSMOS_F19', 'COSMOS_F20' , 'COSMOS_F21' , 'COSMOS_F22' , 'COSMOS_F23']


fieldID = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23,24,25]

msfile = '/raid/scratch/bt2/work/im3shape_work/COSMOS/Radio_noise_simulations/clean_peel/msfiles/AS801_original_CLEANED_COSMOS.ms'
images = [] 

for t in targets:
  imagedir = 'PB05/'+t+'/'
  images.append(imagedir+'clean_'+t+'.widefield.image')

im.open(msfile)

im.defineimage(nx=16000, ny=16000, cellx='0.35arcsec', celly='0.35arcsec', phasecenter=['J2000', '10h00m28.60s', '+02d12m21.00s'])

im.linearmosaic(images=images, mosaic='PB05/clean_COSMOS.widefield.pb05.image', fieldids = fieldID)

im.close()

