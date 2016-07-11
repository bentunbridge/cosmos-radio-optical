
# Script to look at and reduce with CASA 4.2.2 or later

# Data can be downloaded as
# wget -c http://almanas.jb.man.ac.uk/amsr/3C277p1/all_avg.ms.tar
# wget -c http://almanas.jb.man.ac.uk/amsr/3C277p1/3C286_C.clean.model.tt0.tar
# wget -c http://almanas.jb.man.ac.uk/amsr/3C277p1/all_avg_1.flags

# Steps 1-3 are not included here as they are the routine preparation
# of the full data set (many tens G) including sorting and averaging.

# Steps 4 and 5 must be run first to flag bad data.

# The calibration starts with step 6

# Consult http://www.e-merlin.ac.uk/data_red/CASA/3C277.1_cal.html
# to establish the inputs for tasks and then fill them in the gaps ** below.

#############################
# ENTER THE NUMBER OF THE STEP(s) TO RUN (e.g. [6,7]

step_title = {#1: 'Import data and list',
              #2: 'Sort and fixvis data and concatenate',
              #3: 'Time and channel average data',
              4: 'Check averaged data are present, inspect, quack and flag by channel',
              5: 'Flagging by time',
              6: 'Delay calibration',
              7: 'Setting the flux',
              8: 'Initial bandpass calibration, pre-gaincal inspection',
              9: 'Gain calibration of calibration sources',
              10: 'Determine and set fluxes of other calibrators',
              11: 'Derive bandpass with spectral index',
              12: 'Amp gain calibration of phase ref',
              13: 'Apply calibration from cal sources to all sources',
              14: 'Split out target'}


print 'Write the value for variables -> run the script from the beginning'
#definitions
#base = '/raid/scratch/bt2/work/im3shape_work/COSMOS/Radio_noise_simulations/clean_peel/'
#maskdir = base+'masks/'
#msfiledir = base+'msfiles/'
#msfile_original = base+'AS801_original_aips_correct_5_clipped_1.3.ms' #ms multisource file
msfile = "AS801_original_CLEANED_COSMOS.ms"
gain_solution = 'COSMOS_cal.K'

bases=['0521+166', '1024-008', 'COSMOS_F01','COSMOS_F02', 'COSMOS_F03', 'COSMOS_F04', 'COSMOS_F05', 'COSMOS_F06','COSMOS_F07', 'COSMOS_F08', 'COSMOS_F09', 'COSMOS_F10', 'COSMOS_F11', 'COSMOS_F12', 'COSMOS_F13', 'COSMOS_F14', 'COSMOS_F15', 'COSMOS_F16', 'COSMOS_F17','0925+003','COSMOS_F18','COSMOS_F19', 'COSMOS_F20', 'COSMOS_F21', 'COSMOS_F22', 'COSMOS_F23' ]
calibration=['0521+166', '1024-008', '0925+003']
targets=['COSMOS_F01','COSMOS_F02', 'COSMOS_F03', 'COSMOS_F04', 'COSMOS_F05', 'COSMOS_F06','COSMOS_F07', 'COSMOS_F08', 'COSMOS_F09', 'COSMOS_F10', 'COSMOS_F11', 'COSMOS_F12', 'COSMOS_F13', 'COSMOS_F14', 'COSMOS_F15', 'COSMOS_F16', 'COSMOS_F17','COSMOS_F18', 'COSMOS_F19', 'COSMOS_F20' , 'COSMOS_F21' , 'COSMOS_F22' , 'COSMOS_F23']

target = 'COSMOS_F01, COSMOS_F02, COSMOS_F03, COSMOS_F04, COSMOS_F05, COSMOS_F06','COSMOS_F07, COSMOS_F08, COSMOS_F09, COSMOS_F10, COSMOS_F11, COSMOS_F12, COSMOS_F13, COSMOS_F14, COSMOS_F15, COSMOS_F16, COSMOS_F17','COSMOS_F18, COSMOS_F19, COSMOS_F20, COSMOS_F21, COSMOS_F22, COSMOS_F23'
phref  = '1024-008'
bpcal  = '0521+166,0925+003'
leakcal = '0521+166'
fluxcal = '0925+003'

calsources='0521+166 , 1024-008 , 0925+003'
#phref+','+bpcal+','+fluxcal  # list of unique sources
#


antref="11"        # refant - usually - change if known to be bad.
#eMfactor =  0.938     # Flux scale factor if VLA values for 3C286 are used

