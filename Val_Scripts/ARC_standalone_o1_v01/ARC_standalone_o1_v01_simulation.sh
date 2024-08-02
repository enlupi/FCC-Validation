# simulation phase
echo "Sourcing key4hep..."
source /cvmfs/sw.hsf.org/key4hep/setup.sh
echo "Sourcing executed successfully"

echo "Starting simulation..."
ddsim --steeringFile FCC_Validation/Steering_Files/ARC_steering.py \
      --compactFile k4geo/test/compact/ARC_standalone_o1_v01.xml \
      -N 100
echo "Simulation ended successfully"