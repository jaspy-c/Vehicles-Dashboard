import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def load_data(data):
  return pd.read_csv(data)

def main():
  st.header("Vehicles Data Dashboard")
  
  df = load_data("vehicles_us.csv")
  
  df['brand'] = df['model'].str.split().str[0]
  df_counts = df['brand'].value_counts().reset_index()
  df = pd.merge(df, df_counts, left_on='brand', right_on='index', suffixes=('', '_counts'))
  df = df.drop('index', axis=1)

  condition_order = ['new', 'like new', 'excellent', 'good', 'fair', 'salvage']
  df['condition'] = pd.Categorical(df['condition'], categories=condition_order, ordered=True)
  df = df.sort_values('condition')

  brand_list = df['brand'].unique().tolist()
  selected_brand = st.selectbox('Select Brand to view Data', brand_list)
  with st.expander("Data View", expanded=True):
    df_specific = df[df['brand'] == selected_brand]
    st.dataframe(df_specific)
  
  brand_counts = df.groupby(['brand', 'condition']).size().reset_index(name='count')
  
  fig = px.bar(brand_counts, x='brand', y='count', color='condition', title='Total Count by Brand and Condition')
  fig.update_layout(xaxis_categoryorder='total descending')
  st.plotly_chart(fig)

  brand_price = df.groupby(['brand', 'condition']).agg({"price":"mean"}).reset_index()

  fig = px.bar(brand_price, x='brand', y='price', color='condition', title='Average Price by Brand and Condition')
  fig.update_layout(xaxis_categoryorder='total descending')
  st.plotly_chart(fig)
  
  
  normalize_checkbox = st.checkbox('Normalize Histogram', False)
  year_condition = df.groupby(['model_year', 'condition']).size().reset_index(name='count')
  if normalize_checkbox:
    hist_fig = px.histogram(year_condition, x='model_year', y='count', nbins=100, color='condition', histnorm='probability', title='Number of Vehicles by Model Year and Condition (Normalized)')
  else:
    hist_fig = px.histogram(year_condition, x='model_year', y='count', nbins=100, color='condition', title='Number of Vehicles by Model Year and Condition (Non-Normalized)')
  
  st.plotly_chart(hist_fig)

  
  st.markdown('Average Price Comparison between Two Brands By Condition')
  
  brand_list = df['brand'].unique().tolist()
  selected_brand1 = st.selectbox('Select Brand 1 (Blue)', brand_list)
  selected_brand2 = st.selectbox('Select Brand 2 (Red)', brand_list)
  df_brand1 = df[df['brand'] == selected_brand1]
  df_brand2 = df[df['brand'] == selected_brand2]
   
    
  df_brand1 = df_brand1.groupby('condition').agg({"price":"mean"}).reset_index()
  df_brand2 = df_brand2.groupby('condition').agg({"price":"mean"}).reset_index()
  

  fig1 = px.bar(df_brand1, x='condition', y='price')
  fig2 = px.bar(df_brand2, x='condition', y='price', color_discrete_sequence=['red'])

  # Combine the plots using go.Figure
  combined_fig = go.Figure()

  # Add traces from the first plot
  for trace in fig1['data']:
      combined_fig.add_trace(trace)

  # Add traces from the second plot
  for trace in fig2['data']:
      combined_fig.add_trace(trace)

  # Set x and y axis labels
  combined_fig.update_layout(
    xaxis_title='Condition',
    yaxis_title='Average Price'
  )
  # Display the combined plot
  st.plotly_chart(combined_fig)

  fig = px.scatter(df, x='model_year', y='odometer', color='condition', title='Odometer by Model Year and Condition')
  st.plotly_chart(fig)
  

if __name__ == "__main__":
  main()