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

def punchline(prompt,punchline_language):
    prompt_punchline="Ecrit 4 variantes de punchlines à partir texte suivant : "+ prompt + ". Assure-toi que la punchline est claire, simple et impactante. Mets les un après les autres. ex: 1. ... \n 2. ... \n 3. ... (n'hesites à pas mettre des emojis). Ecrit la punchline dans la "+punchline_language +" comme si tu étais un natif"
    prompt_system ="Tu es un expert en création de punchlines de lanque "+punchline_language +". À partir du texte suivant, génère une punchline percutante qui capture l'essence du message de manière concise, mémorable et impactante. Assure-toi que la punchline soit adaptée à un public moderne et qu'elle utilise un langage direct et frappant."
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
                            {"type": "text", "text": prompt_punchline},
                            ],
                            }
                            ],
                            max_tokens=2000,
                            )
    return response.choices[0].message.content