gui = F               # F makes plot files only; T displays 'live' (needs interaction)


thesteps = []
try:
    print 'List of steps to be executed ...', mysteps
    thesteps = mysteps
except:
    print 'global variable mysteps not set'

if (thesteps==[]):
    thesteps = range(0,len(step_title))
    print 'Executing all steps: ', thesteps

#thesteps=[6,8,9,10,11,12,13,14]

# Owing to a current plotms bug, some plotfiles have to be renamed, this
# should not be necessary in the long term.

### 4) Check data, list and identify end channels to flag
mystep = 4

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

# Check whether data need loading
    if not os.path.exists(msfile):
        print 'Please check that all_avg.ms is in this directory'
        exit()

# Uncomment for Linux
#    os.system('rm -rf all_avg.listobs.txt')
#    listobs(vis=msfile, overwrite=T,
#            listfile='all_avg.listobs.txt')

    plotants(vis=msfile, figfile='plotants.png')

    plotuv(vis=msfile,maxnpts=10000000,symb='.',
           field=phref, figfile=phref+'_uv.png')

# Back up original flag state
    flagmanager(vis=msfile,
                mode='save',
                versionname='pre_quack')

    # Flag first quackinterval of each scan, before antennas all on source
    # Ascertain required interval in plotms
    # Inspect phase ref amp v. time, LL,RR,
    # average central chans, zoom in manually

    plotms(vis=msfile,
           field=phref,
           spw='0~3:20~43',
           avgchannel='24',
           xaxis='time',yaxis='amp',
           antenna=antref+'&Pi',           # change if necessary
           correlation='LL,RR',
           coloraxis='corr',
           showgui=gui,                    # change to F if necessary
           overwrite=True,plotfile='pre-quack.png')

# Flag first 40 s of each scan for all sources
    flagdata(vis=msfile,
                 mode='quack',quackinterval=40)

# re-plot to check
    plotms(vis=msfile,
           field='',                      # check all sources
           spw='0~3:20~43',
           avgchannel='24',
           xaxis='time',yaxis='amp',
           antenna=antref+'&Pi',           # change if necessary
           correlation='LL,RR',
           coloraxis='field',            # Now separate fields
           showgui=gui,                    # change to F if necessary
           overwrite=True,plotfile='quacked.png')

# Identify end channels to flag (same for all baselines/fields)
    plotms(vis=msfile,
       field=leakcal,
       gridrows=4,gridcols=1,
       xaxis='channel',yaxis='amp',
       antenna=antref+'&Kn',           # change if necessary
       correlation='LL,RR',
       avgtime='99999',    # if data mostly good
       avgscan=T,
       iteraxis='spw', coloraxis='corr',
       showgui=gui,                          # change to T if you want ,
       overwrite=True,plotfile=leakcal+'_avg_amp-chan.png')
    os.system('mv '+leakcal+'_avg_amp-chan?*.png '+leakcal+'_avg_amp-chan.png')

# Back up flags
    flagmanager(vis=msfile,
                mode='save',
                versionname='pre_endchans')

 # end chans
    flagdata(vis=msfile,mode='manual',
             spw='0:0~6;60~63,1:0~3;61~63,2:0~3;61~63,3:0~3;63')

#  plot again to confirm
    plotms(vis=msfile,
       field=leakcal,
       gridrows=4,gridcols=1,
       xaxis='channel',yaxis='amp',
       antenna=antref+'&Kn',           # change if necessary
       correlation='LL,RR',
       avgtime='99999',    # if data mostly good
       avgscan=T,
       iteraxis='spw', coloraxis='corr',
       showgui=gui,                          # change to T if you want ,
       overwrite=True,plotfile=leakcal+'_flagged_avg_amp-chan.png')
    os.system('mv '+leakcal+'_flagged_avg_amp-chan?*.png '+leakcal+'_flagged_avg_amp-chan.png')

# If you notice any other bad channels, check these in more detail

### 5) Flag bad data by timerange
mystep = 5

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

    flagmanager(vis=msfile,
                mode='save',
                versionname='pre_timeflagging')

# Identify obvious bad data
# If target is faint, don't flag until after some calibration
# Here, it is bright enough to tell good from bad!
    for f in bases:
        plotms(vis=msfile,
               gridrows=5,gridcols=1,
               field=f,
               avgchannel='7',
               xaxis='time',yaxis='amp',
               antenna=antref+'&*',           # change if necessary
               correlation='LL,RR',
               iteraxis='baseline', coloraxis='corr',
               showgui=gui,                    # change to T to inspect closely
               overwrite=True,plotfile=f+'_avg_amp-time.png')

        os.system('mv '+f+'_avg_amp-time?*.png '+f+'_avg_amp-time.png')

