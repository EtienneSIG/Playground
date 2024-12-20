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
with open(r'config.json') as config_file:
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
def Correcteur(prompt, lang):
    prompt_Orthographe="Corrige les fautes de grammaire et d’orthographe dans le texte suivant : "+ prompt + ". Assure-toi que le texte soit clair, fluide et sans erreurs.Et qu'il est bien écrit en "+ lang
    prompt_system ="Tu es un assistant qui aide à corriger des textes. Tu es spécialisé dans la langue "+lang
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
                            {"type": "text", "text": prompt_Orthographe},
                            ],
                            }
                            ],
                            max_tokens=2000,
                            )
    return response.choices[0].message.content
def PunchLine(prompt,punchline_language):
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
def Traduction(prompt,langueSource,langueDestination):

    
    prompt_translate="Peux tu traduire le texte suivant : "+ prompt + ". Assure-toi que le texte traduit est dans un vocabulaire natif de la langue de destination."
    prompt_system ="Tu es un traducteur professionnel. Traduis le texte suivant de "+ langueSource +" vers "+ langueDestination +" en conservant le sens exact, le ton, et le style original. Assure-toi que la traduction soit naturelle, fluide et adaptée au contexte culturel."
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
                            {"type": "text", "text": prompt_translate},
                            ],
                            }
                            ],
                            max_tokens=2000,
                            )
    return response.choices[0].message.content
def DocGeneratorForDev(script):

    
    prompt_doc="generate the detailed technical and functional markdown documentation with summary of the follwing script :\n "+ script
    prompt_system ="Act as senior developper"
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
                            {"type": "text", "text": prompt_doc},
                            ],
                            }
                            ],
                            max_tokens=4096,
                            )
    return response.choices[0].message.content
def WinWireSummary(winwire):
    prompt_winwire="Le résultat doit être une chaine de caractère respectant la forme suivante : | Client | Industrie | Technologie | Revenu | Problématique(limite à 30 mots) | Solution(limite à 30 mots) | Account Executive . Respect le formalise en utilisant les informations nécessaire du texte suivant" + winwire + "evite les caractères non utf8 dans la réponse"
    prompt_system ="Je suis un employé de Microsoft et je cherche à synthétiser les winwire. Surtout ne garde pas l'entête du tableau pour la réponse."
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
                            {"type": "text", "text": prompt_winwire},
                            ],
                            }
                            ],
                            max_tokens=4096,
                            )
    return response.choices[0].message.content.replace("\n","")

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


# Création de l'interface avec Streamlit
st.set_page_config(page_title="Playground", layout="wide")

# Tabs
tabs = st.tabs(["Home", "Text Corrector", "Translation", "Punchline Generator", "Image Analysis", "Documentation Generator", "Summary of Winwire", "Popularizer of Topics/Concepts"])

# Home
with tabs[0]:
    st.title("Welcome")
    st.markdown("""
                Use the tabs above to access various features:
                - Spelling and grammar text correction
                - Punchline creation or translation
                - Text translator
                - Image analysis
                - Source code documentation generator in Markdown format
                - Summarize Winwire files in CSV format
                - Simplifier of topics/concepts
                """)

