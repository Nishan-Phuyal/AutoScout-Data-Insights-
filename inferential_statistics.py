import streamlit as st
import statsmodels.api as sm
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt




def  introduction():
    with st.expander("After familiarization with the dataset and exploration of trends in the EDA section, it became clear that the structure of the data warranted a more comprehensive inferential analysis."):
        st.markdown(""":blue[The Autoscout dataset presents ample opportunities for in-depth exploration through inferential statistics,
                     with the primary objective being the engineering of features and selection of variables to maximize the model's predictive power. 
                    In other words, the goal is to lay the groundwork for a machine learning algorithm with high predictive accuracy.
                    To achieve this, priority is given to metrics that are less punitive towards non-parsimonious models, specifically R-squared and AIC, which are used as the primary model evaluation criteria. 
                    In contrast, metrics such as BIC, the Jarque-Bera test (JB), and even the Variance Inflation Factor (VIF) are deprioritized in favor of enhancing predictability.
                    However, the importance of maintaining statistical rigor is also recognized, leading to the incorporation of interactive tools that allow for the selection of statistically sound models.
                     Despite a focus on maximizing predictability, these tools ensure that traditional statistical requirements can be addressed .
                    Following the convention in statistics, initially a multiple linear regression approach is adopted.  
                    To make the interpretation of coefficents more intuitive  multiple feature transformation techniques are employed. These transformations capture the complex relationships more efficienty and seemingly improve the model's predictive capabilities (based on R2).
                    ]\n

                    The explaination of each transformed variables are as follows\n
                    - 1. Fuel Consumption per 100 km → Kilometers per Liter: This transformation provides a more intuitive measure of fuel efficiency.\n
                    - 2. Total Mileage → Mileage per Year: This transformation standardizes mileage over time,making it easier to compare vehicles of 
                    different ages.\n
                    - 3. Production Year → Vehicle Age: To avoid division by zero, age is scaled by one. Notably, scaling by a constant does not affect
                     the OLS results, ensuring the integrity of the analysis.\n
                     (please enojoy the interative tool to select and run your choice of Multiliner Regresson)
                   """)

#import data globally 
df = pd.read_csv("clean_data.csv")
df["age"] = 2024-df["year"]
df["mile_per_year"] = df["mileage_in_km"]/df["age"]
df["km_per_liter"] = 100/df["fuel_consumption_l_100km"]


def dummy_ols():
    """interactive dummy OLS Regression"""
    with st.form("Dummy_Form"):
            with st.popover("Pooled Regression with Dummy"):

                select_regressand = st.multiselect("Price is default selection", options=["price_in_euro"],default=["price_in_euro"], placeholder= "Do not leave Regressand empty (*)")

                select_quantitative_regressors = st.multiselect("Select the Indipendent Variables", options= ["year","power_ps","fuel_consumption_l_100km","mileage_in_km", "age", "mile_per_year", "km_per_liter" ], default=["age", "mile_per_year", "km_per_liter" ,"power_ps"], placeholder= "please select at least one variable (*)")

                select_qualitative_regressors_ = st.multiselect("Select the Dummies.", options= ["brand","model","transmission_type","fuel_type"], placeholder= "please select the dummy variable/s (Optional)")

                st.form_submit_button(':blue[Run Pooled Regression]')

                # create a dataframe with selected features
                df_ols = pd.get_dummies(df[[i for i in (select_quantitative_regressors + select_qualitative_regressors_ + select_regressand)]] ,columns=[i for i in select_qualitative_regressors_], drop_first=True, dtype=int)
                
                # Extracting the selected features to render above the summary statistics

                qualitative_regressors = [i.upper() for i in select_qualitative_regressors_] # features selected as dummy 
                first_elements = [sorted(df[i])[0].upper() for i in select_qualitative_regressors_] # first element of each category after shorting them alphabetically are the base variable. 
                print_message = 'respectively' if len(select_qualitative_regressors_) > 1 else '' # just to make the sentence grammatically correct

                 # Constructing the info message
            if qualitative_regressors:
                info_message = f"##### The base variable for {', '.join([i for i in qualitative_regressors])} is {', '.join([i for i in first_elements])} {print_message}"
            else:
                info_message = "##### Running regression without Dummy"
                

            # Displaying the information using st.info()
            try:
                y = df_ols[select_regressand]

                X = df_ols.drop(columns=[i for i in select_regressand], axis=1) 
                

                # Add a constant to the model
                X = sm.add_constant(X)
                # Perform OLS regression
                model = sm.OLS(y, X)
                results = model.fit()
                st.info(info_message)
                st.write(results.summary())
            except ValueError:
                st.error("#### Summary not available, did you forget to select the mandatory variables (*)")


def Hierarchical_regression():
        """interative Hierarchical Regression """
        with st.form("Hierarchical regression"):
            with st.popover("Hierarchical regression"):

                select_regressand = st.multiselect("Price is default selection", options=["price_in_euro"],default=["price_in_euro"], placeholder= "Regressand cannot be changed")

                select_quantitative_regressors = st.multiselect("Select the Indipendent Variables", options= ["year","power_ps","fuel_consumption_l_100km","mileage_in_km", "age", "mile_per_year", "km_per_liter" ], default=["age", "mile_per_year", "km_per_liter" ,"power_ps"], placeholder= "please select at least one variable")

                category = st.selectbox("category selection.", options= ["brand","model","transmission_type","fuel_type"], index=0)
                                                              

                subcategories = st.selectbox("Select the subcategory.", options= df[category].unique().tolist(), index=0)
            

                st.form_submit_button(':blue[Run Pooled Regression]')
          
            info_message = (f"##### Showing results for {subcategories}")
            st.info(info_message)


            df_ols = df[[i for i in (select_quantitative_regressors + select_regressand + [category])]] 
            df_ols = df_ols[df_ols[category].isin([subcategories])] # create a new dataframe just having the selected features!!
            try:
                y = df_ols[select_regressand]

                X = df_ols.drop(columns=[i for i in (select_regressand+[category])], axis=1) 

                # Add a constant to the model
                X = sm.add_constant(X)
                # Perform OLS regression
                model = sm.OLS(y, X)
                results = model.fit()
                st.write(results.summary())
            except ValueError as e:
                st.warning("No sufficient Data to run regression ")



def display_ols():
     dummy, hierarchical = st.columns((1,1))
     with dummy:
          dummy_ols()
     with hierarchical:
        Hierarchical_regression()

def app():
    introduction()
    display_ols()
