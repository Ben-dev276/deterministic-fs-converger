import os
import shutil
import re
from datetime import datetime

# ==============================================================================
# CONFIGURATION
# ==============================================================================
USER_PROFILE = os.path.expanduser("~")
SRC_DIRECTORIES = [
    os.path.join(USER_PROFILE, "Downloads"),
    os.path.join(USER_PROFILE, "Documents")
]

GLOBAL_DESTINATIONS = {
    "MEDIA_VIDEOS": os.path.join(USER_PROFILE, "Videos"),
    "MEDIA_IMAGES": os.path.join(USER_PROFILE, "Pictures"),
    "MEDIA_AUDIO": os.path.join(USER_PROFILE, "Music"),
    "BASE_DOCUMENTS": os.path.join(USER_PROFILE, "Documents")
}

# Liste noire des noms de dossiers jugés "incohérents" ou "anarchiques"
# Tout fichier trouvé dans ces dossiers sera extrait et trié à sa vraie place.
DOSSIERS_INCOHERENTS_PATTERN = re.compile(
    r"(nouveau_dossier|vrac|sans_titre|telechargements|downloads|bazar|stuff|recup|trier)", 
    re.IGNORECASE
)

# Répertoires protégés (Le script n'ira JAMAIS extraire des fichiers d'ici)
PROTECTED_FOLDER_NAMES = [
    "01_pdf_documents", "02_markdown_notes", "03_latex_sources", 
    "04_code_scripts", "05_datasets_tables", "06_office_docs", 
    "07_archives", "08_executables_installers", "00_administratif_factures"
]

# ==============================================================================
# MATRICE DE ROUTAGE (Identique à votre standard rigoureux)
# ==============================================================================
ROUTING_MATRIX = {
    ".pdf": ("BASE_DOCUMENTS", "01_PDF_Documents"),
    ".md": ("BASE_DOCUMENTS", "02_Markdown_Notes"),
    ".tex": ("BASE_DOCUMENTS", "03_LaTeX_Sources"),
    ".bib": ("BASE_DOCUMENTS", "03_LaTeX_Sources"),
    ".py": ("BASE_DOCUMENTS", "04_Code_Scripts/Python"),
    ".ipynb": ("BASE_DOCUMENTS", "04_Code_Scripts/Notebooks"),
    ".js": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".ts": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".html": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".css": ("BASE_DOCUMENTS", "04_Code_Scripts/Web"),
    ".csv": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".xlsx": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".xls": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".json": ("BASE_DOCUMENTS", "05_Datasets_Tables"),
    ".docx": ("BASE_DOCUMENTS", "06_Office_Docs"),
    ".doc": ("BASE_DOCUMENTS", "06_Office_Docs"),
    ".txt": ("BASE_DOCUMENTS", "06_Office_Docs"),
    ".zip": ("BASE_DOCUMENTS", "07_Archives"),
    ".rar": ("BASE_DOCUMENTS", "07_Archives"),
    ".7z": ("BASE_DOCUMENTS", "07_Archives"),
    ".exe": ("BASE_DOCUMENTS", "08_Executables_Installers"),
    ".msi": ("BASE_DOCUMENTS", "08_Executables_Installers"),
    ".mp4": ("MEDIA_VIDEOS", ""),
    ".mkv": ("MEDIA_VIDEOS", ""),
    ".mov": ("MEDIA_VIDEOS", ""),
    ".jpg": ("MEDIA_IMAGES", ""),
    ".jpeg": ("MEDIA_IMAGES", ""),
    ".png": ("MEDIA_IMAGES", ""),
    ".mp3": ("MEDIA_AUDIO", ""),
    ".wav": ("MEDIA_AUDIO", "")
}

JUNK_EXTENSIONS = {".tmp", ".crdownload", ".ds_store", ".log", ".cache"}

# ==============================================================================
# FONCTIONS REQUISES
# ==============================================================================
def sanitize_string(string: str) -> str:
    import unicodedata
    string = ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn')
    string = re.sub(r'[^a-zA-Z0-9]', '_', string)
    string = re.sub(r'_+', '_', string)
    return string.strip('_').lower()

