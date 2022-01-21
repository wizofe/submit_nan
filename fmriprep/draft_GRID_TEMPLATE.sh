# ================= GRID Configuration ====================
#$ -N fmriprep
#$ -o /home/k1201823/Data_Research/study_1/logs/
#$ -e /home/k1201823/Data_Research/study_1/logs/
# Set memory limit to be a bit larger then --mem_mb
#$ -l h_vmem=20G
# Set this value to match --nthreads and --omp-nthreads
#$ -pe smp 4

# ================= SHELL Configuration ===================
# First unload any modules loaded by ~/.cshrc, then load the defaults
module purge
module load nan sge

# Prevent .cshrc from loading modules (requires changes to ~/.cshrc)
setenv SGE_CLEAN 1

# Load script dependent modules here
module load fmriprep

# ================= SHELL Commands ========================
# set the working variables
set working_dir = /home/k1201823/Data_Research/study_1
set sge_index   = ${working_dir}/sge.index
set subject     = "`awk 'FNR==$SGE_TASK_ID' ${sge_index}`"
set source_data = ${working_dir}/data/bids_root
set output_data = ${working_dir}/output/${subject}
set work        = ${working_dir}/work/${subject}

# Remove any existing files so we start from scratch each time.
if ( -e ${work} ) then
  rm -rf ${work}
endif

# Remove existing processed data
if ( -e ${output_data} ) then
  rm -rf ${output_data}
endif

# You will require a freesurfer license stored in the top level of your home directory,
# the file is called license.txt.
fmriprep \
${source_data} \
${output_data} \
participant \
--participant_label ${subject} \
--task-id faces \
--output-space {T1w} \
--template {MNI152NLin2009cAsym} \
--template-resampling-grid "2mm" \
--work-dir ${work} \
--write-graph \
--stop-on-first-crash \
--nthreads 4 \ 
--omp-nthreads 4 \ 
--mem_mb 20480 \
--notrack \
-vv
