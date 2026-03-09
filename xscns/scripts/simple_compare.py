#!/usr/bin/env python3

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print("Usage: python ./compare_xs.py <filename1> <filename2> [<filename3>...] [flavornum]")
    print("flavornum is 1 = nue, 2 = numu, 3 = nutau, 4 = nuebar, 5 = numubar, 6 = nutaubar")
    sys.exit(1)

# Parse command-line arguments
flavornum = 1
filelist = []

for arg in sys.argv[1:]:
    if arg.isdigit():
        flavornum = int(arg)
    else:
        filelist.append(arg)

if not (1 <= flavornum <= 6):
    print("Invalid flavornum. Must be an integer between 1 and 6.")
    sys.exit(1)

flavornamelist = ["nue", "numu", "nutau", "nuebar", "numubar", "nutaubar"]

def ReadXS(filename, flavornum=1):
    xs_data = []
    with open(filename, "r") as infile:
        for line in infile:
            if line.startswith("#") or len(line.strip()) < 5:
                continue
            try:
                xs_data.append([float(x) for x in line.split()])
            except ValueError:
                continue

    if not xs_data:
        raise ValueError("No valid data in file: " + filename)

    xs_data = np.array(xs_data)

    # Energy axis is stored as log10(E)
    E = 10 ** xs_data[:, 0]  # GeV
    xs = xs_data[:, flavornum] * E  # scale by E like in ROOT script
    return E, xs

plt.figure(figsize=(8, 6))

for i, fname in enumerate(filelist):
    label = os.path.basename(fname)
    E, xs = ReadXS(fname, flavornum)
    plt.plot(E, xs, lw=2, label=label)

#plt.xscale("log")
plt.xlim(0,0.06)
plt.yscale("log")
plt.xlabel("E (GeV)")
plt.ylabel(r"$10^{-38}$ cm$^2$")
plt.title(f"Cross Section ({flavornamelist[flavornum-1]})")
plt.legend()
plt.tight_layout()
plt.show()

