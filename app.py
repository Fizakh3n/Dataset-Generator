import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()

# Define categories and their default columns
categories = {
    "Sales": ["Customer Name", "Email", "Purchase Amount", "Purchase Date"],
    "Healthcare": ["Patient Name", "Age", "Diagnosis", "Medication"],
    "Finance": ["Account Holder", "Account Number", "Balance", "Transaction Date"],
    "E-commerce": ["Order ID", "Product Name", "Price", "Shipping Address"]
}

# Define data type options
data_types = {
    "Name": fake.name,
    "Email": fake.email,
    "Phone": fake.phone_number,
    "Date": fake.date_this_decade,
    "Address": fake.address,
    "Number": lambda: round(np.random.uniform(10, 500), 2)
}

# Set the page configuration
st.set_page_config(page_title="AI-Powered Dataset Generator", layout="wide")

# Title
st.title("AI-Powered Dataset Generator")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
category = st.sidebar.selectbox("Select a category:", list(categories.keys()))
num_rows = st.sidebar.number_input("Enter number of rows:", min_value=10, max_value=10000, step=10)

# Customize Column Names & Types
st.sidebar.subheader("Customize Columns")
columns = categories[category]
user_columns = []

for col in columns:
    col_name = st.sidebar.text_input(f"Rename '{col}' column:", col)
    col_type = st.sidebar.selectbox(f"Select data type for {col_name}:", list(data_types.keys()), key=col)
    user_columns.append((col_name, col_type))

# Generate Data button
if st.sidebar.button("Generate Dataset"):
    data = {col_name: [data_types[col_type]() for _ in range(num_rows)] for col_name, col_type in user_columns}
    df = pd.DataFrame(data)

    # Display the generated dataset
    st.subheader("Generated Dataset Preview")
    st.dataframe(df)

    # Quick Summary Stats
    st.subheader("Quick Summary Stats")
    st.write("### Descriptive Statistics")
    st.write(df.describe())

    st.write("### Missing Values")
    st.write(df.isnull().sum())

    st.write("### Data Types")
    st.write(df.dtypes)

    # Download button
    csv = df.to_csv(index=False).encode()
    st.download_button(label="Download CSV", data=csv, file_name="generated_dataset.csv", mime="text/csv")

# Add footer for additional info
st.sidebar.markdown("---")
st.sidebar.info("This tool generates realistic fake datasets for various domains. Customize to fit your needs!")



