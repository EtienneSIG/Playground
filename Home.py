import streamlit as st

st.sidebar.title("Demo playground.")


def intro():
    import streamlit as st
    
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        # 📚 Démonstrations IA

#### 🙌 Contributeur
| Nom | Fonction | Entreprise | Profil |
| --- | --- | --- | --- | 
| Alexandre FOURDRAINE | Technical Specialist - Data & AI | Microsoft France | :male-office-worker:[Linkedin](https://www.linkedin.com/in/alexandre-fourdraine-5a338a29/)|
| Etienne SIGWALD | Technical Specialist - Data & AI | Microsoft France | :male-office-worker:[Linkedin](https://www.linkedin.com/in/etienne-sigwald/)|

        
## 🎯 Objectif

Cette application Streamlit propose plusieurs démonstrations interactives de cas d’usage de l’intelligence artificielle (IA) appliquée au **traitement du langage naturel (NLP)** et à l’**analyse d’images**. Elle permet aux utilisateurs de tester des fonctionnalités variées telles que :

- 🖼️ Analyse de scènes à partir d’images
- ✨ Discussion avec un agent IA sur des données
- 💬 Analyse du transcript du support
- 🆚 Compraison d'offres
- 🎤 Génération de punchlines
- 🧠 Vulgarisation de concepts

---

## 🗂️ Structure Générale

L’application repose sur un modèle multipages, où chaque page correspond à une fonctionnalité. La navigation s’effectue via un menu déroulant dans la **barre latérale Streamlit**.

```python
page_names_to_funcs = {
    "—": intro,
    "Image Analysis": ImageAnalysis,
    "Support": support,
    "Chat with Data Agent": dataAgent,
    "Offer analysis": offer,    
    "Punchline Creator": Punchline,
    "Popularized topics": popularize,
    "Settings": setting,
}
```


## :gear: Configuration

Afin d'utiliser toutes les démos tu dois completer les différents paramètres de la page setting\n
| Parameter        | Description      | 
|:------------------|:------------------|   
| COMPLETIONS_MODEL | Deployment name |
| OPENAI_API_BASE | API base url |
| OPENAI_API_VERSION | API Version |
| OPENAI_API_KEY | OPENAI key to access to the model |
| OPENAI_NB_TOKENS | Number of token max for prompt |
| COMPUTER_VISION_KEY | Customer vision api key |
| COMPUTER_VISION_ENDPOINT | url of the computer vision API |
| AIPROJECT_CONNECTION_STRING | AI Agent connection string |
| AGENT_ID | AI Agent ID | 
           """
    )

def Punchline():
    import streamlit as st

    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))


    from lib.punchline import punchline


    # Set page title and layout
    #st.set_page_config(page_title="Punchline Creator", layout="wide")
    st.markdown(f"# {list(page_names_to_funcs.keys())[4]}")
    # Title    
    #st.title("Punchline Creator")
    
    # User input
    text_for_punchline = st.text_area("Enter the text to create punchlines from:", height=200)
    punchline_language = st.selectbox("Select the punchline language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_5")
    if st.button("Create Punchlines", key="punchline_button"):
        if text_for_punchline.strip():
                with st.spinner("Creating punchlines..."):
                    try:
                        result = punchline(text_for_punchline,punchline_language)
                        st.success("Punchlines created successfully!")
                        st.write("### Punchlines:")
                        st.text_area("Punchlines:", value=result, height=200)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        else:
             st.warning("Please enter text before clicking 'Create Punchlines'.")

def ImageAnalysis():
    import streamlit as st

    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    from lib.imageAnalysis import analyse
    
    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")

    popover = st.popover("Demo scenario")
    Repair_en = popover.checkbox("Show repair scenario.", False)
    Phishing_en = popover.checkbox("Show Phishing scenario.", False)
    id_en = popover.checkbox("Show fake ID scenario.", False)

    if Repair_en:
        st.write(''' profil : I am a technician at an oil company, currently working on a pipeline \n\n Context : I am dealing with a leak on a pipe, can you describe a protocol for repairing the leak to me? \n\n Photo illustrant le contexte :https://img.freepik.com/photos-premium/corrosion-rouille-travers-fuite-gaz-vapeur-du-tube-douille-au-niveau-petite-isolation-du-pipeline_478515-3743.jpg ''')
    if Phishing_en:
        st.write(''' Profile: I am a 70-year-old. I’m not very comfortable with computers. \n\n Context: As soon as I start my computer, I get this screen. Is it a scam? \n\n Photo illustrant le contexte :https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEix0XfsY-0wZPr2_Yi8a79zevrySzlxI-CwIdApE5nY6G6aNV8Lk1XHnBZeco3n1ZZ6-rUMXMXgDbSxMu1tXg3yEi119jW178oCBRpxPPSVPXExJuJaCPvuLXI1pe6fj8Q6Xgzzwmat54qjDcTSOEuQUtqfOKQbhGS0EBHQjHDXjzeMuPoqK3saYMjm2att/s728-rw-e365/windws.png''')
    if id_en:
        st.write(''' Profile: I am a customs officer. \n\n Context: I have a doubt about the following ID card. Do you think it's fake? \n\n Photo illustrant le contexte :https://xkauf.net/197-pd4_def/fausse-carte-d-identite-autriche.jpg ''')
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

def popularize():
    import streamlit as st

    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    from lib.vulgarization import Vulgarisation
    
    # Set page title and layout
    #st.set_page_config(page_title="Popularizer of Topics/Concepts", layout="wide")
    st.markdown(f"# {list(page_names_to_funcs.keys())[5]}")
    
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

def support():
    import streamlit as st

    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    from lib.support import SupportDiscussionToTicket

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    with st.expander("Example of support scenario", expanded=False):
        st.write(''' Support Agent: Hello, thank you for calling BE/ES support. This is Alex. How can I help you today?

User: Hi Alex, I'm having trouble with my laptop. It keeps freezing and I can't figure out why.

Support Agent: I'm sorry to hear that. Let's try to troubleshoot this together. Can you tell me when the issue started happening?

User: It started yesterday afternoon, out of nowhere.

Support Agent: Understood. Have you installed any new software or updates recently?

User: No, I haven't installed anything new.

Support Agent: Alright. Let's try a simple step first. Could you please restart your laptop and let me know if the problem persists after rebooting?

User: Sure, I'll do that now.

(A few moments later)

User: Okay, I restarted it, but it's still freezing.

Support Agent: Thank you for trying that. Next, let's check if there are any background programs causing the issue. Could you open the Task Manager by pressing Ctrl + Shift + Esc and let me know what processes are using the most CPU or memory?

User: Okay, I see that there's a program called "Updater" using a lot of CPU.

Support Agent: That might be the culprit. Sometimes, update processes can cause temporary slowdowns. You can try ending that task by selecting it and clicking "End Task." Let me know if that helps.

User: Alright, I ended the task. It seems to be running better now.

Support Agent: Great! It looks like that was the issue. If it happens again, you might want to check for any software updates or consider uninstalling that program if it's not necessary. Is there anything else I can help you with?

User: No, that's all for now. Thank you so much!

Support Agent: You're welcome! Have a great day!
                 ''')

    # Import the necessary function from your custom library   
    # User input
    transcript = st.text_area("Enter the transcript :", height=200)
    selected_option = st.selectbox("Select a language", ["English", "French", "Spanish", "German", "Dutch", "Italian"],key="language_selector_support")
    
    if st.button("Content generation", key="support_button"):
        if transcript.strip():
            with st.spinner("Generate..."):
                try:
                    result = SupportDiscussionToTicket(transcript, selected_option)
                    st.success("Successfully !")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a transcript before clicking 'Generate'.")

def dataAgent():
    import os
    import json
    import re
    import streamlit as st
    import plotly.graph_objects as go
    from dotenv import load_dotenv
    from azure.ai.projects import AIProjectClient
    from azure.identity import InteractiveBrowserCredential
    from azure.ai.projects.models import MessageRole

    # Load environment variables
    # load_dotenv()

    # AIPROJECT_CONNECTION_STRING = os.getenv("AIPROJECT_CONNECTION_STRING")
    # AGENT_ID = os.getenv("AGENT_ID")

    # --- Chargement des paramètres depuis config.json ---
    with open("lib/config.json") as config_file:
        config_details = json.load(config_file)

    AIPROJECT_CONNECTION_STRING = config_details['AIPROJECT_CONNECTION_STRING']
    AGENT_ID = config_details['AGENT_ID']
    #print(AIPROJECT_CONNECTION_STRING)
    #print(AGENT_ID)

    # Initialize Streamlit session state
    if "thread_id" not in st.session_state or "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.thread_id = None
        st.session_state.project_client = None

    #st.set_page_config(page_title="AI Chat", layout="wide")

    #st.title(" 🗨️ Chat with your Fabric DataAgent - :new: ") 

    # Authenticate only once and initialize thread
    if st.session_state.project_client is None:
        credential = InteractiveBrowserCredential()
        project_client = AIProjectClient.from_connection_string(
            conn_str=AIPROJECT_CONNECTION_STRING, credential=credential
        )
        st.session_state.project_client = project_client
        thread = project_client.agents.create_thread()
        st.session_state.thread_id = thread.id
        st.success(f"New Thread created: {thread.id}")
    else:
        project_client = st.session_state.project_client

    # Chart rendering function
    def render_chart(chart_data):
        chart_type = chart_data.get("type", "line")
        fig = go.Figure()

        if chart_type == "bar":
            fig.add_trace(go.Bar(x=chart_data["x"], y=chart_data["y"]))
        elif chart_type == "pie":
            fig = go.Figure(go.Pie(labels=chart_data["x"], values=chart_data["y"]))
        else:  # default to line chart
            fig.add_trace(go.Scatter(x=chart_data["x"], y=chart_data["y"], mode='lines+markers'))

        fig.update_layout(
            title=chart_data.get("title", "Chart"),
            xaxis_title=chart_data.get("xlabel", "X"),
            yaxis_title=chart_data.get("ylabel", "Y")
        )
        st.plotly_chart(fig, use_container_width=True)

    # Chat history display
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"**😏:** {entry['content']}")
        else:
            st.markdown(f"**🤖:** {entry['content']}")
            if entry.get("chart_data"):
                render_chart(entry["chart_data"])

    # User input box
    # Création de colonnes pour aligner le bouton à droite
    user_input = st.chat_input("Ask something...", key="user_input")
    #submit = st.form_submit_button("Send")

    if user_input: #submit and
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        project_client.agents.create_message(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_input,
        )

        run = project_client.agents.create_and_process_run(
            thread_id=st.session_state.thread_id, agent_id=AGENT_ID
        )

        if run.status == "failed":
            st.session_state.chat_history.append({"role": "agent", "content": f"Run failed: {run.last_error}"})
        else:
            messages = project_client.agents.list_messages(st.session_state.thread_id)
            last_msg = messages.get_last_text_message_by_role(MessageRole.AGENT)

            if not last_msg:
                st.session_state.chat_history.append({"role": "agent", "content": "No response from the model."})
            else:
                agent_text = last_msg.text.value
                chart_data = None

                if "#chart" in agent_text:
                    try:
                        chart_match = re.search(r"#chart\s*({.*?})", agent_text, re.DOTALL)
                        if chart_match:
                            chart_data = json.loads(chart_match.group(1))
                            agent_text = re.sub(r"#chart\s*({.*?})", "", agent_text, flags=re.DOTALL).strip()
                    except Exception as chart_error:
                        agent_text += f"\n\n(Chart rendering failed: {str(chart_error)})"

                st.session_state.chat_history.append({
                    "role": "agent",
                    "content": agent_text,
                    "chart_data": chart_data
                })

        st.rerun()

def offer():
    import streamlit as st
    from streamlit_pdf_viewer import pdf_viewer
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    from lib.offer import compare_pdf, lire_pdf, sauvegarder_pdf_local
    # Chemin vers les fichiers PDF

    #pdf1 = "C:/Users/esigwald/Downloads/aap-tsia-2025.pdf"
    #pdf2 = "C:/Users/esigwald/Downloads/annexe_4_modele_d_offre_financiere_iedom.pdf"
    st.title("Chargement des offres")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Offre 1 : ")
            # Widget pour uploader un fichier PDF
        uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf", key="upload_pdf1")
        if uploaded_file is not None:
        # Sauvegarder le fichier localement
            chemin_fichier_1 = sauvegarder_pdf_local(uploaded_file)
            st.success(f"Fichier sauvegardé avec succès : {chemin_fichier_1}")
            pdf_viewer(chemin_fichier_1, width=1000, height=600,key="pdf11")
            #st.write(f"Offre 1 : { pdf1 } ")
        else:
            st.write(f"Please upload a file to view it.")

    with col2:
        st.subheader(f"Offre 2 : ")
        uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf",key="upload_pdf2")
        chemin_fichier_2 = " "
        if uploaded_file is not None:
        # Sauvegarder le fichier localement
            chemin_fichier_2 = sauvegarder_pdf_local(uploaded_file)
            st.success(f"Fichier sauvegardé avec succès : {chemin_fichier_2}")
            pdf_viewer(chemin_fichier_2, width=1000, height=600,key="pdf22")
            contenu_pdf1 = lire_pdf(chemin_fichier_1)
            contenu_pdf2 = lire_pdf(chemin_fichier_2)
            #st.write(f"Offre 2 : { pdf2 } ")
        else:
            st.write(f"Please upload a file to view it.")

    st.divider()
    st.title("Analyse comparative des offres")
    
    # Lire le contenu des PDF

    if st.button("Lancer l'analyse", key="offer_button") : 
        with st.spinner("Generate..."):
            try:
                #st.success("Successfully !")
                st.markdown(compare_pdf(contenu_pdf1,contenu_pdf2))   
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    
 

def setting():
    import streamlit as st
    import pandas as pd
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    
    from lib.env_config import (
        ENV_VARS, 
        get_env_var, 
        update_env_vars, 
        init_env_variables, 
        save_to_config_file, 
        get_all_env_vars,
        get_var_description
    )

    # Titre de la page
    st.title("⚙️ Paramètres de configuration")

    with st.expander("À propos des paramètres", expanded=False):
        st.markdown(''' 
                    Cette page vous permet de configurer les différents points de terminaison et agents nécessaires pour toutes les démos de cette application.
                    
                    Les paramètres sont stockés dans la session Streamlit et persisteront jusqu'à la fermeture de votre navigateur.
                    Pour les conserver de façon permanente, utilisez le bouton "Sauvegarder dans config.json".
                    
                    | Paramètre | Description |
                    |:----------|:------------|
                    | COMPLETIONS_MODEL | Nom du modèle de déploiement |
                    | OPENAI_API_BASE | URL de base de l'API |
                    | OPENAI_API_VERSION | Version de l'API |
                    | OPENAI_API_KEY | Clé d'accès pour le modèle |
                    | OPENAI_NB_TOKENS | Nombre maximal de tokens pour les prompts |
                    | COMPUTER_VISION_KEY | Clé d'accès pour Computer Vision |
                    | COMPUTER_VISION_ENDPOINT | URL du service Computer Vision |
                    | AIPROJECT_CONNECTION_STRING | Chaîne de connexion pour l'agent AI |
                    | AGENT_ID | ID de l'agent AI |
                    ''')

    # Initialiser les variables d'environnement si nécessaire
    init_env_variables()
    
    # Créer un callback pour mettre à jour une variable lorsqu'elle est modifiée
    def update_env_var(var_name):
        def callback():
            value = st.session_state[f"input_{var_name}"]
            update_env_vars({var_name: value})
        return callback
    
    # Section des paramètres éditables
    st.subheader("Paramètres")
    
    # Option pour masquer/afficher les valeurs sensibles
    show_sensitive = st.checkbox("Afficher les valeurs sensibles", value=False, key="show_sensitive")
    
    # Style pour les cartes de paramètres
    st.markdown("""
    <style>
    .param-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #4e8cff;
    }
    .param-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .param-description {
        color: #6c757d;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Obtenir toutes les variables d'environnement actuelles
    env_data = get_all_env_vars()
    
    # Grouper les paramètres par catégorie
    param_categories = {
        "Modèle OpenAI": ["COMPLETIONS_MODEL", "OPENAI_API_BASE", "OPENAI_API_VERSION", "OPENAI_API_KEY", "OPENAI_NB_TOKENS"],
        "Computer Vision": ["COMPUTER_VISION_KEY", "COMPUTER_VISION_ENDPOINT"],
        "AI Project": ["AIPROJECT_CONNECTION_STRING", "AGENT_ID"]
    }
    
    # Afficher les variables par catégorie avec des composants interactifs
    for category, params in param_categories.items():
        st.write(f"### {category}")
        
        for var_name in params:
            current_value = env_data.get(var_name, "")
            description = get_var_description(var_name)
            
            # Déterminer si la valeur est sensible (contient "key", "token", "secret", "password" ou "connection")
            is_sensitive = any(keyword in var_name.lower() for keyword in ["key", "token", "secret", "password", "connection"])
            
            # Créer une carte pour chaque paramètre
            st.markdown(f'<div class="param-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="param-title">{var_name}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="param-description">{description}</div>', unsafe_allow_html=True)
            
            # Champ d'entrée pour la valeur
            if is_sensitive and not show_sensitive:
                # Pour les valeurs sensibles, utiliser un champ de type password
                value = st.text_input(
                    "Valeur",
                    value=current_value,
                    type="password",
                    key=f"input_{var_name}",
                    on_change=update_env_var(var_name),
                    label_visibility="collapsed"
                )
            else:
                # Pour les valeurs non sensibles ou si show_sensitive est True
                value = st.text_input(
                    "Valeur",
                    value=current_value,
                    key=f"input_{var_name}",
                    on_change=update_env_var(var_name),
                    label_visibility="collapsed"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Ajouter des boutons pour les actions supplémentaires
    st.write("### Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Sauvegarder dans config.json", key="save_config_btn"):
            if save_to_config_file():
                st.success("Configuration sauvegardée avec succès dans config.json")
            else:
                st.error("Erreur lors de la sauvegarde de la configuration")
    
    with col2:
        if st.button("Réinitialiser aux valeurs par défaut", key="reset_defaults_btn"):
            from lib.env_config import DEFAULT_VALUES
            update_env_vars(DEFAULT_VALUES)
            st.success("Valeurs réinitialisées aux paramètres par défaut")
            st.rerun()
    
    with col3:
        if st.button("Exporter en .env", key="export_env_btn"):
            env_content = "\n".join([f"{key}={value}" for key, value in env_data.items()])
            st.download_button(
                label="Télécharger le fichier .env",
                data=env_content,
                file_name=".env",
                mime="text/plain"
            )
    
    # Afficher un résumé de la configuration
    st.write("### Résumé de la configuration")
    st.info(f"{len(env_data)} paramètres configurés. Utilisez les champs ci-dessus pour les modifier directement.")
    
    # Option pour afficher un tableau récapitulatif des paramètres
    if st.checkbox("Afficher le tableau récapitulatif", value=False):
        # Créer une version filtrée des données pour le tableau
        display_data = []
        for key, value in env_data.items():
            display_value = value
            if any(keyword in key.lower() for keyword in ["key", "token", "secret", "password", "connection"]) and not show_sensitive:
                display_value = "••••••" + (value[-4:] if len(value) > 4 else "")
            display_data.append({"Paramètre": key, "Valeur": display_value, "Description": get_var_description(key)})
        
        # Afficher le tableau
        st.table(pd.DataFrame(display_data))

page_names_to_funcs = {
    "—": intro,
    "Image Analysis": ImageAnalysis,
    "Support": support,
    "Chat with Data Agent": dataAgent,
    "Offer analysis": offer,    
    "Punchline Creator": Punchline,
    "Popularized topics": popularize,
    "Settings": setting,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()