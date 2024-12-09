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
        EMI_POL = scenario_data["EMI_POL"]
        EMI_POL.columns = ["YYY", "CCCRRRAAA", "GROUP", "EMIPOLSET", "value"]
        EMI_POL.loc[(EMI_POL["CCCRRRAAA"]=="DENMARK") & (EMI_POL["GROUP"]=="ALL_SECTORS") & (EMI_POL["EMIPOLSET"]=="TAX_CO2") & (EMI_POL["value"]>=1e-320), "value"]=sample["CO2_TAX"]
        
        XINVCOST = scenario_data["XINVCOST"]
        XINVCOST.columns = ["YYY", "IRRE", "IRRI", "value"]
        XINVCOST.loc[(XINVCOST["value"]>=1e-320),"value"] *= sample["E_T_INVC"]

        GDATA = scenario_data["GDATA_numerical"]
        GDATA.columns = ["GGG", "GDATASET", "value"]
        GDATA.loc[(GDATA["GGG"].str.contains("ELYS")) & (GDATA["GDATASET"].str.contains("GDINVCOST0")) & (GDATA["value"]>=1e-320),"value"]*=sample["ELEC_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("STEAM")) & (GDATA["GDATASET"].str.contains("GDINVCOST0")) & (GDATA["value"]>=1e-320),"value"]*=sample["ELEC_STEAM_INVC"]

        FUELPRICE = scenario_data["FUELPRICE"]
        FUELPRICE.columns = ["YYY", "AAA", "FFF", "value"]
        FUELPRICE.loc[(FUELPRICE["FFF"]=="NATGAS") & (FUELPRICE["value"]>=1e-320),"value"]*=sample["NATGAS_P"]
        
        SUBTECHGROUPKPOT = scenario_data["SUBTECHGROUPKPOT"]
        SUBTECHGROUPKPOT.columns = ["CCCRRRAAA", "TECH_GROUP", "SUBTECH_GROUP", "value"]
        SUBTECHGROUPKPOT.loc[SUBTECHGROUPKPOT["TECH_GROUP"]=="SOLARPV", "value"]*=sample["PV_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DK")) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["ON_SHORE_DK"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DE")) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["ON_SHORE_DE"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.startswith(("NO","SE","NL", "UK"))) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["ON_SHORE_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DK")) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["OFF_SHORE_DK"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DE")) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["OFF_SHORE_DE"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.startswith(("NO","SE","NL", "UK"))) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["OFF_SHORE_NORTH"]
        
        XH2INVCOST = scenario_data["XH2INVCOST"]
        XH2INVCOST.columns = ["YYY", "IRRE", "IRRI", "value"]
        XH2INVCOST.loc[(XH2INVCOST["value"]>=1e-320),"value"] *= sample["H2_T_INVC"]

        HYDROGEN_DH2 = scenario_data["HYDROGEN_DH2"]
        HYDROGEN_DH2.columns = ["YYY", "CCCRRRAAA", "value"]
        HYDROGEN_DH2.loc[(HYDROGEN_DH2["CCCRRRAAA"].str.contains("DK")) & (HYDROGEN_DH2["value"]>=1e-320), "value"] *= sample["H2_Demand_DK"]
        HYDROGEN_DH2.loc[(HYDROGEN_DH2["CCCRRRAAA"].str.contains("DE")) & (HYDROGEN_DH2["value"]>=1e-320), "value"] *= sample["H2_Demand_DE"]
        HYDROGEN_DH2.loc[(HYDROGEN_DH2["CCCRRRAAA"].str.startswith(("NO", "SE", "NL", "UK"))) & (HYDROGEN_DH2["value"]>=1e-320), "value"] *= sample["H2_Demand_Rest"]
        
        DE = scenario_data["DE"]
        DE.columns = ["YYY", "RRR", "DEUSER", "value"]
        DE.loc[(DE["RRR"].str.contains("DK")) & (DE["value"]>=1e-320), "value"] *= sample["DE_Demand_DK"]
        DE.loc[(DE["RRR"].str.contains("DE")) & (DE["value"]>=1e-320), "value"] *= sample["DE_Demand_DE"]
        DE.loc[(DE["RRR"].str.startswith(("NO", "SE", "NL", "UK"))) & (DE["value"]>=1e-320), "value"] *= sample["DE_Demand_Rest"]

        XKRATE = scenario_data["XKRATE"]
        XKRATE.columns = ["IRRRE", "IRRRI", "SSS", "value"]
        XKRATE.loc[(XKRATE["value"]>=1e-320),"value"] = sample["E_T_AVAIL"]
        
        return scenario_data