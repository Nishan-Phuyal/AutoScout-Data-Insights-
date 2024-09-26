import pandas as pd 
import plotly.express as px 
import streamlit as st
import numpy as np

# import the data globally... 

data = pd.read_csv("clean_data.csv")
    

                                                    ################# Start of Basic-Visualization #####################

def market_overview_simple():
    df = data
    with st.expander(" 2023 Market Overview: Snapshot of Autoscout Trends and Insights"):
        st.write("""This section of the visualization provides a comprehensive overview of the data, 
                 offering a snapshot of the Autoscout market. It is designed for viewers who seek a brief yet current understanding of market trends and key insights.""")
    year_range = st.slider("#### Display the results by the range of Production Year.", min_value= 1995, max_value=2023, value=[1995,2023])

    # visualizing the qualitative, heatmap and quantitative metrics

    qualitative, heatmap, quantitative = st.columns((1,5,1))

    with qualitative:
        st.metric("##### :blue[Vehicle Brands]", value= df[df["year"].isin(range(year_range[0],year_range[1]+1))]["brand"].nunique())
        st.divider()
        st.metric("##### :blue[Distinct Models] ", value= df[df["year"].isin(range(year_range[0],year_range[1]+1))]["model"].nunique())
        st.divider()
        st.metric("##### :blue[Distinct Powertrain Type] ", value= df[df["year"].isin(range(year_range[0],year_range[1]+1))]["fuel_type"].nunique())
        st.divider()
    
    with heatmap: 
        # the heatmap showcases the vehicle placed on Autoscout in 2023 grouped by their production year and Brand
        # Insight : which brand produces the vehicle that last longer.

        count_data = df.groupby(["year", "brand"]).size().reset_index(name ="count")

        # create a Pivot Table: (easier way to visualize the heatmap, where we consider the brad as our pivot index and year as our columns, and the cells are populated by the counts of each brand produced in given year.)
        pivot_table = count_data.pivot(index= "year", columns= "brand", values="count")

        brand_total = pivot_table.sum(axis = 0).sort_values(ascending = False) # Count the total number of occurrences of each branch in the entire data set.

        pivot_table = pivot_table[brand_total.index] # Reorder the pivot table according to the index of brand_total, i.e. the brands that occur most frequently are displayed first.

        pivot_table = pivot_table[abs(1995-year_range[0]):abs((year_range[1]+1)-1995)] # passing the slider parameters to subsample the pivot accordingly.

        # creating the heatmap using plotly.express 

        fig = px.imshow(pivot_table, 
                        labels=dict(x = "Brand", y = "year", color = "Count"),
                        x = pivot_table.columns,
                        y = pivot_table.index,
                        text_auto=True,
                        aspect="auto",
                        color_continuous_scale="rainbow",
                        title="2023 Autoscout Marketplace: Cars Listed by Brand and Production Year")
        
        fig.update_layout(
            title_x = 0.2,
            xaxis_title='Brand',
            yaxis_title='Year',
            xaxis=dict(tickmode='linear'),
            yaxis=dict(tickmode='linear'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#14213d')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#14213d')
        
        st.plotly_chart(fig)

    with quantitative:
        price = df[df["year"].isin(range(year_range[0],year_range[1]+1))]["price_in_euro"].mean().__round__()
    
        price_std = df[df["year"].isin(range(year_range[0],year_range[1]+1))]["price_in_euro"].std().__round__()

        fuel = df[df["year"].isin(range(year_range[0],year_range[1]+1))]["fuel_consumption_l_100km"].mean().__round__()

        fuel_std = df[df["year"].isin(range(year_range[0],year_range[1]+1))]["fuel_consumption_l_100km"].std().__round__()

        power = df[df["year"].isin(range(year_range[0],year_range[1]+1))]["power_ps"].mean().__round__()

        power_std = df[df["year"].isin(range(year_range[0],year_range[1]+1))]["power_ps"].std().__round__()

        st.metric("##### :blue[Ø Price] ", value= f"{price} €", delta=f"Spread = {price_std} €")
        st.divider()
        st.metric("##### :blue[:fuelpump: Ø Energy Efficiency]", value= f"{fuel} ltr / 100KM", delta=f" Spread = {fuel_std}")
        st.divider()
        st.metric("##### :blue[Ø Horse Power] ", value= f"{power}", delta=f" Spread = {power_std}")
        st.divider()


                                                        ################# End of Basic-Visualization #####################

"""-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
                                                        
                                                        ################# Start if Interactive-Visualization #####################


def interactive_autoscout():
    st.divider()
    with  st.expander("### Analyzing Price Distribution: Customizable Brand and Model Insights"):
        st.write("""The price distribution graph allows users to explore and compare vehicle pricing patterns by selecting specific brands and models. 
                 It offers flexibility to analyze one brand in detail or compare multiple brands to identify pricing trends and variations.
                  Users can focus on individual models for in-depth analysis or include all models to gain a comprehensive market view. 
                 This interactive tool provides tailored insights into automotive pricing, helping users easily visualize and understand market dynamics.""")
    # import the data locally
    df = data 
    
    select_box_1, select_box_2 = st.columns((1,0.3))

    with select_box_1:
        with st.popover("Select Brands"):
            selected_brand = st.multiselect("select", options= df.brand.unique().tolist(), default="rover", placeholder="SELECT BRAND/S")
            df = df[df["brand"].isin(selected_brand)]
    with select_box_2:
        with st.popover("Select Models"):
            selected_model = st.multiselect("select model", options= df.model.unique().tolist(), default=df.model.unique().tolist()) 
            df = df[df["model"].isin(selected_model)]

    price, Vehicles_Count = st.columns((1,1))


    with price:
        # visualizing price
        fig = px.histogram(df, x = "price_in_euro", hover_data=df.columns, marginal = "violin", color=("brand" if len(selected_brand)>=2 else "model")) # histogram hue is defined by model if one brand is selected. for multiple brands hue is model.

        fig.update_layout(title=dict(text = "Price Distribution", font = dict(size = 25)),
                            title_x = 0.35,
                            barmode = "stack",
                            xaxis_title = "Price in €",
                            yaxis_title = "Number of Vehicles",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'))
        st.plotly_chart(fig)


    with Vehicles_Count :
        # visualizing Vehicles Count by Production Year
        Vehicles_Count_by_Production_Year = df.groupby(["model", "year"])["model"].count().reset_index(name = "count")
        fig2 = px.bar(Vehicles_Count_by_Production_Year, x = "year", y = "count", color= "model")
        fig2.update_layout(title=dict(text = "Vehicles Count by Production Year ", font = dict(size = 25)),
                            title_x = 0.3,
                            barmode = "group",
                            xaxis_title = "Production Year",
                            yaxis_title = "Vehicles Count",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
            xaxis=dict(tickmode='linear'))
        
        st.plotly_chart(fig2)



    Average_price, Average_Miles = st.columns((1,1))
    with Average_price:
        Average_Vehicles_price_by_production_year= df.groupby(["model", "year"])[["mileage_in_km","price_in_euro"]].mean().reset_index()
        fig3 = px.bar(Average_Vehicles_price_by_production_year, x = "year", y = "price_in_euro", color= "model", barmode = "group")
        fig3.update_layout(title=dict(text = "Average Vehicles price by production year", font = dict(size = 25)),
                            title_x = 0.2,
                            barmode = "group",
                            xaxis_title = "Production Year",
                            yaxis_title = "Avg. Price",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
            xaxis=dict(tickmode='linear'))
        st.plotly_chart(fig3)
        
    with Average_Miles:
        verage_Miles_on_Vehicles_by_production_year = df.groupby(["model", "year"])[["mileage_in_km","price_in_euro"]].mean().reset_index()
        fig4 = px.bar(verage_Miles_on_Vehicles_by_production_year, x = "year", y = "mileage_in_km", color= "model", barmode="group")
        fig4.update_layout(title=dict(text = "Average Miles on Vehicles by production year", font = dict(size = 25)),
                            title_x = 0.2,
                            barmode = "group",
                            xaxis_title = "Production Year",
                            yaxis_title = "Avg Miles",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
            xaxis=dict(tickmode='linear'))
        st.plotly_chart(fig4)

                                                ################# end of Interactive-Visualization #####################

"""-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
                                                        
                                                        

                                                ################# start of relational-Visualization #####################


def scat():
    df = data 
    df_quantitative = df[[ 'price_in_euro', 'power_ps', 'fuel_consumption_l_100km',
       'mileage_in_km']]
    df_qualitative = df[[ 'brand', 'model', 'year',
       'transmission_type', 'fuel_type']]

    with st.form("Create Scatter"):
        with st.popover("Create Scattter"):
            x_selected = st.selectbox("", df_quantitative.columns, index = None, placeholder="Select feture for x axis "  )
            y_selected = st.selectbox("", df_quantitative.columns, index = None, placeholder="Select feture for y axis"  )
            z_selected = st.selectbox("", df_qualitative.columns, index = None, placeholder="Select distintive fetures" )
            line = st.selectbox("", ["True", "False"], index = None, placeholder="Show Trendline" )
            st.form_submit_button("Plot Scatter")
        
    
    
    if x_selected and y_selected:
        fig = px.scatter(
            df, 
            x=x_selected, 
            y=y_selected, 
            color=z_selected, 
            template='plotly_dark', 
            hover_data=df.columns,
            trendline="ols" if line == "True" else None,
            

        )
        fig.update_layout(title = dict(text = f"Scatterplot {x_selected} and {y_selected}", font = dict(size = 23))
                          , title_x = 0.35)
        st.plotly_chart(fig)
    else:
        st.warning("Please select both X and Y columns to create a scatterplot")
        
        
           
    

                                          ################# start of relational-Visualization #####################





def app():
    market_overview_simple()
    interactive_autoscout()
    scat()