# If a source shows bad data, plot interactively and zoom/use locate
# to find the time/antenna affected.
# Write flag command file 'all_avg_1.flags'

    flagdata(vis=msfile,
            mode='list',
            inpfile=msfile+'_1.flags')

    for f in bases:
        plotms(vis=msfile,
               gridrows=5,gridcols=1,
               field=f,
               avgchannel='7',
               xaxis='time',yaxis='amp',
               antenna=antref+'&*',           # change if necessary
               correlation='LL,RR',
               iteraxis='baseline', coloraxis='corr',
               showgui=gui,                    # change to T to inspect closely
               overwrite=True,plotfile=f+'_flagged_avg_amp-time.png')

        os.system('mv '+f+'_flagged_avg_amp-time?*.png '+f+'_flagged_avg_amp-time.png')


### 6) Delay calibration
mystep = 6

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

# If phase-ref is weak, do bp cals only first and apply to all
# Here, phase ref is OK (see all sources have similar solutions).

# Plot baselines to refant for one bright source
# Phase against freq
    plotms(vis=msfile, field=leakcal, xaxis='frequency',
           gridrows=5,gridcols=1,iteraxis='baseline',
           yaxis='phase',ydatacolumn='data',antenna=antref+'&*',
           avgtime='60000',avgscan=True,correlation='LL,RR',
           coloraxis='corr',
           plotfile=leakcal+'_phase_pre-delay.png',
           showgui=gui,                    # change to T to inspect closely
           overwrite=True)
    os.system('mv '+leakcal+'_phase_pre-delay?*.png '+leakcal+'_phase_pre-delay.png')

# Phase against freq per 10-min on bright source to test for
# time stability
    plotms(vis=msfile, field=leakcal, xaxis='frequency',
           yaxis='phase',ydatacolumn='data',antenna=antref,
           avgtime='600',correlation='RR',
           coloraxis='time',plotfile=leakcal+'_phase10min_pre-delay.png',
           showgui=gui,                    # change to T to inspect closely
           overwrite=True)

# amp against time, longest baseline, average all channels
    plotms(vis=msfile, field=leakcal, xaxis='time',
           spw='0~1',avgchannel='7',#plotrange=[-1,-1,0,0.018],
           yaxis='amp',ydatacolumn='data',antenna=antref,
           avgtime='60',correlation='RR',
           coloraxis='spw',plotfile=leakcal+'_amp-allch_pre-delay.png',
           showgui=gui,                    # change to T to inspect closely
           overwrite=True)

# amp against time, longest baseline, single channel
    plotms(vis=msfile, field=leakcal, xaxis='time',
           spw='0~1', #plotrange=[-1,-1,0,0.018],
           yaxis='amp',ydatacolumn='data',antenna=antref,
           avgtime='60',correlation='RR',
           coloraxis='spw',plotfile=leakcal+'_amp-1ch_pre-delay.png',
           showgui=gui,                    # change to T to inspect closely
           overwrite=True)

# Derive gain solutions
    os.system('rm -rf '+gain_solution)
    gaincal(vis=msfile,
            gaintype='K',
            field=calsources,
            caltable=gain_solution,
            spw='0~1',solint='600s',
            refant=antref,
            minblperant=2,
            minsnr=2)

    plotcal(caltable=gain_solution,
            xaxis='time',
            yaxis='delay',
            subplot=321,
            iteration='antenna',
            figfile=gain_solution+'.png')



### 7) Setting the flux
mystep = 7

