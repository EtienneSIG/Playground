import streamlit as st
import os

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


if __name__ == "__main__":

    st.title("Upload de PDF")

    # Widget pour uploader un fichier PDF
    uploaded_file = st.file_uploader("Choisissez un fichier PDF", type="pdf")

    if uploaded_file is not None:
        # Sauvegarder le fichier localement
        chemin_fichier = sauvegarder_pdf_local(uploaded_file)
        st.success(f"Fichier sauvegardé avec succès : {chemin_fichier}")
