import os
import subprocess
import sys

tile = 'h10v05'
base_url = "ftp://ladsweb.nascom.nasa.gov/allData/6/MOD11A1/%(year)i/%(day)03d/*.%(tile)s.*hdf"
save_dir = "/gss_gpfs_scratch/vandal.t/MOD11A1/raw"

os.chdir(save_dir)

for y in range(2000, 2016):
    for d in range(1,367):
        if (y == 2000) and (d < 55):
            continue
        url = base_url % dict(tile=tile, day=d, year=y)
        cmd = ['wget', url]
        subprocess.call(cmd)
