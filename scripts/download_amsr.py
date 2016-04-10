import os
import sys
import subprocess

base_url = "ftp://n5eil01u.ecs.nsidc.org/SAN/AMSA/AE_Land3.002/%(year)i.%(month)02d.%(day)02d/*.hdf"
save_dir = "/gss_gpfs_scratch/vandal.t/amsr-soil-moisture/"
os.chdir(save_dir)
years = range(2002, 2012)
months = range(1, 13)
days = range(1,32)

for y in years:
    for m in months:
        for d in days:
            url = base_url % dict(year=y, month=m, day=d)
            wget_cmd = ['wget', url, '-N']
            subprocess.call(wget_cmd)
