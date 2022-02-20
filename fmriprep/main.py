# template =>>>>>>>>
# Ideally create a qsub class (is it required though?)
# https://github.com/durrantmm/ASETools/blob/master/asetools/mod/misc/qsub.py
# or some ideas from here
# https://github.com/courtois-neuromod/ds_prep/blob/6b87b05a130f526cad9eec140a3c561d86ab98f4/derivatives/mriqc.py
import os
from pathlib import Path
import subprocess

from bids import BIDSLayout
from bids import BIDSValidator
from bids.tests import get_test_data_path

template = """
#$ -N fmriprep 
#$ -o /data/project/ABIDE/abide/logs/fmriprep.output
#$ -e /data/project/ABIDE/abide/logs/fmriprep.output
#$ -l h_vmem=14G
#$ -pe smp 1

module purge
module load nan sge
setenv SGE_CLEAN 1
module load fmriprep

set subject = "`awk 'FNR==$SGE_TASK_ID' {sge_index}`"

fmriprep \
{BIDS_DIR} {FMRIPREP_DERIVS} \
participant \
--participant-label $subject \
--use-aroma --output-spaces MNI152Lin3mm-res:01 \
--work-dir /data/project/ABIDE/abide/work \
--fd-spike-threshold 0.2 \
--skip-bids-validation \
--fs-license-file /home/k19012844/projects/neuro/abide-exploration/code/license.txt \
--write-graph \
--stop-on-first-crash \
--fd-spike-threshold 0.20 \
--nprocs 1 \
--omp-nthreads 1 \
--mem 14336 \
--notrack \
-vv \
"""

# get the BIDS structure
# use click to get arguments
argv1 = "/data/project/ABIDE/abide/RawDataBIDS/"
path_bids = Path(argv1)

# BIDS v1.0 specification treats multi-sites either as a) separate BIDS b) combination in ABIDE datalad is the case a so we need to treat each site separately
dirs_bids = next(os.walk(path_bids))[1]
dirs_bids = [f for f in dirs_bids if not f.startswith(".")]


for site in dirs_bids:
    layout = BIDSLayout(path_bids / site, validate=False)
    path_fmriprep_deriv = path_bids / site / "derivatives/fmriprep"

    # create the derivatives directory
    path_fmriprep_deriv.mkdir(parents=True, exist_ok=True)

    # initiate a qsub and sge.index site-dependent file
    qsub_script_name = Path(os.getcwd()) / Path(f"qsub-{site}.job")
    sge_index = Path(os.getcwd()) / Path(f"sge-{site}.index")
    len_bids = len(layout.get_subjects())

    # extract site subject and save them
    site_subjects = layout.get(return_type="id", target="subject")

    # and write it to an sge file
    ssub_f = open(sge_index, "w")
    for sub in site_subjects:
        ssub_f.write(f"{sub}" + "\n")
    ssub_f.close()

    qsub_script = template.format(
        BIDS_DIR=path_bids / site,
        sge_index=sge_index,
        FMRIPREP_DERIVS=path_fmriprep_deriv,
    )

    # script job writing
    with open(qsub_script_name, "w") as f:
        f.write(qsub_script)

    print(f"Writing job for site {site}...")

    # subprocess.run(
    #     f"qsub -t 1-{len_bids} {qsub_script_name}",
    #     shell=True,
    #     executable="/bin/tcsh",
    # )

print("Finito. Check qstat.")
