import pandas as pd
from config import config 
import logging
import os
from pathlib import Path
import time
import csv


def load_config():
    # Load config from file config/config.py into global variable conf for use throughout project.
    global conf
    conf = config.Config()

def initialize_logging():
    # Configure logging for the project runtime.
    if conf.DEBUG:
        logging.basicConfig(filename=conf.LOG_FILE,level=logging.DEBUG, format='%(asctime)s %(levelname)s:  %(message)s')
        logging.info("Logging initialized...")
    else:
        logging.basicConfig(filename=conf.LOG_FILE,level=logging.INFO, format='%(asctime)s %(levelname)s:  %(message)s')
        logging.info("Logging initialized...")

def check_for_sys_id():
    # Ensure sys_id is included in conf.compare_attributes at the first index 
    if ('sys_id' in conf.compare_attributes):
        conf.compare_attributes.remove('sys_id')
        conf.compare_attributes = ['sys_id'] + conf.compare_attributes
    else:
        conf.compare_attributes = ['sys_id'] + conf.compare_attributes
    
    # Ensure sys_id attribute exists in conf.file1
    if ('sys_id' not in file1.columns):
        raise ValueError('Required attribute sys_id is missing from File1')

    # Ensure sys_id attribute exists in conf.file2
    if ('sys_id' not in file2.columns):
        raise ValueError('Required attribute sys_id is missing from File1')

def load_files():
    # Load the files defined in config/config.py into Pandas dataframes for analysis
    global file1, file2
    file1 = pd.read_csv(conf.file1, usecols=conf.compare_attributes)
    file2 = pd.read_csv(conf.file2, usecols=conf.compare_attributes)
    
    # Ensure the files contain sys_id attributes
    check_for_sys_id()
    
    # Additional logging for debugging purposes
    if (conf.DEBUG):
        print(file1.head())
        print(file2.head())

    return True

def find_different():
    # Find rows where sys_ids are the same but the values defined in conf.compare_attributes are different.
    merged = file1.merge(file2, on=conf.compare_attributes, how='outer', indicator=True)
    merged = merged[merged['_merge'] != 'both']
    merged = merged.set_index('sys_id')
    left = merged[merged['_merge'] == 'left_only']
    left = left.drop(columns='_merge')
    right = merged[merged['_merge'] == 'right_only']
    right = right.drop(columns='_merge')
    concatenated = pd.concat([left, right], axis='columns', keys=['FILE1', 'FILE2'], sort=True)
    concatenated = concatenated.swaplevel(axis='columns')[left.columns[0:]]
    return concatenated
    
def find_additional():
    # Get sys_ids for records that exist in one file but not the other
    merged = file1.merge(file2, on='sys_id', how='outer', indicator=True)
    merged = merged[merged['_merge'] != 'both']
    merged = merged.set_index('sys_id')
    left = merged[merged['_merge'] == 'left_only']
    left = left.drop(columns='_merge')
    right = merged[merged['_merge'] == 'right_only']
    right = right.drop(columns='_merge')
    return_object = {
        "left": left,
        "right": right
    }
    return return_object

def create_output_folder(output_path):
    # Create output folder in the current working directory to store results
    current_working_directory = os.path.dirname(os.path.realpath(__file__))
    output_fqp = str(Path(current_working_directory).joinpath(output_path)) + "/" + time.strftime("%Y%m%d-%H%M%S")
    Path(output_fqp).mkdir(parents=True, exist_ok=True)
    return output_fqp

def deduplicate_different_and_additional(_different, _additional):
    # Remove entries in _different where they already exist in _additional
    for sysid in _additional['left'].index.tolist():
        _different = _different.drop(_different[_different.index == sysid].index)
    for sysid in _additional['right'].index.tolist():
        _different = _different.drop(_different[_different.index == sysid].index)
    return _different

def main():
    # Load files defined in config/config.py as Pandas dataframe objects
    load_files()

    # Find records that exist in one file but not the other.
    additional = find_additional()

    # Find all differences between the two files for the attributes specified in config/config.py
    different = find_different()

    # De-duplicate the records shown in different and additional
    different = deduplicate_different_and_additional(different, additional)

    # Create output directory in the current working directory
    output_path = create_output_folder('output')

    # Write results to the console and to a timestamped directory in the output/ folder
    if(different.empty == False):
        print("RECORDS FOR THE FOLLOWING EXIST IN BOTH FILES, BUT DIFFERENCES WERE FOUND IN THEIR ATTRIBUTES")
        print(different)
        print("")
        print("")
        different.to_csv(output_path + '/different.csv')
    else:
        print("No attribute difference found in records where sys_ids match.")
        print("")
    if(additional['left'].empty == False):
        print("ADDITIONAL UNMATCHED RECORDS FOUND IN FILE1")
        print("\n".join(additional['left'].index.tolist()))
        print("")
        with open(output_path + '/additional_records_file1.csv', mode='w') as file1_additional:
            csv_writer = csv.writer(file1_additional, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for sysid in additional['left'].index.tolist():
                csv_writer.writerow([sysid])
    else:
        print("No unmatched records found in file2.")
        print("")
    if(additional['right'].empty == False):
        print("ADDITIONAL UNMATCHED RECORDS FOUND IN FILE2")
        print("\n".join(additional['right'].index.tolist()))
        print("")
        with open(output_path + '/additional_records_file2.csv', mode='w') as file2_additional:
            csv_writer = csv.writer(file2_additional, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for sysid in additional['right'].index.tolist():
                csv_writer.writerow([sysid])
    else:
        print("No unmatched records found in file2.")
        print("")

# Load config, initialize logging, and run main function
if __name__ == '__main__':
    load_config()
    initialize_logging()
    main()
