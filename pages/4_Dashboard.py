
import numpy as np 
import pandas as pd  
import plotly.express as px  
import plotly.graph_objects as go
import streamlit as st  
import time
from datetime import timedelta
from streamlit_option_menu import option_menu
from scripts.DataRetrive import dataRetrival
from scripts.trendVoilation import trendVolidaltor 
from scripts.fanEfficiency import fanEfficiency
from scripts.falseAir import falseAir
from scripts.Assetdetails import Assetdetails
from scripts.MTBS import Mtbs
import warnings
import random
from datetime import datetime,timedelta
import csv
from email.mime.text import MIMEText
warnings.filterwarnings('ignore')



st.set_page_config(page_title="Dashboard", page_icon="https://cdn.iconscout.com/icon/premium/png-256-thumb/analytics-dashboard-1132933.png")

st.title("Real-Time Dashboard")

st.write(
    """Real-time display of key metrics and performance indicators that help organizations monitor the health and performance of their assets."""
)

# dashboard title

selected = option_menu(
            menu_title=None,  # required
            options=["Graph", "Data"],  # required
            icons=["clipboard-data", "activity"],  # optional
            default_index=0,  # optional
            orientation="horizontal",)
st.sidebar.image("./data/celebal_logo.png")

if selected=='Graph':
    masterTable = pd.read_csv("./data/templateTable.csv")
    emailTable = pd.read_csv('./data/Email.csv')
    Usecase= st.selectbox("Select the Usecase", pd.unique(masterTable["Use Case"]))
    template_name= st.selectbox("Select the Template Name", pd.unique(masterTable[masterTable["Use Case"]==Usecase]["Template Name"]))
    
    Equipment_name=masterTable[masterTable["Template Name"]==template_name]["Equipment Name"].values[0]
    
    tagname = masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['Tag Name'].values[0]
    templateNameU = masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['Template Name'].values[0]
    timedelay = masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Time Delay"].values[0]
    emailid = emailTable[emailTable['Use Case Template']==templateNameU]['Email Recepient'].values[0]
    subject  = emailTable[emailTable['Use Case Template']==templateNameU]['Subject'].values[0]
    
    # creating a single-element container
    placeholder = st.empty()
    if Usecase=='Trend Violation':
        
        
        df_data = pd.read_csv("./data/TrenddataTable.csv")
        while masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Active Status"].values[0]==True:
            datacreate = dataRetrival(timedelay,tagname)
            datacreated,checkData = datacreate.dataCreation()
            df_selected = datacreated[datacreated["Tag ID"] == tagname]
            addvalue =masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['HiHi Value'].values[0]
            hiaddvalue =masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['Hi Value'].values[0]
            df_selected['hihivalue'] = addvalue
            df_selected['hivalue'] = hiaddvalue
            tv = trendVolidaltor(checkData,hiaddvalue,addvalue,subject,emailid,tagname,timedelay)
            #alert 
            tv.compare_trend()
        
                
            # creating KPIs
            
            avg_val = np.mean(df_selected["Value"])
        
            count_value = int(len(df_selected))

            with placeholder.container():

                # create three columns
                kpi1, kpi2, kpi3,kpi4= st.columns(4)

                # fill in those three columns with respective metrics or KPIs
                kpi1.metric(
                    label="Mean Value",
                    value=round(avg_val),
                    delta= 10,
                )
                kpi2.metric(
                    label="Count Value",
                    value=int(count_value),
                    delta=int(timedelay//5),
                )
                kpi3.metric(
                    label="Hi Value",
                    value=hiaddvalue
                )
                kpi4.metric(
                    label="HiHi Value",
                    value=addvalue
                )

                st.subheader(f'Trend Voilation for Tag Name: {tagname}')
                # create the plot
                fig = px.line(df_selected, x='Timestamp', y=['Value', 'hihivalue', 'hivalue'], color_discrete_sequence=['lightskyblue', 'indianred', 'yellow'])
                # display the plot in Streamlit
                st.plotly_chart(fig)

                time.sleep(timedelay)
        
        while masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Active Status"].values[0]==False:
            datacreate = dataRetrival(timedelay,tagname)
            datacreated,checkData = datacreate.dataCreation()
            df_selected = datacreated[datacreated["Tag ID"] == tagname]
            addvalue =masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['HiHi Value'].values[0]
            hiaddvalue =masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['Hi Value'].values[0]
            df_selected['hihivalue'] = addvalue
            df_selected['hivalue'] = hiaddvalue
            tv = trendVolidaltor(checkData,hiaddvalue,addvalue,subject,emailid,tagname,timedelay)
            #alert 
            tv.compare_trend()
        
                
            # creating KPIs
            
            avg_val = np.mean(df_selected["Value"])
        
            count_value = int(len(df_selected))

            with placeholder.container():

                # create three columns
                kpi1, kpi2, kpi3,kpi4= st.columns(4)

                # fill in those three columns with respective metrics or KPIs
                kpi1.metric(
                    label="Mean Value",
                    value=round(avg_val),
                    delta= 10,
                )
                kpi2.metric(
                    label="Count Value",
                    value=int(count_value),
                    delta=int(timedelay//5),
                )
                kpi3.metric(
                    label="Hi Value",
                    value=hiaddvalue
                )
                kpi4.metric(
                    label="HiHi Value",
                    value=addvalue
                )

                st.subheader(f'Trend Voilation for Tag Name: {tagname}')
                # create the plot
                fig = px.line(df_selected, x='Timestamp', y=['Value', 'hihivalue', 'hivalue'], color_discrete_sequence=['lightskyblue', 'indianred', 'yellow'])
                # display the plot in Streamlit
                st.plotly_chart(fig)

                time.sleep(timedelay)           

                
    elif Usecase=='Fan Efficiency':
        
        df_fanEff=pd.read_csv("./data/FanEff Demo.csv")
        while masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Active Status"].values[0]==True:
            
            last_time = pd.to_datetime(df_fanEff['Timestamp'].iloc[-1])
            
            hihi_value=masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['HiHi Value'].values[0]
            hi_value =masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['Hi Value'].values[0]
            data,eff =fanEfficiency().data_creation()
            
            
            msg = f'''Hi,
                Alert has be been triggered for {template_name}
                Alert Type:CriticalValue (Low fanEfficiency)
                Value :{eff}
                
                '''
            msg1 = f'''Hi,
                Alert has be been triggered for {template_name}
                Alert Type:MajorValue (fanEfficiency is very Low)
                Value :{eff}
                '''
            if eff<hihi_value:
                fanEfficiency().sendMail(msg1,subject,emailid)
            elif eff<hi_value:
            
                fanEfficiency().sendMail(msg,subject,emailid)
                
            
            
            new_row = pd.DataFrame({'Timestamp': [last_time + timedelta(seconds=10)], 'Speed':float(data['speed']) ,'Load':float(data['load']),'Inlet Draft':float(data['inlet_draft']),'Outlet Draft':float(data['outlet_draft']),'Temperature':float(data['temperature']), 'eff':float(eff)})
            new_row_df = pd.DataFrame(new_row, index=[0])
            df1 = pd.concat([df_fanEff, new_row_df], ignore_index=True)
            # compare_eff(eff)
            #df1= df_fanEff.append(new_row, ignore_index=True)
            df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])
            df1['Timestamp'] = df1['Timestamp'].dt.strftime('%d-%m-%Y %H:%M:%S')
          
            df1.to_csv("./data/FanEff Demo.csv",index=False)
            with placeholder.container():
                col1, col2,col3 = st.columns(3)
                with col1:
                    st.metric(
                        label="Fan Efficiency",
                        value=eff
                    )
                with col2:
                    st.metric(
                        label="HiValue",
                        value=hi_value
                    )
                with col3:
                    st.metric(
                        label="HiHiValue",
                        value=hihi_value
                    )
                col1,col2,col3,col4,col5=st.columns(5)
                with col1:
                    st.metric(
                        label="Temperature",
                        value=float(data['temperature']),
                        
                    )
                with col2:
                    st.metric(
                        label="Fan Speed",
                        value=float(data['speed']),
                    
                    )
                with col3:
                    st.metric(
                        label="Fan Load",
                        value=float(data['load'])
                    )
                with col4:
                    st.metric(
                        label="Fan Inlet draft",
                        value=float(data['inlet_draft'])
                    )
                with col5:
                    st.metric(
                        label="Fan Outlet draft",
                        value=float(data['outlet_draft'])
                    )
                st.subheader(f'Fan efficiency: {tagname}')
                df_faneff=df_fanEff[df_fanEff["Equipment Name"]==Equipment_name]
                df_fanEff = df_fanEff.drop_duplicates(subset='Timestamp')
           
                fig = px.line(df_fanEff,x='Timestamp', y='eff')
                fig.add_hline(y=hi_value, line_color='red', line_width=2)
                fig.add_hline(y=hihi_value, line_color='blue', line_width=2)
                
                fig.update_layout(yaxis_title='Fan efficiency')
                    # display the plot in Streamlit
                st.plotly_chart(fig)
                
    
                    
                time.sleep(10.0)
        while masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Active Status"].values[0]==False:
            
            last_time = pd.to_datetime(df_fanEff['Timestamp'].iloc[-1])
            
            hihi_value=masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['HiHi Value'].values[0]
            hi_value =masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]['Hi Value'].values[0]
            data,eff =fanEfficiency().data_creation()
            
            
            msg = f'''Hi,
                Alert has be been triggered for {tagname}
                Alert Type:CriticalValue (Low fanEfficiency)
                Value :{eff}
                
                '''
            msg1 = f'''Hi,
                Alert has be been triggered for {tagname}
                Alert Type:MajorValue (fanEfficiency is very Low)
                Value :{eff}
                '''
            if eff<hihi_value:
                fanEfficiency().sendMail(msg1,subject,emailid)
            elif eff<hi_value:
            
                fanEfficiency().sendMail(msg,subject,emailid)
                
            
            
            new_row = pd.DataFrame({'Timestamp': [last_time + timedelta(seconds=10)], 'Speed':float(data['speed']) ,'Load':float(data['load']),'Inlet Draft':float(data['inlet_draft']),'Outlet Draft':float(data['outlet_draft']),'Temperature':float(data['temperature']), 'eff':float(eff)})
            new_row_df = pd.DataFrame(new_row, index=[0])
            df1 = pd.concat([df_fanEff, new_row_df], ignore_index=True)
            # compare_eff(eff)
            #df1= df_fanEff.append(new_row, ignore_index=True)
            df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])
            df1['Timestamp'] = df1['Timestamp'].dt.strftime('%d-%m-%Y %H:%M:%S')
          
            df1.to_csv("./data/FanEff Demo.csv",index=False)
            with placeholder.container():
                col1, col2,col3 = st.columns(3)
                with col1:
                    st.metric(
                        label="Fan Efficiency",
                        value=eff
                    )
                with col2:
                    st.metric(
                        label="HiValue",
                        value=hi_value
                    )
                with col3:
                    st.metric(
                        label="HiHiValue",
                        value=hihi_value
                    )
                col1,col2,col3,col4,col5=st.columns(5)
                with col1:
                    st.metric(
                        label="Temperature",
                        value=float(data['temperature']),
                        
                    )
                with col2:
                    st.metric(
                        label="Fan Speed",
                        value=float(data['speed']),
                    
                    )
                with col3:
                    st.metric(
                        label="Fan Load",
                        value=float(data['load'])
                    )
                with col4:
                    st.metric(
                        label="Fan Inlet draft",
                        value=float(data['inlet_draft'])
                    )
                with col5:
                    st.metric(
                        label="Fan Outlet draft",
                        value=float(data['outlet_draft'])
                    )
                st.subheader(f'Fan efficiency: {tagname}')
                st.dataframe(df_fanEff)
               
           
                fig = px.line(df_fanEff,x='Timestamp', y='eff')
                fig.add_hline(y=hi_value, line_color='red', line_width=2)
                fig.add_hline(y=hihi_value, line_color='blue', line_width=2)
                
                fig.update_layout(yaxis_title='Fan efficiency')
                    # display the plot in Streamlit
                st.plotly_chart(fig)
                time.sleep(10.0)        
 
            
                
    elif Usecase=='False Air':
        df_false_iot=pd.read_csv("./data/False_Air_iot.csv")
        table=falseAir().template_execution()
        table.to_csv('./data/FalseAir output.csv')
        check=round((table[table['Asset']=='Killn']['False Air%'].values[0]),2)
        hi_value=masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Hi Value"].values[0]
        hihi_value=masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["HiHi Value"].values[0]
        
        msg = f'''Hi,
                Alert has be been triggered for {tagname}
                Alert Type:CriticalValue (Low fanEfficiency)
                Value :{check}
                
                '''
        msg1 = f'''Hi,
                Alert has be been triggered for {tagname}
                Alert Type:MajorValue (fanEfficiency is very Low)
                Value :{check}
                '''
        if check<hihi_value:
                falseAir().sendMail(msg1,subject,emailid)
        elif check<hi_value:
            falseAir().sendMail(msg,subject,emailid)
        
        
        
        
        col1, col2, col3,col4 = st.columns(4)
        with col1:
            st.metric(
                label="False Air % Kiln",
                value=round((table[table['Asset']=='Killn']['False Air%'].values[0]),2)
            )
        with col2:
            st.metric(
                label="False Air % PC",
                value=round((table[table['Asset']=='PC']['False Air%'].values[0]),2)
            )
        with col3:
            st.metric(
                label="HiValue",
              
              value=hi_value
            )
        with col4:
            st.metric(
                label="HiHiValue",
                value=hihi_value
            )
        curr_time=datetime.now().date()
        st.subheader(f"False Air Table of :{curr_time-timedelta(days=1)}")
        st.dataframe(table)
        False_air_result=pd.read_csv("./data/False_Air_result.csv")    
        fig = px.line(False_air_result,x='Time stamp', y="falseair_per")
        fig.add_hline(y=hi_value, line_color='red', line_width=2)
        fig.add_hline(y=hihi_value, line_color='yellow', line_width=2)
       
        st.plotly_chart(fig)
    elif Usecase=="Asset Details":
        #df_false_iot=pd.read_csv("C:/Users/SHYAM/OneDrive/Desktop/Celebal_tech/streamlitDEV/data/False_Air_iot.csv")
        df=pd.read_csv(".\\data\\False_Air_iot.csv")
        df1=pd.read_csv(".\\data\\False_Air_master.csv")
        
        
        merged_df = pd.merge(df1, df, on='Id', how='left')
        merged_df["Equipment Name"]=merged_df["Parameters"]
        
        new_df=merged_df[merged_df["Equipment Name"]==Equipment_name]
        
       # x=Assetdetails.output_table(new_df)
       
        
        table=Assetdetails.output_table(new_df)
        st.dataframe(table)
        
        html_table = table.to_html(index=False)
        
        msg = MIMEText(html_table, 'html')
        
        last_time=Assetdetails.last_time(merged_df)
        subject=subject+"Summary info of:"+str(last_time)
        Assetdetails().sendMail(msg,subject,emailid)
        
        
    elif Usecase=="MTBS":
        #df_false_iot=pd.read_csv("C:/Users/SHYAM/OneDrive/Desktop/Celebal_tech/streamlitDEV/data/False_Air_iot.csv")
        df=pd.read_csv(".\\data\\False_Air_iot.csv")
        df1=pd.read_csv(".\\data\\False_Air_master.csv")
        merged_df = pd.merge(df1, df, on='Id', how='left')
        #merged_df["Equipment Name"]=merged_df["Parameters"]
        #new_df=merged_df[merged_df["Equipment Name"]==Equipment_name]
        res1,res2,res3=Mtbs.MTBS(merged_df)
        
        x=Mtbs.hrs_stoppage_count(res1)
        y=Mtbs.weekly_stoppage_count(res2)
        z=Mtbs.monthly_stoppage_count(res3)
        
        
