# setup phase

echo "Downloading necessary Github repos..."

git clone --depth 1 https://github.com/key4hep/k4geo.git
#git clone https://github.com/key4hep/key4hep-reco-validation.git
mkdir -p $WORKAREA/$PLOTAREA/DCH_standalone_o1_v02/no_Wires/plots

echo "Download terminated - setup stage successful"