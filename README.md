### Documentation: Script for Utilizing Azure OpenAI Services and Streamlit
## Summary
The provided script leverages the Azure OpenAI API to perform multiple text-related tasks such as text correction, translation, punchline generation, image analysis, documentation generation, winwire summarization, and topic popularization. The script incorporates a Streamlit-based web interface that allows users to interact with these functionalities in a user-friendly manner.


## Functional Description

# Libraries and Imports
The script uses several libraries, including openai, nltk, argparse, and streamlit, among others:

openai: Used to make requests to Azure OpenAI services.
nltk: Natural Language Toolkit, for language processing.
streamlit: Used to create the web interface for the application.
nltk, argparse, os, sys, subprocess, time, io, urllib: Standard Python libraries for system-level operations and handling HTTP requests.
PIL: For handling and displaying images with the Pillow library.
base64: For encoding and decoding binary data.
Configuration
The script reads configuration values from a config.json file:

OPENAI_API_KEY
OPENAI_API_BASE
OPENAI_NB_TOKENS
COMPLETIONS_MODEL
OPENAI_API_VERSION
These configurations are used to set up the OpenAI client.


## Functions
# analyse(prompt_system, prompt, url_or_path, lang)
Analyzes an image by prompting the OpenAI model with the user's request and the image URL or path.


# Correcteur(prompt, lang)
Corrects grammatical and spelling errors in a given text and ensures clarity and fluency.


# PunchLine(prompt, punchline_language)
Generates punchlines from a given text.


# Traduction(prompt, langueSource, langueDestination)
Translates text from a source language to a target language.


# DocGeneratorForDev(script)
Generates detailed technical and functional documentation in markdown format from a given Python script.


# WinWireSummary(winwire)
Synthesizes winwire texts into a summarized format suitable for a CSV file.


# Vulgarisation(prompt_vulg, lang)
Popularizes a concept by breaking it down into simpler sections and making it understandable for different audiences.


## Technical Description
Initialization and Configuration
Reading Configuration:

with open(r'config.json') as config_file:
    config_details = json.load(config_file)

Setting up the OpenAI client:

client = openai.AzureOpenAI(
    azure_endpoint=config_details['OPENAI_API_BASE'],
    api_version=config_details['OPENAI_API_VERSION'],
    api_key=config_details['OPENAI_API_KEY']
)

## Function Implementations
# Image Analysis:

def analyse(prompt_system, prompt, url_or_path, lang):
    if url_or_path.startswith("http"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_system},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt + "La réponse est ... en " + lang + " ."},
                        {"type": "image_url", "image_url": {"url": url_or_path}},
                    ],
                }
            ],
            max_tokens=2000,
        )
        return response.choices[0].message.content

# Text Correction:

def Correcteur(prompt, lang):
    prompt_Orthographe = "Corrige les fautes de grammaire ... en " + lang
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un assistant ... de la langue " + lang},
            {"role": "user", "content": [{"type": "text", "text": prompt_Orthographe}]}
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content

# Punchline Generation:

def PunchLine(prompt, punchline_language):
    prompt_punchline = "Ecrit 4 variantes ... ... en " + punchline_language
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un expert ... en punchline de lanque " + punchline_language},
            {"role": "user", "content": [{"type": "text", "text": prompt_punchline}]}
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content

# Translation:

def Traduction(prompt, langueSource, langueDestination):
    prompt_translate = "Peux tu traduire ... de la langue de destination."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un traducteur ... en conservant ... le ton, et le style original."},
            {"role": "user", "content": [{"type": "text", "text": prompt_translate}]}
        ],
        max_tokens=2000,
    )
    return response.choices[0].message.content

# Documentation Generation:

def DocGeneratorForDev(script):
    prompt_doc = "generate the detailed technical and functional markdown documentation ... \n " + script
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Act as senior developper"},
            {"role": "user", "content": [{"type": "text", "text": prompt_doc}]}
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content

# Winwire Summary:

def WinWireSummary(winwire):
    prompt_winwire = "Le résultat doit être ... ."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Je suis un employé ... ."},
            {"role": "user", "content": [{"type": "text", "text": prompt_winwire}]}
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content.replace("\n", "")

# Topic Popularization:

def Vulgarisation(prompt_vulg, lang):
    prompt_vulg = "Vulgarise le texte suivant : " + prompt_vulg + "."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Je suis une personne spécialisée ... ."},
            {"role": "user", "content": [{"type": "text", "text": prompt_vulg}]}
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content

## Streamlit Interface
The Streamlit interface sets up different tabs for each functionality. Users can interact with the application by entering text, selecting options, and uploading files:

Setting up the Streamlit Page:

st.set_page_config(page_title="Playground", layout="wide")
tabs = st.tabs(["Home", "Text Corrector", ...])

Creating Tabs and Adding UI Elements:

For example, the "Text Corrector" tab:

with tabs[1]:
    st.title("Text Corrector")
    text_to_correct = st.text_area("Enter the text to correct:", height=200)
    text_to_correct_language = st.selectbox("Select destination language", [...], key="text_to_correct_language")
    if st.button("Correct Text", key="correct_button"):
        if text_to_correct.strip():
            with st.spinner("Correction in progress..."):
                try:
                    result = Correcteur(text_to_correct, text_to_correct_language)
                    st.success("Text corrected successfully!")
                    st.write("### Corrected Result:")
                    st.text_area("Corrected Text:", value=result, height=200)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text before clicking 'Correct Text'.")

### Conclusion
This script integrates Azure OpenAI functionalities into a user-friendly Streamlit application, offering a range of text-related services like correction, translation, punchline generation, and more. This documentation provides detailed insights into both technical and functional aspects, ensuring developers and users can understand and modify the script as needed.
