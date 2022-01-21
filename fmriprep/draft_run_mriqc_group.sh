#!/bin/tcsh
module load mriqc
set abide_bids = "/data/project/ABIDE/abide/RawDataBIDS"

cd $abide_bids

foreach i (`ls $abide_bids`)
    mriqc $i $i"/derivatives/mriqc/" group
end

