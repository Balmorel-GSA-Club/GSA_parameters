import pandas as pd
import numpy as np

# This class is used to deal with paramneters in the model
class GSA_parameters :
    def __init__(self, input_file):
        self.input = pd.read_csv(input_file)
        self.parameters = self.input["Parameter"]

    def load_sets(self):
        sets = "FUELPRICE, GDATA_numerical, GDATA_categorical, EMI_POL, CCS_CO2CAPTEFF_G, XINVCOST, XH2INVCOST, DE, SUBTECHGROUPKPOT, HYDROGEN_DH2"
        return sets
    
    def update_input(self, scenario_data, sample):
        North_l_PV = ["DK","NO","SE","NL", "DE4-E","DE4-N","DE4-W","FIN", "UK","EE","LV","LT","PL","BE"]
        North_PV = '|'.join(North_l_PV)
        South_l_PV = ["DE4-S","FR","IT","CH","AT","CZ","ES","PT","SK","HU","SI","HR","RO","BG","GR","IE","LU","AL","ME","MK","BA","RS","TR","MT","CY"]
        South_PV = '|'.join(South_l_PV)
        SUBTECHGROUPKPOT = scenario_data["SUBTECHGROUPKPOT"].records
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="SOLARPV") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains(North_PV)), "value"]*= sample["PV_LIMIT_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="SOLARPV") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains(South_PV)), "value"]*= sample["PV_LIMIT_SOUTH"]
    
    
        North_l = ["NO","SE","NL","FIN", "UK","EE","LV","LT","PL","BE"]
        North = '|'.join(North_l)
        South_l = ["FR","IT","CH","AT","CZ","ES","PT","SK","HU","SI","HR","RO","BG","GR","IE","LU","AL","ME","MK","BA","RS","TR","MT","CY"]
        South = '|'.join(South_l)
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DK")), "value"]*= sample["ONS_LIMIT_DK"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains("DE")), "value"]*= sample["ONS_LIMIT_DE"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains(North)), "value"]*= sample["ONS_LIMIT_NORTH"]
        SUBTECHGROUPKPOT.loc[(SUBTECHGROUPKPOT["TECH_GROUP"]=="WINDTURBINE_ONSHORE") & (SUBTECHGROUPKPOT["CCCRRRAAA"].str.contains(South)), "value"]*= sample["ONS_LIMIT_SOUTH"]
    
        HYDROGEN_DH2 = scenario_data["HYDROGEN_DH2"].records
        HYDROGEN_DH2.loc[HYDROGEN_DH2["CCCRRRAAA"].str.contains("DK"), "value"] *= sample["DH2_DEMAND_DK"]
        North_and_South_l = ["NO","SE","NL","FIN", "UK","EE","LV","LT","PL","BE","FR","IT","CH","AT","CZ","ES","PT","SK","HU","SI","HR","RO","BG","GR","IE","LU","AL","ME","MK","BA","RS","TR","MT","CY"]
        North_and_South = '|'.join(North_and_South_l)
        HYDROGEN_DH2.loc[HYDROGEN_DH2["CCCRRRAAA"].str.contains("DE"), "value"] *= sample["DH2_DEMAND_DE"]
        HYDROGEN_DH2.loc[HYDROGEN_DH2["CCCRRRAAA"].str.startswith((North_and_South)), "value"] *= sample["DH2_DEMAND_Rest"]

        EMI_POL = scenario_data["EMI_POL"].records
        EMI_POL.loc[(EMI_POL["GROUP"]=="ALL_SECTORS") & (EMI_POL["EMIPOLSET"]=="TAX_CO2"), "value"] *= sample["CO2_TAX"]
        
        CCS_CO2CAPTEFF_G = scenario_data["CCS_CO2CAPTEFF_G"].records
        CCS_CO2CAPTEFF_G.loc[:, "value"] *= sample["CO2_EFF"]
        
        GDATA = scenario_data["GDATA_numerical"].records
        GDATA_CAT = scenario_data["GDATA_categorical"].records
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_ELYS_ELEC_AEC")) & (GDATA["GDATASET"]=="GDFE"),"value"] *= sample["ELYS_ELEC_EFF"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_ELYS_ELEC_AEC")) & (GDATA["GDATASET"]=="GDOMFCOST0"),"value"] *= sample["H2_OandM"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_H2S_H2")) & (GDATA["GDATASET"]=="GDINVCOST0"),"value"] *= sample["H2S_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_STEAM-REFORMING-CCS")) & (GDATA["GDATASET"]=="GDINVCOST0"),"value"] *= sample["SMR_CCS_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_STEAM-REFORMING-CCS")) & (GDATA["GDATASET"]=="GDOMFCOST0"),"value"] *= sample["SMR_CCS_OandM"]
        GDATA.loc[(GDATA["GGG"].isin(GDATA_CAT.loc[(GDATA_CAT["TYPES"]=="SOLARPV"), "GGG"])) & (GDATA["GDATASET"]=="GDINVCOST0"),"value"] *= sample["PV_INVC"]
        GDATA.loc[(GDATA["GGG"].isin(GDATA_CAT.loc[(GDATA_CAT["TYPES"]=="WINDTURBINE_ONSHORE"), "GGG"])) & (GDATA["GDATASET"]=="GDINVCOST0"),"value"] *= sample["ONS_WT_INVC"]
        
        XH2INVCOST = scenario_data["XH2INVCOST"].records
        XH2INVCOST.loc[:,"value"] *= sample["H2_TRANS_INVC"]
        
        XINVCOST = scenario_data["XINVCOST"].records
        XINVCOST.loc[:,"value"] *= sample["ELEC_TRANS_INVC"]
        
        FUELPRICE = scenario_data["FUELPRICE"].records
        FUELPRICE.loc[FUELPRICE["FFF"]=="IMPORT_H2","value"] *= sample["IMPORT_H2_P"]
        
        DE = scenario_data["DE"].records
        DE.loc[DE["RRR"].str.contains("DK"), "value"] *= sample["DE_DEMAND_DK"]
        DE.loc[DE["RRR"].str.contains("DE"), "value"] *= sample["DE_DEMAND_DE"]
        DE.loc[~DE["RRR"].str.contains("DK|DE"), "value"] *= sample["DE_DEMAND_Rest"]

        
        DE.loc[DE["RRR"].str.contains("DE") & (DE["DEUSER"].str.contains("TRANS_TRAINS|TRANS_BUS")), "value"] *= sample["TRANS_DEMAND_DE"]
        DE.loc[~DE["RRR"].str.contains("DE") & (DE["DEUSER"].str.contains("TRANS_TRAINS|TRANS_BUS")), "value"] *= sample["TRANS_DEMAND_REST"]
        
        return scenario_data