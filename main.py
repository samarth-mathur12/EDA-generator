import streamlit 
import pandas as pd
import matplotlib.pyplot as plt

streamlit.title("Simple Data Dashboard")

uploaded_file = streamlit.file_uploader("Choose your file to be uploaded" , type="CSV")


if uploaded_file is not None:
    streamlit.write("File uploaded..........")
    df = pd.read_csv(uploaded_file)
    
    streamlit.subheader("Data Preview: ")
    streamlit.write(df.head())
    
    streamlit.subheader("Data Summary")
    streamlit.write(df.describe())
    
    streamlit.subheader("Filter data")
    columns =  df.columns.tolist()
    selected_column = streamlit.selectbox("Select columns to filter by: ", columns)
    unique_values =  df[selected_column].unique()
    selected_values = streamlit.selectbox("Select value: ", unique_values)
    
    filtered_df = df[df[selected_column] == selected_values]
    streamlit.write(filtered_df)
    
    streamlit.subheader("Plot data")
    x_column = streamlit.selectbox("Select a x_value :", columns)
    y_column = streamlit.selectbox("Select a y_value :", columns)
    
    if streamlit.button("Generate Plot"):
        streamlit.line_chart(filtered_df.set_index(x_column)[y_column])


else:
    streamlit.write("Waiting for a file upload........ ")
    
    