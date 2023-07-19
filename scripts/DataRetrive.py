import pandas as pd
import time

class dataRetrival:
     def __init__(self,timeDelay,tagName):
        self.templatelist  = pd.read_csv('./data/templateTable.csv')
        self.dataTable = pd.read_csv('./data/TrenddataTable.csv')
        self.dataTable['Timestamp'] = pd.to_datetime(self.dataTable['Timestamp'])
        self.timeDelay= timeDelay
        self.tagName = tagName

     def retriveValue(self):
        """ Function used to retrive value for the given table timestamp"""
        
        data = self.dataTable[self.dataTable['Tag ID']==self.tagName]
        timestamp_value = data['Timestamp'].iloc[-1] - pd.Timedelta(seconds=int(self.timeDelay))
        last_values = data[data['Timestamp']>timestamp_value]
        return last_values
    
     def addDataPoint(self,numOfPoint):
        """ Function to add new function """
        data = self.dataTable[self.dataTable['Tag ID']==self.tagName]
        for i in range(numOfPoint):
            random_value = data['Value'].sample().values[0]
            dict_value = {'Tag ID':self.tagName,'Timestamp':data['Timestamp'].iloc[-1]+pd.Timedelta(seconds=int(5)),"Value":random_value,'Equipment Name':data['Equipment Name'][0]}
            self.dataTable = self.dataTable._append(dict_value, ignore_index=True)
            data = data._append(dict_value, ignore_index=True)
            self.dataTable.to_csv('./data/TrenddataTable.csv',index=False)
        return self.dataTable
     
     def dataCreation(self):
         data = self.retriveValue()
         addedData = self.addDataPoint(len(data))
         return addedData,data
         
        

    