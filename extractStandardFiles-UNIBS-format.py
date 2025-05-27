import sys
import os
from datetime import datetime
import numpy as np
import pandas as pd

# Naming convention must follow "Material-date-OperatingTemperature" ex: "WO3-20241106-200°C"
def process_file(file_path, output_dir=None):
    print(file_path)
    if output_dir is None:
        output_dir = file_path + r"\Project Standard Extractions"
        
    os.makedirs(output_dir, exist_ok=True)
    print("Extracted files will be stored in : " + output_dir)
    path = file_path
    
    folder = path.split("\\")[-1]

    elements = folder.split("-")
    
    material = elements[0]
    date = datetime.strptime(elements[1],"%Y%m%d")
    temperature = elements[2]
    
    files = os.listdir(path)

    file = [f for f in files if ".XLS" in f or ".xls" in f]

    data = pd.read_excel(path + "\\" + file[0])
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
                filepath = output_dir + rf"\{filename}"
                out.to_csv(filepath,sep = ";",index=False)
    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractStandardFiles-UNIBS-format.py [input_dir] [output_dir]")
        print("Note: Wrap paths with spaces in quotes!")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    if len(sys.argv) > 3 and not os.path.exists(sys.argv[1]):
        # Try to reconstruct the path
        potential_path = " ".join(sys.argv[1:-1])  # Everything except last arg
        if os.path.exists(potential_path):
            input_file = potential_path
            output_dir = sys.argv[-1]
        else:
            input_file = " ".join(sys.argv[1:])  # Everything as one path
            output_dir = None
    else:
        input_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) >= 3 else None
        
    process_file(input_dir,output_dir)