import time
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage

class trendVolidaltor:

    def __init__(self,data,hivalue,hihivalue,subject,emailid,tagname,timeDelay):
        self.data = data
        self.hi = hivalue
        self.hihi = hihivalue
        self.subject = subject
        self.emailid = emailid
        self.tagName = tagname
        self.timeDelay = timeDelay

    def sendMail(self,Content):
        msg = EmailMessage()
        msg['Subject']=self.subject
        msg['From']='nandanshyam81@gmail.com'
        msg['To']=self.emailid
        msg.set_content(Content) #body
        try :
            with smtplib.SMTP('smtp.gmail.com',587) as server:
                server.starttls()
                server.login('nandanshyam81@gmail.com','xcqxxvyzbuyslhzt')
                server.send_message(msg)
        except Exception as e:
            print(e)

    def compare_trend(self):
        """Function to find the trend voilation"""
        try:
            hi_alert = np.where(self.data['Value']>self.hi,1,0)
            hihi_alert = np.where(self.data['Value']>self.hihi,1,0)
            if len(self.data)==0:
                return f'No data for {self.tagName} within time delay of {self.timeDelay} seconds'
            elif hihi_alert.sum()==len(self.data):
                value = self.data['Value'].values
                msg = f'''Hi,
                Alert has be been triggered for {self.tagName}
                Alert Type:CriticalValue
                Value :{value[0],value[1]}
                '''
                self.sendMail(msg)
                return f'HiHi Alert for {self.tagName} has been triggered'
            elif hi_alert.sum()==len(self.data):
                value = self.data['Value'].values
                msg = f'''Hi,
                Alert has be been triggered for {self.tagName}
                Alert Type:MajorValue
                Value :{value[0],value[1]}
                '''
                return f'Hi Alert for {self.tagName} has been triggered'
            else:
                return f'Everything is alright for {self.tagName}'
        except Exception as e:
            return f'Exception occured while comparing non-vibration data in Trend Violation:{e}'

                