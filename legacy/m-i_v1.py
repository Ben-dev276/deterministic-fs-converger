import os
import shutil
import re
from datetime import datetime

# ==============================================================================
# CONFIGURATION DES CHEMINS ET ARCHITECTURE TARGET
# ==============================================================================
USER_PROFILE = os.path.expanduser("~")
SRC_DIRECTORIES = [
    os.path.join(USER_PROFILE, "Downloads"),
    os.path.join(USER_PROFILE, "Documents")
]

# Rangement global déporté vers les répertoires dédiés OS X/Windows
GLOBAL_DESTINATIONS = {
    "MEDIA_VIDEOS": os.path.join(USER_PROFILE, "Videos"),
    "MEDIA_IMAGES": os.path.join(USER_PROFILE, "Pictures"),
    "MEDIA_AUDIO": os.path.join(USER_PROFILE, "Music"),
    "BASE_DOCUMENTS": os.path.join(USER_PROFILE, "Documents")
}

# ==============================================================================
# MATRICE DE ROUTAGE EXTENSION -> TARGET_FOLDER
# ==============================================================================
ROUTING_MATRIX = {
    # Documents de recherche & Données
    ".pdf": ("BASE_DOCUMENTS", "01_PDF_Documents"),
    ".md": ("BASE_DOCUMENTS", "02_Markdown_Notes"),
    ".tex": ("BASE_DOCUMENTS", "03_LaTeX_Sources"),
    ".bib": ("BASE_DOCUMENTS", "03_LaTeX_Sources"),
    
    # Notebooks & Code
    ".py": ("BASE_DOCUMENTS", "04_Code_Scripts/Python"),
    ".ipynb": ("BASE_DOCUMENTS", "04_Code_Scripts/Notebooks"),
    ".js": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".ts": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".html": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".css": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".c": ("BASE_DOCUMENTS", "04_Code_Scripts/Low_Level"),
    ".cpp": ("BASE_DOCUMENTS", "04_Code_Scripts/Low_Level"),
    ".sh": ("BASE_DOCUMENTS", "04_Code_Scripts/Shell"),
    
    # Données Structurées & Datasets
    ".csv": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".xlsx": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".xls": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".json": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".xml": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    
    # Bureautique Classique
    ".docx": ("BASE_DOCUMENTS", "06_Office_Docs"),
    ".doc": ("BASE_DOCUMENTS", "06_Office_Docs"),
    ".pptx": ("BASE_DOCUMENTS", "06_Office_Docs"),
    ".txt": ("BASE_DOCUMENTS", "06_Office_Docs"),
    
    # Archives compressées
    ".zip": ("BASE_DOCUMENTS", "07_Archives"),
    ".rar": ("BASE_DOCUMENTS", "07_Archives"),
    ".7z": ("BASE_DOCUMENTS", "07_Archives"),
    ".tar": ("BASE_DOCUMENTS", "07_Archives"),
    ".gz": ("BASE_DOCUMENTS", "07_Archives"),
    
    # Exécutables et Binaires
    ".exe": ("BASE_DOCUMENTS", "08_Executables_Installers"),
    ".msi": ("BASE_DOCUMENTS", "08_Executables_Installers"),
    ".iso": ("BASE_DOCUMENTS", "08_Executables_Installers"),
    
    # Flux Multimédia (Routage direct vers les dossiers systèmes dédiés)
    ".mp4": ("MEDIA_VIDEOS", ""),
    ".mkv": ("MEDIA_VIDEOS", ""),
    ".mov": ("MEDIA_VIDEOS", ""),
    ".avi": ("MEDIA_VIDEOS", ""),
    
    ".jpg": ("MEDIA_IMAGES", ""),
    ".jpeg": ("MEDIA_IMAGES", ""),
    ".png": ("MEDIA_IMAGES", ""),
    ".gif": ("MEDIA_IMAGES", ""),
    ".svg": ("MEDIA_IMAGES", ""),
    ".webp": ("MEDIA_IMAGES", ""),
    
    ".mp3": ("MEDIA_AUDIO", ""),
    ".wav": ("MEDIA_AUDIO", ""),
    ".flac": ("MEDIA_AUDIO", ""),
    ".aac": ("MEDIA_AUDIO", ""),
}

# Fichiers à purger (Filtre anti-bruit)
JUNK_EXTENSIONS = {".tmp", ".crdownload", ".ds_store", ".log", ".cache"}

# ==============================================================================
# ENGIN DE CORRECTION, NORMALISATION ET ROUTAGE
# ==============================================================================

def sanitize_string(string: str) -> str:
    """
    Normalise une chaîne de caractères en appliquant une règle stricte de snake_case.
    Supprime les accents, remplace les caractères spéciaux et espaces par des '_'.
    """
    import unicodedata
    # Déshabillage des accents
    string = ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn')
    # Remplacement de tout caractère non-alphanumérique par un underscore
    string = re.sub(r'[^a-zA-Z0-9]', '_', string)
    # Remplacement des underscores multiples '__+' par un seul '_'
    string = re.sub(r'_+', '_', string)
    return string.strip('_').lower()

