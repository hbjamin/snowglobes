"""
from_sntools.py

Script to generate a GLoBES cross section file from a cross section implemented
in sntools (https://github.com/SNEWS2/sntools).
To use this script:
  1) Install sntools. (See link above for instructions.)
  2) If necessary, adjust the lines marked with a "TODO" comment below
  3) Run this script. (Python 3.7 or later recommended.)
"""
from math import log10
from numpy import linspace
from scipy import integrate


##### TODO: adjust variables in this block as necessary #####

# import the desired interaction channel from sntools
import sntools.interaction_channels.o16eb as channel

# flavor of interacting neutrino ('nue', 'nuebar', 'numu', 'numubar', 'nutau', 'nutaubar')
flv = 'nuebar'

# name of output file
output_file = f'xs_{flv}_O16_Suzuki2018.dat'

# comments to be written at the top of the output file
preamble = ("# Electron antineutrino-oxygen charged-current cross section 5MeV-100MeV (10^-38 cm^2/GeV)\n"
            "# Based on arXiv:1807.02367 (calculations) and arXiv:1809.08398 (fit).\n")


##### No need to change anything below this line #####

sntools_flavors = {'nue': 'e', 'numu': 'x', 'nutau': 'x', 'nuebar': 'eb', 'numubar': 'xb', 'nutaubar': 'xb'}

c = channel.Channel(sntools_flavors[flv])

def xs(eNu):
    try:
        eE_min, eE_max = c.bounds_eE(eNu)
    except UnboundLocalError:
        return 0  # if eNu is below energy threshold of the interaction
    
    if eNu >= c.bounds_eNu[0]:
        xs_in_natural_units = integrate.quad(lambda eE: c.dSigma_dE(eNu, eE), eE_min, eE_max, points=c._opts(eNu)["points"])[0]
    else:
        xs_in_natural_units = 0
    cm2mev = 5.067731E10  # conversion factor derived from hbar*c = 197 MeV*fm = 1
    xs_in_cm2 = xs_in_natural_units / cm2mev**2
    e_in_GeV = eNu / 1000
    return xs_in_cm2 * 1e38 / e_in_GeV


with open(output_file, 'w') as outfile:
    outfile.write(preamble)
    outfile.write("# log(energy in GeV)   nu_e       nu_mu      nu_tau       nu_e_bar    nu_mu_bar  nu_tau_bar\n\n")

    for log10eNu in linspace(log10(0.005), log10(0.100), num=1001):
        eNu = 10**log10eNu * 1000  # convert log10(GeV) to MeV
        val = xs(eNu)
        entry = f"{log10eNu:^+20.6f}"
        for f in sntools_flavors.keys():
            if f == flv:
                entry += f" {val:^15.5e}"
            else:
                entry += f" {0:^10}"
        outfile.write(f"{entry}\n")
