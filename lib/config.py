import streamlit as st
import pandas as pd
import json
import os


with open("lib/config.json") as f:
    data = json.load(f)

df_json = pd.DataFrame(list(data.items()), columns=['Parameter', 'Value'])
df_json_edited=st.data_editor(df_json, num_rows="dynamic")

# Convert DataFrame back to JSON
df_json_edited = df_json_edited.set_index('Parameter').to_dict()['Value']

# Display the JSON result
def json_write(df_json_edited): 
    ouput=json.dumps(df_json_edited, indent=4)
    f = open("config.json", "w")
    f.write(ouput)
    f.close()
    st.write(ouput)
