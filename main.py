import streamlit 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import time


streamlit.title("Simple Data Dashboard")

uploaded_file = streamlit.file_uploader("Choose your file to be uploaded" , type="CSV")


# Function to load data without caching
def load_data(file, progress_callback=None):
    # Simulate loading process with updates
    if progress_callback:
        for i in range(10):
            time.sleep(0.01)  # Simulate time-consuming task
            progress_callback((i + 1) * 10)  # Update progress to (i+1)*10%
    
    # Read the CSV file
    df = pd.read_csv(file)
    return df

@streamlit.cache_data
def get_unique_values(df, column):
    return df[column].unique()


def save_to_pdf(df, filtered_df):
    pass

if uploaded_file is not None:
    streamlit.write("File uploaded..........")

    # Progress bar
    progress_bar = streamlit.progress(0)
    
    # Load the data without caching
    df = load_data(uploaded_file, progress_callback=progress_bar.progress)
    
    # Update progress bar after loading data
    progress_bar.progress(0)
    
    
    # Exporting reports generated
    left_column , right_column = streamlit.columns(2)
    with left_column:    
        if streamlit.button('Export to PDF'):
            #save_to_pdf(df, filtered_df)
            streamlit.write("Exported to PDF")
    with right_column:
        if streamlit.button('Export to Excel'):
            #save_to_pdf(df, filtered_df)
            streamlit.write("Exported to Excel")
    
    streamlit.subheader("Data Preview: ")
    streamlit.write(df.head())
    
    
    # NULL and Duplicate values 
    left_column , right_column = streamlit.columns(2)
    with left_column:
        streamlit.subheader("Null Values: ")
        streamlit.write(df.isna().sum())
        
    with right_column:
        streamlit.subheader("Duplicate Values: ")
        streamlit.write(df.duplicated().sum())
    
    streamlit.subheader("Data Summary")
    streamlit.write(df.describe())
    
    
    
    # Filtering Data
    streamlit.subheader("Filter data")
    columns =  df.columns.tolist()
    selected_column = streamlit.selectbox("Select columns to filter by: ", columns)
    
    unique_values = get_unique_values(df, selected_column)
    selected_values = streamlit.selectbox("Select value: ", unique_values)
    
    filtered_df = df[df[selected_column] == selected_values]
    streamlit.write(filtered_df)
    
    
    
    
    # Plotting Data
    streamlit.subheader("Plot data")
    x_column = streamlit.selectbox("Select a x_value :", columns)
    y_column = streamlit.selectbox("Select a y_value :", columns)
    
    
    
    # Adjustting plotting 
    left_column, middle_column , right_column = streamlit.columns(3)
        
    with left_column:
        if streamlit.button("Generate Plot"):
            streamlit.subheader("Line Chart")
            streamlit.line_chart(filtered_df.set_index(x_column)[y_column])
    
    with right_column:
        if streamlit.button("Generate Scatter Plot"):
            streamlit.subheader("Scatter Plot")
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x_column], df[y_column])
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            streamlit.pyplot(plt)
        

    
else:
    streamlit.write("Waiting for a file upload........ ")
    
    