import streamlit 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import time
from fpdf import FPDF



streamlit.title("Simple Data Dashboard")

uploaded_file = streamlit.file_uploader("Choose your file to be uploaded" , type="CSV")


# Function to load data without caching
def load_data(file ):  
    # Read the CSV file
    df = pd.read_csv(file)
    return df

@streamlit.cache_data
def get_unique_values(df, column):
    return df[column].unique()


def save_to_pdf(df, filtered_df, x_column, y_column):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    #title
    pdf.cell(200, 10, txt="EDA Report", ln=True, align="C")
    
    # Data Preview
    pdf.ln(10)
    pdf.cell(200,10, txt="Data Preview",ln=True, align="L")
    for i in range(min(len(df), 5)):
        pdf.cell(200,10, txt=str(df.iloc[i].to_dict()), ln=True, align="L")
        
    #NULL Values
    pdf.ln(10)
    pdf.cell(200, 10, txt="NULL Values", ln=True, align="L")
    null_values  = df.isna().sum().to_dict()
    for k, v in null_values.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True, align="L")
    
    # Duplicate Values
    pdf.ln(10)
    pdf.cell(200, 10, txt="Duplicate Values", ln=True, align="L")
    pdf.cell(200, 10, txt=str(df.duplicated().sum()), ln=True, align="L")
    
    # Data Summary
    pdf.ln(10)
    pdf.cell(200, 10, txt="Data Summary", ln=True, align="L")
    summary = df.describe().to_dict()
    for k, v in summary.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True, align="L")
        
    #Save plot as an image and add to PDF
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_df[x_column], filtered_df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title("Scatter Plot")
    plt.savefig("plot.png")
    pdf.ln(10)
    pdf.image("plot.png", x=10, y=None, w=100)

    # Save the PDF
    pdf.output("EDA_Report.pdf")
    
if uploaded_file is not None:
    streamlit.write("File uploaded..........")
    
    # Load the data without caching
    df = load_data(uploaded_file)

   
    # Exporting reports generated
    left_column , right_column = streamlit.columns(2)
    with left_column:    
        if streamlit.button('Export to PDF'):
            save_to_pdf(df, df, x_column, y_column)
            streamlit.write("Exported to PDF")
            with open("EDA_Report.pdf", "rb") as file:
                streamlit.download_button("Download PDF", file, file_name="EDA_Report.pdf")
    
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
    
    