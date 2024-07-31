#steering.py 
from DDSim.DD4hepSimulation import DD4hepSimulation
SIM = DD4hepSimulation()
from g4units import mm, GeV, MeV

# Register optical physics and Cerenkov process to the default physics
def setupCerenkov(kernel):
        from DDG4 import PhysicsList

        seq = kernel.physicsList()
        cerenkov = PhysicsList(kernel, "Geant4CerenkovPhysics/CerenkovPhys")
        cerenkov.MaxNumPhotonsPerStep = 10
        cerenkov.MaxBetaChangePerStep = 10.0
        cerenkov.TrackSecondariesFirst = False
        cerenkov.VerboseLevel = 0
        cerenkov.enableUI()
        seq.adopt(cerenkov)
        ph = PhysicsList(kernel, "Geant4OpticalPhotonPhysics/OpticalGammaPhys")
        ph.addParticleConstructor("G4OpticalPhoton")
        ph.VerboseLevel = 0
        ph.BoundaryInvokeSD = True
        ph.enableUI()
        seq.adopt(ph)
        return None
SIM.physics.setupUserPhysics(setupCerenkov)

# Associate the Geant4OpticalTrackerAction to these detectors
# this action register total energy of the opt photon as a single hit
# and kills the optical photon, so no time is wasted tracking them
SIM.action.mapActions["ARCBARREL"] = "Geant4OpticalTrackerAction"
SIM.action.mapActions["ARCENDCAP"] = "Geant4OpticalTrackerAction"

# Disable user tracker particle handler, so hits can be associated to photons
SIM.part.userParticleHandler = ""

# Register hit with low energy, compatible with zero
SIM.filter.tracker = "edep0"

# Define filter, so detector is only sensitive to optical photons
SIM.filter.filters["opticalphotons"] = dict(
        name="ParticleSelectFilter/OpticalPhotonSelector",
        parameter={"particle": "opticalphoton"},
        )
SIM.filter.mapDetFilter["ARCBARREL"] = "opticalphotons"
SIM.filter.mapDetFilter["ARCENDCAP"] = "opticalphotons"

# Particle gun settings: pions with fixed energy, random direction
SIM.numberOfEvents = 1
SIM.enableGun = True
SIM.gun.particle = "kaon+"
SIM.gun.energy = "10*GeV"
SIM.gun.multiplicity = 1
SIM.gun.position = "0 0 0"
SIM.gun.direction = "-1 0 0"

#SIM.gun.distribution = 'cos(theta)'
## Maximal azimuthal angle for random distribution
#SIM.gun.phiMax = 0.52
## Minimal azimuthal angle for random distribution
#SIM.gun.phiMin = 0.52
## Maximal polar angle for random distribution
#SIM.gun.thetaMax = 1.57
## Minimal polar angle for random distribution
#SIM.gun.thetaMin = 1.57

SIM.outputFile = "arc_kaon+_10GeV.root"
