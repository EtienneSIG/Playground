import os
import json
import streamlit as st
from typing import Dict, Any, Optional

# Liste des variables de configuration requises
ENV_VARS = [
    "COMPLETIONS_MODEL",
    "OPENAI_API_BASE",
    "OPENAI_API_VERSION",
    "OPENAI_API_KEY",
    "OPENAI_NB_TOKENS",
    "COMPUTER_VISION_KEY",
    "COMPUTER_VISION_ENDPOINT",
    "AIPROJECT_CONNECTION_STRING",
    "AGENT_ID"
]

# Valeurs par défaut pour les variables d'environnement
DEFAULT_VALUES = {
    "COMPLETIONS_MODEL": "gpt-4",
    "OPENAI_API_BASE": "https://your-api-endpoint.openai.azure.com/",
    "OPENAI_API_VERSION": "2023-05-15",
    "OPENAI_API_KEY": "",
    "OPENAI_NB_TOKENS": "4000",
    "COMPUTER_VISION_KEY": "",
    "COMPUTER_VISION_ENDPOINT": "https://your-vision-endpoint.cognitiveservices.azure.com/",
    "AIPROJECT_CONNECTION_STRING": "",
    "AGENT_ID": ""
}

# Descriptions des variables pour l'aide contextuelle
VAR_DESCRIPTIONS = {
    "COMPLETIONS_MODEL": "Nom du modèle de déploiement OpenAI",
    "OPENAI_API_BASE": "URL de base de l'API Azure OpenAI",
    "OPENAI_API_VERSION": "Version de l'API Azure OpenAI",
    "OPENAI_API_KEY": "Clé d'accès pour Azure OpenAI Service",
    "OPENAI_NB_TOKENS": "Nombre maximal de tokens pour les prompts",
    "COMPUTER_VISION_KEY": "Clé d'accès pour Azure Computer Vision",
    "COMPUTER_VISION_ENDPOINT": "URL du service Azure Computer Vision",
    "AIPROJECT_CONNECTION_STRING": "Chaîne de connexion pour l'agent AI Project",
    "AGENT_ID": "ID de l'agent AI Project"
}

def init_env_variables() -> None:
    """Initialise les variables d'environnement à partir du session state de Streamlit et du système"""
    # Initialiser les variables d'environnement dans le session state si elles n'existent pas
    if "env_initialized" not in st.session_state:
        # Essayer de charger à partir du fichier config.json pour la compatibilité
        config_data = {}
        try:
            with open("lib/config.json") as f:
                config_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            st.warning("Fichier config.json non trouvé ou invalide. Utilisation des valeurs par défaut.")
        
        # Initialiser le session state avec les valeurs, en donnant la priorité aux variables d'environnement système
        for var in ENV_VARS:
            # Priorité: 1) Variable d'environnement système, 2) Fichier config.json, 3) Valeur par défaut
            env_value = os.environ.get(var)
            if env_value is not None:
                st.session_state[var] = env_value
            elif var in config_data:
                value = config_data[var]
                # Convertir les valeurs numériques en chaînes pour la session state
                if isinstance(value, (int, float)):
                    st.session_state[var] = str(value)
                else:
                    st.session_state[var] = value
            else:
                st.session_state[var] = DEFAULT_VALUES.get(var, "")
        
        st.session_state.env_initialized = True

def get_env_var(var_name: str) -> Any:
    """Récupère une variable d'environnement du session state ou du système"""
    if var_name not in st.session_state:
        init_env_variables()
    
    # Récupérer depuis le session state ou le système
    value = st.session_state.get(var_name, os.environ.get(var_name, DEFAULT_VALUES.get(var_name, "")))
    
    # Convertir les valeurs numériques si nécessaire
    if var_name == "OPENAI_NB_TOKENS" and isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return DEFAULT_VALUES.get("OPENAI_NB_TOKENS", 4000)
    
    return value

def update_env_vars(updated_values: Dict[str, str]) -> None:
    """Met à jour les variables d'environnement dans le session state et le système"""
    for var, value in updated_values.items():
        if var in ENV_VARS:
            # Mettre à jour le session state
            st.session_state[var] = value
            
            # Mettre à jour la variable d'environnement système
            # Cela n'affecte que le processus actuel, pas l'environnement système global
            os.environ[var] = value

def save_to_config_file() -> bool:
    """Sauvegarde les variables d'environnement actuelles dans le fichier config.json
    
    Returns:
        bool: True si la sauvegarde a réussi, False sinon
    """
    if "env_initialized" not in st.session_state:
        init_env_variables()
    
    try:
        # Récupérer toutes les variables d'environnement
        config_data = {}
        for var in ENV_VARS:
            value = st.session_state.get(var, DEFAULT_VALUES.get(var, ""))
            # Convertir certaines valeurs en nombres si nécessaire
            if var == "OPENAI_NB_TOKENS" and isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    pass
            config_data[var] = value
        
        # Écrire dans le fichier config.json
        with open("lib/config.json", "w") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde du fichier config.json: {str(e)}")
        return False

def get_all_env_vars() -> Dict[str, str]:
    """Récupère toutes les variables d'environnement configurées
    
    Returns:
        Dict[str, str]: Dictionnaire des variables d'environnement
    """
    if "env_initialized" not in st.session_state:
        init_env_variables()
    
    env_data = {}
    for var in ENV_VARS:
        env_data[var] = st.session_state.get(var, DEFAULT_VALUES.get(var, ""))
    
    return env_data

def get_var_description(var_name: str) -> str:
    """Récupère la description d'une variable
    
    Args:
        var_name (str): Nom de la variable
        
    Returns:
        str: Description de la variable
    """
    return VAR_DESCRIPTIONS.get(var_name, "Aucune description disponible")