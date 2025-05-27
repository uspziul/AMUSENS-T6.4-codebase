# UNIBS Raw Data Converter

This code converts the raw measurement files coming from experiments in UNIBS to the standard project file format as described in D4.2.

## Installation and Setup

### 1. Install Python
- Download and install Python from: https://www.python.org/downloads/
- **Important**: During installation, make sure to check "Add Python to PATH"
- Restart your computer after installation

### 2. Install Dependencies
Open a terminal (search for "cmd" on Windows) and install the required packages:

```bash
pip install numpy
pip install pandas
pip install xlrd
```

### 3. Navigate to Script Directory
Change to the folder containing the downloaded files:

```bash
cd [file_dir]
```

Where `[file_dir]` is the path to the folder, for example:
```bash
cd C:\Users\user\downloads\AMUSENS-T6.4-codebase
```

## Usage

### Basic Command
```bash
python extractStandardFiles-UNIBS-format.py "input_folder_path" "output_folder_path"
```

- **Input folder path**: Path to the folder containing the raw measurement file
- **Output folder path**: *(Optional)* Path where extracted files will be saved

> **Note**: If no output folder is specified, a new folder called "Project Standard Extractions" will be created in the same location as the input folder.

### Examples

#### Example 1: Using Default Output Folder
```bash
python extractStandardFiles-UNIBS-format.py "C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C"
```
**Result**: Files are automatically saved to:
```
C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C\Project Standard Extractions
```

#### Example 2: Specifying Custom Output Folder
```bash
python extractStandardFiles-UNIBS-format.py "C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C" "C:\Users\user\extractions\WO3"
```
**Result**: Files are saved to:
```
C:\Users\user\extractions\WO3
```

#### Complete Workflow Example
```bash
# Step 1: Navigate to script directory
cd C:\Users\user\downloads\AMUSENS-T6.4-codebase

# Step 2: Run the extraction
python extractStandardFiles-UNIBS-format.py "C:\Users\user\downloads\UNIBS\Raw_Data\WO3-20241106-200°C"
```

## ⚠️ Important Requirements

### Folder Naming Convention
The folder containing the raw file **must** follow this naming structure:
```
Material-Date-Temperature
```

**Example**: `WO3-20241106-200°C`

Where:
- **Material**: Sensor material name (e.g., `WO3`, `SnO2`)
- **Date**: `YYYYMMDD` format (e.g., `20241106` for November 6, 2024)
- **Temperature**: Operating temperature with °C (e.g., `200°C`)

### File Requirements
- The folder must contain at least one Excel file (`.xls` or `.xlsx`) with the measurement data

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named "numpy"` | Install dependencies using: `pip install numpy pandas xlrd` |
| `IndexError: list index out of range` | Check for typos in the folder path |
| `FileNotFoundError: [Errno 2] No such file or directory` | Verify folder paths and ensure they match the expected format. Use quotes around Windows paths containing spaces |
| `ImportError: Missing optional dependency 'xlrd'` | Install xlrd: `pip install xlrd` |
| `PermissionError: [Errno 13] Permission denied` | Ensure write permissions to output folder or choose a different location |
| `UnicodeDecodeError` or special character issues | Use only standard characters in paths (degree symbol ° in temperature is acceptable) |

## Testing Installation

Verify your setup with these commands:

```bash
# Test Python installation
python --version

# Test dependencies
python -c "import pandas, numpy, xlrd; print('All dependencies installed successfully')"
```
