import argparse
import numpy as np


def load_newton_table(path):
    """
    Expect a simple 2‑column file:
      E [MeV]   sigma(E) [10^-38 cm^2]
    """
    data = np.loadtxt(path)
    energy_mev = data[:, 0]
    sigma = data[:, 1]
    return energy_mev, sigma


def load_template_logE(path):
    """
    Read a SNOwGLoBES‑style xs file and return the log10(E/GeV) grid
    from the first non‑comment column.
    """
    logE_vals = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            try:
                logE_vals.append(float(parts[0]))
            except ValueError:
                continue
    return np.array(logE_vals)


def compute_bin_edges_from_centers(logE_centers):
    """
    Given log10(E/GeV) bin centers, construct bin edges in the same space
    by midpoints between neighboring centers, with simple extrapolation
    at the ends.
    """
    logE_centers = np.asarray(logE_centers)
    n = logE_centers.size
    if n < 2:
        raise ValueError("Need at least two template points to define bin edges.")

    edges = np.empty(n + 1)
    # interior edges: midpoints
    edges[1:-1] = 0.5 * (logE_centers[:-1] + logE_centers[1:])
    # extrapolate first and last
    edges[0] = logE_centers[0] - 0.5 * (logE_centers[1] - logE_centers[0])
    edges[-1] = logE_centers[-1] + 0.5 * (logE_centers[-1] - logE_centers[-2])
    return edges


def rebin_newton_to_template(energy_mev, sigma, logE_template):
    """
    Map Newton's (E[MeV], sigma(E)) table onto the SNOwGLoBES logE grid.

    Assumptions:
      - Newton input: sigma(E) in units of 10^-38 cm^2 (total cross section).
      - SNOwGLoBES expects: sigma(E) / E in units of 10^-38 cm^2 / GeV,
        tabulated at the bin centers given by logE_template.

    So we:
      1. Convert the SNOwGLoBES log10(E/GeV) grid to energies in MeV.
      2. Interpolate the Newton σ(E) onto those energies.
      3. Divide by E[GeV] to obtain σ(E)/E in 10^-38 cm^2 / GeV.
    """
    # Ensure sorted by energy
    order = np.argsort(energy_mev)
    energy_mev = np.asarray(energy_mev)[order]
    sigma = np.asarray(sigma)[order]

    # Convert SNOwGLoBES log10(E/GeV) bin centers to energies
    E_gev = 10.0 ** np.asarray(logE_template)
    E_mev = E_gev * 1.0e3

    # Interpolate Newton sigma(E) onto those energies (in MeV).
    # Outside the Newton range, set sigma = 0.
    sigma_interp = np.interp(E_mev, energy_mev, sigma, left=0.0, right=0.0)

    # Convert to SNOwGLoBES units: sigma(E)/E in 10^-38 cm^2 / GeV.
    # Guard against division by zero, though E_gev should always be > 0.
    with np.errstate(divide="ignore", invalid="ignore"):
        sigma_sg = np.where(E_gev > 0.0, sigma_interp / E_gev, 0.0)

    return sigma_sg


def write_snowglobes_xs(outfile, logE, sigma_binned, channel):
    # Map channel name to column index: 0..5 for
    # (nu_e, nu_mu, nu_tau, nu_e_bar, nu_mu_bar, nu_tau_bar)
    flavor_to_col = {
        "nue": 0,
        "numu": 1,
        "nutau": 2,
        "nuebar": 3,
        "numubar": 4,
        "nutaubar": 5,
    }
    col_idx = flavor_to_col[channel]

    with open(outfile, "w") as f:
        f.write(
            "# log(energy in GeV)  nu_e      nu_mu      nu_tau"
            "      nu_e_bar  nu_mu_bar  nu_tau_bar #\n\n"
        )

        for lE, sig in zip(logE, sigma_binned):
            cols = [0.0] * 6
            cols[col_idx] = sig
            f.write(
                f"{lE:15.5f}"
                f" {cols[0]:10.5e} {cols[1]:10.5e} {cols[2]:10.5e}"
                f" {cols[3]:10.5e} {cols[4]:10.5e} {cols[5]:10.5e}\n"
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Rebin a 2‑column Newton xscn file (E[MeV], σ[10^-38 cm^2]) "
            "onto a SNOwGLoBES log‑spaced GeV grid, preserving the "
            "integrated cross section per bin and writing a standard "
            "SNOwGLoBES xs table (log10(E[GeV]), 6 flavor columns)."
        )
    )
    parser.add_argument("infile", help="Input Newton file (E[MeV], sigma)")
    parser.add_argument("template", help="Template SNOwGLoBES xs file to define the logE grid")
    parser.add_argument("outfile", help="Output rebinned SNOwGLoBES‑style xs file")
    parser.add_argument(
        "--channel",
        choices=["nue", "nuebar", "numu", "numubar", "nutau", "nutaubar"],
        default="nue",
        help="Which neutrino flavor column to fill (others set to zero).",
    )

    args = parser.parse_args()

    energy_mev, sigma = load_newton_table(args.infile)

    # Use template grid and preserve the integral in each bin
    logE_template = load_template_logE(args.template)
    sigma_binned = rebin_newton_to_template(energy_mev, sigma, logE_template)

    write_snowglobes_xs(args.outfile, logE_template, sigma_binned, args.channel)


if __name__ == "__main__":
    main()