def resolve_collision(target_path: str) -> str:
    """
    Algorithme de résolution de collision de noms de fichiers.
    Ajoute un suffixe d'incrémentation arithmétique indexé (n) au format ISO.
    """
    if not os.path.exists(target_path):
        return target_path
    
    base, ext = os.path.splitext(target_path)
    counter = 1
    new_path = f"{base}_v{counter}{ext}"
    
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}_v{counter}{ext}"
        
    return new_path

def compute_smart_subfolder(filename: str, ext: str, base_subfolder: str) -> str:
    """
    Analyse sémantique de premier niveau pour router dynamiquement les documents
    par typologie d'importance (Série temporelle mensuelle pour la facturation).
    """
    fn_lower = filename.lower()
    
    # Extraction et isolation des documents administratifs temporels
    if ext in [".pdf", ".docx", ".xlsx"] and any(k in fn_lower for k in ["facture", "releve", "impot", "bulletin", "paie", "edf"]):
        current_date = datetime.now().strftime("%Y_%m")
        return os.path.join("00_Administratif_Factures", current_date)
        
    # Isolation des CV et Lettres de Motivation
    if any(k in fn_lower for k in ["lm", "cv", "candidature", "motivation", "resume"]):
        return os.path.join("06_Office_Docs", "Carrieres_Recrutement")

    return base_subfolder

# ==============================================================================
# PIPELINE PRINCIPAL D'EXÉCUTION
# ==============================================================================
def execute_pipeline():
    print(f"[{datetime.now().isoformat()}] Début du traitement du système de fichiers...")
    
    for src_dir in SRC_DIRECTORIES:
        if not os.path.exists(src_dir):
            print(f"[WARN] Répertoire source inexistant : {src_dir}")
            continue
            
        print(f"[INFO] Scan du répertoire : {src_dir}")
        
        for element in os.listdir(src_dir):
            full_element_path = os.path.join(src_dir, element)
            
            # CLAUSE DE SÉCURITÉ ABSOLUE : On n'altère aucun dossier déjà existant
            if os.path.isdir(full_element_path):
                continue
                
            raw_filename, ext = os.path.splitext(element)
            ext_lower = ext.lower()
            
            # 1. Traitement des résidus système / Fichiers temporaires
            if ext_lower in JUNK_EXTENSIONS:
                try:
                    os.remove(full_element_path)
                    print(f"[PURGE] Fichier obsolète supprimé : {element}")
                except Exception as e:
                    print(f"[ERREUR] Impossible de purger {element} : {e}")
                continue
            
            # 2. Évaluation de la matrice de routage
            if ext_lower in ROUTING_MATRIX:
                dest_key, subfolder = ROUTING_MATRIX[ext_lower]
                base_dest_path = GLOBAL_DESTINATIONS[dest_key]
                
                # Injection de l'analyse comportementale de nommage pour affiner le sous-dossier
                final_subfolder = compute_smart_subfolder(raw_filename, ext_lower, subfolder)
                
                # Normalisation stricte du nom du fichier
                sanitized_name = sanitize_string(raw_filename)
                normalized_filename = f"{sanitized_name}{ext_lower}"
                
                # Construction déterministe de la destination
                target_directory = os.path.join(base_dest_path, final_subfolder)
                target_file_path = os.path.join(target_directory, normalized_filename)
                
                # Évitement de boucle infinie (si le fichier est déjà à sa place idéale)
                if full_element_path == target_file_path:
                    continue
                    
                # Allocation dynamique des répertoires si non existants
                os.makedirs(target_directory, exist_ok=True)
                
                # Résolution mathématique des collisions de noms
                final_destination_path = resolve_collision(target_file_path)
                
                # Mutation (Déplacement)
                try:
                    shutil.move(full_element_path, final_destination_path)
                    print(f"[OK] {element} -> {os.path.relpath(final_destination_path, USER_PROFILE)}")
                except Exception as e:
                    print(f"[ERREUR] Mutation échouée pour {element} : {e}")
            else:
                # Gestion des extensions non indexées (Routage par défaut vers un pôle d'archivage non classé)
                unclassified_dir = os.path.join(GLOBAL_DESTINATIONS["BASE_DOCUMENTS"], "99_Non_Classes")
                os.makedirs(unclassified_dir, exist_ok=True)
                
                sanitized_name = sanitize_string(raw_filename)
                target_file_path = os.path.join(unclassified_dir, f"{sanitized_name}{ext_lower}")
                final_destination_path = resolve_collision(target_file_path)
                
                try:
                    shutil.move(full_element_path, final_destination_path)
                    print(f"[NON_CLASSIFIÉ] {element} -> Répertoire d'attente 99_Non_Classes")
                except Exception as e:
                    print(f"[ERREUR] Déplacement impossible (Inconnu) {element} : {e}")

    print(f"[{datetime.now().isoformat()}] Opération de tri et normalisation achevée.")

if __name__ == "__main__":
    execute_pipeline()