# simulation phase
source /cvmfs/sw.hsf.org/key4hep/setup.sh

ddsim --steeringFile FCC_Validation/Steering_Files/ARC_steering.py \
      --compactFile k4geo/test/compact/ARC_standalone_o1_v01.xml \
      -N 100