def resolve_collision(target_path: str) -> str:
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
    fn_lower = filename.lower()
    if ext in [".pdf", ".docx", ".xlsx"] and any(k in fn_lower for k in ["facture", "releve", "impot", "bulletin", "paie", "edf"]):
        return os.path.join("00_Administratif_Factures", datetime.now().strftime("%Y_%m"))
    if any(k in fn_lower for k in ["lm", "cv", "candidature", "motivation", "resume"]):
        return os.path.join("06_Office_Docs", "Carrieres_Recrutement")
    return base_subfolder

# ==============================================================================
# PIPELINE EXÉCUTIF RÉCURSIF
# ==============================================================================
def execute_recursive_pipeline():
    print(f"[{datetime.now().isoformat()}] INITIALISATION DU SCAN PROFOND...")
    
    for root_dir in SRC_DIRECTORIES:
        if not os.path.exists(root_dir):
            continue
            
        print(f"[INFO] Analyse récursive de : {root_dir}")
        
        # os.walk(topdown=False) permet de traiter les sous-dossiers du plus profond vers la racine
        # C'est mathématiquement nécessaire pour pouvoir supprimer les dossiers vides sans casser la boucle
        for current_path, subdirs, files in os.walk(root_dir, topdown=False):
            
            # Déterminer le nom du dossier actuel en snake_case pour vérification
            folder_name = os.path.basename(current_path)
            sanitized_folder_name = sanitize_string(folder_name)
            
            # ÉVALUATION DE LA COHÉRENCE DU DOSSIER
            # Si le dossier fait partie de notre structure propre, on n'analyse pas son contenu vrac
            if sanitized_folder_name in PROTECTED_FOLDER_NAMES:
                continue
                
            # Décider si le dossier est "anarchique" ou s'il s'agit d'une racine d'analyse
            est_dossier_incoherent = bool(DOSSIERS_INCOHERENTS_PATTERN.search(sanitized_folder_name))
            est_racine_source = current_path in SRC_DIRECTORIES
            
            # Si le dossier n'est ni une racine, ni un dossier identifié comme incohérent,
            # on le considère par défaut comme une structure que VOUS avez créée. On protège son contenu.
            if not est_racine_source and not est_dossier_incoherent:
                # OPTIONNEL: Si vous voulez quand même extraire les fichiers multimédias (.mp4, .png)
                # des dossiers cohérents, on pourrait ajouter un filtre ici. Pour l'instant, sécurité maximale.
                continue

            # TRAITEMENT DES FICHIERS DANS LES DOSSIERS INCOHÉRENTS OU À LA RACINE
            for file in files:
                full_element_path = os.path.join(current_path, file)
                raw_filename, ext = os.path.splitext(file)
                ext_lower = ext.lower()
                
                if ext_lower in JUNK_EXTENSIONS:
                    try:
                        os.remove(full_element_path)
                    except:
                        pass
                    continue
                
                if ext_lower in ROUTING_MATRIX:
                    dest_key, subfolder = ROUTING_MATRIX[ext_lower]
                    base_dest_path = GLOBAL_DESTINATIONS[dest_key]
                    
                    final_subfolder = compute_smart_subfolder(raw_filename, ext_lower, subfolder)
                    sanitized_name = sanitize_string(raw_filename)
                    normalized_filename = f"{sanitized_name}{ext_lower}"
                    
                    target_directory = os.path.join(base_dest_path, final_subfolder)
                    target_file_path = os.path.join(target_directory, normalized_filename)
                    
                    if full_element_path == target_file_path:
                        continue
                        
                    os.makedirs(target_directory, exist_ok=True)
                    final_destination_path = resolve_collision(target_file_path)
                    
                    try:
                        shutil.move(full_element_path, final_destination_path)
                        print(f"[EXTRACTION] Dossier '{folder_name}' -> {normalized_filename}")
                    except Exception as e:
                        print(f"[ERREUR] Échec du déplacement : {e}")
                        
            # NETTOYAGE DES COQUILLES VIDES
            # Si le sous-dossier incohérent est vidé de ses fichiers, on le supprime
            if not est_racine_source and est_dossier_incoherent:
                try:
                    if not os.listdir(current_path): # Si le dossier est vide
                        os.rmdir(current_path)
                        print(f"[NETTOYAGE] Suppression du dossier vide : {folder_name}")
                except Exception as e:
                    pass

    print(f"[{datetime.now().isoformat()}] Tri profond et dissolution du désordre achevés.")

if __name__ == "__main__":
    execute_recursive_pipeline()