if(mystep in thesteps):
    print 'Step ', mystep, step_title[


    setjy(vis=msfile,
          field=fluxcal,
          standard='',
          model='')

    os.system('rm -rf '+fluxcal+'_model.png')
    plotms(vis=msfile, field=fluxcal, xaxis='uvwave',
           yaxis='amp', coloraxis='spw',ydatacolumn='model',
           correlation='LL,RR',
           showgui=gui,                    # change to T to inspect closely
           symbolsize=4, plotfile=fluxcal+'_model.png')


### 8) Initial bandpass calibration
mystep = 8

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

# Pre-calibrate phase and amp as a function of time

# First, phase: plot to estimate suitable solution interval
# constrained by longest baseline
    plotms(vis=msfile, field=leakcal, xaxis='time',
           spw='0~1',
           yaxis='phase',ydatacolumn='data',antenna=antref,
           coloraxis='spw',plotfile=leakcal+'_1ch_phase-time.png',
           showgui=gui,
           overwrite=True)

# Zoom in to help decide what phase solution interval to use
# The similar plot made for amplitude in Step 6 (delay) shows
# that the amplitudes are stable for longer.

    os.system('rm -rf bpcals_precal.p1')
    gaincal(vis=msfile,
        calmode='p',
        field=bpcal,
        caltable='bpcals_precal.p1',
        solint='30s',
        refant=antref,
        minblperant=2,
        gaintable=gain_solution,
        minsnr=2)

# Check solutions are not just noise
    plotcal(caltable='bpcals_precal.p1',
            xaxis='time',
            yaxis='phase',
            subplot=321,
            #plotrange=[-1,-1,-180,180],
            iteration='antenna',
            figfile='bpcals_precal.p1.png')

# Then amp and phase.
# Have to do sources separately because of normalisation

    os.system('rm -rf bpcals_precal.ap1')
    for bp in bpcal.split(','):
        gaincal(vis=msfile,
                calmode='ap',
                field=bp,
                caltable='bpcals_precal.ap1',
                solint='120s',
                solnorm=T,
                refant=antref,
                minblperant=2,
                append=T,
                gaintable=[gain_solution,'bpcals_precal.p1'],
                minsnr=2)

# Check there are no wild solutions
    plotcal(caltable='bpcals_precal.ap1',
            xaxis='time',
            yaxis='amp',
            subplot=321,
            iteration='antenna',
            figfile='bpcals_precal.ap1.png')

    os.system('rm -rf bpcal.B1')
    bandpass(vis=msfile,
        caltable='bpcal.B1',
        field=bpcal,
        fillgaps=16,
        solint='inf',combine='scan',
        solnorm=T,
        refant=antref,
        minblperant=2,
        gaintable=[gain_solution,'bpcals_precal.p1','bpcals_precal.ap1'],
        minsnr=3)

    # Plot bandpass solutions
    plotcal(caltable='bpcal.B1',xaxis='freq',
        #plotrange=[-1,-1,-180,180],
        iteration='antenna',yaxis='phase',subplot=321,
        figfile='bpcal.B1_phase.png')
    plotcal(caltable='bpcal.B1',xaxis='freq',
        iteration='antenna',yaxis='amp',subplot=321,
        figfile='bpcal.B1_amp.png')

# Apply delay and bandpass solutions to calibration sources to check
# bandpass calibration effect.

    applycal(vis=msfile,
             field=calsources,
             calwt=F,
             applymode='calonly',
             gaintable=[gain_solution,'bpcal.B1'],
             interp=['linear','nearest,linear'])

# Plot baselines to refant
    plotms(vis=msfile, field=phref, xaxis='frequency',
           gridrows=5,gridcols=1,iteraxis='baseline',
           yaxis='phase',ydatacolumn='data',antenna=antref+'&*',
           avgtime='600',correlation='LL,RR',overwrite=True,
           showgui=gui,                    # change to T to inspect closely
           coloraxis='scan',plotfile= phref+'_beforeBP_phase.png')
    os.system('mv '+phref+'_beforeBP_phase?*.png '+phref+'_beforeBP_phase.png')

    plotms(vis=msfile, field= phref, xaxis='frequency',
           gridrows=5,gridcols=1,iteraxis='baseline',
           yaxis='amp',ydatacolumn='data',antenna=antref+'&*',
           avgtime='600',correlation='LL,RR',overwrite=True,
           showgui=gui,                    # change to T to inspect closely
           coloraxis='scan',plotfile= phref+'_beforeBP_amp.png')
    os.system('mv  '+phref+'_beforeBP_amp?*.png  '+phref+'_beforeBP_amp.png')

    plotms(vis=msfile, field=phref, xaxis='frequency',
           gridrows=5,gridcols=1,iteraxis='baseline',
           yaxis='phase',ydatacolumn='corrected',antenna=antref+'&*',
           avgtime='600',correlation='LL,RR',overwrite=True,
           showgui=gui,                    # change to T to inspect closely
           coloraxis='scan',plotfile= phref+'_afterBP_phase.png')
    os.system('mv  '+phref+'_afterBP_phase?*.png  '+phref+'_afterBP_phase.png')

    plotms(vis=msfile, field= phref, xaxis='frequency',
           gridrows=5,gridcols=1,iteraxis='baseline',
           yaxis='amp',ydatacolumn='corrected',antenna=antref+'&*',
           avgtime='600',correlation='LL,RR',overwrite=True,
           showgui=gui,                    # change to T to inspect closely
           coloraxis='scan',plotfile= phref+'_afterBP_amp.png')
    os.system('mv  '+phref+'_afterBP_amp?*.png  '+phref+'_afterBP_amp.png')

# Use BP-corrected data to examine time-dependent fluctuations
# Use showgui=T to check for reasonable solution intervals
    plotms(vis=msfile, field=phref, xaxis='time',
           yaxis='phase',ydatacolumn='corrected',antenna=antref+'&*',
           iteraxis='baseline',avgchannel='7',
           correlation='LL',overwrite=True,
           showgui=gui,                    # change to T to inspect closely
           coloraxis='spw',plotfile= phref+'_afterBP_phase-time.png' )
    os.system('mv  '+phref+'_afterBP_phase-time?*.png  '+phref+'_afterBP_phase-time.png')

# Zoom in on a few scans.  Inspect several baselines including Mk2-Cm.
# Also inspect amplitude

### 9) Gain calibration of calibration sources
mystep = 9

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]



