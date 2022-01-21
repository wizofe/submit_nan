 local task_mriqc_cmd=$(echo "singularity run --cleanenv \
 -B ${cwd}:/work \
 $KUL_mriqc_singularity \
 --participant_label $BIDS_participant \
 $mriqc_options \
 -w /work/mriqc_work_${mriqc_log_p} \
 --n_procs $ncpu_mriqc --ants-nthreads $ncpu_mriqc_ants --mem_gb $mem_gb --no-sub \
 /work/${bids_dir} /work/mriqc participant \
 > $mriqc_log 2>&1 ") 

mriqc-0.15.1.simg \
${BIDS_folder} ${output_dir} \
participant \
-w /tmp/cbpdmaindata/ \
--participant_label ${subject} \
--session-id ${ses} \
--fd_thres ${threshold} \
--no-sub \
--n_procs 10 \

GROUPPPP##
/mriqc-0.15.1.simg \
${BIDS_folder}/ ${output_dir} \
group \
-w ${SBIA_TMPDIR} \

qsub -o ${home}/OBIWAN/ClusterOutput -j oe -l walltime=80:00:00,pmem=16GB -M david.munoz@etu.unige.ch -m n -l nodes=1 -q queue1 -N obQC_${group}${subjID} -F "${subjID} ${group}" ${Script}
