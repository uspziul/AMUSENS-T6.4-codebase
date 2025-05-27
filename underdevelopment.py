#%%
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

#%% #Naming convention must follow "material-date-temperature"
path = r"C:\Users\luiz.miranda\Dropbox\IMT\Postdoc - TSP - 2025\Data\UNIBS\Raw_Data\WO3-20241106-200°C"
folder = path.split("\\")[-1]
elements = folder.split("-")
material = elements[0]                    
date = pd.to_datetime(elements[1],format="%Y%m%d")
temperature = elements[2]
files = os.listdir(path)

file = [f for f in files if ".XLS" in f or ".xls" in f]

data = pd.read_excel(path + "\\" + file[0])

    
# %% Gas control column must be between column 32 and 38
gasesColumns = data.iloc[:,32:38]
nonZeroGases = gasesColumns.loc[:, (gasesColumns != 0).any()]
gasNames = nonZeroGases.columns

materialColumns = data.iloc[:,2:32]
saveGases = np.array([])
for gas in gasNames: # fast protocol -> 2h injection followed by 4h recovery

    start = np.where(np.diff(nonZeroGases[gas]) > .1*np.max(nonZeroGases[gas]))[0]
    end = np.where(np.diff(nonZeroGases[gas]) < -.1*np.max(nonZeroGases[gas]))[0]
    
    each = []
    for s in start: # Sampling time of 30s makes 2h become 240 samples, so total time for a cycle is 720 samples 
        dfGas_temp = data.iloc[s:s+720,:]
        for cols in range(0,materialColumns.shape[1],3):
            currentMaterial = np.abs(materialColumns.iloc[s:s+720,cols:cols+3].reset_index(drop=True))
            timestamp = (date + pd.to_timedelta(data["t(s)"][s:s+720], unit='s')).reset_index(drop=True)
            signal = dfGas_temp.iloc[:,1].reset_index(drop=True) / currentMaterial.iloc[:,0].reset_index(drop=True)
            signal = signal.fillna(0)
            hVoltage = np.zeros(signal.shape)
            hCurrent = np.zeros(signal.shape)
            hPower = hVoltage*hCurrent
            sensorBiasV = dfGas_temp.iloc[:,1].reset_index(drop=True)
            sensorBiasA = currentMaterial.iloc[:,0].reset_index(drop=True)
            hTemp = int(temperature[:-2])*np.ones(signal.shape)
            RH = np.abs(dfGas_temp["RHC(%)"]).reset_index(drop=True)
            totalFlow = (dfGas_temp["FC(sccm)"]/1000).reset_index(drop=True)
            Gas = np.array([gas]*signal.shape[0])
            gasConc = dfGas_temp[gas].reset_index(drop=True)
            aux = {"Timestamp": timestamp, "Signal": signal, "Heater Voltage": hVoltage,
                               "Heater Current": hCurrent, "Heater Power": hPower, "Sensor Bias Voltage": sensorBiasV,
                               "Sensor Bias Current": sensorBiasA, "Heater Temperature": hTemp, "Relative Humidity": RH,
                               "Total Gas Flow": totalFlow, "Gas": Gas, "Gas concentration": gasConc}
            out = pd.DataFrame(data=aux)
            Material = currentMaterial.columns[0].split("_")[0]
            filename = f"{Material}_gas_{gas[:-5]}_RH_{int(RH[0])}_Temp_{int(hTemp[0])}_{date.year}_{date.month}_{date.day}.csv"
            filepath = rf"C:\Users\luiz.miranda\Desktop\Nouveau dossier\testes\{filename}"
            out.to_csv(filepath,sep = ";",index=False)
            #measurement = Measurement(gas = gas, data = dfGas_temp, )
            
        
        
# %%
