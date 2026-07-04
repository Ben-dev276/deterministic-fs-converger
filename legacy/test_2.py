import os
import shutil

# 1. DÉTECTION DES DOSSIERS PRINCIPAUX DE WINDOWS
USER_PROFILE = os.path.expanduser("~")
DOWNLOADS_PATH = os.path.join(USER_PROFILE, "Downloads")
DOCUMENTS_PATH = os.path.join(USER_PROFILE, "Documents")

# Dossiers cibles pour envoyer les fichiers (Images, Vidéos) sans toucher au reste de ces dossiers
SYSTEM_VIDEOS_PATH = os.path.join(USER_PROFILE, "Videos")
SYSTEM_IMAGES_PATH = os.path.join(USER_PROFILE, "Pictures")

# Les dossiers à analyser (uniquement Téléchargements et Documents)
DOSSIERS_A_TRIER = [DOWNLOADS_PATH, DOCUMENTS_PATH]

# Extensions de fichiers temporaires à supprimer
JUNK_EXTENSIONS = [".tmp", ".crdownload", ".ds_store"]


def get_new_filename(path):
    """Gère les doublons en ajoutant un numéro (1), (2), etc."""
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base}({counter}){ext}"
        counter += 1
    return new_path


def orienter_fichier(nom_fichier, ext, chemin_origine):
    """
    Analyse le nom et l'extension du fichier pour renvoyer le dossier de destination idéal.
    """
    nom_minuscule = nom_fichier.lower()
    ext_minuscule = ext.lower()

    # --- TRI INTELLIGENT PAR NOM ---
    # Détection des Lettres de Motivation (commence par LM ou contient lettre de motivation)
    if ext_minuscule in [".pdf", ".docx", ".doc"] and (nom_minuscule.startswith("lm") or "lettre de motivation" in nom_minuscule):
        return os.path.join(DOCUMENTS_PATH, "Lettres de Motivation")
    
    # Détection des relevés
    if "releve" in nom_minuscule or "facture" in nom_minuscule:
        return os.path.join(DOCUMENTS_PATH, "Relevés et Factures")
        
    # Détection des captures d'écran -> direction le dossier Images global de Windows
    if ext_minuscule in [".jpg", ".jpeg", ".png"] and ("capture" in nom_minuscule or "screenshot" in nom_minuscule):
        return SYSTEM_IMAGES_PATH

    # --- TRI PAR EXTENSION (Si pas filtré par le nom avant) ---
    # Les Vidéos trouvées vont directement dans le dossier "Vidéos" général de Windows
    if ext_minuscule in [".mp4", ".mkv", ".mov", ".avi"]:
        return SYSTEM_VIDEOS_PATH

    # Les autres Images (qui ne sont pas des captures) vont dans Documents > Images Triées
    if ext_minuscule in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        return os.path.join(DOCUMENTS_PATH, "Images Triées")

    # Tri des documents classiques dans le dossier Documents
    if ext_minuscule == ".pdf":
        return os.path.join(DOCUMENTS_PATH, "Fichiers PDF")
    if ext_minuscule in [".docx", ".doc", ".txt", ".odt"]:
        return os.path.join(DOCUMENTS_PATH, "Fichiers Texte")
    if ext_minuscule in [".xlsx", ".xls", ".csv"]:
        return os.path.join(DOCUMENTS_PATH, "Tableaux Excel")
    if ext_minuscule in [".zip", ".rar", ".7z"]:
        return os.path.join(DOCUMENTS_PATH, "Archives ZIP")
    if ext_minuscule in [".exe", ".msi"]:
        return os.path.join(DOCUMENTS_PATH, "Installateurs Logiciels")

    # Si le type de fichier n'est pas reconnu, on ne le touche pas
    return None


# --- SCRIPT PRINCIPAL ---
print("Lancement du tri intelligent...")

for dossier_racine in DOSSIERS_A_TRIER:
    if not os.path.exists(dossier_racine):
        continue
        
    print(f"Analyse du dossier : {dossier_racine}")
    
    for element in os.listdir(dossier_racine):
        chemin_element = os.path.join(dossier_racine, element)
        
        # IMPORTANT : On ne touche PAS aux dossiers déjà existants pour ne pas casser votre organisation
        if os.path.isdir(chemin_element):
            continue
            
        nom_fichier, ext = os.path.splitext(element)
        
        # Suppression des fichiers inutiles/temporaires
        if ext.lower() in JUNK_EXTENSIONS:
            try:
                os.remove(chemin_element)
                print(f"Supprimé (Junk) : {element}")
            except Exception as e:
                print(f"Impossible de supprimer {element}: {e}")
            continue
            
        # Trouver la bonne destination
        dossier_destination = orienter_fichier(nom_fichier, ext, dossier_racine)
        
        # Si on a trouvé une destination valide et qu'elle est différente du dossier actuel
        if dossier_destination and dossier_destination != dossier_racine:
            # Créer le dossier de destination s'il n'existe pas encore
            os.makedirs(dossier_destination, exist_ok=True)
            
            # Préparer le nouveau chemin complet et déplacer
            nouveau_chemin = os.path.join(dossier_destination, element)
            nouveau_chemin_final = get_new_filename(nouveau_chemin)
            
            try:
                shutil.move(chemin_element, nouveau_chemin_final)
                print(f"Déplacé : {element} -> {os.path.basename(dossier_destination)}")
            except Exception as e:
                print(f"Erreur lors du déplacement de {element}: {e}")

print("Tri terminé avec succès !")