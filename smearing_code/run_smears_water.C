void run_smears_water() {
    TString config = "eos";
    // TString res = "0.10";
    TString res = "unit_matrix";


    smear(config, "ibd", res);
    smear(config, "nue_e", res);
    smear(config, "nuebar_e", res);
    smear(config, "numu_e", res);
    smear(config, "numubar_e", res);
    smear(config, "nutau_e", res);
    smear(config, "nutaubar_e", res);
    smear(config, "nue_O16", res);
    smear(config, "nue_O16_2", res);
    smear(config, "nue_O16_Newton", res);
    smear(config, "nuebar_O16", res);
    smear(config, "nc_nue_O16", res);
    smear(config, "nc_nuebar_O16", res);
    smear(config, "nc_numu_O16", res);
    smear(config, "nc_numubar_O16", res);
    smear(config, "nc_nutau_O16", res);
    smear(config, "nc_nutaubar_O16", res);
}

