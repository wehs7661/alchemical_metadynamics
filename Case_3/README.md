Case 3: Methylation of adenosine in its isolated form and in a duplex
=====================================================================
- `AlchMet.mdp`: The MDP file used in all simulations of this case.

- Each folder contains topologies (.top, .itp), the .tpr and a .pdb. Then in two separate folders are present the input files needed for simulation with static or dynamic bias.
  - `Dynamic Bias`: A folder containing the PLUMED file input (`plumed.dat`), the final structure (`confout.gro`) and free energy surafce (`fes.dat`) obtained from a dynamic-bias simulation.
  - `Static Bias`: A folder containing the PLUMED file input (`plumed.dat`), the HILLS files generated in the dynamic-bias simulation, and the final structure (`confout.gro`). 
