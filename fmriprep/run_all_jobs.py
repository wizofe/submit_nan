import os
import glob
from pathlib import Path
import subprocess


def count_lines(some_file):
    return sum(1 for line in open(some_file))


for qsub_script_name in glob.glob("*.job"):
    site = Path(qsub_script_name).stem

    sge_index = site + ".index"
    sge_index = sge_index.replace("qsub", "sge")

    num_subs = count_lines(Path(sge_index))

    print(f"Sending job for site {site}...")
    subprocess.run(
        f"qsub -t 1-{num_subs} {qsub_script_name}",
        shell=True,
        executable="/bin/tcsh",
    )

print("Finito. Check qstat.")
