import pandas as pd
import time

class anamoly_data:
   
   def __init__(self,timeDelay):
        
      self.dataTable = pd.read_csv('./data/anamoly_data.csv')
      self.timeDelay= timeDelay
        






   def gen_data(self):
      data=self.dataTable

   #    new_row_data = {
   #      'Timestamp': next_timestamp,
   #      'Value1': np.random.randint(1, 100),  # Replace the range as needed
   #      'Value2': np.random.randint(1000, 2000)  # Replace the range as needed
   #      # Add more columns as needed with their respective random value generation
   #  }
      #dataframe = dataframe.append(new_row, ignore_index=True)
      return data

