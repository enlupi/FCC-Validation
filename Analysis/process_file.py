import ROOT
from podio import root_io
import dd4hep as dd4hepModule
from ROOT import dd4hep
import argparse
import numpy as np
import os
import tqdm


n_layers = 112
nphi_max = 816


def process_file(inputFile, save=False, outputPath="./"):
  
  # set file reader
  podio_reader = root_io.Reader(inputFile)
  metadata = podio_reader.get("metadata")[0]
  cellid_encoding = metadata.get_parameter("DCHCollection__CellIDEncoding")
  decoder = dd4hep.BitFieldCoder(cellid_encoding)
  n_evts = len(podio_reader.get("events"))
                  
                  
  ########## Analyze Simulation #########################
  
  # prepare arrays for quantities of interest
  E_per_hit = []
  E_per_layer = np.zeros(shape=(n_evts, n_layers)) # n_evts(100) by 112 matrix
  cell_fired = np.zeros(shape=(n_evts, n_layers, nphi_max), dtype=bool)
  hits_per_evt = np.zeros(n_evts)
  
  # loop over dataset
  for i_evt, event in enumerate(podio_reader.get("events")):
    for dc_hit in event.get("DCHCollection"):
      particle =  dc_hit.getParticle()
      cellID = dc_hit.getCellID()
      layer = decoder.get(cellID, "layer")
      superlayer = decoder.get(cellID, "superlayer")
      nphi = decoder.get(cellID, "nphi")
      if nphi == nphi_max:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      edepo = dc_hit.getEDep()*1e6 # convert from GeV to keV
      # i_layer is a counter that runs from 0 to 111
      i_layer = superlayer*8 + layer
      
      E_per_hit.append(edepo)
      E_per_layer[i_evt, i_layer] += edepo
      cell_fired[i_evt, i_layer, nphi] = True
      hits_per_evt[i_evt] += 1
    
  E_per_hit = np.array(E_per_hit)
  E_per_evt = E_per_layer.sum(axis=1)
  cell_per_layer = cell_fired.sum(axis=2)
  cell_per_evt = cell_fired.sum(axis=(2,1))
  
  results = {
    "E_per_hit": E_per_hit,
    "E_per_layer": E_per_layer,
    "E_per_evt": E_per_evt,
    "cell_per_layer": cell_per_layer,
    "cell_per_evt": cell_per_evt,
    "hits_per_evt": hits_per_evt    	
  }
  
  if save:
    filename = os.path.splitext(os.path.basename(inputFile))[0] # removes path and extension
    if outputPath[-1] != '/':
      outputPath += '/'
    output_start = outputPath + filename
    
    for key, value in results.items():
      np.save(output_start+"_"+key+".npy", value)
    
  return results
  
  
  
  
        
###########################################################################################        
        
        
if __name__ == "__main__":
  parser = argparse.ArgumentParser(
        description="Process simulation"
    )
  parser.add_argument('-f', "--inputFile",  type=str, 
                      help='The name of the simulation file to be processed', default='dch_proton20GeV.root')
  parser.add_argument('-o', "--outputPath", type=str, 
                      help='The name of the directory where to save output files', default='./')
  parser.add_argument("--save",           action='store_true', help='Save output arrays')
  
  args = parser.parse_args()
    
  process_file(args.inputFile, args.save, args.outputPath)
