class Config:
    def __init__(self):
        self.APP_NAME = 'sn_compare'
        self.LOG_FILE = self.APP_NAME + '.log'
        self.DEBUG = False

        # IMPORTANT: Update the config values below this line to match your envioronment and use case before running compare.py
        self.file1 = '/Users/paul.ramsey/Documents/compare/cmdb_identifier_entry_list_dev3.csv'
        self.file2 = '/Users/paul.ramsey/Documents/compare/cmdb_identifier_entry_list_prod.csv'
        self.compare_attributes = ['sys_id','table','active','attributes']
        