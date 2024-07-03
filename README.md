# CERN Summer School 2024: IDEA Drift Chamber Validation


# Day 1

DD4hep stands for Detector Description for High Energy Physics (HEP). It exploits the ROOT machinery (TGeo clases, TMaterial, etc) that reproduce the same features as Geant4 (+CLHEP). It adds some extra features with respect to Geant4 (such as the data extension mechanism) and at the same time allows to simplify part of the code needed to run a simulation. For example, by using `ddsim` ones does not have to create from scratch a Geant4 standalone application; one can see `ddsim` as an skeleton of a Geant4 standalone application.

As a starting point for learning, please check the fullsim of FCC detector concepts [page](https://fcc-ee-detector-full-sim.docs.cern.ch), that contains
- short description of DD4hep (for geometry) and steering file for `ddsim`
- key4hep (the software stack that gathers the 600 packages including ROOT and Geant4)
- Description of the 3 main detector concepts (CLD, IDEA, ALLEGRO)

## Basic Instructions

### How to start

The work will start by getting familiar with the drift chamber of IDEA. To do so, we can work with a local copy of `k4geo`, the repository that contains the geometry description for FCC, as follows:

```bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
git clone --depth 1 https://github.com/key4hep/k4geo.git
cd k4geo
cmake -B build -S . -D CMAKE_INSTALL_PREFIX=install
cmake --build build -j 4 --target install
k4_local_repo
```

My recommendation is that for each test or study, you copy the main `XML` file that contains the description of the drift chamber, taken from [k4geo repository](https://github.com/key4hep/k4geo/blob/main/lcgeoTests/compact/DCH_standalone_o1_v02.xml). Remember to:
* remove the `debugGeometry` tag
* use the proper path to the materials and elements `XML` files

Other links to interesting pieces of information:
* Presentation about the geometry of the drift chamber, [link](https://indico.cern.ch/event/1402578/)
* Collection of useful commands to start using DD4hep, [link](https://github.com/atolosadelgado/ARC_detector)
* Some notes about EDM4hep, [link](https://indico.cern.ch/event/1307378/contributions/5729652/attachments/2789482/4864493/fccphysweek24_atd_240130.pdf#page=11)

### Run the Simulation
After configuring the description of the drift chamber and the steering file as desired, we can run the simulation using one of the following commands:
```bash
ddsim --steeringFile DCH_steering.py --compactFile lcgeoTests/compact/DCH_standalone_o1_v02.xml -N 10
```
```bash
ddsim --steeringFile DCH_steering.py --compactFile lcgeoTests/compact/DCH_standalone_o1_v02.xml --runType qt --macroFile example/vis.mac
```
The first one runs a simulation of 10 events, while the second starts an interactive session with visualization using qt.

### Inspecting output file from ddsim

We can use the following python code to read the file produced by ddsim

```python
import ROOT
from podio import root_io
import dd4hep as dd4hepModule
from ROOT import dd4hep

input_file_path = "myfile.root"
podio_reader = root_io.Reader(input_file_path)
metadata = podio_reader.get("metadata")[0]
cellid_encoding = metadata.get_parameter("DCHCollection__CellIDEncoding")
decoder = dd4hep.BitFieldCoder(cellid_encoding)
for event in podio_reader.get("events"):
  for dc_hit in event.get("DCHCollection"):
    particle =  dc_hit.getParticle()
    cellID = dc_hit.getCellID()
    layer = decoder.get(cellID, "layer")
    superlayer = decoder.get(cellID, "superlayer")
    # ilayer is a counter that runs from 1 to 112
    ilayer = superlayer*8 + layer + 1
    if particle.getPDG() == 111:
      # do stuff
```

----


Links to official documentation (*mainly in case of problems*):
* DD4hep (FCC): https://fcc-ee-detector-full-sim.docs.cern.ch/DD4hep/
* DD4hep (github): https://github.com/AIDASoft/DD4hep
* DD4hep (doxigen): https://dd4hep.web.cern.ch/dd4hep/reference/
* DD4hep (manual): https://dd4hep.web.cern.ch/dd4hep/usermanuals/DD4hepManual/DD4hepManual.pdf
* EDM4hep (github): https://github.com/key4hep/EDM4hep
* ROOT (doxigen): https://root.cern/doc/master/

## Tasks for Enrico

1. Run full simulation of the stand alone drift chamber. Study the output file, for example by plotting the energy distribution, number of cells fired per event, the energy distribution by layers, and in principle any other thing you consider useful 
2. Study the effect of including/removing the wires on the previous plots. You can include/exclude the wires by changing the main XML.
3. Compare the energy deposited with the [analytical formula](https://en.wikipedia.org/wiki/Bethe_formula#The_mean_excitation_energy), given the mean excitation energy provided in the XML (48 eV)

```

## General good practices

1. Keep track of the work, for example by a dedicated git(hub) project. This would include the inputs files that are used, a README that explains how to reproduce the outputfiles and a script to generate the plots of interest
2. Quantify (with numbers) the subject of study
3. My door/email will be always open in case of need, please do not hesistate to ask if you need help or find a showstopper
4. Learn more about Geant4, by following the begining course available [here](https://indico.cern.ch/event/1370034/timetable/#20240415)
