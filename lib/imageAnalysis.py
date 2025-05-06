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

def analyse(prompt_system, prompt, url_or_path, lang):
    # Vérifier si l'URL ou le chemin local est fourni
    if url_or_path.startswith("http"):
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
                        {"type": "text", "text": prompt+"La réponse est constituer de deux éléments. 1. un tableau en markdown comme suit : [Level of confidence in the response in %, Requires human intervention for validation (yes/no).] . 2. un texte explicatif détaillant précisemment le pourquoi. (mettre en gras la conclusion). Ecrit la réponse en " + lang +" ."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url_or_path,
                            },
                        },
                    ],
                }
            ],
            max_tokens=2000,
        )
    return response.choices[0].message.content


