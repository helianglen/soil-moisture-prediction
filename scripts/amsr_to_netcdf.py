from pyhdf.SD import SD, SDC
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import xray as xr
import datetime as dt

raw_dir = "/gss_gpfs_scratch/vandal.t/amsr-soil-moisture/raw"
netcdf_dir = "/gss_gpfs_scratch/vandal.t/amsr-soil-moisture/netcdf"

ncols, nrows = 1383, 586
r0, s0 = 691, 293           # origin col/row
R = 6371.228                # radius of earth
C = 25                      # cell size (km)

lats, lons = [], []
for r in range(ncols):
    lons += [(r + r0 - (ncols - 1)) * C / R / np.cos(np.pi/6) * 180 / np.pi]

for s in range(nrows):
    lt = np.arcsin(-(s + s0 - (nrows - 1)) * C / R * np.cos(np.pi/6)) * 180 / np.pi
    lats += [lt]

lats = np.array(lats)
lons = np.array(lons)
prev_year = None
sm_data = []

for f in sorted(os.listdir(raw_dir)):
    print f
    fpath = os.path.join(raw_dir, f)
    s = f.split("_")
    year = int(s[5][:4])
    month = int(s[5][4:6])
    day = int(s[5][6:8])

    hdf = SD(fpath, SDC.READ)
    sm = hdf.select("A_Soil_Moisture")
    tp = hdf.select("A_Land_Surface_Temp")

    if year != prev_year:
        if len(sm_data) > 0:
            sm_data = np.concatenate(sm_data, axis=2).astype('float32')
            tp_data = np.concatenate(tp_data, axis=2).astype('float32')
            sm_data[(sm_data == 9999) | (sm_data == -9999)] = np.nan
            tp_data[(tp_data == 9999) | (tp_data == -9999)] = np.nan
            dr_sm = xr.DataArray(sm_data, coords=[lats, lons, times], dims=['lat', 'lon', 'time'])
            dr_tp = xr.DataArray(tp_data, coords=[lats, lons, times], dims=['lat', 'lon', 'time'])
            ds = xr.Dataset(dict(temperature=dr_tp, soil_moisture=dr_sm))
            ds.to_netcdf(os.path.join(netcdf_dir, "amsr_daily_%i.nc" % prev_year))

        sm_data = []
        tp_data = []
        times = []

    sm_data += [sm[:][:,:,np.newaxis]]
    tp_data += [tp[:][:,:,np.newaxis]]
    times += [dt.datetime(year, month, day)]
    prev_year = year

sm_data = np.concatenate(sm_data, axis=2).astype('float32')
tp_data = np.concatenate(tp_data, axis=2).astype('float32')
sm_data[(sm_data == 9999) | (sm_data == -9999)] = np.nan
tp_data[(tp_data == 9999) | (tp_data == -9999)] = np.nan
dr_sm = xr.DataArray(sm_data, coords=[lats, lons, times], dims=['lat', 'lon', 'time'])
dr_tp = xr.DataArray(tp_data, coords=[lats, lons, times], dims=['lat', 'lon', 'time'])
ds = xr.Dataset(dict(temperature=dr_tp, soil_moisture=dr_sm))
ds.to_netcdf(os.path.join(netcdf_dir, "amsr_daily_%i.nc" % prev_year))
