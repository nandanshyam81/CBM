import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import warnings
from scripts.anamoly_data_retrive import anamoly_data
warnings.filterwarnings('ignore')
import numpy as np
import scipy.io as sio
from sklearn.utils import shuffle
import pathlib
from pathlib import Path
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import random
import time
import h5py
import zipfile

from IPython.display import clear_output, display # clear the output if needed

import tensorflow as tf
from tensorflow import keras
import tensorboard
from tensorflow.keras.models import model_from_json
from scripts.data_prep import DataPrep
from scripts.threshold import SelectThreshold
from scripts.tcn import TCN


st.set_page_config(page_title="Predictive Maintenance", page_icon="https://www.pngwing.com/en/free-png-tfoae")
st.title("Predictive Maintenance")
st.sidebar.image("./data/celebal_logo.png")
st.header("Anomaly Detection")
selected = option_menu(
            menu_title=None,  # required
            options=["Graph", "Data"],  # required
            icons=["clipboard-data", "activity"],  # optional
            default_index=0,  # optional
            orientation="horizontal",)
K = keras.backend

 

class Sampling(keras.layers.Layer):
    def call(self, inputs):
        mean, log_var = inputs
        return K.random_normal(tf.shape(log_var)) * K.exp(log_var / 2) + mean

def mse( X_val, recon_val):
        """Calculate MSE for images in X_val and recon_val"""
        # need to calculate mean across the rows, and then across the columns
        try:
            # if this works, then you will be getting the mean across all the signals
            return np.mean(np.mean(np.square(X_val - recon_val), axis=1), axis=1)
        except:
            # if the above does not work, then it is assumed that you are only looking
            # for the mean of one signal -- therefore the below should work
            return np.mean(np.square(X_val - recon_val), axis=1)


def load_train_test(directory):

    path = directory

    with h5py.File(path, "r") as f:

        X_val = f["X_val"][:]
        return X_val

threshold=300
def random_data(X_val):
    i=random.randint(0,len(X_val))
    return X_val[i].reshape(1,64,6)

def load_model(model_folder,model_name):
    loaded_json = open(
    r"{}/{}/model.json".format(model_folder, model_name), "r").read()
    
    model = model_from_json(loaded_json, custom_objects={"TCN": TCN, "Sampling": Sampling})
    
    model.load_weights(r"{}/{}/weights.h5".format(model_folder, model_name))
    return model

model_folder="C:\\Users\\SHYAM\\OneDrive\\Desktop\\Celebal_tech\\ml-tool-wear-master\\models\\best_models\\best_models"
model_name="20200620-053315_bvae"
model=load_model(model_folder,model_name) 
X_val=load_train_test("./data/X_val.hdf5") 

 


def get_prediction_mre(model,x_random,threshold):
    
    recon_value=model.predict(x_random)
    
    recon_error=mse(x_random,recon_value)
    
    if recon_error>=threshold:
        
        return recon_error,threshold,-1
    return recon_error,threshold,1


if 'loop_count' not in st.session_state:
    st.session_state.loop_count = 0




def updated_g():
            df1=pd.read_csv("./data/anamoly_data.csv")
            df=df1.tail(50)
            anomaly_df = df[df['prediction']==-1]
            non_anomaly_df = df[df['prediction']==1]
            
            
            
            plt.figure(figsize=(8, 6))
            #plt.scatter(non_anomaly_df['Unnamed: 0'], non_anomaly_df['metric'], color='green', label='Not Anomaly', s=100)
            plt.scatter(anomaly_df['Cut'], anomaly_df['error'], color='red', label='Anomaly', s=100)
            plt.plot(df["Cut"],df["error"])
            plt.axhline(y=300, color='green', linestyle='--', label='Metric Value')

            plt.xlabel('Number of cuts')
            plt.ylabel('Threshold')
            plt.title('Anomaly Detection')
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)


coun=0
while True:
    x_random=random_data(X_val) 
    error,thresh,prediction=get_prediction_mre(model,x_random,threshold)


    df = pd.read_csv("./data/anamoly_data.csv")
    

    cut_no=len(df)+1
    new_row_data = {'Cut': cut_no, 'error': error[0],"prediction":prediction}
    new_row_df = pd.DataFrame([new_row_data])

    # Concatenate the new row DataFrame with the original DataFrame
    df = pd.concat([df, new_row_df], ignore_index=True)
    df.to_csv("./data/anamoly_data.csv", index=False)
    
    if selected=="Data":
        if coun==0:
            coun+=1
            df=pd.read_csv("./data/Features_data.csv")
            st.dataframe(df)
        
        st.empty()
    elif selected=="Graph":
        updated_g()

    # Increment the loop_count to update the plot on the next iteration
        st.session_state.loop_count += 0.1

    # Introduce a short pause to control the update rate
        st.experimental_rerun()
        
        
            
        
        plot_placeholder.pyplot(plt)
        plot_placeholder.empty()
        
    time.sleep(5)
    





