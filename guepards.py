
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate, Hasher

#region AUTHENTIFICATION
# la partie authentification
import yaml
from yaml.loader import SafeLoader

with open('authentification.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
try:
    authenticator.login()
except Exception as e:
    st.error(e)


#endregion


#region Présentation de la page principale avec menu latéral ##

# ---Création du menu qui va afficher le menu dans la barre latérale---

if st.session_state.get('authentication_status'):
    
    with st.sidebar:
        # --- Bienvenue + Déconnexion ---
        st.write(f"Bienvenue *{st.session_state.get('name')}*")
        authenticator.logout("Déconnexion")
        
        # Code hexadécimal pour un Jaune Fauve/Ocre :
        COULEUR_FAUVE ='#DAA520'
        COULEUR_NOIRE ='black' # Couleur au survol (hover) : noir
        selection = option_menu(
            menu_title=None,
            options = ["Accueil", "Photos"],
            icons = ["house-check-fill", "image-alt"],
            orientation="vertical", # Maintenez cette orientation pour un look de sidebar
            key="main_menu",
            
            
            styles={
                # --- 1. ÉTAT INACTIF (Parfait, icône/texte en Jaune Fauve) ---
                "nav-link": {
                    "color": COULEUR_FAUVE, 
                    "font-size": "16px",
                    "padding-right": "10px",
                },
                
                # --- 2. ÉTAT SÉLECTIONNÉ (CORRIGÉ : Jaune Fauve en fond, Noir en texte) ---
                "nav-link-selected": {
                    "background-color": COULEUR_FAUVE, # Nouvelle couleur de fond : Jaune Fauve
                    "color": COULEUR_NOIRE,           # Nouvelle couleur de texte/icône : Noir
                },
                
                # --- 3. ÉTAT SURVOLÉ (Parfait, icône/texte en Noir) ---
                "nav-link:hover": {
                    "color": COULEUR_NOIRE, 
                },
            }
        )

    # ---On indique au programme quoi faire en fonction du choix---


    if selection == "Accueil":
    #--- Contenu principal de la page "Accueil" ---
        st.title("Bienvenue sur la page d'accueil du site dédié aux Guépards!")

        st.image(
            "images/gif_guepards.gif", 
            caption="Mon magnifique Guépard", # (Optionnel : ajoute une légende sous le GIF)
            width='stretch' # (Optionnel : force le GIF à prendre toute la largeur de la colonne)
        )
        
    elif selection == "Photos":
    #--- Contenu principal de la page "Photos" ---
        st.title("Bienvenue sur mon album photo")
        
        # Création de 3 colonnes 
        col1, col2, col3 = st.columns(3)


        # Initialisation des compteurs au début du script (avant la logique du menu)
        if 'likes_photo1' not in st.session_state:
            st.session_state.likes_photo1 = 0
        if 'likes_photo2' not in st.session_state:
            st.session_state.likes_photo2 = 0
        if 'likes_photo3' not in st.session_state:
            st.session_state.likes_photo3 = 0
        # Contenu de la première colonne : 
        with col1:
            st.write("Guépard et son petit")
            st.image("images/guepard_bb_2.jpeg")
            if st.button(f"👍 ({st.session_state.likes_photo1})", key="btn1"):
                st.session_state.likes_photo1 += 1

        # Contenu de la deuxième colonne :
        with col2:
            st.write("Bébé Guépard")
            st.image("images/bb.jpg")
            if st.button(f"👍 ({st.session_state.likes_photo2})", key="btn2"):
                st.session_state.likes_photo2 += 1
                
        # Contenu de la troisième colonne : 
        with col3:
            st.write("Groupe de Guépards")
            st.image("images/gp3_guepards.jpg")
            if st.button(f"👍 ({st.session_state.likes_photo3})", key="btn3"):
                st.session_state.likes_photo3 += 1
                
                
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password incorrecte')
elif st.session_state.get('authentication_status') is None:
    st.warning('Merci de renseigner vos identifiants')
#endregion