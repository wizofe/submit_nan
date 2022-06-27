#!/bin/bash
MASK="/data/project/ABIDE/abide/Resources/mask_85_abide1_ref_smoothAROMAnonaggr.nii.gz"
FILE="/data/project/ABIDE/abide/RawDataBIDS/CMU_a/derivatives/fmriprep/sub-0050649/func/sub-0050649_task-rest_run-1_space-MNI152NLin6Asym_desc-smoothAROMAnonaggr_bold.nii.gz"
FNAME="CMU_a_sub-0050649_dc_weighted_nobw_aroma"

3dDegreeCentrality -thresh 0.25 -mask $MASK -prefix $FNAME $FILE
3dAFNItoNIFTI $FNAME[1] $FNAME.nii.gz
