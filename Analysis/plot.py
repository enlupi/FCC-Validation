from process_file import process_file
import argparse
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm, LogNorm
from matplotlib.ticker import FuncFormatter
import numpy as np
import os


n_layers = 112
nphi_max = 816


def log_to_energy(x, pos):
    return f"$10^{{{x:.0f}}}$"

def plot_results(results, filename, args):

  full_plot = not (args.E_per_hit or args.E_per_layer or args.E_per_evt or \
                   args.cell_per_layer or args.cell_per_evt or args.cell_per_evt)
  
  if args.outputPath[-1] != '/':
    args.outputPath += '/'
  output_start = args.outputPath + filename 
  
  n_evts = len(results["hits_per_evt"])

  ########## Compute histos #########################
  
  # E per hit
  if args.E_per_hit or full_plot:
    logEmin = -6
    logEmax = 6
    nbins = 36
    
    fig1, ax1 = plt.subplots(figsize=(8,6))
    hist1 = ax1.hist(np.log10(results["E_per_hit"], where=results["E_per_hit"]!=0),
                     bins=nbins, range=(logEmin, logEmax),
                     color='lightblue', edgecolor='black')
    ax1.set_xlabel('Energy [keV]')
    ax1.xaxis.set_major_formatter(FuncFormatter(log_to_energy))
    ax1.set_ylabel(f'Counts / third of decade')
    ax1.set_yscale('log')
    ax1.set_title('Energy per Hit')
    
    if not args.no_save:
      fig1.savefig(output_start+'_E_per_hit.png', bbox_inches='tight')
    if args.no_show:
      plt.close(fig1)
      
      
  # E per layer
  if args.E_per_layer or full_plot:
    E_per_layer_flat = results["E_per_layer"].flatten('F') #flatten in column-major order
    layers = np.repeat(np.arange(1, n_layers+1), n_evts)
    logEmin = -3
    logEmax = 5
    nbins = 32
    
    fig2, ax2 = plt.subplots(figsize=(8,6))
    hist2 = ax2.hist2d(np.log10(E_per_layer_flat, where= E_per_layer_flat != 0),
                       layers, bins=[nbins, n_layers],
                       range=[[logEmin, logEmax],[1, n_layers+1]], cmap='viridis',
                       norm=SymLogNorm(vmin=0, vmax=1e4, linthresh=1))
    cbar = plt.colorbar(hist2[3], ax=ax2)
    cbar.set_label(f'Counts / layer / quarter of decade')
    ax2.set_xlabel('Energy [keV]')
    ax2.xaxis.set_major_formatter(FuncFormatter(log_to_energy))
    ax2.set_ylabel(f'Layer')
    ax2.set_title('Energy per Layer')
    
    if not args.no_save:
      fig2.savefig(output_start+'_E_per_layer.png', bbox_inches='tight')
    if args.no_show:
      plt.close(fig2)
      
      
  # E total
  if args.E_per_evt or full_plot:
    logEmin = -2
    logEmax = 5
    nbins = 21
      
    fig3, ax3 = plt.subplots(figsize=(8,6))
    hist3 = ax3.hist(np.log10(results["E_per_evt"], where=results["E_per_evt"]!=0),
                     range=(logEmin, logEmax), bins=nbins,
                     color='lightblue', edgecolor='black')
    ax3.set_xlabel('Energy [keV]')
    ax3.set_ylabel(f'Counts / third of decade')
    ax3.xaxis.set_major_formatter(FuncFormatter(log_to_energy))
    ax3.set_yscale('log')
    ax3.set_title('Total Energy per Event')
    
    if not args.no_save:
      fig3.savefig(output_start+'_E_per_evt.png', bbox_inches='tight')
    if args.no_show:
      plt.close(fig3)
      
      
  # cells fired per layer
  if args.cell_per_layer or full_plot:
    cell_per_layer_flat = results["cell_per_layer"].flatten('F') #flatten in column-major order
    layers = np.repeat(np.arange(1, n_layers+1), n_evts)
    cmin = 0
    cmax = 50
    nbins = 25
    
    fig4, ax4 = plt.subplots(figsize=(8,6))
    hist4 = ax4.hist2d(cell_per_layer_flat, layers, bins=[nbins, n_layers],
                       range=[[cmin, cmax],[1, n_layers+1]], cmap='viridis',
                       norm=SymLogNorm(vmin=0, vmax=5e4, linthresh=1))
    cbar = plt.colorbar(hist4[3], ax=ax4)
    cbar.set_label(f'Counts / layer / {(cmax - cmin)/nbins:.1f} cells')
    ax4.set_xlabel('Number of Cells')
    ax4.set_ylabel(f'Layer')
    ax4.set_title('Cells Fired per Layer')
    
    if not args.no_save:
      fig4.savefig(output_start+'_cell_per_layer.png', bbox_inches='tight')
    if args.no_show:
      plt.close(fig4)
      
      
  # cells fired per evt
  if args.cell_per_evt or full_plot:
    cmin = 0
    cmax = 1500
    nbins = 30
      
    fig5, ax5 = plt.subplots(figsize=(8,6))
    hist5 = ax5.hist(results["cell_per_evt"], bins=nbins, range=(cmin,cmax),
                     color='lightblue', edgecolor='black')
    ax5.set_xlabel('Number of Cells')
    ax5.set_ylabel(f'Counts / {(cmax - cmin)/nbins:.1f} cells')
    ax5.set_yscale('log')
    ax5.set_title('Cells Fired per Event')
    
    if not args.no_save:
      fig5.savefig(output_start+'_cell_per_evt.png', bbox_inches='tight')
    if args.no_show:
      plt.close(fig5)
  
  
  # hits per evt
  if args.hits_per_evt or full_plot:
    hmin = 0
    hmax = 1500
    nbins = 30
    
    fig6, ax6 = plt.subplots(figsize=(8,6))
    hist6 = ax6.hist(results["hits_per_evt"], range=(hmin,hmax), bins=nbins,
                     color='lightblue', edgecolor='black')
    ax6.set_xlabel('Hits')
    ax6.set_ylabel(f'Counts / {(hmax - hmin)/nbins:.1f} hits')
    ax6.set_yscale('log')
    ax6.set_title('Hits per Event')
    
    if not args.no_save:
      fig6.savefig(output_start+'_hits_per_evt.png', bbox_inches='tight')
    if args.no_show:
      plt.close(fig6)
      
  plt.show()
        
        
        
        
             
