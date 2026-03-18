import numpy as np

# Input and output file names
infile = 'ibdNewton.txt'  # your original two-column file
outfile = 'ibd_bad.dat'

# Load the data
data = np.loadtxt(infile)  
energy = data[:, 0]        
# Newton values are 10x lower than SNOwGLoBES due to binning normalization
# Proven by comparing ibd cross section values in Newton and SNOwGLoBES 
cross = data[:, 1] * 10 

# Convert energy to GeV if in MeV
energy_gev = energy * 1e-3  

# Take log10
logE = np.log10(energy_gev)

# Open output file
with open(outfile, 'w') as f:
    # Write headers
    f.write('# Electron neutrino-oxygen scattering cross section 5MeV-60MeV (10^-38 cm^2/GeV) #\n')
    f.write('# log(energy in GeV)       nu_e       nu_mu       nu_tau       nu_e_bar       nu_mu_bar       nu_tau_bar #\n\n')

    # Write data
    for l, c in zip(logE, cross):
        f.write(f'{l:15.5f} {c:10.5e} {0:10.0f} {0:10.0f} {0:10.0f} {0:10.0f} {0:10.0f}\n')

