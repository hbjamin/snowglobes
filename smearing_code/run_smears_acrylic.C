void run_smears_acrylic() {
    TString config = "eos_av";
    // TString res = "0.10";
    TString res = "unit_matrix";

    smear(config, "nue_e", res);
    smear(config, "nuebar_e", res);
    smear(config, "numu_e", res);
    smear(config, "numubar_e", res);
    smear(config, "nuebar_O16", res);
    smear(config, "nc_nue_O16", res);
    smear(config, "nc_nuebar_O16", res);
    smear(config, "nc_numu_O16", res);
    smear(config, "nc_numubar_O16", res);
    smear(config, "nue_O16", res);
    smear(config, "nue_O16_2", res);
    smear(config, "nue_O16_Suzuki2018", res);
    smear(config, "nue_O16_Newton", res);
    smear(config, "nue_C12", res);
    smear(config, "nc_nue_C12", res);
    smear(config, "nc_nuebar_C12", res);
    smear(config, "nc_numu_C12", res);
    smear(config, "nc_numubar_C12", res);
    smear(config, "nue_C13", res);
    smear(config, "nc_nue_C13", res);
    smear(config, "nc_numu_C13", res);
    smear(config, "nc_nuebar_C13", res);
    smear(config, "nc_numubar_C13", res);
}

