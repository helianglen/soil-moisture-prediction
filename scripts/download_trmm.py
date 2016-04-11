import os
import sys
import subprocess
import numpy as np

base_url = "ftp://disc3.nascom.nasa.gov/data/s4pa/TRMM_L3/TRMM_3B42_daily/" \
            "%(year)i/%(dayofyear)03d/*.bin"
save_dir = "/gss_gpfs_scratch/vandal.t/trmm/raw"
os.chdir(save_dir)

for y in range(1998, 2016):
    for d in range(1, 367):
        url = base_url % dict(year=y, dayofyear=d)
        cmd = ['wget', url]
        subprocess.call(cmd)
