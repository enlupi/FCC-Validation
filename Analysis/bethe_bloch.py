import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# constants
m_e = 0.51099895069 # electron mass (MeV)
c = 1 # speed of light (natural units)
N_A = 6.022140761e23 # mol**-1
e = 1 # electron charge (natural units)
eps_0 = 55.26349406e10 # vacuum permittivity (e**2 * MeV**-1 * cm**-1)
M_u = 1  # Molar mass constant (g/mol)


# detector size  
r = 35  # cm, inner cylinder radius
R = 200 # cm, outer cylinder radius
half_L = 200 # cm, lenght of the cylinders 

  
  
def beta(E, m):
  gamma = E/m
  b = np.sqrt(1 - (1/gamma)**2)
  return b

def electron_density(material):
  n = N_A*material['Z']*material['rho']/material['A']/M_u
  return n
  
  
def bethe_bloch(E0, particle, I, mult, length, step):
  E = E0
  E_lost = 0
  for i in range(int(length//step)):
    b = beta(E, particle['mass'])
    dE_dx = mult * 1/b**2 * (np.log(2*m_e*c**2*b**2/(I*(1 - b**2))) - b**2)
    Delta_E = dE_dx*step
    E -= Delta_E
    E_lost += Delta_E
  return E_lost  
  
  
def energy_loss(particle, material, E0, length, step=0.1):
  n = electron_density(material)
  I = material['I']
  mult = 4*np.pi/(m_e*c**2) * n*particle['z']**2 * (e**2/(4*np.pi*eps_0))**2
  try:
    iter(length)
  except:
    length = [length]
  E_lost = np.array([bethe_bloch(E0, particle, I, mult, l, step) for l in tqdm(length)])
    
  return E_lost


def path_length(theta):
  excess = R/np.tan(theta) - half_L
  try:
    iter(theta)
  except:
    if excess < 0:
      excess = 0
  else: 
    excess[excess < 0] = 0
    
  L = (R - r)/np.sin(theta) - excess/np.cos(theta)
  return L
  
  

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
        description="Process simulation"
    )
  parser.add_argument('-d', "--distribution",  type=str, 
                      help='Distribution for angle theta', default='uniform')  
  parser.add_argument('-N', "--evtNumber",  type=int, 
                      help='Number of events to simulate', default=100000) 
  parser.add_argument('-E', "--startingEnergy",  type=float, 
                      help='Starting energy of the particle [MeV]', default=1)
  parser.add_argument("--theta",  type=float, help='Select single value for angle theta') 
  parser.add_argument("--stepSize",  type=float, help='Select value for the step size [cm]')                    
  parser.add_argument("--no_save", action='store_true', help='Save output distribution plot')
  parser.add_argument("--no_show", action='store_true', help='Show E distribution plot')
  parser.add_argument('-o', "--outputPath", type=str,
                      help='The name of the directory where to save output plots', default='./')
                      
  args = parser.parse_args()
  
  
  # define particle characteristics
  proton = {
    'mass': 938.2720813, #MeV
    'z': e
  }
  
  
  # define material characteristics
  He = {
    'Z': 2,
    'A': 4,
    'I': 48e-6,
    'rho': 0.178e-3 # g/cm3
  }
  
  
  if args.theta is not None:
    try:
      args.theta >= 0 and args.theta <= np.pi
    except:
      print("Please select value of theta between zero and pi/2")
    else:
      theta = args.theta
      args.evtNumber = 1
  else:
    if args.distribution == "uniform":  
      theta = np.random.uniform(low=0, high=np.pi/2, size=args.evtNumber)
    elif args.distribution == "cos(theta)":
      z = np.random.uniform(size=args.evtNumber)
      theta = np.arccos(z)
      
  l = path_length(theta)
  
  E = energy_loss(proton, He, args.startingEnergy, l, args.stepSize)
  
  if args.evtNumber > 1:
    nbins = 20
    cmin = 0
    cmax = 0.1
    fig, ax = plt.subplots(figsize=(8,6))
    hist = ax.hist(E, bins=nbins, 
                   color='lightblue', edgecolor='black')
    ax.set_xlabel('Energy Deposited [MeV]')
    ax.set_ylabel(f'Counts / {(cmax - cmin)/nbins:.1f} MeV')
    ax.set_yscale('log')
    plt.show()
  else:
    print("Total Energy Deposit:", E[0], "MeV")
  
  
      
  
