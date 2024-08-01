# make plots
python FCC_Validation/Analysis/ARC_val_plots.py -f ARC_sim.root --no_show \
       -o key4hep-reco-validation/www/ARC_standalone_o1_v01/


# upload them on website
cd key4hep-reco-validation/web/python
python3 make_web.py --dest ../../www