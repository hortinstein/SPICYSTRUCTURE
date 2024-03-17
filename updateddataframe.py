import streamlit as st
import time
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Function to simulate the work being done in the background
def do_work(argument):
    time.sleep(argument)
    update_table()
    # Here, ensure that `start_time` is accessed safely
    return time.time() - st.session_state.get('start_time', time.time())

# Function to update the table with the latest results
def update_table():
    with st.spinner("Waiting for results..."):
        # Check if the DataFrame is in the session state, otherwise initialize it
        if 'results_df' not in st.session_state:
            st.session_state.results_df = pd.DataFrame(columns=["Argument", "Status", "Result"])
        
        futures = st.session_state.get('futures', [])
        arguments = st.session_state.get('arguments', [])
        
        # Update DataFrame with the latest results
        for i, future in enumerate(futures):
            if future.done():
                result = future.result()
                st.session_state.results_df.loc[i] = [arguments[i], "Complete", result]
            else:
                # Only update the status if the future is not yet complete to avoid overwriting results
                if i >= len(st.session_state.results_df) or st.session_state.results_df.loc[i, "Status"] != "Complete":
                    st.session_state.results_df.loc[i] = [arguments[i], "Waiting", "-"]
        
        # Display the table using the DataFrame
        st.table(st.session_state.results_df)

# Main function to run the Streamlit app
def main():
    # Set Streamlit app title
    st.title("Background Work")
    # Get user input for number of functions and sleep time
    num_functions = st.number_input("Number of Functions", min_value=1, max_value=10, value=3)
    sleep_time = st.number_input("Sleep Time (seconds)", min_value=1, max_value=10, value=3)
    
    # Initialize session_state variables with default values if not present
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    if 'arguments' not in st.session_state:
        st.session_state.arguments = []
    if 'futures' not in st.session_state:
        st.session_state.futures = []
    
    # Start button to initiate the background work
    if st.button("Start"):
        st.session_state.start_time = time.time()
        st.session_state.arguments = [random.randint(1, sleep_time) for _ in range(num_functions)]
        st.session_state.futures = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            for argument in st.session_state.arguments:
                future = executor.submit(do_work, argument)
                st.session_state.futures.append(future)
        update_table()
    
    # Update button to manually refresh the table
    if st.button("Update"):
        update_table()

# Run the Streamlit app
if __name__ == "__main__":
    main()
