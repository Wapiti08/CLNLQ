'''
    Parse the table structure to generate RDB elements MetaTable

'''
import pandas as pd

class TableParser:

    def __int__(self, filename):
        self.filename = filename

    def read_json_data(self,):
        ''' function to read json data for key names only

        '''

    def read_table_jsonl_data(self,):
        ''' function to read table json data for column names only
        
        '''
    
    def read_format_jsonl_data(self,):
        ''' read format NLQ data 
        
        '''
    
    def read_csv(self,):
        '''
        
        '''
        df = pd.read_csv(self.filename)
        return df
