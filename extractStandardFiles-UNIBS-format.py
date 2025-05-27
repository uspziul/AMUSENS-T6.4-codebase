import sys
import os
from datetime import datetime
import numpy as np
import pandas as pd

# Main function to process gas sensor data files
# Naming convention must follow "Material-date-OperatingTemperature" ex: "WO3-20241106-200°C"
def process_file(file_path, output_dir=None):
    print(file_path)
    
    # Set default output directory if not specified
    if output_dir is None:
        output_dir = file_path + r"\Project Standard Extractions"
    
    # Create output directory if it doesn't exist    
    os.makedirs(output_dir, exist_ok=True)
    print("Extracted files will be stored in : " + output_dir)
    path = file_path
    
    # Extract folder name from path
    folder = path.split("\\")[-1]

    # Parse folder name to extract material, date, and temperature information
    elements = folder.split("-")
    material = elements[0]  # e.g., "WO3"
    date = datetime.strptime(elements[1],"%Y%m%d")  # e.g., "20241106"
    temperature = elements[2]  # e.g., "200°C"
    
    # Get list of files in the directory
    files = os.listdir(path)

    # Find Excel file (case-insensitive search for .xls or .XLS)
    file = [f for f in files if ".XLS" in f or ".xls" in f]

    # Read Excel data
    data = pd.read_excel(path + "\\" + file[0],sheet_name='esportamisura')
    
    # Extract gas concentration columns (columns 32-38)
    gasesColumns = data.iloc[:,32:38]
    
    # Keep only gas columns that have non-zero values
    nonZeroGases = gasesColumns.loc[:, (gasesColumns != 0).any()]
    gasNames = nonZeroGases.columns

    # Extract material sensor data columns (columns 2-32)
    materialColumns = data.iloc[:,2:32]

    # Process each gas type
    for gas in gasNames: 
        # Fast protocol -> 2h injection followed by 4h recovery
        
        # Find start points: where gas concentration increases by >10% of max value
        start = np.where(np.diff(nonZeroGases[gas]) > .1*np.max(nonZeroGases[gas]))[0]
        
        # Find end points: where gas concentration decreases by >10% of max value
        end = np.where(np.diff(nonZeroGases[gas]) < -.1*np.max(nonZeroGases[gas]))[0]
        
        # Process each injection cycle
        for s in start: 
            # Sampling time of 30s makes 2h become 240 samples, so total time for a cycle is 720 samples 
            dfGas_temp = data.iloc[s:s+720,:]
            
            # Process each material sensor (grouped in sets of 3 columns)
            for cols in range(0,materialColumns.shape[1],3):
                
                # Extract current material sensor data (3 columns per sensor)
                # Take absolute value and reset index for proper alignment
                currentMaterial = np.abs(materialColumns.iloc[s:s+720,cols:cols+3].reset_index(drop=True))
                
                # Create timestamps by adding elapsed seconds to base date
                timestamp = (date + pd.to_timedelta(data["t(s)"][s:s+720], unit='s')).reset_index(drop=True)
                
                # Calculate sensor signal (voltage/current ratio)
                signal = dfGas_temp.iloc[:,1].reset_index(drop=True) / currentMaterial.iloc[:,0].reset_index(drop=True)
                signal = signal.fillna(0)  # Replace NaN values with 0
                
                # Initialize heater parameters (set to zero for this setup)
                hVoltage = np.zeros(signal.shape)
                hCurrent = np.zeros(signal.shape)
                hPower = hVoltage*hCurrent
                
                # Extract sensor bias parameters
                sensorBiasV = dfGas_temp.iloc[:,1].reset_index(drop=True)  # Sensor bias voltage
                sensorBiasA = currentMaterial.iloc[:,0].reset_index(drop=True)  # Sensor bias current
                
                # Set heater temperature (extract numeric value from temperature string)
                hTemp = int(temperature[:-2])*np.ones(signal.shape)  # Remove "°C" and convert to int
                
                # Extract relative humidity data
                RH = np.abs(dfGas_temp["RHC(%)"]).reset_index(drop=True)
                
                # Extract total gas flow rate (convert from sccm to L/min)
                totalFlow = (dfGas_temp["FC(sccm)"]/1000).reset_index(drop=True)
                
                # Create gas name and concentration arrays
                Gas = np.array([gas]*signal.shape[0])  # Repeat gas name for all samples
                gasConc = dfGas_temp[gas].reset_index(drop=True)  # Gas concentration values
               
                # Create dictionary with all sensor data
                aux = {"Timestamp": timestamp, "Signal": signal, "Heater Voltage": hVoltage,
                                "Heater Current": hCurrent, "Heater Power": hPower, "Sensor Bias Voltage": sensorBiasV,
                                "Sensor Bias Current": sensorBiasA, "Heater Temperature": hTemp, "Relative Humidity": RH,
                                "Total Gas Flow": totalFlow, "Gas": Gas, "Gas concentration": gasConc}
                
                # Convert to DataFrame
                out = pd.DataFrame(data=aux)
                
                # Extract material name from column header
                Material = currentMaterial.columns[0].split("_")[0]
                
                # Create descriptive filename with all relevant parameters
                filename = f"{Material}_gas_{gas[:-5]}_RH_{int(RH[0])}_Temp_{int(hTemp[0])}_{date.year}_{date.month}_{date.day}.csv"
                filepath = output_dir + rf"\{filename}"
                
                # Save to CSV with semicolon separator
                out.to_csv(filepath,index=False)
    

# Main execution block - handles command line arguments
if __name__ == "__main__":
    # Check if minimum arguments provided
    if len(sys.argv) < 2:
        print("Usage: python extractStandardFiles-UNIBS-format.py [input_dir] [output_dir]")
        print("Note: Wrap paths with spaces in quotes!")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    # Handle case where path contains spaces and user forgot quotes
    if len(sys.argv) > 3 and not os.path.exists(sys.argv[1]):
        # Try to reconstruct the path by joining arguments
        potential_path = " ".join(sys.argv[1:-1])  # Everything except last arg
        if os.path.exists(potential_path):
            input_file = potential_path
            output_dir = sys.argv[-1]
        else:
            input_file = " ".join(sys.argv[1:])  # Everything as one path
            output_dir = None
    else:
        # Standard case: properly quoted arguments
        input_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) >= 3 else None
    
    # Process the file
    process_file(input_dir,output_dir)