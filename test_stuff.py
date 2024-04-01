import streamlit as st
import pandas as pd
import os

# Path to save the DataFrame CSV
csv_file_path = 'data.csv'

# Load or create the DataFrame
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
else:
    # Sample DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Status': ['Single', 'Married', 'Single']
    }
    df = pd.DataFrame(data)

# Function to update the DataFrame and save to CSV
def update_df(updated_row, index=None):
    if index is not None:
        df.loc[index] = updated_row
    else:  # For adding a new row
        df.loc[len(df)] = updated_row
    df.to_csv(csv_file_path, index=False)

# Automatically load row data for editing
def load_row_data(index):
    for col in df.columns:
        st.session_state[col] = df.loc[index, col]

# Expander for editing or adding rows
with st.expander("Edit or Add Row"):
    edit_or_add = st.radio("Edit or Add:", ["Edit", "Add"], on_change=load_row_data, args=([0] if df.shape[0] > 0 else [None]))  # Load first row by default if adding is not selected

    if edit_or_add == "Edit":
        row_to_edit = st.selectbox("Select a row to edit", range(len(df)), format_func=lambda x: f"Row {x+1}", on_change=load_row_data, args=(st.session_state.get('row_to_edit', 0),))
        st.session_state['row_to_edit'] = row_to_edit  # Store the selected row index for potential use in callbacks or elsewhere

    # Inputs for data
    new_data = {}
    for col in df.columns:
        if col == 'Status':
            new_data[col] = st.selectbox(f"{col}", ['Single', 'Married', 'Divorced', 'Widowed'], index=0 if edit_or_add == "Add" else ['Single', 'Married', 'Divorced', 'Widowed'].index(st.session_state.get(col, 'Single')))
        else:
            new_data[col] = st.text_input(f"{col}", value=st.session_state.get(col, ""))

    if st.button('Update/Add Row'):
        if edit_or_add == "Edit":
            update_df(new_data, row_to_edit)
            st.success("Row updated successfully!")
        else:  # Adding a new row
            update_df(new_data)
            st.success("Row added successfully!")

# Display the DataFrame
st.write("DataFrame:")
st.dataframe(df)
