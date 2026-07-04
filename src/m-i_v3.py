import os
import shutil
import re
from datetime import datetime

# ==============================================================================
# 1. MATRICE DE CONFIGURATION (L'ÉTAT IDÉAL CIBLE)
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

# Regex pour détecter les structures anarchiques à dissoudre
ANARCHIC_FOLDERS_PATTERN = re.compile(
    r"(nouveau_dossier|vrac|sans_titre|telechargements|downloads|bazar|stuff|recup|trier)", 
    re.IGNORECASE
)

# Répertoires cibles protégés contre l'extraction
PROTECTED_FOLDERS = [
    "01_pdf_documents", "02_markdown_notes", "03_latex_sources", 
    "04_code_scripts", "05_archives", "06_data_spreadsheets", 
    "07_administrative_records", "99_non_classes"
]

ROUTING_MATRIX = {
    ".pdf":  ("BASE_DOCUMENTS", "01_PDF_Documents"),
    ".md":   ("BASE_DOCUMENTS", "02_Markdown_Notes"),
    ".tex":  ("BASE_DOCUMENTS", "03_LaTeX_Sources"),
    ".bib":  ("BASE_DOCUMENTS", "03_LaTeX_Sources"),
    ".py":   ("BASE_DOCUMENTS", "04_Code_Scripts"),
    ".c":    ("BASE_DOCUMENTS", "04_Code_Scripts"),
    ".cpp":  ("BASE_DOCUMENTS", "04_Code_Scripts"),
    ".h":    ("BASE_DOCUMENTS", "04_Code_Scripts"),
    ".zip":  ("BASE_DOCUMENTS", "05_Archives"),
    ".tar":  ("BASE_DOCUMENTS", "05_Archives"),
    ".gz":   ("BASE_DOCUMENTS", "05_Archives"),
    ".rar":  ("BASE_DOCUMENTS", "05_Archives"),
    ".xlsx": ("BASE_DOCUMENTS", "06_Data_Spreadsheets"),
    ".csv":  ("BASE_DOCUMENTS", "06_Data_Spreadsheets"),
    ".jpg":  ("MEDIA_IMAGES", ""),
    ".jpeg": ("MEDIA_IMAGES", ""),
    ".png":  ("MEDIA_IMAGES", ""),
    ".mp4":  ("MEDIA_VIDEOS", ""),
    ".mkv":  ("MEDIA_VIDEOS", ""),
    ".mp3":  ("MEDIA_AUDIO", ""),
    ".wav":  ("MEDIA_AUDIO", "")
}

JUNK_EXTENSIONS = {".tmp", ".crdownload", ".ds_store", ".lnk"}

# ==============================================================================
# 2. FONCTIONS UTILITAIRES (NORMALISATION ET COLLISION)
# ==============================================================================
def sanitize_name(filename):
    """Normalise le nom en snake_case strict."""
    name, ext = os.path.splitext(filename)
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[_\s-]+", "_", name)
    return f"{name.strip('_')}{ext.lower()}"

def resolve_collision(target_path):
    """Gère les doublons par incrémentation déterministe."""
    if not os.path.exists(target_path):
        return target_path
    
    base, ext = os.path.splitext(target_path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"

# ==============================================================================
# 3. MOTEUR DE CONVERGENTÉ (LOGIQUE PRINCIPALE)
# ==============================================================================
def execute_fs_convergence():
    """Analyse récursive et dissolution des structures incohérentes."""
    print(f"[{datetime.now().isoformat()}] Lancement du pipeline de convergence...")

    for source_root in SRC_DIRECTORIES:
        if not os.path.exists(source_root):
            continue

        # Parcours Depth-First Search (DFS) en partant du plus profond (topdown=False)
        for current_path, subdirs, files in os.walk(source_root, topdown=False):
            folder_name = os.path.basename(current_path)
            
            # Détection des états du dossier courant
            is_source_root = (current_path == source_root)
            is_protected = folder_name.lower() in PROTECTED_FOLDERS
            is_anarchic = bool(ANARCHIC_FOLDERS_PATTERN.search(folder_name))

            # Règle de décision : on traite si c'est la racine ou un dossier anarchique non protégé
            should_process = is_source_root or (is_anarchic and not is_protected)

            if not should_process:
                continue

            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                full_file_path = os.path.join(current_path, file)

                # Élimination immédiate du bruit (Junk)
                if file_ext in JUNK_EXTENSIONS:
                    try:
                        os.remove(full_file_path)
                        print(f"[PURGE JUNK] -> {file}")
                    except Exception:
                        pass
                    continue

                # Calcul du routage cible selon la matrice
                if file_ext in ROUTING_MATRIX:
                    dest_key, subfolder = ROUTING_MATRIX[file_ext]
                    base_dest_path = GLOBAL_DESTINATIONS[dest_key]
                else:
                    # Routage par défaut (Non classé)
                    base_dest_path = GLOBAL_DESTINATIONS["BASE_DOCUMENTS"]
                    subfolder = "99_Non_Classes"

                # Normalisation sémantique du fichier
                normalized_name = sanitize_name(file)
                target_dir = os.path.join(base_dest_path, subfolder)
                target_file_path = os.path.join(target_dir, normalized_name)

                # Propriété d'Idempotence : Si le fichier est déjà à sa place idéale, on ne fait rien
                if full_file_path == target_file_path:
                    continue

                # Exécution sécurisée de la mutation (Déplacement)
                os.makedirs(target_dir, exist_ok=True)
                final_destination = resolve_collision(target_file_path)

                try:
                    shutil.move(full_file_path, final_destination)
                    print(f"[CONVERGENCE] {file} -> {os.path.relpath(final_destination, USER_PROFILE)}")
                except Exception as e:
                    print(f"[ERREUR MUTATION] {file} : {e}")

            # Dissolution des coquilles vides (Nettoyage post-extraction)
            if not is_source_root and is_anarchic:
                try:
                    if not os.listdir(current_path):
                        os.rmdir(current_path)
                        print(f"[DISSOLUTION DOSSIER] {folder_name} supprimé.")
                except Exception:
                    pass

    print(f"[{datetime.now().isoformat()}] Système de fichiers convergent et stable.")

if __name__ == "__main__":
    execute_fs_convergence()