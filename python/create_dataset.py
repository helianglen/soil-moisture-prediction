import xray as xr
import numpy as np
import os

MODIS_DIR = "/gss_gpfs_scratch/vandal.t/MOD11A1/netcdf/"
TRMM_DIR = "/gss_gpfs_scratch/vandal.t/trmm/netcdf/"
AMSR_DIR = "/gss_gpfs_scratch/vandal.t/amsr-soil-moisture/netcdf/"

def read_data(data_dir, lat, lon, resample=None):
    files = sorted([os.path.join(data_dir, f) for f in os.listdir(data_dir)])
    dss = [xr.open_dataset(f).sel(lat=lat, lon=lon, method='nearest') for f in files]
    ds = xr.concat([dr.load() for dr in dss], 'time')
    if resample is not None:
        ds = ds.resample(resample, 'time')
    return ds

def create_dataset(lat, lon, outfile):
    modis = read_data(MODIS_DIR, lat, lon, resample='D')['LST_Day_1km'].to_dataframe()
    trmm = read_data(TRMM_DIR, lat, lon, resample='D')['prcp'].to_dataframe()
    amsr = read_data(AMSR_DIR, lat, lon, resample='D')['soil_moisture'].to_dataframe()

    df = modis.join(amsr).join(trmm).dropna()
    d1 = df.index[:-1].values
    d2 = df.index[1:].values
    daydiff = (d2-d1).astype('timedelta64[D]') / np.timedelta64(1, 'D') # convert nanosecond to days
    daydiff = np.insert(daydiff, 0, np.nan)
    df['days_missing'] = daydiff
    df.to_csv(outfile)
    return df


if __name__ == "__main__":
    lat = 36.888
    lon = -90.804
    outfile = "sm_%0.3f_%0.3f.csv" % (lat, lon)
    df = create_dataset(lat, lon, outfile)
