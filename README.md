# 📚 Démonstrations IA

#### 🙌 Contributeur
| Nom | Fonction | Entreprise | Profil |
| --- | --- | --- | --- | 
| Alexandre FOURDRAINE | Technical Specialist - Data & AI | Microsoft France | 👨‍💼 [Linkedin](https://www.linkedin.com/in/alexandre-fourdraine-5a338a29/)|
| Etienne SIGWALD | Technical Specialist - Data & AI | Microsoft France | 👨‍💼 [Linkedin](https://www.linkedin.com/in/etienne-sigwald/)|

        
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
           
