import streamlit as st
import pandas as pd 
import plotly.express as px 
import time




## texts 
data_info = """A comprehensive study of Autoscout data using Explorative Data Analys, inferential statistics, machine learning and predictive analysis. 
The dataset has undergone several preprocessing steps, which are essential for further implementation. Detailed information about these preprocessing activities can be found in the :blue[_preprocessing_] 
    directory. 
    I welcome and appreciate any comments or suggestions for improvement. "Nevertheless, please find brief overview on the data in Hand. """

quantitativ = f"""
:green[Registration Date]: _The date when the car was registered (Month/Year)._\n
:green[Year of Production]: _The year in which the car was manufactured._\n
:green[Price in Euro]: _The price of the car in Euros._\n
:green[Power]: _The power of the car in kilowatts (kW) and horsepower (ps)._\n
:green[Fuel Consumption]: _Information about the car's fuel consumption in L/100km ang g/km._\n
:green[Mileage]: _The total distance traveled by the car in km._\n


"""

qualitative = """
:green[Brand]: _The brand or manufacturer of the car._\n
:green[Model]: _The specific model of the car._\n
:green[Color]: _The color of the car's exterior._\n
:green[Transmission Type]: The type of transmission (e.g., automatic, manual)._\n
:green[Fuel Type]: _The type of fuel the car requires._\n
:green[Offer Description]: _Additional description provided in the car offer._\n
"""
data = pd.read_csv("data.csv")

def text_flow(text:str, delay: float) -> any:
        
        """ Function to display text in chat GPT style. """

        for word in text.split(" "):
            yield word + " "
            time.sleep(delay)



def show(delay: float):
    url = "https://www.kaggle.com/datasets/wspirat/germany-used-cars-dataset-2023"
    st.write("The data is sourced from Kaggle.please visit [Kaggle](%s) for original dataset"% url) 
    
    st.write_stream(text_flow(data_info, delay))
    st.divider()
    col1, col2 = st.columns((2))
    with col1:
        st.info("Qunantitative features")
        st.write_stream(text_flow(quantitativ, delay))
    with col2:
            st.info("Qualitative features")
            st.write_stream(text_flow(qualitative, delay))
    st.warning(f" The Dataframe has dimention of {data.shape[1]} Columns and {data.shape[0]} Rows, Here is an overview unprocessed data ! ")    
    with st.spinner(text="In progress..."):
        time.sleep(delay)
        st.dataframe(data)

############## preprocessing overview #########################

def Preprocessing(delay: float):
    st.header("Pre-Processing")
    st.divider() 
    step_one(delay)
    step_two(delay)
   




def step_one(delay):
    st.info("#### Features Selections")
    st.write_stream(text_flow(""" First, the features were analyzed for their relevance and redundancy. 
                Only the significant features were retained. Most of the feature entries in the raw data were stored as strings.
                 Therefore, an additional action in step 1 was to transform each feature into its respective variable class. 
                The following DataFrame demonstrates the actions taken in this step.""", delay))
    data = pd.read_csv("data.csv")
    data = data[["fuel_consumption_l_100km","brand", "model", "year", "price_in_euro", "power_ps", "transmission_type","fuel_type", "mileage_in_km"]]
    st.session_state.data = data
    df_columns =  data.columns.to_list()
    columns_type = [str(type(data[i][1])) for i in df_columns]
    columns_type_corrected = ["Str", "Str", "Int", "Float", "Int", "Str", "Str", "Float", "Float"]

    data_type_df = pd.DataFrame({"Features": df_columns,
                                "Data_type": columns_type,
                                "Data_type_corrected": columns_type_corrected})
    col1, col2 = st.columns((1,1), gap= "small")
    with col1:
        time.sleep(1)
        st.subheader(" _Features data-type correction_")
        st.dataframe(data_type_df[::], hide_index=True)
    with col2:
         time.sleep(delay)
         st.subheader(" _Shows inconsistent entries and NAN values within the raw dataset_")
         st.dataframe(data.head(9).style.highlight_null(color='#5a189a'))




def step_two(delay):
    st.info("#### Dealing with Inconsistent and Missing Data")
    st.write_stream(text_flow("""
                As can be seen above the dataset contains several columns with inconsistent entries and missing values (NaN), 
                necessitating robust imputation strategies to ensure data integrity. Initially, 
                I am adopting a straightforward approach by removing rows that exhibit missing or inconsistent entries across any of the nine key features.
                To minimize the impact and retain as much valuable data as possible, I plan to implement the following advanced imputation techniques:""",delay))
    
    time.sleep(delay)
    st.markdown(" - 1. Contextual Imputation: I will fill inconsistent entries by identifying and leveraging similar records within the dataset. This method aims to ensure continuity and accuracy in data representation.")
    time.sleep(delay)
    st.markdown( """ - 2. Statistical Imputation: Should the contextual method fail, and depending on the distribution and skewness of the data, the appropriate statistical imputation methods—'Mean', 'Median', or 'Linear Regression'—will be implemented.""")
    time.sleep(delay)
    st.markdown(""" - 3. Predictive Imputation: Appropriate machine learning algorithms will be employed to predict and impute missing values based on patterns derived from the existing data.
                These methods are designed to enhance the dataset's completeness while maintaining its quality, enabling more reliable analysis and decision-making.""")

############## preprocessing overview end #########################




def app():
    if "flow_text" not in st.session_state:
        st.session_state["flow_text"] = show(0.06)
        st.session_state["flow_text"]
        Preprocessing(0.06)
        
    else:
        st.session_state["flow_text"] =  show(0)
        st.session_state["flow_text"]
        Preprocessing(0)


        
        
       


    

    
