# setup phase
source /cvmfs/sw.hsf.org/key4hep/setup.sh
git clone --depth 1 https://github.com/key4hep/k4geo.git
# git clone https://github.com/key4hep/key4hep-reco-validation.git
git clone https://github.com/enlupi/key4hep-reco-validation.git
git clone https://github.com/enlupi/FCC_Validation.git
mkdir -p key4hep-reco-validation/www/ARC_standalone_o1_v01/

# simulation phase
ddsim --steeringFile FCC_Validation/Steering_Files/ARC_steering.py \
      --compactFile k4geo/test/compact/ARC_standalone_o1_v01.xml \
      -N 10000

# make plots
python FCC_Validation/Analysis/ARC_val_plots.py -f ARC_sim.root --no_show \
       -o key4hep-reco-validation/www/ARC_standalone_o1_v01/


