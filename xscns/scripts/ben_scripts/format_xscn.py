import numpy as np

# Input and output file names
infile = '16ONewton.txt'  # your original two-column file
outfile = 'xs_nue_O16_Newton200.dat'

# Load the data
data = np.loadtxt(infile)  # assumes two columns: energy, cross-section
energy = data[:, 0]        # first column: energy
cross = data[:, 1]*1e2     # second column: nu_e cross section

# Convert energy to GeV if in MeV
energy_gev = energy * 1e-3  # comment out if already in GeV

# Take log10
logE = np.log10(energy_gev)

# Open output file
with open(outfile, 'w') as f:
    # Write headers
    f.write('# Electron neutrino-oxygen scattering cross section 5MeV-60MeV (10^-8 cm^2/GeV) #\n')
    f.write('# log(energy in GeV)       nu_e       nu_mu       nu_tau       nu_e_bar       nu_mu_bar       nu_tau_bar #\n\n')

    # Write data
    for l, c in zip(logE, cross):
        f.write(f'{l:15.5f} {c:10.5e} {0:10.0f} {0:10.0f} {0:10.0f} {0:10.0f} {0:10.0f}\n')

