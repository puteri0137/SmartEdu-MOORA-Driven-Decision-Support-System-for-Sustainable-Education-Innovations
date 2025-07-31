
import subprocess
import sys

# Function to install openpyxl if not already installed
def install_openpyxl():
    try:
        import openpyxl
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        print("openpyxl has been installed successfully.")
    else:
        print("openpyxl is already installed.")

# Call the function to check and install openpyxl
install_openpyxl()

# Now you can safely import pandas and openpyxl
import streamlit as st
import pandas as pd
import numpy as np

# Function to perform MOORA ranking
def moora(data, weights):
    # Normalize the data (min-max normalization)
    normalized_data = data.apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    # Multiply by weights
    weighted_data = normalized_data * weights

    # Calculate the MOORA Ratio (sum of weighted normalized values)
    moora_score = weighted_data.sum(axis=1)

    # Ranking based on the highest MOORA score
    data['MOORA Score'] = moora_score
    data['Rank'] = data['MOORA Score'].rank(ascending=False)

    return data

# Streamlit app UI
st.title("EduRank: A MOORA-based Big Data System for Evaluating Educational Technologies")

st.write("""
This application allows you to evaluate and rank different educational technologies using the MOORA method.
You will upload an Excel file containing the data for various educational tools and their criteria, and the system will calculate the ranks based on a multi-criteria decision-making process.
""")

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        # Read the uploaded file into a pandas DataFrame
        df = pd.read_excel(uploaded_file)

        # Show the uploaded data
        st.write("### Input Data from Excel")
        st.write(df)

        # Ensure the required columns are present
        required_columns = ['Technology', 'Cost', 'Ease of Use', 'Effectiveness', 'Accessibility', 'Innovation']

        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            st.write(f"### Error: The Excel file is missing the following columns: {', '.join(missing_cols)}")
        else:
            # Weighting for each criteria (can be adjusted by the user)
            weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])  # Sum of weights should equal 1

            # Apply MOORA method to rank the technologies
            ranked_data = moora(df[required_columns[1:]], weights)

            st.write("### Ranking Based on MOORA Method")
            st.write(ranked_data[['Technology', 'MOORA Score', 'Rank']])

    except Exception as e:
        st.write(f"### Error: An issue occurred while reading the Excel file. Please check the format. Error: {str(e)}")
