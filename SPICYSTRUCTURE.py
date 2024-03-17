import pandas as pd
import streamlit as st
import json
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

#reads json string into a dictionary
def json_string_to_dict(json_string):
    return json.loads(json_string)

tests =  [
    {
        "irregular_data": "5 birds, three cats, 2 dogs",
        "expected_data":{
            "birds": 5,
            "cats": 3,
            "dogs": 2
        } 
    },
    {
        "irregular_data": "2xbirds, 4xcats, 1xdog",
        "expected_data":{
            "birds": 2,
            "cats": 4,
            "dogs": 1
        } 
    },
    {
        "irregular_data": "1 bird 1 cat 1 dog",
        "expected_data":{
            "birds": 1,
            "cats": 1,
            "dogs": 1
        } 
    },
      {
        "irregular_data": "3 fish, 2 hamsters, 5 parrots",
        "expected_data": {
            "fish": 3,
            "hamsters": 2,
            "parrots": 5
        }
    },
    {
        "irregular_data": "6xrabbits, 3xturtles, 2xguinea pigs",
        "expected_data": {
            "rabbits": 6,
            "turtles": 3,
            "guinea pigs": 2
        }
    },
    {
        "irregular_data": "4 mice, 7 snakes",
        "expected_data": {
            "mice": 4,
            "snakes": 7
        }
    },
    {
        "irregular_data": "1xowl, 2xfrogs, 4xlizards",
        "expected_data": {
            "owl": 1,
            "frogs": 2,
            "lizards": 4
        }
    },
    {
        "irregular_data": "5 cows, two pigs, 3 goats",
        "expected_data": {
            "cows": 5,
            "pigs": 2,
            "goats": 3
        }
    },
    {
        "irregular_data": "2sheep, 4chickens, 3ducks",
        "expected_data": {
            "sheep": 2,
            "chickens": 4,
            "ducks": 3
        }
    },
    {
        "irregular_data": "10 fish, 20 birds",
        "expected_data": {
            "fish": 10,
            "birds": 20
        }
    },
    {
        "irregular_data": "4zebras, 2000giraffes",
        "expected_data": {
            "zebras": 4,
            "giraffes": 20000
        }
    }
]

system_prompt = """
You work for SpicyStructure! you help structure data.
Please provide me with the data you'd like to structure.  You should only return valid json and nothing else with now tabs or line breaks!
"""

content_prompt = """
Please take the data below and structure it into JSON
"5 birds, three turtles, 2 dogs" would be: 
{
    "birds": 5,
    "turtles": 3,
    "dogs": 1
}
return only the JSON! here is the data:
"""


def groq_inference(system_prompt: str, 
                   content_prompt: str,
                   temperature = 0,
                   model: str = "mixtral-8x7b-32768"):
    

    # The API URL
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Headers including the Authorization and Content-Type
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # The data payload
    data = {
        "messages": [
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": content_prompt
            },
        ],
        "model": model
    }

    # Making the POST request
    response = requests.post(url, json=data, headers=headers)
    json_response = response.json()
    
    # Printing the response
    return(json_response["choices"][0]['message']['content'])
    # return response.text.chocies[0].content

# Streamlit app title
st.title("🌶️SPICYSTRUCTURE🚧")

# Slider input for temperature
spice_level = st.slider("Select 🌶️ level (0-2.0)", 0.0, 2.0, 0.0)
placeholder = st.empty()

if st.button("Start"):
    # Initialize an empty DataFrame to store results
    # Now including "Return" and "Passing" columns initialized as blank
    results_df = pd.DataFrame(columns=["Irregular Data", "Expected","Return", "Passing"])

    for test in tests:
         # Create an empty list to store the results
        # Get the irregular data from the test
        irregular_data = test["irregular_data"]
        
        # Use the groq_inference function to structure the data
        structured_data = groq_inference(system_prompt, content_prompt+irregular_data, temperature=spice_level)
        
        print(json.dumps(test["expected_data"]))

        new_row = {
            "Irregular Data": irregular_data,
            "Expected": json.dumps(test["expected_data"]),
            "Return": structured_data,
            "Passing": json_string_to_dict(structured_data) == test["expected_data"]
        }
        df2 = pd.DataFrame(new_row, index=[0]) 

        # Add the structured data to the results list
        results_df = pd.concat([results_df, df2], ignore_index=True)
        with placeholder.container():
            st.dataframe(results_df)

    # Convert the results list to a pandas DataFrame
    results_df = pd.DataFrame(results_df)
