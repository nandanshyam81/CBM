import pandas as pd
from datetime import timedelta
import smtplib
from email.message import EmailMessage



class Assetdetails:
    def sendMail(self,Content,subject,emailid):
        msg = EmailMessage()
        msg['Subject']=subject
        msg['From']='nandanshyam81@gmail.com'
        msg['To']=emailid
        msg.set_content(Content) #body
        try :
            with smtplib.SMTP('smtp.gmail.com',587) as server:
                server.starttls()
                server.login('nandanshyam81@gmail.com','xcqxxvyzbuyslhzt')
                server.send_message(msg)
        except Exception as e:
            print(e)

    
    def last_time(df):
        last_timestamp = df['Timestamp'].max()
        return last_timestamp
    def current_value(df):
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        current_time=Assetdetails.last_time(df)
        start_time = current_time - timedelta(hours=1)
        last_one_hour_values = df.loc[(df['Timestamp'] >= start_time) & (df['Timestamp'] <= current_time)]
        return last_one_hour_values["Value"]
    
        
    
        
    def previous_100hour_value(df):
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
        current_time= Assetdetails.last_time(df) - pd.Timedelta(hours=100)
        start_time =Assetdetails.last_time(df)- pd.Timedelta(hours=101)

    
        last_one_hour_values = df.loc[(df['Timestamp'] >= start_time) & (df['Timestamp'] <= current_time)]
        min=last_one_hour_values["Value"].min()
        max=last_one_hour_values["Value"].max()
        mean=last_one_hour_values["Value"].mean()
    
        return min,max,mean
    def deviation_curr_previous(df):
        x=Assetdetails.current_info(df)[0]
        y=Assetdetails.previous_100hour_value(df)[2]
        return x-y
    def current_info(df):
        x=Assetdetails.current_value(df).mean()
        y=Assetdetails.current_value(df).max()
        z=Assetdetails.current_value(df).min()
        k=df[df["Timestamp"]==Assetdetails.last_time(df)]["Value"].values[0]
        return x,y,z,k
    def output_table(df):
        current_data=Assetdetails.current_info(df)
        previous_data=Assetdetails.previous_100hour_value(df)
        dev=Assetdetails.deviation_curr_previous(df)
        data = {
            "Current Value":current_data[3],
            'Current Mean': current_data[0],
            'Current Max': current_data[1],
            'Current Min': current_data[2],
            'Previous Mean':previous_data[2],
            'Previous Max': previous_data[1],
            'Previous Min': previous_data[0],
            "Deviation":dev
            }

        df = pd.DataFrame(data,index=[0])
        return df

        
        
        

        
