import time
import pandas as pd
import numpy as np
import smtplib
from datetime import datetime,timedelta
from email.message import EmailMessage

class falseAir:
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

    
    def extract_datetimes(self,current_datetime):
        try:
            one_day_ago_datetime = current_datetime - timedelta(days=1)
            one_day_ago_start_time=datetime.strptime(datetime.strftime(one_day_ago_datetime,'%y-%m-%d'),'%y-%m-%d')
            current_day_start_time = one_day_ago_start_time+timedelta(days=1)
            return pd.Timestamp(current_day_start_time,tz='UTC'),pd.Timestamp(one_day_ago_start_time,tz='UTC')
        except Exception as e:
            print(f'Exception occured while extracting datetimes for False Air:{e}')
        
    def calculate_kiln_false_air(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            kiln_oxygen_outlet = df.loc[df['Parameters']=='Kiln String Oxygen Outlet','Value'].mean()
            kiln_oxygen_inlet = df.loc[df['Parameters']=='Kiln String Oxygen Inlet','Value'].mean()
            return (kiln_oxygen_outlet-kiln_oxygen_inlet)/(21-kiln_oxygen_outlet)
        except Exception as e:
            print(f'Exception occured while calculating kiln false air for False Air:{e}')

    def calculate_calciner_false_air(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            calciner_oxygen_outlet = df.loc[df['Parameters']=='Calciner String Oxygen Outlet','Value'].mean()
            calciner_oxygen_inlet = df.loc[df['Parameters']=='Calciner String Oxygen Inlet','Value'].mean()
            return (calciner_oxygen_outlet-calciner_oxygen_inlet)/(21-calciner_oxygen_outlet)
        except Exception as e:
            print(f'Exception occured while calculating calciner false air for False Air:{e}')

    def calculate_feed_rate(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            return df.loc[df['Parameters']=='Kiln Feed Rate','Value'].mean(),df.loc[df['Parameters']=='Calciner Feed Rate','Value'].mean()
        except Exception as e:
            print(f'Exception occured while calculating Feed rate for false air:{e}')

    def return_average_oxygen_inlet(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            return df.loc[df['Parameters']=='Kiln String Oxygen Inlet','Value'].mean(),df.loc[df['Parameters']=='Calciner String Oxygen Inlet','Value'].mean()
        except Exception as e:
            print(f'Exception occured while calculating oxygen inlet for False Air:{e}')

    def return_average_oxygen_outlet(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            return df.loc[df['Parameters']=='Kiln String Oxygen Outlet','Value'].mean(),df.loc[df['Parameters']=='Calciner String Oxygen Outlet','Value'].mean()
        except Exception as e:
            print(f'Exception occured while calculating oxygen outlet for False Air:{e}')

    def return_fan_load(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            return df.loc[df['Parameters']=='Kiln String Fan KW','Value'].mean(),df.loc[df['Parameters']=='Calciner String Fan KW','Value'].mean()
        except Exception as e:
            print(f'Exception occured while calculating fan load for false air:{e}')

    def return_fan_rotation(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            return df.loc[df['Parameters']=='Kiln String Fan RPM','Value'].mean(),df.loc[df['Parameters']=='Calciner String Fan RPM','Value'].mean()
        except Exception as e:
            print(f'Exception occured while calculating while calculating fan rotation:{e}')

    def calculate_tpd(self,date_filtered_df):
        try:
            df = date_filtered_df.copy()
            kiln_tph = df.loc[df['Parameters']=='Kiln TPH','Value'].mean() 
            kiln_df=df.loc[df['Parameters']=='Kiln Running Status']
            kiln_minutes_count=np.where(kiln_df['Value']==5,1,0)
            kiln_running_hours = kiln_minutes_count.sum()/60
            return kiln_tph*kiln_running_hours
        except Exception as e:
            print(e)


    def template_execution(self):
    # try:
        # single_template,current_datetime = args[:]
        # user_id = single_template['UserId'].iloc[0]
        # template_name = single_template['TemplateName'].iloc[0]
        # df,tuple_of_ids=extract_template_parameters(single_template)
        df=pd.read_csv('./data/False_Air_master.csv')
        current_day_start_time,one_day_ago_start_time=self.extract_datetimes(datetime(2023, 4, 4))
        iot_data=pd.read_csv('./data/False_Air_iot.csv')
        merge_df = df.merge(iot_data[['Id','Value','Timestamp']],on='Id',how='inner')
        merge_df['Timestamp']=pd.to_datetime(merge_df['Timestamp'])
        date_filtered_df = merge_df.loc[(merge_df['Timestamp']>one_day_ago_start_time) & (merge_df['Timestamp']<current_day_start_time)]
        # table for each template
        table_dict = {
            'Asset':['Killn','PC'],
            'TPD':[],
            'Feed Rate':[],
            'Inlet O2%':[],
            'Outlet O2%':[],
            'False Air%':[],
            'Fan RPM':[],
            'Fan KW':[]
        }
        for j in table_dict.keys():
            if j == 'Asset':
                pass
            elif j == 'TPD':
                kiln_tpd=self.calculate_tpd(date_filtered_df)
                table_dict[j].append(kiln_tpd)
                table_dict[j].append(kiln_tpd)
            elif j == 'Feed Rate':
                kiln_feed_rate,calciner_feed_rate=self.calculate_feed_rate(date_filtered_df)
                table_dict[j].append(kiln_feed_rate)
                table_dict[j].append(calciner_feed_rate)
            elif j == 'Inlet O2%':
                kiln_inlet,calciner_inlet = self.return_average_oxygen_inlet(date_filtered_df)
                table_dict[j].append(kiln_inlet)
                table_dict[j].append(calciner_inlet)
            elif j == 'Outlet O2%':
                kiln_outlet,calciner_outlet = self.return_average_oxygen_outlet(date_filtered_df)
                table_dict[j].append(kiln_outlet)
                table_dict[j].append(calciner_outlet)
            elif j == 'False Air%':
                table_dict[j].append(self.calculate_kiln_false_air(date_filtered_df)*100)
                table_dict[j].append(self.calculate_calciner_false_air(date_filtered_df)*100)
            elif j == 'Fan RPM':
                kiln_rotation,calciner_rotation = self.return_fan_rotation(date_filtered_df)
                table_dict[j].append(kiln_rotation)
                table_dict[j].append(calciner_rotation)
            elif j == 'Fan KW':
                kiln_load,calciner_load = self.return_fan_load(date_filtered_df)
                table_dict[j].append(kiln_load)
                table_dict[j].append(calciner_load)
            else:
                print(f'Why do u have unnecessary key {j} in the dict?')
        table=pd.DataFrame(table_dict)
        return table
        # table.to_csv("C:/Users/VarunAgarwal/Desktop/streamlitDEV/data/test.csv")
    #     html_table = table.to_html()
    #     html_table += f'<br> This is a system generated notfication for false air report generated by {user_id}'
    #     mail_query = f'Utcl_Fan_Efficiency_MailAlerts_Testing| where UseCaseTemplate=="{template_name}"'
    #     mail_df = connect_ADX_with_AAD_application_key_auth(mail_query)
    #     subject = mail_df['Subject'].iloc[0]
    #     recipient_list = mail_df['Recipients'].iloc[0].split(',')
    #     send_mail(recipient_list,subject,html_table)
    #     return f'Execution for False Air template {template_name} completed'
    # except Exception as e:
    #     print(f'Exception occured while executing template {template_name} for False Air:{e}')


                