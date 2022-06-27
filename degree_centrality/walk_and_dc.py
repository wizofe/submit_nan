import os
import glob
from pathlib import Path


## Quick script to generate an sge.index with names of files
## to be processed on the NAN server (SUN Grid)
## ---
## Copyright 2022 Ioannis Valasakis <code@wizofe.uk>
## under the GNU GPL v3.0+

cwd = str(Path().resolve())

# grab each site and save it inside a list
sites = [f for f in os.listdir(cwd) if (not f.startswith('.') and os.path.isdir(f))]

# for every site transverse into derivatives/fmriprep/sub-xxxx
# get the *MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz
for site in sites:
    bolds = glob.glob(f"{cwd}/{site}/derivatives/fmriprep/**/*MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz", recursive=True)
#    for f in bolds:

print(bolds)

# write each resulting filename to an sge.index file )one line per file
