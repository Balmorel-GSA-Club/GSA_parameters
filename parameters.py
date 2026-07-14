import pandas as pd
import numpy as np

# This class is used to deal with paramneters in the model
class GSA_parameters :
    def __init__(self, input_file):
        self.input = pd.read_csv(input_file)
        self.parameters = self.input["Parameter"]

    def load_sets(self):
        #sets = "FUELPRICE, GDATA_numerical, GDATA_categorical, EMI_POL, CCS_CO2CAPTEFF_G, XINVCOST, XH2INVCOST, DE, SUBTECHGROUPKPOT, HYDROGEN_DH2, EV_BEV_available, BEV_TECH_DATA, DR_ADOPTIONRATE, DR_DATA"
        sets = "FUELPRICE, GDATA_numerical, EMI_POL, CCS_CO2CAPTEFF_G, XINVCOST, XH2INVCOST, DE, SUBTECHGROUPKPOT, HYDROGEN_DH2, EV_BEV_available, BEV_TECH_DATA, DR_ADOPTIONRATE, DR_DATA"
        
        return sets
    
    def update_input(self, scenario_data, sample):
        North_l = ["DK","NO","SE","FIN","EE","LV","LT"]
        North = '|'.join(North_l)
        South_l = ["IT","ES","PT","GR","SI","HR","AL","MT","CY","BA","ME","MK","RS"]
        South = '|'.join(South_l)
        East_l = ["PL","CZ","SK","RO","BG","HU",]
        East = '|'.join(East_l)
        West_l = ["FR","DE","NL","UK","BE","LU","AT","CH","IE" ]
        West = '|'.join(West_l)



        FUELPRICE = scenario_data["FUELPRICE"]
        FUELPRICE.columns = ["YYY", "AAA", "FFF", "value"]
        FUELPRICE.loc[(FUELPRICE["FFF"]=="NATGAS") & (FUELPRICE["value"]>=1e-320),"value"]*=sample["NATGAS_P"]
        
      
        EMI_POL = scenario_data["EMI_POL"]
        EMI_POL.columns = ["YYY", "CCCRRRAAA", "GROUP", "EMIPOLSET", "value"]
        EMI_POL.loc[(EMI_POL["GROUP"]=="ALL_SECTORS") & (EMI_POL["EMIPOLSET"]=="TAX_CO2") & (EMI_POL["value"]>=1e-320), "value"] *= sample["CO2_TAX"]
        
        
        GDATA = scenario_data["GDATA_numerical"]
        GDATA.columns = ["GGG", "GDATASET", "value"]
        #GDATA_CAT = scenario_data["GDATA_categorical"]
        #GDATA_CAT.columns = ["GGG", "GDATASET_categorical", "TYPES"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_ELYS_ELEC_AEC")) & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["H2_INVCOST0"]
        GDATA.loc[(GDATA["GGG"].str.contains("PV")) & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["PV_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("ONS")) & (GDATA["GDATASET"]=="GDINVCOST0")  & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["ONS_WT_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("OFF")) & (GDATA["GDATASET"]=="GDINVCOST0")  & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["OFF_WT_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_H2S_H2")) & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["H2S_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_HS_HEAT")) & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["HS_INVC"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_HP_ELEC")) & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["HP_INVC"]
        
        #Batteries GRID Lithium
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_ES_ELEC_BAT-LITHIO-GRID")) & (GDATA["GDATASET"]=="GDOMFCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["BATTERIES_OandM"]
        GDATA.loc[(GDATA["GGG"].str.contains("GNR_ES_ELEC_BAT-LITHIO-GRID")) & (GDATA["GDATASET"]=="GDINVCOST0") & (GDATA["value"]>=1e-320),"value"] *= sample["BATTERIES_INVCOST0"]
        

        XH2INVCOST = scenario_data["XH2INVCOST"]
        XH2INVCOST.columns = ["YYY", "IRRE", "IRRI", "value"]
        XH2INVCOST.loc[(XH2INVCOST["value"]>=1e-320),"value"] *= sample["H2_TRANS_INVC"]
        
        XINVCOST = scenario_data["XINVCOST"]
        XINVCOST.columns = ["YYY", "IRRE", "IRRI", "value"]
        XINVCOST.loc[(XINVCOST["value"]>=1e-320),"value"] *= sample["ELEC_TRANS_INVC"]
        
        
        #EV fleet available
        EV_BEV_AVAILABLE = scenario_data["EV_BEV_available"]
        EV_BEV_AVAILABLE.columns = ["YYY", "RRR", "value"]
        EV_BEV_AVAILABLE["value"]*=sample["EV_BEV_available"]

        #EV V2G efficiency
        EV_TECH_DATA = scenario_data["BEV_TECH_DATA"]
        EV_TECH_DATA.columns = ["YYY", "TYPE", "value"]
        EV_TECH_DATA.loc[(EV_TECH_DATA["TYPE"]=="EV_V2G_PEFF"),"value"]*=sample["V2G_EFF"]

    


        #EV Charger capacity
        EV_TECH_DATA = scenario_data["BEV_TECH_DATA"]
        EV_TECH_DATA.columns = ["YYY", "TYPE", "value"]
        EV_TECH_DATA.loc[(EV_TECH_DATA["TYPE"]=="EV_CHARGE_CAP"),"value"]*=sample["EV_CHARGE_CAP"]

        #EV V2G share
        #EV Charger capacity
        EV_TECH_DATA = scenario_data["BEV_TECH_DATA"]
        EV_TECH_DATA.columns = ["YYY", "TYPE", "value"]
        EV_TECH_DATA.loc[(EV_TECH_DATA["TYPE"]=="Share_EV_V2G"),"value"]*=sample["V2G_SHARE"]



        #DR adoption rate
        DR_ADOPTIONRATE = scenario_data["DR_ADOPTIONRATE"]
        DR_ADOPTIONRATE.columns = ["DR_TECHNOLOGIES", "YYY", "value"]
        DR_ADOPTIONRATE.loc[(DR_ADOPTIONRATE["DR_TECHNOLOGIES"]=="DR_SHIFT_HH_HEAT"),"value"]*=sample["ADOPTION_RATE_DR"]
        DR_ADOPTIONRATE.loc[(DR_ADOPTIONRATE["DR_TECHNOLOGIES"]=="DR_SHIFT_HH_WATER"),"value"]*=sample["ADOPTION_RATE_DR"]


        #H2 demand
        HYDROGEN_DH2 = scenario_data["HYDROGEN_DH2"]
        HYDROGEN_DH2.columns = ["YYY", "CCCRRRAAA", "value"]
        HYDROGEN_DH2.loc[(HYDROGEN_DH2["value"]>=1e-320), "value"] *= sample["DH2_DEMAND"]
                
        return scenario_data