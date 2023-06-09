# Make lightcurve of NuSTAR evt solar data, both FPMA and FPMB 
# and return pandas dataframe (optionally can save to csv as well)
# 
# Only does any other filtering (xy, det_id) if engery filtering
# 
# If det_id is given then xy_range is ignored
# 
# If no outfile given then no .csv file created
# 
# Default return livetime and rates, lvt=False will return/save rate only
# 
# In theory could do using astropy.table.Table with
# from astropy.table import Table
# t=Table.read(maindir+nsid+'/hk/nu'+nsid+fpm+'_fpm.hk',hdu=1).to_pandas()
# but doesn't load header info so can't convert the time, so have to do more manual fit.open()  
# 
# 24-Sep-2022 IGH
# 11-Apr-2023 Tweaked for nsx plotting
# 26-Apr-2023 Added option to return more hk info
# -----------------------------------

from astropy.io import fits
import astropy.time as atime
import astropy.units as u

import numpy as np
import sunpy.map

import nustar_pysolar as nustar
import pandas as pd

import warnings
warnings.simplefilter('ignore')

# ------------------------------------------
# Find the centre of a NuSTAR map
def nsmapcen(nsmap):
    nnx=np.sum(nsmap.data,0)
    nny=np.sum(nsmap.data,1)

    idx=np.where(nnx > 0)
    cx=int((np.max(idx)+np.min(idx))/2)
    idy=np.where(nny > 0)
    cy=int((np.max(idy)+np.min(idy))/2)
    pw=nsmap.pixel_to_world(cx*u.pix,cy*u.pix)
    return pw, cx*u.pix, cy*u.pix

# ------------------------------------------
# Lightcurve with livetime and rate per FPM
def nsrate(maindir='',nsid='',clid='06_cl_sunpos',outfile='',\
        englow=0,enghigh=0,xy_range=[],det_id='',lvt=True, hk=False):

    fpm='A'
    hdulist = fits.open(maindir+nsid+'/event_cl/nu'+nsid+fpm+clid+'.evt')
    evda=hdulist[1].data
    hdra = hdulist[1].header
    hdulist.close()

    hdulist = fits.open(maindir+nsid+'/hk/nu'+nsid+fpm+'_fpm.hk')
    lda=hdulist[1].data
    lhdra = hdulist[1].header
    hdulist.close()

    fpm='B'
    hdulist = fits.open(maindir+nsid+'/event_cl/nu'+nsid+fpm+clid+'.evt')
    evdb=hdulist[1].data
    hdrb = hdulist[1].header
    hdulist.close()

    hdulist = fits.open(maindir+nsid+'/hk/nu'+nsid+fpm+'_fpm.hk')
    ldb=hdulist[1].data
    lhdrb = hdulist[1].header
    hdulist.close()

    # Sort out the time index of the livetimes
    mjdref=atime.Time(hdra['mjdrefi'],format='mjd')
    ltimsa=atime.Time(mjdref+lda['time']*u.s,format='mjd')
    ltimsb=atime.Time(mjdref+ldb['time']*u.s,format='mjd')

    # If not englow or enghigh specified don't filter the evt
    if (englow!=0) and (enghigh!=0):
        if (len(xy_range)==4):
            evda=nustar.filter.event_filter(evda,fpm='A',energy_low=englow, energy_high=enghigh,hdr=hdra,xy_range=xy_range)
            evdb=nustar.filter.event_filter(evdb,fpm='B',energy_low=englow, energy_high=enghigh,hdr=hdrb,xy_range=xy_range)
        else:
            if (det_id != ''):
                evda=nustar.filter.event_filter(evda,fpm='A',energy_low=englow, energy_high=enghigh,hdr=hdra,dets_id=det_id)
                evdb=nustar.filter.event_filter(evdb,fpm='B',energy_low=englow, energy_high=enghigh,hdr=hdrb,dets_id=det_id)
            else:
                evda=nustar.filter.event_filter(evda,fpm='A',energy_low=englow, energy_high=enghigh)
                evdb=nustar.filter.event_filter(evdb,fpm='B',energy_low=englow, energy_high=enghigh)


    timsa=atime.Time(mjdref+evda['time']*u.s,format='mjd')
    timsb=atime.Time(mjdref+evdb['time']*u.s,format='mjd')

    # Use the 1sec time binning of the livetime for the binning of the counts
    tda=(timsa-ltimsa[0]).sec
    tdb=(timsb-ltimsb[0]).sec

    # Time bin edges should be same for A and B
    tdedgs=(ltimsa-ltimsa[0]).sec

    # hisotgram number of events per the livetime 1s bins
    cnta, bea=np.histogram(tda,bins=tdedgs)
    cntb, beb=np.histogram(tdb,bins=tdedgs)
    rta=cnta/lda['LIVETIME'][:len(cnta)]
    rtb=cntb/ldb['LIVETIME'][:len(cntb)]

    # turn it into a pandas dataframe
    if lvt:
        dfl=pd.DataFrame(np.array([lda['LIVETIME'][:len(cnta)],ldb['LIVETIME'][:len(cntb)],rta,rtb]).T, \
            index=ltimsa.datetime[:len(cnta)], columns=['lvta','lvtb','rta','rtb'])
    else:
        dfl=pd.DataFrame(np.array([rta,rtb]).T, \
            index=ltimsa.datetime[:len(cnta)], columns=['rta','rtb'])
        
    if hk:
        dfl=pd.DataFrame(np.array([lda['LIVETIME'][:len(cnta)],ldb['LIVETIME'][:len(cntb)],rta,rtb,\
                                lda['NACCEPT'][:len(cnta)],ldb['NACCEPT'][:len(cntb)],\
                                lda['NREJECT'][:len(cnta)],ldb['NREJECT'][:len(cntb)]]).T, \
            index=ltimsa.datetime[:len(cnta)], columns=['lvta','lvtb','rta','rtb','acca','accb','reja','rejb'])

    # truncate to time range of the evt file
    # Start/End round up/down to nearest 1s
    mint=atime.Time(min(timsa[0].isot,timsb[0].isot),format='isot',precision=0) + 1*u.s
    maxt=atime.Time(max(timsa[-1].isot,timsb[-1].isot),format='isot',precision=0) - 1*u.s
    dflt=dfl.truncate(mint.isot,maxt.isot)

    # save out
    if outfile != '':
        dflt.to_csv(outfile)
    
    return dflt