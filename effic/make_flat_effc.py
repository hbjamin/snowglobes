import os
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate flat (1.0) efficiency files for all channels from a given channel list."
    )
    parser.add_argument(
        "detector", type=str,
        help="Detector name (used in output filenames and directory)"
    )
    parser.add_argument(
        "channel_basename", type=str,
        help="Base name of the channel list (e.g., 'heavywater' for channels_heavywater.dat)"
    )
    return parser.parse_args()


def add_curlies(file_path):
    """Wrap the file contents in curly braces for SNOwGLoBES compatibility."""
    with open(file_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("{" + content + "}")
        f.truncate()


def make_flat_efficiencies(detector, channel_basename):
    """Generate flat (1.0) efficiency arrays for all channels in a given file."""
    channel_file = f"../channels/channels_{channel_basename}.dat"
    output_dir = f"{detector}"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(channel_file):
        raise FileNotFoundError(f"Could not find channel file: {channel_file}")

    with open(channel_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) < 5:
                print(f"Skipping malformed line: {line}")
                continue

            channel = parts[0]

            # Default binning: 200 bins from 0.0005 to 0.1 GeV (0.5 MeV to 100 MeV)
            out_bins = 200
            lo_en = 0.0005  # GeV
            hi_en = 0.1     # GeV

            energies = np.linspace(lo_en, hi_en, out_bins)
            eff = np.ones_like(energies)

            output_file = f"{output_dir}/effic_{channel}_{detector}.dat"
            with open(output_file, "w") as out:
                out.write(",".join(f"{x:.6f}" for x in eff))

            add_curlies(output_file)
            print(f"Created {output_file} with {out_bins} bins ({lo_en}–{hi_en} GeV)")

if __name__ == "__main__":
    args = parse_args()
    make_flat_efficiencies(args.detector, args.channel_basename)