# Text Corrector
with tabs[1]:
    st.title("Text Corrector")
    
    # User input
    text_to_correct = st.text_area("Enter the text to correct:", height=200)
    text_to_correct_language = st.selectbox("Select destination language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="text_to_correct_language")
    if st.button("Correct Text", key="correct_button"):
        if text_to_correct.strip():
            with st.spinner("Correction in progress..."):
                try:
                    result = Correcteur(text_to_correct,text_to_correct_language)
                    st.success("Text corrected successfully!")
                    st.write("### Corrected Result:")
                    st.text_area("Corrected Text:", value=result, height=200)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text before clicking 'Correct Text'.")

# Translation
with tabs[2]:
    st.title("Translation")
    
    # User input
    text_to_translate = st.text_area("Enter the text to translate:", height=200)
    source_language = st.selectbox("Select source language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_1", index=1)
    target_language = st.selectbox("Select destination language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_2")
    
    if st.button("Translate Text", key="translate_button"):
        if text_to_translate.strip() and source_language.strip() and target_language.strip():
            with st.spinner("Translation in progress..."):
                try:
                    result = Traduction(text_to_translate, source_language, target_language)
                    st.success("Text translated successfully!")
                    st.write("### Translated Text:")
                    st.text_area("Translation:", value=result, height=200)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in all fields before clicking 'Translate Text'.")

# Punchline Generator
with tabs[3]:
    st.title("Punchline Creator")
    
    # User input
    text_for_punchline = st.text_area("Enter the text to create punchlines from:", height=200)
    punchline_language = st.selectbox("Select the punchline language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_5")
    if st.button("Create Punchlines", key="punchline_button"):
        if text_for_punchline.strip():
            with st.spinner("Creating punchlines..."):
                try:
                    result = PunchLine(text_for_punchline,punchline_language)
                    st.success("Punchlines created successfully!")
                    st.write("### Punchlines:")
                    st.text_area("Punchlines:", value=result, height=200)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text before clicking 'Create Punchlines'.")

# Image Analysis
with tabs[4]:
    st.title("Image Analysis")
    
    # Input prompts
    prompt_system = st.text_area("Define your profile:", placeholder="Describe who you are...")
    prompt = st.text_area("Enter your problem:", placeholder="Describe your request here...")
    selected_option = st.selectbox("Select a language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_3")
    # URL or local file selection
    url = st.text_input("Enter the URL of the image describing the context:", placeholder="https://example.com/image.jpg")
    if url:
        try:
            st.image(url, caption="Image Preview", use_container_width=True)
        except Exception as e:
            st.warning(f"Unable to display the image: {e}")
    
    # Analyze button
    if st.button("Analyze"):
        if prompt_system and prompt and url:
            try:
                st.write("Analyzing...")
                # Call the analysis function
                result = analyse(prompt_system, prompt, url,selected_option)

                # Display the result
                st.success("Analysis completed successfully!")
                st.markdown("### Result:")
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill in all fields before starting the analysis.")

# Documentation Generator
with tabs[5]:
    st.title("Documentation Generator")
    
    # Input method selection
    input_choice = st.radio(
        "How would you like to provide the Python script?",
        options=["Text field", "Upload a file"],
        index=0
    )
    
    script_code = ""
    if input_choice == "Text field":
        # User input for the script in a text field
        script_code = st.text_area("Paste the Python script to generate documentation:", height=300)
    else:
        # File upload
        uploaded_file = st.file_uploader("Upload a Python file:", type=["py"])
        if uploaded_file is not None:
            # Read the file content
            script_code = uploaded_file.read().decode("utf-8")

    # Generate documentation button
    if st.button("Generate Documentation", key="doc_generator_button"):
        if script_code.strip():
            with st.spinner("Generating documentation..."):
                try:
                    result = DocGeneratorForDev(script_code)
                    st.success("Documentation generated successfully!")
                    # Add download button
                    st.download_button(
                        label="Save Documentation",
                        data=result,
                        file_name="documentation.md",
                        mime="text/markdown"
                                            )
                    st.write("### Generated Documentation:")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please provide a script before clicking 'Generate Documentation'.")

# Winwire Summary
with tabs[6]:
    st.title("Summary of Winwire")
    
    # Input method selection
    input_choice = st.radio(
        "How would you like to provide the text to summarize?",
        options=["Text field", "Upload one or multiple files"],
        index=0
    )
    
    text_to_summarize = ""
    if input_choice == "Text field":
        text_to_summarize = st.text_area("Copy/Paste the text:", height=300)
    else:
        uploaded_files = st.file_uploader(
            "Upload one or more text files:",
            type=["txt", "csv"],
            accept_multiple_files=True
        )
        if uploaded_files:
            st.write(f"### {len(uploaded_files)} uploaded files.")

    # Generate summary button
    if st.button("Generate Summary", key="summary_button"):
        if input_choice == "Text field" and text_to_summarize.strip():
            with st.spinner("Summarizing..."):
                try:
                    result = WinWireSummary(text_to_summarize)
                    st.success("Summary generation: Successful!")
                    st.write(result)
                    st.download_button(label="Download Summary", data=result, file_name="WinwireSummary.csv")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif input_choice == "Upload one or multiple files" and uploaded_files:
            with st.spinner("Summarizing..."):
                try:
                    results = "| Customer | Industry | Technology | Revenue | Problem statement | Solution | Contact | \n|:--------|----------:|---------:|--------------:|-----------------:|-----------------:|----------:|\n" 
                    for uploaded_file in uploaded_files:
                        file_content = uploaded_file.read().decode("utf-8", errors="replace")
                        result = WinWireSummary(file_content)
                        results += f"{result.replace('\'', ' ')} \n"

                    st.success("Summary successfully generated for all files!")
                    st.download_button(
                        label="Download Summary",
                        data=results,
                        file_name="WinwireSummary.csv"
                    )
                    st.write(results)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text or upload files before clicking 'Generate Summary'.")

# Topic Popularizer
with tabs[7]:
    st.title("Popularizer of Topics/Concepts")
    
    # User input
    text_to_popularize = st.text_area("Enter the text to popularize:", height=200)
    selected_option = st.selectbox("Select a language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_4")
    
    if st.button("Popularize Text", key="popularize_button"):
        if text_to_popularize.strip():
            with st.spinner("Popularizing..."):
                try:
                    result = Vulgarisation(text_to_popularize, selected_option)
                    st.success("Successfully popularized!")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text before clicking 'Popularize Text'.")