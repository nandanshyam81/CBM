import pandas as pd
import datetime
from datetime import timedelta
import smtplib
from email.message import EmailMessage

class Mtbs:
    
    def sendMail(self,content,subject,emailid):
        msg = EmailMessage()
        msg['Subject']=subject
        msg['From']='nandanshyam81@gmail.com'
        msg['To']=emailid
        msg.set_content(content) #body
        try :
            with smtplib.SMTP('smtp.gmail.com',587) as server:
                server.starttls()
                server.login('nandanshyam81@gmail.com','xcqxxvyzbuyslhzt')
                server.send_message(msg)
        except Exception as e:
            print(e)
    
    def MTBS(iot):
        try:
            iot["Timestamp"]=pd.to_datetime(iot["Timestamp"])
            current_time =  iot['Timestamp'].max()
            
            # Calculate the time one hour ago
            one_hour_ago = current_time - pd.Timedelta(hours=1)
            one_week_ago=current_time - pd.Timedelta(weeks=1)
            one_month_ago=current_time - pd.Timedelta(weeks=4)
            # Filter the DataFrame for the last one hour
            df1 = iot[iot['Timestamp'] >= one_hour_ago]
            df2= iot[iot['Timestamp'] >= one_week_ago]
            df3 = iot[iot['Timestamp'] >= one_month_ago]
            
            
            return df1,df2,df3
    
        except Exception as e:
            print(f'Exception occoured in Asset Details in MTBS function:', {e})
    
    def hrs_stoppage_count(iot): 
        try:
            running_hour=1
            count = 0
            zeros_count = 0
            for num in iot["Value"]:
                if num ==0:
                    zeros_count += 1
                else:
                    if zeros_count >= 3:
                        count += 1
                        zeros_count = 0
            if count==0:
                return 0
            else:
                return running_hour/count
                   
                   
        except Exception as e:
            print(f'Exception occoured in Asset Details in hrs_stoppage_count function:', {e})


    def weekly_stoppage_count(iot): # iot = week_df 
        try:
           
            running_hour=24*7
            count = 0
            zeros_count = 0
            
            for num in iot["Value"]:
                if num ==0:
                    zeros_count += 1
                else:
                    if zeros_count >= 3:
                        count += 1
                        zeros_count = 0
            if count==0:
                return 0
            else:
                return running_hour/count
           
        except Exception as e:
           print(f'Exception occoured in Asset Details in weekly_stoppage_count function:', {e})
    
    def monthly_stoppage_count(iot): # iot = month_df
        try:
           
            running_hour=24*7*30
            count = 0
            zeros_count = 0
            
            for num in iot["Value"]:
                if num ==0:
                    zeros_count += 1
                else:
                    if zeros_count >= 3:
                        count += 1
                        zeros_count = 0
            if count==0:
                return 0
            else:
                return running_hour/count
           
        except Exception as e:
           print(f'Exception occoured in Asset Details in weekly_stoppage_count function:', {e})
    