# imaging script in CASA 4.4.0
import shutil
import re
import os

#Calibration steps
thesteps = [0]
step_title = {0: 'clean image (clean)'}

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

caldir='/raid/scratch/bt2/work/im3shape_work/COSMOS/Radio_noise_simulations/clean_peel/calibration/'
maskdir='/raid/scratch/bt2/work/im3shape_work/COSMOS/Radio_noise_simulations/clean_peel/masks/'
outlierdir='/raid/scratch/bt2/work/im3shape_work/COSMOS/Radio_noise_simulations/clean_peel/outliers/'
files = []
name = []
for file in os.listdir(maskdir):
  if file.endswith(".clean.mask"):
    files.append(re.sub('.clean.mask', '', file))
    name.append(re.sub('AS801_original_CLEANED_', '', re.sub('.clean.mask', '', file)))

targets=['COSMOS_F01','COSMOS_F02', 'COSMOS_F03', 'COSMOS_F04', 'COSMOS_F05', 'COSMOS_F06','COSMOS_F07', 'COSMOS_F08', 'COSMOS_F09', 'COSMOS_F10', 'COSMOS_F11', 'COSMOS_F12', 'COSMOS_F13', 'COSMOS_F14', 'COSMOS_F15', 'COSMOS_F16', 'COSMOS_F17','COSMOS_F18', 'COSMOS_F19', 'COSMOS_F20' , 'COSMOS_F21' , 'COSMOS_F22' , 'COSMOS_F23']

#'COSMOS_F05',  'COSMOS_F07', 
name = ['COSMOS_F08', 'COSMOS_F09', 'COSMOS_F10', 'COSMOS_F11', 'COSMOS_F12', 'COSMOS_F13', 'COSMOS_F14']

print 'Numbe of .mask files ', len(files)

con='n'
for m in range(len(name)):
  print '.ms file:', name[m]
  msfile = name[m]+'/'+name[m]+'.ms' #ms multisource file
  imname=name[m]+'/clean_'+name[m]
  f_num=""#"13"
  maskfile = name[m]+'/AS801_original_CLEANED_'+name[m]+'.clean.mask'
  outlier = name[m]+'/AS801_outlier_file_'+name[m]+'.txt'
  myspw = '' #spw of interest, use myspw = '3' if your computer is slow
  antref="11"
  if not os.path.exists(name[m]):
    os.makedirs(name[m])
  if not os.path.exists(maskfile):
    shutil.copytree(maskdir+'AS801_original_CLEANED_'+name[m]+'.clean.mask', maskfile)
  if not os.path.exists(msfile):
    shutil.copytree(caldir+name[m]+'.ms', msfile)
  if not os.path.isfile(outlier):
    shutil.copy2(outlierdir+'AS801_outlier_file_'+name[m]+'.txt',   outlier)

  # description of step
  mystep = 0
  if(mystep in thesteps):
    casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
    print 'Step ', mystep, step_title[mystep]

    pb=0.5
    pbdir = 'PB05/'
    if not os.path.exists(pbdir):
      os.makedirs(pbdir)
    if not os.path.exists(pbdir+name[m]):
      os.makedirs(pbdir+name[m])

    if not os.path.exists(pbdir):
      imname = pbdir+imname
      shutil.copytree(name[m], pbdir+name[m]+'/')

    clean(vis=msfile,imagename=imname+".widefield",outlierfile="",field=f_num,spw="",selectdata=True,timerange="",uvrange="",antenna="",scan="",observation="",intent="",mode="mfs",resmooth=False,gridmode="widefield",wprojplanes=-1,facets=1,cfcache="cfcache.dir",rotpainc=5.0,painc=360.0,aterm=True,psterm=False,mterm=True,wbawp=False,conjbeams=True,epjtable="",interpolation="linear",niter=100000,gain=0.05,threshold="0.045mJy",psfmode="clark",imagermode="csclean",ftmachine="mosaic",mosweight=False,scaletype="SAULT",multiscale=[0],negcomponent=-1,smallscalebias=0.6,interactive=False,mask=maskfile,nchan=-1,start=0,width=1,outframe="",veltype="radio",imsize=[12000, 12000],cell=['0.35arcsec'],phasecenter="",restfreq="",stokes="I",weighting="natural",robust=0.0,uvtaper=False,outertaper=[''],innertaper=['1.0'],modelimage="",restoringbeam=[''],pbcor=False,minpb=pb,usescratch=True,noise="1.0Jy",npixels=0,npercycle=100,cyclefactor=1.5,cyclespeedup=-1,nterms=1,reffreq="",chaniter=False,flatnoise=True,allowchunk=False)
  

    clean(vis=msfile,imagename=pbdir+imname+".widefield",outlierfile="",field=f_num,spw="",selectdata=True,timerange="",uvrange="",antenna="",scan="",observation="",intent="",mode="mfs",resmooth=False,gridmode="widefield",wprojplanes=-1,facets=1,cfcache="cfcache.dir",rotpainc=5.0,painc=360.0,aterm=True,psterm=False,mterm=True,wbawp=False,conjbeams=True,epjtable="",interpolation="linear",niter=100000,gain=0.05,threshold="0.045mJy",psfmode="clark",imagermode="csclean",ftmachine="mosaic",mosweight=False,scaletype="SAULT",multiscale=[0],negcomponent=-1,smallscalebias=0.6,interactive=False,mask=maskfile,nchan=-1,start=0,width=1,outframe="",veltype="radio",imsize=[12000, 12000],cell=['0.35arcsec'],phasecenter="",restfreq="",stokes="I",weighting="natural",robust=0.0,uvtaper=False,outertaper=[''],innertaper=['1.0'],modelimage="",restoringbeam=['1.5', '1.4', '-50.0deg'],pbcor=True,minpb=pb,usescratch=True,noise="1.0Jy",npixels=0,npercycle=100,cyclefactor=1.5,cyclespeedup=-1,nterms=1,reffreq="",chaniter=False,flatnoise=True,allowchunk=False)
