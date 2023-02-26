alchemical_metadynamics
=======================
[//]: # (Badges)
[![plumID:23.003](https://www.plumed-nest.org/eggs/23/003/badge.svg)](https://www.plumed-nest.org/eggs/23/003/)
[![DOI](https://img.shields.io/badge/DOI-10.1021%2Facs.jctc.2c01258-success.svg)](https://doi.org/10.1021/acs.jctc.2c01258)

## Description
This is a repository for maintaining the simulation files and analysis codes for the alchemical metadynamics project, which has been published in the Journal of Chemical Theory and Computation, titled [Alchemical Metadynamics: Adding Alchemical Variables to Metadynamics to Enhance Sampling in Free energy calculations](https://doi.org/10.1021/acs.jctc.2c01258).


In the paper, we proposed adding alchemical variables to metadynamics to enhance sampling for free energy calculations. The method, termed as **alchemical metadynamics**, is demonstrated with three different test systems/alchemical processes, including decoupling an argon atom and a 4-site model from water, and the methylation of a nucleoside both in the isolated form and in a duplex. Note that
- To keep the repository lightweight, we don't store simulation output files, including `*.edr`, `*.log`, `*.trr`, `*.xtc`, `*cpt`, `*COLVAR*`, `*HILLS*` and most of the `*xvg` files. We do keep some `*txt` files storing analysis results and some analysis outputs in the `*png` format.
- Some preliminary tests of the project were stored in the archived project repository [MetaD_EXE_TestSys](https://github.com/wehs7661/MetaD_EXE_TestSys).
- The first version of this repository is the same as the [commit 65cd812](https://github.com/wehs7661/alchemical_MetaD_archived/tree/65cd812a1c11042126abd0d177dfb5e9701f8864) of our previous project repository [alchemical_MetaD_archived](https://github.com/wehs7661/alchemical_MetaD_archived) but without the previous git history the files of the old System 3 that have been migrated to [MetaD_EXE_TestSys](https://github.com/wehs7661/MetaD_EXE_TestSys).

This repository includes the folders listed below. For more details about the files in each folder, please refer to the README file in each folder. Note that any COLVAR or HILLS files named in the form of `HILLS*fake` or `COLVAR*fake` in this repo are just placeholders used to pass the test on PLUMED-NEST and were not used in our study. (The corresponding changes have also been made to each `plumed_sum_bias.dat`.) The names of the real files used in our study are without the suffix of `_fake`.
- `Case_1`: In Case 1, we compared 1D alchemical metadynamics with expanded ensemble in decoupling an argon atom in water. This case validates the usage of our algorithm.

- `Case_2`: In Case 2, we compared 1D alchemical metadynamics with 2D alchemical metadynamics in decoupling a 4-site model in water. This case demonstrates the advantages of introducing configurational collective variables (CVs) in higher-dimensional alchemical metadynamics. 

- `Case_3`: In Case 3, we compared Hamiltonian replica exchange with 1D + 2D alchemical metadynamics in methylating adenosine in its isolated form and in a duplex. This case shows that alchemical metadynamics eliminates the need for running multiple Hamiltonian replica exchange simulations to calculate relative free energy differences. 

- `project_paper`: This folder contains LaTex-relevant files for different versions of the paper submitted to arXiv and the Journal of Chemical Theory and Computation (JCTC). It also includes intermediate files for preparing the final figures in the manuscript and relevant codes for generating the figures. 

## Contributors of the repo
- Wei-Tse Hsu (wehs7661@colorado.edu)
- Valerio Piomponi (vpiompon@sissa.it)