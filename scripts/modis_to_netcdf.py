from pyhdf.SD import SD, SDC
import os
import sys
import numpy as np
import xray as xr
import datetime as dt

raw_dir = "/gss_gpfs_scratch/vandal.t/MOD11A1/raw/"
netcdf_dir = "/gss_gpfs_scratch/vandal.t/MOD11A1/netcdf/"

# Bounds: http://modis-land.gsfc.nasa.gov/pdf/sn_bound_10deg.txt
latmin, latmax = 30, 40
lonmin, lonmax = -104.4326, -80.8194
ncol, nrow = 1200, 1200

latstep = 1. * (latmax - latmin) / nrow
lonstep = 1. * (lonmax - lonmin) / ncol

lats = latstep * np.arange(nrow) + latmin
lons = lonstep * np.arange(ncol) + lonmin

prev_year = 2000
daytemps = []
dates = []
for f in sorted(os.listdir(raw_dir)):
    print f
    fpath = os.path.join(raw_dir, f)
    year = int(f.split('.')[1][1:5])
    dayofyear = int(f.split('.')[1][5:8])
    date = dt.datetime(year, 1, 1) + dt.timedelta(days=dayofyear-1)
    if prev_year != year:
        tp_data = np.concatenate(daytemps, axis=2)
        tp_data[tp_data == 0] = np.nan
        dr = xr.DataArray(tp_data, coords=[lats, lons, dates], dims=['lat', 'lon', 'time'])
        ds = xr.Dataset(dict(LST_Day_1km=dr))
        ds.to_netcdf(os.path.join(netcdf_dir, "MOD11A1_%i.nc" % prev_year))
        daytemps = []
        dates = []

    hdf = SD(fpath, SDC.READ)
    tp = hdf.select("LST_Day_1km")[:] * 0.02    #scale factor
    daytemps += [tp[:,:,np.newaxis]]
    dates += [date]
    prev_year = year


tp_data = np.concatenate(daytemps, axis=2)
tp_data[tp_data == 0] = np.nan
dr = xr.DataArray(tp_data, coords=[lats, lons, dates], dims=['lat', 'lon', 'time'])
ds = xr.Dataset(dict(LST_Day_1km=dr))
ds.to_netcdf(os.path.join(netcdf_dir, "MOD11A1_%i.nc" % prev_year))






