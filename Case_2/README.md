Case 2: Hydration of a 4-site system
====================================
- `Prep`: A folder containing input files for preparing the system with a standard protocol composed of steps including system solvation, energy minimization, NVT and NPT equilibration and finally a short standard MD simulation in the NPT ensemble. This folder additionally include the simulation inputs for running short torsional metadynamics simulations that were used to generate configurations in different metastable states. 

- `Test_1`: A folder containing simulation inputs for running 4 types of simulations in 3 replicates, including
  - 1D alchemical metadynamics starting from State A
  - 1D alchemical metadynamics starting from State B
  - 2D alchemical metadynamics starting from State A
  - 2D alchemical metadynamics starting from State B

  Some analysis results are also included.
