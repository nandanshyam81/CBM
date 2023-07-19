import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="EquipmentTemplate", page_icon="https://cdn.iconscout.com/icon/premium/png-256-thumb/robotic-production-1628355-1381799.png")
st.title("Equipment Template")
#st.sidebar.header("Equipment Template")
st.sidebar.image("./data/celebal_logo.png")
st.write(
    """To create and manage Equipment Templates. 

     Functionaliy:
     1.Allow users to create and edit templates.
     2.Display them in a table.
     3.Allow users to disable a templates."""
)


def displayTemplateList():
     """Function used to showcase all the template list"""
     df = pd.read_csv('./data/templateTable.csv')
     df = df[['Template Name', 'Plant Name', 'Tag Name', 'Equipment Name', 'Use Case','Active Status']]
     return df
def make_dataframe_editable(df):
    df_copy = df.copy()

    with st.form(key='edit_form'):
        st.dataframe(df_copy, edit_columns=True, key='editable_df')
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        edited_df = st.session_state.editable_df
        return edited_df
def UpateTemplateList(templateName,plantName,tagName,useCase,seconds,hivalue,hihivalue,Alert_Option,Equipment_name,active):
     """Function used to update the template list that as created"""
     df = pd.read_csv('./data/TrenddataTable.csv')
     df_master = pd.read_csv('./data/templateTable.csv')
     equipmentName = Equipment_name
     new_row = {'Template Name':templateName,'Plant Name':plantName,'Tag Name':tagName,'Equipment Name':equipmentName,'Use Case':useCase,'Time Delay':seconds,'Hi Value':hivalue,'HiHi Value':hihivalue,'Alert Option':Alert_Option,'Active Status':active}
    # df_master = df_master.append(new_row, ignore_index=True)
     df_master.loc[len(df_master)] = new_row

     df_master.to_csv('./data/templateTable.csv',index=False)

def updateTable(data):
     df = pd.read_csv('./data/templateTable.csv') 
     for i in range(len(data)):
          df.at[i,'Hi Value'] = df.iloc[i]['Hi Value']
          df.at[i,'HiHi Value'] = df.iloc[i]['HiHi Value']
          df.at[i,'Template Name'] = df.iloc[i]['Template Name']
          if data['Active Status'][i]==False:
              df.at[i,'Active Status']= False
          elif data['Active Status'][i]==True:
              df.at[i,'Active Status']=True
     df.to_csv("./data/templateTable.csv",index=False)
#def update_hi_and_hihi(df,hi_value,hihi_value,Equipment_name):
    # df[df["Template Name"]==Equipment_name]]["Hi Value"]=hi_value
    # df[df["Template Name"]==Equipment_name]["HiHi Value"]=hihi_value
    
    
    #return df
    
selected = option_menu(
            menu_title=None,  # required
            options=["Template List", "Create Template"],  # required
            icons=["card-list", "projector-fill"],  # optional
            default_index=0,  # optional
            orientation="horizontal",)


if selected=='Template List':
    st.subheader("Equipment Template List")
    data_trend = displayTemplateList()
    edited_df = st.data_editor(data_trend,width=850)
    updateTable(edited_df)


    st.subheader("Edit here Hi Value and HiHi Value")
    
    masterTable=pd.read_csv("./data/templateTable.csv")
    Usecase= st.selectbox("Select your Usecase", options=["Trend Violation","Fan Efficiency", "False Air"])
        
    with st.form("Edit Hi value and HiHi Value"):
        
        
        
        template_name=st.selectbox("Select the Equipment", pd.unique(masterTable[masterTable["Use Case"]==Usecase]["Equipment Name"]))
        
        hi_value = st.number_input("Edit Hi value", value=0.0)
        hihi_value = st.number_input("Edit HiHi value", value=0.0)
    
    
        submit_button = st.form_submit_button("Submit")

    
    
    if submit_button:
        df = pd.read_csv('./data/templateTable.csv')
    
        df.loc[(df['Use Case'] == Usecase) &(df['Template Name'] == template_name), "Hi Value"] = hi_value
        df.loc[(df['Use Case'] == Usecase) &(df['Template Name'] == template_name), "HiHi Value"] = hihi_value
        df.to_csv('./data/templateTable.csv', index=False)
        st.write("value Updated successfully")




