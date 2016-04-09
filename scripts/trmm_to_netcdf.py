import numpy as np
import xray as xr
import os
import sys
import datetime as dt

file_dir = "/gss_gpfs_scratch/vandal.t/trmm/raw/"
netcdf_dir = "/gss_gpfs_scratch/vandal.t/trmm/netcdf/"
lats = np.linspace(-49.875, 49.875, 400)
lons = np.linspace(-179.875, 179.875, 1440)

prev_year = 1998
data, dates = [], []

for f in sorted(os.listdir(file_dir)):
    _, year, month, day, _, _ = f.split(".")
    date = dt.datetime(int(year), int(month), int(day))
    if (prev_year != int(year)):
        data = np.concatenate(data, axis=2)
        dr = xr.DataArray(data, coords=[lats, lons, dates], dims=['lat', 'lon', 'time'])
        ds = xr.Dataset(dict(prcp=dr))
        ds.to_netcdf(os.path.join(netcdf_dir, "trmm_3B42_%s.nc" % year))
        prev_year = year
        data = []
        dates = []

    dates += [date]
    prcp = np.fromfile(os.path.join(file_dir, f), dtype='>f4')
    prcp = np.reshape(prcp, (400, 1440))
    prcp[prcp < -9999] = np.nan
    data.append(prcp[:, :, np.newaxis])
