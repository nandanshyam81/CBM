import requests
import random
import time 
import pandas as pd
import smtplib
import matplotlib.pyplot as plt
from email.message import EmailMessage


class fanEfficiency:
    def __init__(self) -> None:
        self.designFlow = 208
        self.designSpeed = 940
        self.designTemp = 253
        self.designLoad = 2538
        self.designHead = 1055
       
        
        
        
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
   
    
    def updateConstants(self,flow,speed,temp,load,head):
        self.designFlow = flow
        self.designSpeed = speed
        self.designTemp = temp
        self.designLoad = load
        self.designHead = head
    
    def calculateEfficiency(self,data:dict):
        speed = float(data['speed'])
        # print(speed)
        load = float(data['load'])
        inlet_draft = float(data['inlet_draft'])
        outlet_draft = float(data['outlet_draft'])
        temperature = float(data['temperature'])
        converted_flow = (273/(273+self.designTemp))*self.designFlow
        flow_speed = (speed/self.designSpeed)*converted_flow
        flow_load = ((load/self.designLoad)**(1/3))*converted_flow
        flow_head = (((outlet_draft-inlet_draft)/(self.designHead*-1))**(1/2))*converted_flow
        flow_average = (flow_speed+flow_load+flow_head)/3
        flow_average_converted = ((273+temperature)/273)*flow_average
        # print(flow_load,flow_speed,converted_flow)
        efficiency = (flow_average_converted*(-1)*(outlet_draft-inlet_draft))/(102*0.95*load)
        return round(efficiency,2)
 
    def data_creation(self):
        speed = random.randint(734,784)
        load = random.randint(2046,2410)
        inlet_draft = random.randint(544,688)
        outlet_draft = random.randint(15,22)
        temperature = random.randint(250,300)
        req_info = {
            'speed': speed,
            'load': load,
            'inlet_draft': inlet_draft,
            'outlet_draft': outlet_draft,
            'temperature': temperature
        }
        # print(req_info)
        t = fanEfficiency()
        ef=t.calculateEfficiency(req_info)
        return req_info,ef
    
fan_Efficiency=fanEfficiency()
# print(fan_Efficieny.data_creation())