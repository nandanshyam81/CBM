import streamlit as st
from scripts.loadanimation import load_lottiefile
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
from scripts.loadanimation import load_lottiefile

st.set_page_config(
    page_title="Conditional Based Monitoring",
    page_icon="https://cdn-icons-png.flaticon.com/512/5799/5799222.png")
     


# st.markdown(
#     f'<img src="{"./data/celebal_logo.png"}" style="position: absolute; top: 1px; left: 1px;" width="250" height="100">',
#     unsafe_allow_html=True
# )

st.title("Conditional Based Monitoring System ")
st.subheader('About')
st.write('The main goal of conditional based monitoring System is to help you optimize and maintain your resources by CBM and its Robust funtion which will accurately predict when something will fail. Because it is not always that straightforward. As a result, CBM brings its own set of advantages and does the prediction and complete visual analytics for your company and how you can apply CBM to your organization..')
lottie_coding = load_lottiefile("./data/99797-data-management.json")  # replace link to local lottie file
st.sidebar.image("./data/celebal_logo.png")
st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="Hight", # medium ; high 
    height=500,
    width=None,
    key=None,
)