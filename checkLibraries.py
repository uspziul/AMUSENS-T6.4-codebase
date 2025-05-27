import importlib

def is_installed(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False
    
def checkFor_np_pd(): #Returns True if both numpy and pandas are installed
    count = 0
    if is_installed("numpy"):
        count += 1
    else:
        print("Numpy library is required and it is not installed. To install it input the following command: pip install numpy")

    if is_installed("pandas"):
        count += 1
    else:
        print("Pandas library is required and it is not installed. To install it input the following command: pip install pandas")
    
    if count == 2:
        return True
    else:
        return False