###########################################################################################        
        
        
if __name__ == "__main__":
  parser = argparse.ArgumentParser(
        description="Process simulation"
    )
  parser.add_argument('-f', "--inputFile",  type=str, 
                      help='The name of the simulation file to be processed', default='dch_proton20GeV.root')
  parser.add_argument('-l', "--load",  type=str, 
                      help='Load results directly from specified file', default='')
  parser.add_argument('-o', "--outputPath", type=str,
                      help='The name of the directory where to save output plots', default='./')
  parser.add_argument("--no_save",        action='store_true', help='Save output arrays')
  parser.add_argument("--no_show",        action='store_true', help='Plot output histograms')
  parser.add_argument("--E_per_hit",      action='store_true', help='Compute energy per hit histogram')
  parser.add_argument("--E_per_layer",    action='store_true', help='Compute energy per layer histogram')
  parser.add_argument("--E_per_evt",      action='store_true', help='Compute total energy per event histogram')
  parser.add_argument("--cell_per_layer", action='store_true', help='Compute n. of cells per layer histogram')
  parser.add_argument("--cell_per_evt",   action='store_true', help='Compute n. of cells per event histogram')
  parser.add_argument("--hits_per_evt",   action='store_true', help='Compute n. of hits per event histogram')
  
  args = parser.parse_args()
  
  results = {}
  filename = ''
  if not args.load:
    results = process_file(args.inputFile)
    filename = os.path.splitext(os.path.basename(args.inputFile))[0] # removes path and extension
  else:
    directory, file_prefix = os.path.split(args.load)
    if not directory:
      directory = "."
    all_files = os.listdir(directory)
    matching_files = [f for f in all_files if f.startswith(file_prefix)]
    for f in matching_files:
      key = os.path.splitext(os.path.basename(f))[0][len(file_prefix)+1:]
      results[key] = np.load(directory+'/'+f)
  
  if args.no_save and args.no_show:
    print("No action selected: please do not use --no_show and --no_save together!")
  else:  
    plot_results(results, filename, args)
