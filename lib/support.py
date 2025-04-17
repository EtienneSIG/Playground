# OpenAI Library
from openai import AzureOpenAI
import openai
import nltk

# System Library
import argparse
import os
import sys
import subprocess
import time
import io
import urllib.request
from urllib.parse import urlparse

# Json Library
import json
import streamlit as st
from PIL import Image
import base64

###########################################################
#print("####################################################")
#print("##START - Sanity check")
#print("####################################################")

#print("##Python dependencies\n")
#Mandatory_Library = ['openai', 'nltk', 'tkinter']
#
#for lib in Mandatory_Library:
#    if lib not in sys.modules:
#        print("Module " + lib + " is not installed.")
#        subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])

#print("All python library is installed\n")
#print("##Variables check\n")
# Load config values
with open(r'lib/config.json') as config_file:
    config_details = json.load(config_file)

# Set up config var
#Mandatory_Config = ['OPENAI_API_KEY', 'OPENAI_API_BASE', 'OPENAI_NB_TOKENS', 'COMPLETIONS_MODEL', 'OPENAI_API_VERSION']
#i = 0
#print("        VARIABLE       | Status")
#for configM in Mandatory_Config:
#    if config_details[configM] == "":
#        n_occur = ""
#        if len(configM) < 24:
#            n_occur = " " * (24 - len(configM))
#        print(configM + " | KO ")
#    else:
#        n_occur = ""
#        if len(configM) < 24:
#            n_occur = " " * (24 - len(configM))
#        print(configM + n_occur + " | OK ")
#        i = i + 1

gpt_key = config_details['OPENAI_API_KEY']
gpt_endpoint = config_details['OPENAI_API_BASE']
gpt_token_max = config_details['OPENAI_NB_TOKENS']
gpt_model_id = config_details['COMPLETIONS_MODEL']
gpt_api_version = config_details['OPENAI_API_VERSION']

client = openai.AzureOpenAI(
    azure_endpoint=gpt_endpoint,
    api_version=gpt_api_version,
    api_key=gpt_key
    )

def SupportDiscussionToTicket(prompt_support,lang):
    prompt_support="Can summarize the following discussion : "+ prompt_support +".Can you strucuture the summarize with those section : 1. Topic of the discussion and impact for the user (scale between 1 to 5, where 1 is the less impacting) 2. how is the users is skills with the software 3. Description of the issue 4. Describe different step to repeat the issue (error message, screenshot, frequency) 5. Describe different step to solve the issue (you can provide some documentation from the link)(respect the following structure step 1: ... \n Step 2 : ...).  could structure the answer using markdown (you can use list and table if necessary). "#Translate it in the following langage : "+ lang
    prompt_system ="I'm a support level, I need to write a ticket for the dev team. "
    # Vérifier si l'URL ou le chemin local est fourni
    # Traiter comme une URL
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": prompt_system,
                },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_support},
                            ],
                            }
                            ],
                            max_tokens=4096,
                            )
    return response.choices[0].message.content