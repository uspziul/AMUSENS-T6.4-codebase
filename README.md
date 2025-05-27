This code converts the raw measurement files coming from experiments in UNIBS to the standard project file format as described in D4.2. 
To use it:
  1 - Download and install Python: https://www.python.org/downloads/
    - During installation, make sure to check "Add Python to PATH"
    - Restart your computer after installation
  2 - Open a terminal (search for cmd on windows) and install dependencies, numpy and pandas, by writing and executing the following commands:
    2.1 - pip install numpy
    2.2 - pip install pandas
    2.3 - pip install xlrd
  3 - Change the current folder to the folder in which you downloaded these files by writing: cd [file_dir] . [file_dir] is the path to the folder, something similar to C:\\Users\user\downloads\AMUSENS-T6.4-codebase
  4 - Execute the program to extract the file using the following command: python extractStandardFiles-UNIBS-format.py "path to the folder in which the file is located" "path to the output files folder".
    4.1 - The output files folder is optional, so if it is not specified a new folder (Project Standard Extractions) will be generated in the same folder as the input path.
    4.2 - Example of usage:
      Example 1 - Using default output folder:
        Command: python extractStandardFiles-UNIBS-format.py "C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C"
          Result: Files are automatically saved to C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C\Project Standard Extractions

      Example 2 - Specifying custom output folder:
        Command: python extractStandardFiles-UNIBS-format.py "C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C" "C:\Users\user\extractions\WO3"
          Result: Files are saved to C:\Users\user\extractions\WO3

      Complete workflow example:
        Step 1: cd C:\Users\user\downloads\AMUSENS-T6.4-codebase
        Step 2: python extractStandardFiles-UNIBS-format.py "C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C"
    
!!!! Important !!!! - Requirements:
- The folder containing the raw file must be named: "Material-Date-Temperature"
  Example: "WO3-20241106-200°C"
  - Material: sensor material name (e.g., WO3, SnO2)
  - Date: YYYYMMDD format (e.g., 20241106 for November 6, 2024)
  - Temperature: operating temperature with °C (e.g., 200°C)
- The folder must contain at least one Excel file (.xls or .xlsx) with the measurement data

**Possible errors of execution:**
  A - ModuleNotFoundError: No module named "numpy". **Solution**: Make sure the dependencies are installed by executing steps 2.1, 2.2 and 2.3 of this list.
  B - IndexError: list index out of range. **Solution:** It is likely the path for the folder with the raw files has a typo.
  C - FileNotFoundError: [Errno 2] No such file or directory. **Solution:** Double-check the folder paths used in the command. Ensure the folder structure and file names match the expected format. Use quotes around Windows paths if they contain spaces.
  D - ImportError: Missing optional dependency 'xlrd'. **Solution:** Install openpyxl by running: pip install xlrd
  E - PermissionError: [Errno 13] Permission denied. **Solution:** Make sure you have write permissions to the output folder, or choose a different output location.
  F - UnicodeDecodeError or special character issues. **Solution:** Ensure folder names only contain standard characters. Avoid special symbols in paths except for the degree symbol (°) in temperature.
