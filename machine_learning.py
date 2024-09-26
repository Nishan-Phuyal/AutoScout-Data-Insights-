import pandas as pd 
import plotly.express as px 
import streamlit as st


def visualize_error(results, title_x = 0.2):
    """Function to visualize the prediction error by brand using a violin plot."""
    
    fig = px.violin(results, x="brand", y="error", color="brand", hover_data=results.columns)
    fig.update_layout(
        title=dict(text="Prediction Errors", font=dict(size=25)),
        title_x=title_x,
        xaxis_title="Brand",
        yaxis_title="Prediction Error",
        paper_bgcolor='rgba(0,0,0,0)',  # Makes the background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Makes the plot area background transparent
        font=dict(color='white'),
        xaxis=dict(tickmode='linear')
    )
    st.plotly_chart(fig)


def visualize_metrics(MAE : float, Rsquared:float,Hyperparameter:any):
    col1, col2, col3 = st.columns((1,1,1), vertical_alignment="top")
    with col1:
        st.metric("MAE", value= MAE)
    with col2:
        st.metric("R-Squared", value= Rsquared)
    with col3:
        st.metric("Alpha", value= Hyperparameter)


def linear_regression():
    with st.expander("##### Linear Regression"):
            st.markdown("This model takes all the categorical variables as dummies and predicts the price of a car using simple OLS (Ordinary Least Squares).")
    results = pd.read_csv("LinearRegression_results.csv")  # Load the results of Linear Regression
    visualize_metrics(4682.88, 73.91, "None")
    visualize_error(results)

def ridgeCV():
    with st.expander("##### Ridge Regression (L2 Regularization)"):
        st.markdown("""In Ridge Regression, an additional penalty term is added to the loss function along with the squared error. 
                    This penalizes the size of coefficients, shrinking those of less significant features.""")
    
    results = pd.read_csv("RidgeCV_results.csv")  # Load the results of Ridge Regression
    visualize_metrics(4697.77, 69.90, 1.0)
    visualize_error(results)


def lassoCV(): 
        with st.expander("##### Lasso Regression"):
            st.write("""Like Ridge, Lasso penalizes insignificant features. Unlike Ridge, where coefficients asymptotically approach zero for large alphas, 
                     Lasso sets some coefficients exactly to zero, effectively performing feature selection.""")
        results = pd.read_csv("LassoCV_results.csv")  # Load the results of Lasso Regression
        visualize_metrics(6531.75, 20.77, 61.43)
        visualize_error(results)



def elasticCV():
        with st.expander("##### ElasticNet Regression"):
            st.markdown("ElasticNet combines both Lasso (L1) and Ridge (L2) penalties, balancing the strengths of both methods for better generalization.")
        
        results = pd.read_csv("ElasticNetCV_results.csv")  # Load the results of ElasticNet Regression

        col1, col2, col3, col4 = st.columns((1,1,1,1), vertical_alignment="top")
        with col1:
            st.metric("MAE", value= 14090.80)
        with col2:
            st.metric("R-Squared", value= 4.41)
        with col3:
            st.metric("Alpha", value= 41.55)
        with col4:
            st.metric("L1 Ratio", value= 0.5)

        visualize_error(results)


def Tree_model(): 
    with st.expander("##### Extreme Gradient Boosting (XGBoost)"):
        st.markdown("""XGBoost is an advanced implementation of Gradient Boosting that is highly efficient and optimized for speed and performance. 
                    It is more efficient than the Gradient Boosting Regressors available in scikit-learn due to features like regularization and tree pruning.
                    XGBoost is an ensemble learning technique where each new decision tree is trained to correct the residual errors of the previous trees. 
                    These models from residuals are scaled by a learning rate to prevent overfitting. The final prediction is the sum of all individual tree predictions, making it a robust ensemble learning method.""")

    results = pd.read_csv("XGBRegressor_results.csv")  # Load the results of ElasticNet Regression
    mse, r2, alpha, n_estimator, depth = st.columns((1,1,1,1,1))  # Create columns to display MSE, R-squared, Alpha, and L1 Ratio
    
    with mse:
        st.metric("MAE",3871.58 )
    with r2:
        st.metric("R-squared", 72.04)
    with alpha:
        st.metric("Alpha: ", value=0.1)  # default alpha, Iterative search for optimal alpha is possible but computationally intesive. 
    with n_estimator:
        st.metric("Tree: ", value=100)  # Display the Default Trees 
    with depth:
        st.metric("Depth", value= 6) # Display the default Depth

    visualize_error(results,0.35)  # Visualize the prediction error by brand



def app():
    st.header("Linear Models")
    col1, col2 = st.columns((1,1))
    with col1:
        linear_regression()
    with col2: 
        ridgeCV()
    col3, col4 = st.columns((1,1))
    with col3:
         lassoCV()
    with col4:
         elasticCV()
    st.divider()
    st.header("Tree Models")
    Tree_model()
         
    
