# CERN Summer School 2024: <br> New Developments in Full Simulation Software for FCC

## Table of Contents
- [Main Purpose of the Project](#main-purpose-of-the-project)
- [How Does the Pipeline Work?](#how-does-the-pipeline-work)
  - [Pipeline Variables](#pipeline-variables)
  - [Pipeline Stages](#pipeline-stages)
    - [Setup](#setup)
    - [Execute Scrpits](#execute-scripts)
    - [Make Plots](#make-plots)
    - [Make Web](#make-web)
    - [Deploy](#deploy)
    - [Cleanup](#cleanup)
- [How to Use the Pipeline: Adding a New Detector Concept](#how-to-use-the-pipeline-adding-a-new-detector-concept)

<br>

# Main Purpose of the Project

The main idea of this project is developing new tools for the **validation of the FCC software**. Software validation is a fundamental step in the software development lifecycle, and is needed to ensure that the final products meets the specified requirements and fulfills its intended purpose. <br>
In the context of this work, this means making sure that, even though the code may compile and run without any issues, the physics results that we obtain from the simulations and analyses are compatible with what we expect.

In order to achieve these goals, we use a **GitLab CI/CD pipeline** to run daily automated tests using the new versions of the code available. The results of these tests, comparing the output of new versions with reference stable ones, can be seen on [this website](https://key4hep-validation.web.cern.ch/index.html).

<br>

# How Does the Pipeline Work?

## Pipeline Variables

The pipeline acts as a long bash script, whose behaviour can be controlled through specific **pipeline variables**. These variables are defined at the [beginnig of the pipeline](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L1-49), and can be set to the desired values when instantiating a new pipeline via the *Pipeline Schedule Editor*. <br>
Here is the list of the variables used in this specific pipeline:

1. **VALIDATION_JOB_TYPE**: Which type of validation job to run. In order to use the new version of the pipeline, please select *run_script*.
2. **VERSIONS**: List of detector versions that need to tested, separated by a comma (e.g. "ALLEGRO_o1_v03, IDEA_o1_v03, CLD_o3_v01").
3. **MAKE_REFERENCE_SAMPLE**: Whether to store the output of the simulation and reconstruction phase as a reference for future use or new results to be checked.
4. **WORKAREA**: Where to run the validation on the runner.
5. **PLOTAREA**: Where to store the plots and information for the validation website on the runner (path relative to *WORKAREA*).
6. **REFERENCE_SAMPLE**: Where to find the reference sample on the runner (path relative to *WORKAREA*).
7. **NUMBER_OF_EVENTS**: How many events to run in the simulation step.
8. **TAG**: Which tag to use for the key4hep release
9. **CI_OUTPUT_DIR**: Path to the web page files, needed for the website deployment.

## Pipeline Stages

The pipeline main process is divided into so-called **stages**, logically distinct steps that are run in a specified order. Stages can contain multiple **jobs** that are run concurrently, though in this pipeline each stage only has one specific job assigned to it.
The execution of the stages can depend on the global pipeline variables set at the start or on the success of the previous stages, providing a very flexible way to handle different situations.

### [Setup](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L84-117)

The first stage of the pipeline is tasked with cleaning up the working directory of any trace of previous iterations of the pipeline for the detector versons to be tested, and/or create the necessary directories if they are not present yet. It also clones the [key4hep-reco-validation](https://github.com/key4hep/key4hep-reco-validation) containing the scripts that will be executed in the next stage.

### [Execute Scripts](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L120-153)

In this stage, as the name implies, the scripts for the tests are executed. In order for this stage to work properly, care should be put into following the proper structure and naming conventions.

The bash scripts to be executed are contained in the *key4hep-reco-validation/* directory, downloaded in the previous step. This repository is structured to mirror the [k4geo repository](https://github.com/key4hep/k4geo/tree/main/FCCee), so that each detector concept and the path leading to its files are individuated by its **geometry** (its generic name, e.g. *ALLEGRO*) and its **version** (the geometry followed by the option and version number, e.g. *ALLEGRO_o1_v03*). <br>
An example structure would look like this:
```
key4hep-reco-validation/
└── scripts/
    └── FCCee/
        ├── ALLEGRO/
        |   └── ALLEGRO_o1_v03/
        |       └── ALLEGRO_o1_v03_script.sh
        ├── IDEA/
        |   └── IDEA_o1_v03/
        |       └── IDEA_o1_v03_script.sh
        ├── CLD/
        |   ├── CLD_o2_v06/
        |   |   └── CLD_o2_v06_script.sh
        |   └── CLD_o3_v01/
        |       ├── CLD_o3_v01_script.sh
        |       └── ARC_standalone_script.sh
        └── utils/
``` 

For each of the detector versions specified in the *VERSIONS* list, the *GEOMETRY* is defined by extracting the substring before the first underscore character.
For each geometry-version pair thus found, the bash scripts contained in the *key4hep-reco-validation/scripts/FCCee/GEOMETRY/VERSION* directory are executed. To be recognised as such, their file name must end in *_script.sh*. <br>
For example, using the example *key4hep-reco-validation* shown above, if the *VERSIONS* list contains *CLD_o3_v01* both *CLD_o3_v01_script.sh* and *ARC_standalone_script.sh* will be run.

These scripts are not properly part of the pipeline and should be submitted by the users, but ideally they should include a simulation (and optionally reconstruction) steps, followed by the desired analyses and checks. Their output must be a ROOT file containing the histograms of the variable of interest. This ROOT file must also follow a strict structure, where each TH1 object is stored inside a TDirectory whose name reflects the subsystem that is currently being analyzed. <br>
See section () for further comments on how to properly create these scripts and what structure to follow.

Finally, at the end of this stage the output ROOT files are saved in the correct reference folders if the *MAKE_REFERENCE_SAMPLE* variable is set to "yes".

### [Make Plots](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L156-188)

The [plotting script](https://github.com/enlupi/key4hep-reco-validation/blob/validation_project/scripts/FCCee/utils/plot_histograms.py) is run on all the output ROOT files produced in the previous step. This script checks all the histograms saved inside a file and compares them to a reference file, producing plots of the two distributions with different backgrounds depending on the outcome of the comparison: white if they match, red if they do not, and yellow if the reference histogram could not be found.

Three tests are available to compare the histograms:
1. Check if all bins have exactly the same edges and number of entries.
2. Chi squared test.
3. Kolmogorov-Smironov test.

This stage is only executed if the *MAKE_REFERENCE_SAMPLE* variable is set to "no".

### [Make Web](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L191-230)

This stage is responsible of creating the html files for the static website by running a [python script](https://github.com/enlupi/key4hep-reco-validation/blob/validation_project/web/python/make_web.py). <br>
Information about the current release of *key4hep* is also collected and stored to a file, to be included into the website.

This stage is only executed if the *MAKE_REFERENCE_SAMPLE* variable is set to "no".

### [Deploy](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L233-259)

As the name implies, this stage simply deploys the website.

This stage is only executed if the *MAKE_REFERENCE_SAMPLE* variable is set to "no".

### [Cleanup](https://gitlab.cern.ch/key4hep/k4-validation/-/blob/add_comparison/.gitlab-ci.yml?ref_type=heads#L262-275)

A final cleanup is done to remove the *key4hep-reco-validation* cloned in  the *setup* stage and the metadata file with the key4hep release info created in the *make_web* step. <br>
Note that all the other files produced by the pipeline will not be deleted until the *setup* stage in the next pipeline execution, so that they can be further inspected in case of issues.

# How to Use the Pipeline: Adding a new Detector Concept 

The pipeline is very flexible and takes care of the majority of the work, so adding new detector concepts to be tested is relatively easy and straightforward. Here are the necessary steps to follow.

## 

