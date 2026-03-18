#!/bin/bash

# Channel-to-threshold mapping
declare -A thresholds=(

  [nue_e]=0.0
  [nuebar_e]=0.0
  [numu_e]=0.0
  [numubar_e]=0.0
  [nutau_e]=0.0
  [nutaubar_e]=0.0

  [nue_O16]=16.3
  [nue_O16_2]=19.9
  [nue_O16_Suzuki2018]=16
  [nue_O16_Newton]=16
  [nuebar_O16]=13.6
  [nc_nue_O16]=14.0
  [nc_nuebar_O16]=14.0
  [nc_numu_O16]=14.0
  [nc_numubar_O16]=14.0

  [nue_C12]=19.1
  [nc_nue_C12]=15.1
  [nc_nuebar_C12]=15.1
  [nc_numu_C12]=15.1
  [nc_numubar_C12]=15.1

  [nue_C13]=2.2
  [nc_nue_C13]=3.7
  [nc_nuebar_C13]=3.7
  [nc_numu_C13]=3.7
  [nc_numubar_C13]=3.7
)

for channel in "${!thresholds[@]}"; do
  thresh=${thresholds[$channel]}
  echo "Generating interaction matrix for $channel with threshold $thresh MeV"
  
  perl threshold_interaction.pl "$thresh"
  mv interaction_threshold.ssv "interaction_${channel}.ssv"
done

