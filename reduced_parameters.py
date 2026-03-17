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

        GDATA = scenario_data["GDATA_numerical"]
        GDATA.columns = ["GGG", "GDATASET", "value"]
        GDATA.loc[(GDATA["GGG"].str.contains("STEAM")) & (GDATA["GDATASET"].str.contains("GDINVCOST0")) & (GDATA["value"]>=1e-320),"value"]*=sample["ELEC_STEAM_INVC"]

        FUELPRICE = scenario_data["FUELPRICE"]
        FUELPRICE.columns = ["YYY", "AAA", "FFF", "value"]
        FUELPRICE.loc[(FUELPRICE["FFF"]=="NATGAS") & (FUELPRICE["value"]>=1e-320),"value"]*=sample["NATGAS_P"]
        
        SUBTECHGROUPKPOT = scenario_data["SUBTECHGROUPKPOT"]
        SUBTECHGROUPKPOT.columns = ["CCCRRRAAA", "TECH_GROUP", "SUBTECH_GROUP", "value"]
        SUBTECHGROUPKPOT.loc[SUBTECHGROUPKPOT["TECH_GROUP"]=="SOLARPV", "value"]*=sample["PV_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_OFFSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DK")) & (SUBTECHGROUPKPOT["value"]>=1e-320), "value"]*= sample["OFF_SHORE_DK"]
        
        DE = scenario_data["DE"]
        DE.columns = ["YYY", "RRR", "DEUSER", "value"]
        DE.loc[(DE["RRR"].str.contains("DE")) & (DE["value"]>=1e-320), "value"] *= sample["DE_Demand_DE"]
        DE.loc[(DE["RRR"].str.startswith(("NO", "SE", "NL", "UK"))) & (DE["value"]>=1e-320), "value"] *= sample["DE_Demand_Rest"]
        
        return scenario_data