# sn_compare

This project provides a quick and dirty method of comparing a given table from two ServiceNow instances against each other using a CSV export from each table.

## Using the Project

Complete the following steps to use this project:
- Download and install Python 3 if not already installed on your local environment.
- Clone the project to a local folder.
- Navigate to the project folder root in a terminal session.
- Create and activate a virtualenv if desired.
- Install project depedencies using the requirements.txt file included in this project. 
```bash
pip3 install -r requirements.txt
```
- Download CSV files from the two instances you want to compare using syntax like the following:
https://example.service-now.com/cmdb_identifier_entry_list.do?CSV&sysparm_default_export_fields=all
    > NOTE: The `sysparm_default_export_fields=all` parameter is very important as you will not get the sys_id without this.
- Update `config/config.py` with the file paths of the files you just downloaded (`self.file1` and `self.file2`), as well as the attributes you would like to compare (`self.compare_attributes`).
- Run `compare.py`.
- Review output in the console and in the `output/<timestamp>/` directory.
    - `different.csv` provides a list of records where the sys_ids match in both files, but the attribute values are different.
    - `additional_records_file1.csv` and `additional_records_file2.csv` provide a respective list of sys_ids appearing in one file but not the other.

## Configuration

Config file values should be used where appropriate to make the code dynamic across environments. Configs are located in `./config/config.py` and use native Python data structures.

> IMPORTANT: Update the following config values to match your envioronment and use case before running compare.py:
```python
self.file1 = '<Full path to first CSV file used in comparison>'
self.file2 = '<Full patch to second CSV file used in comparison>'
self.compare_attributes = ['<List of attributes you want to compare>','sys_id is required and will be added for you']
```

## Logging

This project uses Python's `logging` module. Be sure to include `import logging` at the top of each of your modules. View function `setup_logging` in `main.py` for an example of setting up logging.

## Compatability

This project was coded and tested using Python version 3.6.3 on a Mac (High Sierra). Slight modifications may be needed to support different versions of Python or to run on Windows (i.e. path issues).