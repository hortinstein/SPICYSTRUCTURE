import pandas as pd
import plotly.express as px
import streamlit as st
import reverse_geocode

from dotenv import load_dotenv
import os
import requests

def groq_inference():
    load_dotenv()
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

    # The API URL
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Headers including the Authorization and Content-Type
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # The data payload
    data = {
        "messages": [{"role": "user", "content": "Explain the importance of low latency LLMs"}],
        "model": "mixtral-8x7b-32768"
    }

    # Making the POST request
    response = requests.post(url, json=data, headers=headers)

    # Printing the response
    print(response.text)


# Streamlit app title
st.title("List Sum Comparison")

# Input fields for the lists
list1 = st.text_input("Enter the first list of numbers, separated by commas:", "1,2,3")
list2 = st.text_input("Enter the second list of numbers, separated by commas:", "4,5,6")

# Convert input string to lists of integers
list1 = [int(x.strip()) for x in list1.split(',')]
list2 = [int(x.strip()) for x in list2.split(',')]

# Calculate sums
sum1 = sum(list1)
sum2 = sum(list2)

# Prepare data for display
data = {
    "List 1": [[list1],[list1]],
    "List 2": [[list2],[list2]],
    "Sum of List 1": [[sum1],[sum1]],
    "Sum of List 2": [[sum2],[sum2]],
    "Equal Sums?": [["✅" if sum1 == sum2 else "❌"],["✅" if sum1 == sum2 else "❌"]]
}

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
st.table(df)