# Derive phase solutions

    os.system('rm -rf calsources.p1')
    gaincal(vis=msfile,
        calmode='p',
        caltable='calsources.p1',
        field=calsources,
        solint='30',
        refant=antref,
        minblperant=2,minsnr=2,
        gaintable=[gain_solution,'bpcal.B1'],
        interp=['linear','nearest,linear'])

    # Plot solutions
    plotcal(caltable='calsources.p1',xaxis='time',
        #plotrange=[-1,-1,-180,180],
        iteration='antenna',yaxis='phase',subplot=321,
        poln='L',figfile='calsources.p1_L.png')

    plotcal(caltable='calsources.p1',xaxis='time',
        #plotrange=[-1,-1,-180,180],
        iteration='antenna',yaxis='phase',subplot=321,
        poln='R',figfile='calsources.p1_R.png')

# Derive amp solutions

    os.system('rm -rf calsources.ap1')
    gaincal(vis=msfile,
            calmode='ap',
            caltable='calsources.ap1',
            field=calsources,
            solint='180s',
            refant=antref,
            minblperant=2,minsnr=2,
            gaintable=[gain_solution,'bpcal.B1','calsources.p1'],
            interp=['linear','nearest,linear','nearest'])

    # Plot solutions
    plotcal(caltable='calsources.ap1',xaxis='time',
        iteration='antenna',yaxis='amp',subplot=321,
        poln='L',figfile='calsources.ap1_L.png')

    plotcal(caltable='calsources.ap1',xaxis='time',
        iteration='antenna',yaxis='amp',subplot=321,
        poln='R',figfile='calsources.ap1_R.png')

### 10) Determine and set the fluxes of the calibration sources
mystep = 10

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

# Gains contain scale from correlator counts to known
# flux density in Jy
# Compare these with gains for other calibrators to estimate
# their flux densities
# Choose gainthreshold to get good SNR (trial and error)
# Too high a threshold - divergent gains add noise
# Too low - little data left, also worsens noise

    os.system('rm -rf calsources.ap1_flux calsources_flux.txt')
    calfluxes=fluxscale(vis=msfile,
                        caltable='calsources.ap1',
                        fluxtable='calsources.ap1_flux',
                        listfile='calsources_flux.txt',
                        gainthreshold=0.3,
                        antenna='19',      # Least sensitive
                        reference=fluxcal)

    eMcalfluxes={}
    for k in calfluxes.keys():
        if len(calfluxes[k]) > 4:
            a=[]
            a.append(calfluxes[k]['fitFluxd'])#*eMfactor)
            a.append(calfluxes[k]['spidx'][0])
            a.append(calfluxes[k]['fitRefFreq'])
            eMcalfluxes[calfluxes[k]['fieldName']]=a
# eMcalfluxes now contains the scaled flux density for each source

# Use these to set flux densities of calibrators
# See messages

    for f in eMcalfluxes.keys():
        setjy(vis=msfile,
              field=f,
              standard='manual',
              fluxdensity=eMcalfluxes[f][0],
              spix=eMcalfluxes[f][1],
              reffreq=str(eMcalfluxes[f][2])+'Hz')

