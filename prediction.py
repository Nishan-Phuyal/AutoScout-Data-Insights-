import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor



def predictive_model(model, new_data):
    "Select any model to pass in the pipeline and predict"
    # import data
    df = pd.read_csv("clean_data.csv")
    # feature transofrmation
    df["age"] = 2024-df["year"]
    df["mile_per_year"] = df["mileage_in_km"]/df["age"]
    df["per_liter_km"] = 100/df["fuel_consumption_l_100km"]
    # Define features and Target (Regressand and Regressor)
    y = df["price_in_euro"]
    X = df[['brand', 'model', 'power_ps', 'transmission_type', 'fuel_type', 'age', 'mile_per_year', 'per_liter_km']]

    
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing for categorical and numerical data using sklearn ColumnTransformer model

    preprocessor = ColumnTransformer(transformers= [
        ("num", StandardScaler(), ["power_ps", "age", "mile_per_year", "per_liter_km"]),
        ("cat", OneHotEncoder(handle_unknown="ignore",drop='first'),["brand", "model", "transmission_type", "fuel_type"])
    ]
    )
    # create a pipeline that combines preprocessing and model training 
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', model())
    ])
    # fit the model on the training data
    pipeline.fit(X_train, y_train)
    
    # results are saved for each model to visualize it stremlit.
    return pipeline.predict(new_data)


def input_data():

    df = pd.read_csv("clean_data.csv")
    st.info("Please select Features for Price prediction")
    col1, col2, = st.columns((1,1))

    with col1:
        Brand = st.selectbox("Brand",df["brand"].unique())
        Model = st.selectbox("Model",df[df["brand"]==str(Brand)]["model"].unique())
        Transmission = st.selectbox("Transmission", df["transmission_type"].unique())
        Fuel = st.selectbox("Fuel Type", df["fuel_type"].unique())
        with col2:
            PS = st.slider("Horse Power ", min_value=14, max_value=999, value=60, step=5)
            Age = st.slider("Vehicle Age ", min_value=1, max_value=29, value = 5)
            Driven_KM_Per_Year = st.slider("Per Year KM ", min_value=0, max_value= 100000, step=1000, value = 10000)
            Km_per_liter = st.slider("KM per Liter", min_value=1, max_value= 100, value = 15)


        new_data = pd.DataFrame({
        'brand': Brand,
        'model': Model,
        'power_ps': PS,
        'transmission_type': Transmission,
        'fuel_type': Fuel,
        'age': Age,
        'mile_per_year': Driven_KM_Per_Year,
        'per_liter_km': [Km_per_liter]
    })
    predict = st.button("Predict Price")
    st.divider
    try:
        if predict:
            with st.spinner("Prediction in progress..."):
                col1, col2 = st.columns((1,1))
                with col1:
                    # Predicting the price of the new car entry
                    predicted_price = predictive_model(LinearRegression,new_data)
                    st.metric("#### :blue[The Linear model Predicted Price is:] ", f" {predicted_price[0]:.2f} Euro")
                    st.snow()
                with col2:
                    # Predicting the price of the new car entry
                    predicted_price = predictive_model(XGBRegressor,new_data)
                    st.metric("#### :green[The Tree Model Predicted Price is:] ", f" {predicted_price[0]:.2f} Euro")
                    st.snow()
    except ValueError:
        st.error("something went wrong. Please check your input.")

        
        




def app():
    input_data()
