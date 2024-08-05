# make plots
echo "Sourcing key4hep..."
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
echo "Sourcing executed successfully"

echo "Starting analysis and plot script..."
python FCC_Validation/Analysis/DCH_val_plots.py -f DCH_sim.root --no_show \
       -o $WORKAREA/$PLOTAREA/DCH_standalone_o1_v02/no_Wires/plots
echo "Script executed successfully"

# upload them on website
echo "Starting website script..."
cd key4hep-reco-validation/web/python
python3 make_web.py --dest $WORKAREA/$PLOTAREA
echo "Script executed successfully"