# Plot the  models we have just set

    plotms(vis=msfile, field=bpcal, xaxis='frequency',
           yaxis='amp',ydatacolumn='model',
           coloraxis='spw',correlation='LL',
           customsymbol=T,symbolshape='circle',
           showgui=gui,                    # change to T to inspect closely
           symbolsize=5,plotfile='bpcal_model.png',overwrite=T)


### 11) Derive bandpass with spectral index
mystep = 11

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

    os.system('rm -rf bpcal.B2')
    bandpass(vis=msfile,
        caltable='bpcal.B2',
        field=bpcal,
        fillgaps=16,
        solint='inf',combine='scan',
        refant=antref,
        minblperant=2,
        solnorm=F,
        gaintable=[gain_solution,'calsources.p1','calsources.ap1_flux'],
        gainfield=bpcal,
        minsnr=3)

    # Plot bandpass solutions
    plotcal(caltable='bpcal.B2',xaxis='freq',
        plotrange=[-1,-1,-180,180],
        iteration='antenna',yaxis='phase',subplot=321,
        figfile='bpcal.B2_phase.png')
    plotcal(caltable='bpcal.B2',xaxis='freq',
        iteration='antenna',yaxis='amp',subplot=321,
        figfile='bpcal.B2_amp.png')

### 12) Derive new amp solutions for all cal sources  with improved bandpass table
mystep = 12

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

    os.system('rm -rf calsources.ap2')
    gaincal(vis=msfile,
            calmode='ap',
            caltable='calsources.ap2',
            field=calsources,
            solint='inf',
            refant=antref,
            minblperant=2,minsnr=2,
            gaintable=[gain_solution,'bpcal.B2','calsources.p1'],
            interp=['linear','nearest,linear','nearest'])

    # Plot solutions
    plotcal(caltable='calsources.ap2',xaxis='time',
        iteration='antenna',yaxis='amp',subplot=321,
        #plotrange=[-1,-1,0.01,0.06],
        poln='L',figfile='calsources.ap2_L.png')

    plotcal(caltable='calsources.ap2',xaxis='time',
        iteration='antenna',yaxis='amp',subplot=321,
        #plotrange=[-1,-1,0.01,0.06],
        poln='R',figfile='calsources.ap2_R.png')

### 13) Apply solutions to target sources and calibrators
mystep = 13

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]

    cals=calibration#bases
#    for t in targets:
#      cals.remove(t)
    for c in cals:
        applycal(vis=msfile,
                 field=c,
                 gainfield=[c, '',c,c],
                 calwt=F,
                 applymode='calflag',
                 gaintable=[gain_solution,'bpcal.B2','calsources.p1','calsources.ap2'],
                 interp=['linear','nearest,linear','linear','linear'],
                 flagbackup=F)

# Now apply corrections to the target
        for t in targets:
            applycal(vis=msfile,
                     field=t,
                     gainfield=[phref,'',phref,phref],
                     calwt=F,
                     applymode='calflag',  # Not too many failed solutions - OK to flag target data
                     gaintable=[gain_solution,'bpcal.B2','calsources.p1','calsources.ap2'],
                     interp=['linear','nearest,linear','linear','linear'],
                     flagbackup=T)

# Plotms - first check phase-ref - is it point-like?
    plotms(vis=msfile, field=phref, xaxis='uvdist',
           yaxis='amp',ydatacolumn='corrected',
           avgchannel='7',correlation='LL,RR',
           overwrite=True,
           showgui=gui,                    # change to T to inspect closely
           coloraxis='spw',plotfile=phref+'_amp-uvdist.png')

# If there is just a little bad data, no need to worry if the target
# is bright enough to self-calibrate

# Check target
    for t in targets:
        plotms(vis=msfile, field=t, xaxis='uvdist',
             yaxis='amp',ydatacolumn='corrected',
             avgchannel='7',correlation='LL,RR',
             overwrite=T,
             showgui=gui,                    # change to T to inspect closely
             coloraxis='spw',plotfile=t+'_amp-uvdist.png')

### 14) Split out corrected target
mystep = 14

if(mystep in thesteps):
    print 'Step ', mystep, step_title[mystep]
    for t in targets:
        os.system('rm -rf '+t+'.ms*')
        split(vis=msfile,
            field=t,
            outputvis=t+'.ms',
            keepflags=F)

# Fix for CASA 4.4 (not needed in 4.5)
        tb.open(t+'.ms',nomodify=F)
        SIDorig=tb.getcol('STATE_ID')
        SID=SIDorig*0
        SIDnew=SID-1
        tb.putcol('STATE_ID',SIDnew)
        tb.close()

