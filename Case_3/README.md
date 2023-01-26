Case 3: Methylation of adenosine in its isolated form and in a duplex
=====================================================================
- The AlchMet.mdp is the parameters input file used in all simulations of this case

- Each folder contains topologies (.top, .itp), the .tpr and a .pdb. Then in two separate folders are present the input files needed for simulation with static or dynamic bias.
  - Dynamic Bias: contain the plumed file input (plumed.dat), the final structure (confout.gro) and Free energy surafce (fes.dat) obtained from the simulation.
  - Static Bias: contain the plumed file input (plumed.dat), the HILLS files generated in the dynamic bias simulation, and the final structure (confout.gro). 
