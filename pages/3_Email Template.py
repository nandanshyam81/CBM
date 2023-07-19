import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import warnings 
import warnings
warnings.filterwarnings('ignore')


#
st.set_page_config(page_title="EmailTemplates", page_icon="envelope")
st.title("Email Templates")
#st.sidebar.header("Email Templates")
st.write(
     """To create and manage Email Templates. 

     Functionaliy:
     1.Allow users to create and edit email templates.
     2.Display them in a table.
     3.Allow users to disable a templates."""
)


def displayTemplateList():
     """Function used to showcase all the template list"""
     df = pd.read_csv("./data/Email.csv")
     df = df[['Email Template Name','Usecase','Subject','Active Status']]
     return df

def UpateTemplateList(emailtemplatename,usecase,mailsubject,emailrecepient,templatename,active):
     """Function used to update the template list that as created"""
     df = pd.read_csv("./data/templateTable.csv")
     df_email = pd.read_csv("./data/Email.csv")
     equipmentName = df[df['Template Name']==templatename]['Equipment Name'].values[0]
     new_row = {'Email Template Name':emailtemplatename,'Usecase':usecase,'Equipment Name':equipmentName,'Subject':mailsubject,'Email Recepient':emailrecepient,'Use Case Template':templatename,'Active Status':active}
     #df_email = df_email.append(new_row, ignore_index=True)
     df_email.loc[len(df_email)] = new_row
     df_email.to_csv("./data/Email.csv",index=False)


def updateTable(data):
     df = pd.read_csv("./data/Email.csv") 
     for i in range(len(data)):
          if data['Active Status'][i]==False:
              df.at[i,'Active Status']= False
          elif data['Active Status'][i]==True:
              df.at[i,'Active Status']=True
     df.to_csv("./data/Email.csv",index=False)

selected = option_menu(
            menu_title=None,  # required
            options=["Email Template List", "Create Email Template"],  # required
            icons=["card-list", "envelope-check"],  # optional
            default_index=0,  # optional
            orientation="horizontal",)


if selected=='Email Template List':
    st.subheader("Email Template List")
    data_trend = displayTemplateList()
    edited_df_value = st.data_editor(data_trend,width=1500)
    updateTable(edited_df_value)
   

elif selected =="Create Email Template":
    st.subheader("Email Template Details")
    df = pd.read_csv('./data/templateTable.csv')
    listtemplatename = list(df['Template Name'].unique())
    emailtemplatename = st.text_input('Email Template Name')
    templatename = st.selectbox(label='Equipment Template Name',options=listtemplatename)
    emailrecepient = st.text_input('Email Recepient',help='Mail-ID of recepient')
    mailsubject = st.text_input('Mail Subject',help='Subject for the Mail')
    new_form_submit_button = st.button('Submit')
    usecase = df[df['Template Name']==templatename]['Use Case'].values[0]
    if new_form_submit_button:
        # Handle new form submission here
        UpateTemplateList(emailtemplatename,usecase,mailsubject,emailrecepient,templatename,True)
        st.success('Template has been created')
st.sidebar.image("./data/celebal_logo.png")

