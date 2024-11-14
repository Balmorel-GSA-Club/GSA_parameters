import pandas as pd
import numpy as np
from gamspy import SpecialValues

# This class is used to deal with paramneters in the model
class GSA_parameters :
    def __init__(self, input_file):
        self.input = pd.read_csv(input_file)
        self.parameters = self.input["Parameter"]

    def load_sets(self):
        sets = "FUELPRICE, GDATA_numerical, GDATA_categorical, EMI_POL, XINVCOST, XH2INVCOST, DE, SUBTECHGROUPKPOT, HYDROGEN_DH2, XKRATE"
        return sets
    
    def update_input(self, scenario_data, sample):
        EMI_POL = scenario_data["EMI_POL"].records
        EMI_POL.loc[(EMI_POL["CCCRRRAAA"]=="DENMARK") & (EMI_POL["GROUP"]=="ALL_SECTORS") & (EMI_POL["EMIPOLSET"]=="TAX_CO2"), "value"]=sample["CO2_TAX"]
        
        XINVCOST = scenario_data["XINVCOST"].records
        XINVCOST.loc[:,"value"] *= sample["E_T_INVC"]

        GDATA = scenario_data["GDATA_numerical"].records
        GDATA.loc[(GDATA["GGG"].str.contains("ELYS")) & (GDATA["GDATASET"].str.contains("GDINVCOST0")),"value"]*=sample["ELEC_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("STEAM")) & (GDATA["GDATASET"].str.contains("GDINVCOST0")),"value"]*=sample["ELEC_STEAM_INVC"]

        FUELPRICE = scenario_data["FUELPRICE"].records
        FUELPRICE.loc[FUELPRICE["FFF"]=="NATGAS","value"]*=sample["NATGAS_P"]
        
        SUBTECHGROUPKPOT = scenario_data["SUBTECHGROUPKPOT"].records
        SUBTECHGROUPKPOT.loc[SUBTECHGROUPKPOT["TECH_GROUP"]=="SOLARPV", "value"]*=sample["PV_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DK")), "value"]*= sample["ON_SHORE_DK"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DE")), "value"]*= sample["ON_SHORE_DE"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.startswith(("NO","SE","NL"))), "value"]*= sample["ON_SHORE_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DK")), "value"]*= sample["OFF_SHORE_DK"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DE")), "value"]*= sample["OFF_SHORE_DE"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.startswith(("NO","SE","NL"))), "value"]*= sample["OFF_SHORE_NORTH"]
        
        XH2INVCOST = scenario_data["XH2INVCOST"].records
        XH2INVCOST.loc[:,"value"] *= sample["H2_T_INVC"]

        HYDROGEN_DH2 = scenario_data["HYDROGEN_DH2"].records
        HYDROGEN_DH2.loc[HYDROGEN_DH2["CCCRRRAAA"].str.contains("DK"), "value"] *= sample["H2_Demand_DK"]
        HYDROGEN_DH2.loc[HYDROGEN_DH2["CCCRRRAAA"].str.contains("DE"), "value"] *= sample["H2_Demand_DE"]
        HYDROGEN_DH2.loc[HYDROGEN_DH2["CCCRRRAAA"].str.startswith(("NO", "SE", "NL")), "value"] *= sample["H2_Demand_Rest"]
        
        DE = scenario_data["DE"].records
        DE.loc[DE["RRR"].str.contains("DK"), "value"] *= sample["DE_Demand_DK"]
        DE.loc[DE["RRR"].str.contains("DE"), "value"] *= sample["DE_Demand_DE"]
        DE.loc[DE["RRR"].str.startswith(("NO", "SE", "NL")), "value"] *= sample["DE_Demand_Rest"]

        XKRATE = scenario_data["XKRATE"].records
        XKRATE.loc[:,"value"] = sample["E_T_AVAIL"]
        
        return scenario_data