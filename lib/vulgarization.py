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

# Import du module de configuration des variables d'environnement
from lib.env_config import get_env_var

# Configuration du client OpenAI avec les variables d'environnement
gpt_key = get_env_var('OPENAI_API_KEY')
gpt_endpoint = get_env_var('OPENAI_API_BASE')
gpt_token_max = get_env_var('OPENAI_NB_TOKENS')
gpt_model_id = get_env_var('COMPLETIONS_MODEL')
gpt_api_version = get_env_var('OPENAI_API_VERSION')

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

