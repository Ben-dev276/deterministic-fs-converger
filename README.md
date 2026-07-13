# 🧠 deterministic-fs-converger 🚀

Bienvenue dans **Deterministic FS Converger** ! Un outil d'ingénierie système puissant, conçu avec une **rigueur mathématique et informatique**, pour automatiser le tri, le nettoyage et la normalisation de votre ordinateur.

---

## 🧐 C'est quoi ce projet ?

Imaginez que votre ordinateur soit une chambre totalement en désordre. Ce programme agit comme une "IA" de rangement (un algorithme intelligent) qui :
1. **Fouille partout** : Même au fond des dossiers oubliés grâce à un parcours en profondeur ($DFS$).
2. **Dissout le chaos** : Il repère les dossiers anarchiques (comme `Vrac` ou `Nouveau dossier`) et en extrait les fichiers.
3. **Normalise les noms** : Il renomme vos fichiers proprement selon la norme informatique `snake_case` (exemple : `Lettre_De_Motivation.pdf` devient `lettre_de_motivation.pdf`).
4. **Range au bon endroit** : Chaque fichier est envoyé de manière **déterministe** (toujours la même logique) vers son dossier idéal (Vidéos, PDF, Code, etc.).

> ⚙️ **Note de l'auteur :** Je suis actuellement développeur débutant-intermédiaire en Python (en cours d'apprentissage). J'ai utilisé l'IA pour améliorer mes différents programmes au fil des versions, en partant de mon tout premier script initial nommé `test_1.py` in "legacy" folder.

---

## 🛠️ Comment ça fonctionne ? (Pour les Techs)

Le script fonctionne comme un moteur de règles :
* **Idempotent** : Vous pouvez le lancer 1 fois ou 100 fois, le résultat final sera le même sans créer de bugs.
* **Respectueux** : Il détecte vos dossiers déjà bien rangés et ne les touche jamais.
* **Anti-collision** : Si deux fichiers ont le même nom, il ajoute un suffixe mathématique (`_v1`, `_v2`) pour ne jamais rien écraser.

---

## 🚨 ATTENTION : SÉCURITÉ D'ABORD 🚨

> ⚠️ **Message important pour ma communauté :** > **N'exécutez pas le programme principal directement sur votre vrai système** afin de ne pas impacter ou modifier vos fichiers importants par surprise. Prenez toujours le temps de vérifier le code et de l'adapter à votre propre situation.

---

## 🔬 Envie de tester et de comprendre ?

Si vous êtes curieux et que vous voulez voir le script en action, vous pouvez faire des tests **en ayant l'entière responsabilité de vos fichiers**. 

Pour cela, utilisez le dossier **`legacy`** inclus dans ce projet :
1. Allez dans le dossier `legacy`.
2. Placez-y de faux fichiers en désordre (des faux `.pdf`, `.mp4`, `.txt`).
3. Lancez le script de test_1.py ou test_2.py pour observer comment l'algorithme nettoie et structure le dossier de manière chirurgicale avec des underscores `_`.

---
🔬 *Fait avec rigueur par un passionné de maths et d'info. Codez prudemment !*
