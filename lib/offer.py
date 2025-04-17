import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import fitz  # PyMuPDF
from token_count import TokenCount
# OpenAI Library
from openai import AzureOpenAI
import openai
import json
import os


tc = TokenCount(model_name="gpt-3.5-turbo")

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


def sauvegarder_pdf_local(uploaded_file):
    # Créer un dossier pour stocker les PDF s'il n'existe pas déjà
    if not os.path.exists("lib/pdf_uploads"):
        os.makedirs("lib/pdf_uploads")

    # Chemin où le fichier sera sauvegardé
    chemin_fichier = os.path.join("lib/pdf_uploads", uploaded_file.name)

    # Écrire le fichier sur le disque
    with open(chemin_fichier, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return chemin_fichier

def compare_pdf(contenu_pdf1, contenu_pdf2):
    prompt_criteria= f"Fait un tableau de synthèse de {contenu_pdf1} et {contenu_pdf2} en suivant les critères suivants : le prix,la valeur technique"
    prompt_system =f"Je suis acheteur, je dois analyser deux offres de fournisseurs pour un appel d'offre. Je dois comparer les deux offres en fonction de critères spécifiques. Je vais te donner les deux offres et tu devras me donner un tableau de synthèse qui met en évidence les différences et les similitudes entre les deux offres."
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
                            {"type": "text", "text": prompt_criteria},
                            ],
                            }
                            ],
                            max_tokens=2000,
                            )
    return response.choices[0].message.content


def lire_pdf(chemin_fichier):
    doc = fitz.open(chemin_fichier)
    texte = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        texte += page.get_text()
    return texte