elif selected =="Create Template":
    st.subheader("Equipment Template Configuration")
    df = pd.read_csv('./data/TrenddataTable.csv')
    tag_idlt = list(df['Tag ID'].unique())
    templatename = st.text_input("Template Name")
    plantname = st.selectbox(label='Plant Name',options=["CP","RN"])
    usecase = st.selectbox(label='Usecase',options=['Fan Efficiency','Trend Violation','False Air',"Asset Details","MTBS"])
   
    if usecase == 'Trend Violation':
        with st.form('new_form'):
            masterTable=pd.read_csv("./data/TrenddataTable.csv")
            Equipment_name=st.selectbox("Select the Equipment",options=pd.unique(masterTable["Equipment Name"]))
            tagid = st.selectbox(label='Tag Name',options=tag_idlt)
            seconds = st.number_input('Time Delay(s)')
            hivalue = st.number_input('Hi Value')
            hihivalue = st.number_input('HiHi value')
            Alert_Option = st.selectbox(label='Alert Option',options=["Email","SMS","Both"])
            
            new_form_submit_button = st.form_submit_button('Submit')
    elif usecase=="Fan Efficiency":
         with st.form('new_form'):
             masterTable=pd.read_csv("./data/FanEff Demo.csv")
             Equipment_name=st.selectbox("Select the Equipment",options=pd.unique(masterTable["Equipment Name"]))
             tagid =tag_idlt[0]
             seconds = -99
             hivalue = st.number_input('Hi Value')
             hihivalue = st.number_input('HiHi value')
             Alert_Option = st.selectbox(label='Alert Option',options=["Email","SMS","Both"])
             new_form_submit_button = st.form_submit_button('Submit')
    elif usecase=="False Air":
         with st.form('new_form'):
             df1=pd.read_csv("./data/False_Air_master.csv")
             df=pd.read_csv("./data/False_Air_iot.csv")
             masterTable = pd.merge(df1, df, on='Id', how='left')
             masterTable["Equipment Name"]=masterTable["Parameters"]
             Equipment_name=st.selectbox("Select the Equipment",options=pd.unique(masterTable["Equipment Name"]))
             tagid = tag_idlt[0]
             seconds = -99
             hivalue = st.number_input('Hi Value')
             hihivalue = st.number_input('HiHi value')
             Alert_Option = st.selectbox(label='Alert Option',options=["Email","SMS","Both"])
             new_form_submit_button = st.form_submit_button('Submit')
    elif usecase=="Asset Details":
         with st.form('new_form'):
             df=pd.read_csv("./data/False_Air_master.csv")
             df1=pd.read_csv("./data/False_Air_iot.csv")
             masterTable = pd.merge(df1, df, on='Id', how='left')
             masterTable["Equipment Name"]=masterTable["Parameters"]
             
             Equipment_name=st.selectbox("Select the Equipment",options=pd.unique(masterTable["Equipment Name"]))
             tagid = tag_idlt[0]
             seconds = -99
             hivalue = -99
             hihivalue =-99
             Alert_Option = st.selectbox(label='Alert Option',options=["Email","SMS","Both"])
             new_form_submit_button = st.form_submit_button('Submit')
    elif usecase=="MTBS":
         with st.form('new_form'):
             df=pd.read_csv("./data/False_Air_master.csv")
             df1=pd.read_csv("./data/False_Air_iot.csv")
             masterTable = pd.merge(df1, df, on='Id', how='left')
             masterTable["Equipment Name"]=masterTable["Parameters"]
             Equipment_name=st.selectbox("Select the Equipment",options=pd.unique(masterTable["Equipment Name"]))
             tagid = tag_idlt[0]
             seconds = -99
             hivalue = -99
             hihivalue = -99
             Alert_Option = st.selectbox(label='Alert Option',options=["Email","SMS","Both"])
             new_form_submit_button = st.form_submit_button('Submit')        
    if new_form_submit_button:
            # Handle new form submission here
        UpateTemplateList(templatename,plantname,tagid,usecase,seconds,hivalue,hihivalue,Alert_Option,Equipment_name,True)
        st.success('Template has been created')


