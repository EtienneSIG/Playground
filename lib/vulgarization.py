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

def Vulgarisation(prompt_vulg,lang):
    prompt_vulg="Vulgarise le texte suivant : "+ prompt_vulg +".la structure de la réponse doit être diviser en section avec les titres suivants : 1. Explication (tu peux ajouter des liens vers la documentation)  2. Process de mise en place(tu peux ajouter des liens vers la documentation) : 3. Synthèse 4. Vulgarisation si vous parliez à un enfant de 4 ans 5. Fait un tableau composer des colonnes suivantes [Persona, Vulgarisation, Point clé pour le persona]. Fait ce tableau pour les personnes suivants : membre du comex, chief data officer, chief technology officer, architect d'entreprise data, business analyst, data analyst, data scientist, data engineer. Traduit toutes la réponse en "+ lang
    prompt_system ="Je suis une personne spécilisé dans la vulgarisation de concept de data & AI."
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
                            {"type": "text", "text": prompt_vulg},
                            ],
                            }
                            ],
                            max_tokens=4096,
                            )
    return response.choices[0].message.content

