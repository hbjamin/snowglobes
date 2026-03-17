#!/bin/bash

# Channel-to-threshold mapping
declare -A thresholds=(
  [nue_d]=2.2
  [nuebar_d]=2.2
  [nc_nue_d]=2.2
  [nc_nuebar_d]=2.2
  [nc_numu_d]=2.2
  [nc_numubar_d]=2.2
  [nc_nutau_d]=2.2
  [nc_nutaubar_d]=2.2

  [nue_e]=0.0
  [nuebar_e]=0.0
  [numu_e]=0.0
  [numubar_e]=0.0
  [nutau_e]=0.0
  [nutaubar_e]=0.0

  [nue_O16]=16.3
  [nuebar_O16]=13.6
  [nc_nue_O16]=14.0
  [nc_nuebar_O16]=14.0
  [nc_numu_O16]=14.0
  [nc_numubar_O16]=14.0
  [nc_nutau_O16]=14.0
  [nc_nutaubar_O16]=14.0

  [nue_O16_2]=19.9
  [nue_O16_Suzuki2018]=16
  [nue_O16_Newton]=16
)

for channel in "${!thresholds[@]}"; do
  thresh=${thresholds[$channel]}
  echo "Generating interaction matrix for $channel with threshold $thresh MeV"
  
  perl threshold_interaction.pl "$thresh"
  mv interaction_threshold.ssv "interaction_${channel}.ssv"
done

