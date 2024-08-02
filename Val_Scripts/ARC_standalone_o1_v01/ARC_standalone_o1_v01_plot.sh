# make plots
echo "Sourcing key4hep..."
source /cvmfs/sw.hsf.org/key4hep/setup.sh
echo "Sourcing executed successfully"

echo "Starting analysis and plot script..."
python FCC_Validation/Analysis/ARC_val_plots.py -f ARC_sim.root --no_show \
       -o key4hep-reco-validation/www/ARC_standalone_o1_v01/validation
echo "Script executed successfully"

# upload them on website
echo "Starting website script..."
cd key4hep-reco-validation/web/python
python3 make_web.py --dest ../../www
echo "Script executed successfully"