#         msg = f'''Hi,
#                 Alert has be been triggered for {tagname}
#                 Alert Type:CriticalValue 
# #                 Value :{check}
                
# #                 '''
#         msg1 = f'''Hi,
#                 Alert has be been triggered for {tagname}
#                 Alert Type:MajorValue 
#                 Value :{check}
#                 '''
        
        hi_value=masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["Hi Value"].values[0]
        hihi_value=masterTable[(masterTable["Equipment Name"]==Equipment_name) & (masterTable["Use Case"]==Usecase)]["HiHi Value"].values[0]
  
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Hourly Stoppage",
                value=round(x,2)
            )
        with col2:
            st.metric(
                label="Weekly Stoppage",
                value=round(y,2)
            )
        with col3:
            st.metric(
                label="Monthly Stoppage",
                value=round(z,2)
            )
        st.subheader("Note:")
        st.write("Hourly Stoppage:","After how much time asset tends to stop in last one hour")
        
        st.write("Weekly Stoppage:","After how much time asset tends to stop in last one Week")
        st.write("Monthly Stoppage:","After how much time asset tends to stop in last one Month")
        
           
elif selected =="Data":
    masterTable= pd.read_csv("./data/templateTable.csv")
    Usecase= st.selectbox("Select the Usecase", pd.unique(masterTable["Use Case"]))
    Equipment_name= st.selectbox("Select the Equipment Name", pd.unique(masterTable[masterTable["Use Case"]==Usecase]["Equipment Name"]))
    #template_name = st.selectbox("Select the Template", pd.unique(masterTable[masterTable["Use Case"]==Usecase]["Template Name"]))
    tagname = masterTable[masterTable['Equipment Name']==Equipment_name]['Tag Name'].values[0]
    if Usecase=='Trend Violation':
    
            
            df = pd.read_csv('./data/TrenddataTable.csv')
            data_present = df[df['Equipment Name']==Equipment_name]
            st.subheader(f"Data for: {tagname}")
            st.dataframe(data_present,width=1500)
        
    elif Usecase=='Fan Efficiency':
        df = pd.read_csv('./data/FanEff Demo.csv')
        st.dataframe(df,width=1500)
    elif Usecase=='False Air':
        df = pd.read_csv('./data/FalseAir output.csv')
        st.dataframe(df,width=1500)
    elif Usecase=="Asset Details":
        df=pd.read_csv(".\\data\\False_Air_iot.csv")
        df1=pd.read_csv(".\\data\\False_Air_master.csv")
        merged_df = pd.merge(df, df1, on='Id', how='left')
        st.dataframe(merged_df,width=1500)
    elif Usecase=="MTBS":
        df=pd.read_csv(".\\data\\False_Air_iot.csv")
        df1=pd.read_csv(".\\data\\False_Air_master.csv")
        merged_df = pd.merge(df, df1, on='Id', how='left')
        st.dataframe(merged_df,width=1500)
        
        
        
        
    
# 