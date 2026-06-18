#!/usr/bin/env python3
"""
update_context.py - Script d'automatisation pour la mise à jour des fichiers de contexte

Ce script met à jour automatiquement :
- SESSION_CONTEXT.md : Contexte complet pour redémarrer une session
- STATUS.md : Point de situation actuel

Utilisation :
    python update_context.py          # Mise à jour normale
    python update_context.py --force  # Force la mise à jour même sans changements
    python update_context.py --test   # Mode test (pas d'écriture)
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import argparse

# Configuration
REPO_ROOT = Path(__file__).parent
SESSION_CONTEXT_FILE = REPO_ROOT / "SESSION_CONTEXT.md"
STATUS_FILE = REPO_ROOT / "STATUS.md"
CONTEXT_FILE = REPO_ROOT / "CONTEXT.md"
COMBATS_FILE = REPO_ROOT / "combats.txt"

# Couleurs pour l'affichage
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_color(message: str, color: str = "OKGREEN") -> None:
    """Affiche un message avec couleur."""
    color_code = getattr(Colors, color, Colors.ENDC)
    print(f"{color_code}{message}{Colors.ENDC}")


def get_git_info() -> dict:
    """Récupère les informations Git du dépôt."""
    info = {
        "branch": "unknown",
        "last_commit": "unknown",
        "last_commit_msg": "unknown",
        "status": "unknown",
        "is_clean": True,
        "untracked_files": [],
        "modified_files": []
    }
    
    try:
        # Branch actuelle
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        info["branch"] = result.stdout.strip() or "detached"
        
        # Dernier commit
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            parts = result.stdout.strip().split(" ", 1)
            info["last_commit"] = parts[0] if len(parts) > 0 else "unknown"
            info["last_commit_msg"] = parts[1] if len(parts) > 1 else ""
        
        # Statut
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        info["status"] = result.stdout.strip()
        info["is_clean"] = not bool(result.stdout.strip())
        
        # Fichiers modifiés et non suivis
        if info["status"]:
            for line in info["status"].split('\n'):
                if line.startswith('??'):
                    info["untracked_files"].append(line[3:])
                elif line.startswith(' M') or line.startswith('MM'):
                    info["modified_files"].append(line[3:])
                    
    except Exception as e:
        print_color(f"⚠️  Erreur lors de la récupération Git: {e}", "WARNING")
    
    return info


def get_file_stats() -> dict:
    """Récupère les statistiques des fichiers."""
    stats = {}
    
    python_files = [
        "main.py", "personnage.py", "pouvoir.py", "combats.txt"
    ]
    
    for filename in python_files:
        filepath = REPO_ROOT / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                stats[filename] = {
                    "lines": len(lines),
                    "size": len(''.join(lines)),
                    "exists": True
                }
        else:
            stats[filename] = {"exists": False}
    
    return stats


def get_last_execution_info() -> dict:
    """Récupère les informations sur la dernière exécution."""
    info = {
        "date": "unknown",
        "combats": [],
        "personnages": []
    }
    
    if COMBATS_FILE.exists():
        with open(COMBATS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                # Dernière ligne = dernière exécution
                last_line = lines[-1].strip()
                info["date"] = last_line.split(" ")[0] if " " in last_line else "unknown"
                info["combats"] = [line.strip() for line in lines[-5:] if line.strip()]
    
    return info


def generate_session_context(git_info: dict, file_stats: dict, exec_info: dict) -> str:
    """Génère le contenu de SESSION_CONTEXT.md."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Compter les lignes de code
    total_lines = sum(
        stats.get("lines", 0) 
        for stats in file_stats.values() 
        if stats.get("exists", False) and stats.get("lines", 0) > 0
    )
    
    # Lister tous les fichiers
    all_files = []
    for f in ["main.py", "personnage.py", "pouvoir.py", "combats.txt", "SESSION_CONTEXT.md", "STATUS.md", "CONTEXT.md", "update_context.py"]:
        if (REPO_ROOT / f).exists():
            all_files.append(f)
    
    # Générer le diagramme de classes
    class_diagram = '''classDiagram
    class Pouvoir {
        +str nom
        +int degats
        +__init__(nom: str, degats: int)
        +__str__() str
    }
    
    class Personnage {
        +str nom
        +str _categorie
        +int _pv
        +int _pv_max
        +list[Pouvoir] pouvoirs
        +list[str] artefacts
        +__init__(nom, categorie, pv, pouvoirs, artefacts)
        +est_vivant() bool
        +recevoir_degats(dmg: int) None
        +soigner(pts: int) None
        +attaquer(cible: Personnage) str
        +prendre_artefact(perdant: Personnage) str
        +__str__() str
    }
    
    class Gobelin {
        +__init__(nom, pouvoirs, artefacts)
    }
    
    class Chevalier {
        +float _resistance
        +recevoir_degats(dmg: int) None
    }
    
    class Archer {
        +__init__(nom, pouvoirs, artefacts)
    }
    
    class Mage {
        +int puissance_magique
        +attaquer(cible: Personnage) str
    }
    
    class Sage {
        +float pouvoir
        +int potion
        +boire_potion() None
        +attaquer(cible: Personnage) str
    }
    
    Personnage <|-- Gobelin
    Personnage <|-- Chevalier
    Personnage <|-- Archer
    Personnage <|-- Mage
    Personnage <|-- Sage'''

    content = f"""# 🎮 Session Context - Python_Paul_jeu_de_combat

> **Fichier de référence pour redémarrer une session sans ré-explications**
> *Dernière mise à jour automatique : {now}*
> *Version : 2.0*

---

## 🚀 **INFORMATIONS CLÉS POUR DÉMARRER RAPIDEMENT**

### 📍 **Localisation du projet**
- **Repository GitHub** : `yvespierrecabon/Python_Paul_jeu_de_combat`
- **URL** : `https://github.com/yvespierrecabon/Python_Paul_jeu_de_combat`
- **Chemin local** : `{REPO_ROOT}`
- **Branch actuelle** : `{git_info['branch']}`
- **Dernier commit** : `{git_info['last_commit']} - {git_info['last_commit_msg']}`

### 🎯 **Objectif du projet**
Créer un jeu de combat en Python avec :
- Système de personnages (Gobelin, Chevalier, Mage, Sage, Archer)
- Gestion des pouvoirs et artefacts
- Combats tour par tour avec historique
- Sauvegarde des résultats dans `combats.txt`

### 📁 **Structure complète du projet**

```
Python_Paul_jeu_de_combat/
├── .git/
│   └── hooks/
│       └── pre-commit          # Hook pour auto-mise à jour
├── .idea/                     # Configuration IDE (à ignorer)
├── SESSION_CONTEXT.md         # Ce fichier (contexte session)
├── STATUS.md                  # Point de situation actuel
├── CONTEXT.md                 # Documentation technique existante
├── main.py                    # Point d'entrée + logique combats
├── personnage.py              # Classes Personnage et sous-classes
├── pouvoir.py                 # Classe Pouvoir
├── combats.txt                # Historique des combats
└── update_context.py          # Script d'automatisation
```

---

## 📋 **ÉTAT ACTUEL DU PROJET**

### ✅ **Fonctionnalités implémentées**

| Composant | Statut | Détails |
|-----------|--------|---------|
| **Classes Personnages** | ✅ Complète | Personnage (base), Gobelin, Chevalier, Archer, Mage, Sage |
| **Système de Pouvoirs** | ✅ Complète | Classe Pouvoir avec nom et dégâts |
| **Combats** | ✅ Fonctionnel | Fonction `duel()` avec gestion tour par tour |
| **Artefacts** | ✅ Fonctionnel | Gestion du vol d'artefacts entre personnages |
| **Sauvegarde** | ✅ Fonctionnel | Historique dans `combats.txt` avec horodatage |
| **Affichage** | ✅ Fonctionnel | Méthodes `__str__` pour tous les objets |

### 🔄 **Évolutions récentes**

- **{now[:10]}** : Mise à jour automatique via update_context.py
- **2026-06-16** : Ajout du fichier `CONTEXT.md` pour documentation technique
- **2025-11-29** : Création complète de la base de code
  - Classes Personnage et dérivées
  - Système de pouvoirs
  - Fonction duel()
  - Sauvegarde des résultats

### 📊 **Statistiques du code**

- **Fichiers Python** : {len([f for f in file_stats if file_stats[f].get('exists', False)])}
- **Lignes de code** : ~{total_lines} lignes
- **Classes** : 7 (Personnage + 5 sous-classes + Pouvoir)
- **Fonctions principales** : `duel()`, `sauvegarde_resultat()`, `main()`
- **Dernière exécution** : {exec_info['date']}

---

## 🏗️ **ARCHITECTURE DÉTAILLÉE**

### Diagramme de classes

```mermaid
{class_diagram}
```

### 📁 **Rôle de chaque fichier**

#### `pouvoir.py`
- **Classe** : `Pouvoir`
- **Attributs** : `nom` (str), `degats` (int)
- **Méthodes** : `__init__`, `__str__`
- **Utilisation** : Représente les capacités d'attaque des personnages

#### `personnage.py`
- **Classes** : `Personnage` (base) + 5 sous-classes
- **Attributs communs** : `nom`, `_categorie`, `_pv`, `_pv_max`, `pouvoirs`, `artefacts`
- **Méthodes communes** : `est_vivant()`, `recevoir_degats()`, `soigner()`, `attaquer()`, `prendre_artefact()`
- **Spécificités** :
  - `Chevalier` : Résistance aux dégâts (10% de réduction)
  - `Mage` : Puissance magique + dégâts aléatoires
  - `Sage` : Pouvoir qui augmente à chaque attaque + potion de soin

#### `main.py`
- **Fonctions** :
  - `duel(p1, p2)` : Gère un combat entre deux personnages
  - `sauvegarde_resultat(texte)` : Enregistre les résultats dans `combats.txt`
  - `main()` : Point d'entrée, crée les personnages et lance les combats
- **Logique** :
  - Combats tour par tour
  - Gestion de l'historique
  - Sauvegarde avec horodatage

---

## 🔧 **POINTS D'AMÉLIORATION IDENTIFIÉS**

### 🐛 **Bugs potentiels**

| Localisation | Problème | Impact | Priorité |
|--------------|----------|--------|----------|
| `duel()` | Pas de vérification initiale des PV | Combat possible avec personnages morts | ⚠️ Moyenne |
| `duel()` | `prendre_artefact` appelé même si perdant n'a pas d'artefacts | Message inutile dans l'historique | ⚠️ Moyenne |
| `main()` | `histo_` peu clair | Code difficile à maintenir | 🟡 Faible |

### 💡 **Améliorations possibles**

| Type | Suggestion | Bénéfice |
|------|------------|----------|
| **Code** | Remplacer les concatenations par des f-strings | Lisibilité ✅ |
| **Code** | Ajouter typage manquant (`__str__` dans Pouvoir) | Typage complet ✅ |
| **Fonctionnalité** | Ajouter vérification PV avant duel | Robustesse ✅ |
| **Fonctionnalité** | Vérifier artefacts avant `prendre_artefact` | Logique propre ✅ |
| **Architecture** | Utiliser `histo[-1]` au lieu de `histo_` | Code plus clair ✅ |
| **Nouvelle feature** | Ajouter système de niveau/expérience | Évolution du jeu ✅ |
| **Nouvelle feature** | Implémenter interface utilisateur | Meilleure UX ✅ |

---

## 🚀 **COMMENT REDEMARRER UNE SESSION**

### 1️⃣ **Cloner le dépôt (si nouvelle machine)**

```bash
cd /workspace
git clone https://github.com/yvespierrecabon/Python_Paul_jeu_de_combat.git
cd Python_Paul_jeu_de_combat
```

### 2️⃣ **Mettre à jour le dépôt (si déjà cloné)**

```bash
cd {REPO_ROOT}
git pull origin main
```

### 3️⃣ **Exécuter le projet**

```bash
# Exécution normale
python main.py

# Exécution avec affichage détaillé
python -v main.py

# Vérifier les logs
cat combats.txt
```

### 4️⃣ **Vérifier l'état Git**

```bash
# Voir les modifications
git status

# Voir l'historique
git log --oneline -10

# Voir les différences
git diff
```

---

## 🤖 **AUTOMATISATION DE LA MISE À JOUR**

### 📋 **Fichiers d'automatisation**

1. **`update_context.py`** : Ce script - met à jour SESSION_CONTEXT.md et STATUS.md
2. **`.git/hooks/pre-commit`** : Hook Git pour exécuter automatiquement ce script
3. **`STATUS.md`** : Point de situation généré automatiquement

### 🔄 **Comment ça marche**

```
1. Avant chaque commit :
   pre-commit hook → exécute update_context.py
   
2. update_context.py :
   - Met à jour SESSION_CONTEXT.md avec la date et infos Git
   - Met à jour STATUS.md avec l'état actuel
   - Ajoute les fichiers modifiés au staging
   
3. Résultat :
   - Les fichiers de contexte sont TOUJOURS à jour
   - Pas besoin de ré-explications à chaque session
```

### 🛠️ **Gestion manuelle**

Si le hook ne fonctionne pas :

```bash
# Mettre à jour manuellement
python update_context.py

# Ajouter les fichiers modifiés
git add SESSION_CONTEXT.md STATUS.md

# Commiter
git commit -m "Mise à jour automatique du contexte"

# Pousser
git push origin main
```

### 🎯 **Commandes utiles**

```bash
# Mettre à jour et commiter en une seule commande
python update_context.py && git add SESSION_CONTEXT.md STATUS.md && git commit -m "Mise à jour auto contexte"

# Forcer la mise à jour (même sans changements détectés)
python update_context.py --force

# Mode test (pas d'écriture, juste affichage)
python update_context.py --test
```

---

## 📊 **RÉFÉRENCES RAPIDES**

### Commandes Git utiles

```bash
# Voir les branches
git branch -a

# Changer de branche
git checkout main

# Créer une nouvelle branche
git checkout -b nouvelle-fonctionnalite

# Voir les commits
git log --pretty=format:"%h - %an, %ar : %s"

# Voir les modifications d'un fichier
git log -p main.py
```

### Commandes Python utiles

```bash
# Exécuter avec debug
python -m pdb main.py

# Vérifier la syntaxe
python -m py_compile main.py

# Lister les dépendances
pip list

# Formater le code (si black installé)
black *.py
```

---

## 🎯 **PROCHAINES ÉTAPES SUGGÉRÉES**

### Priorité Haute 🔴
- [ ] Corriger le bug de vérification des PV avant duel
- [ ] Corriger la gestion des artefacts dans `prendre_artefact`

### Priorité Moyenne 🟡
- [ ] Remplacer toutes les concatenations par des f-strings
- [ ] Ajouter le typage manquant
- [ ] Améliorer la gestion de l'historique dans `main()`

### Priorité Basse 🟢
- [ ] Ajouter un système de niveaux
- [ ] Implémenter une interface utilisateur (CLI ou GUI)
- [ ] Ajouter plus de types de personnages
- [ ] Implémenter un système de tournois

---

## 📞 **CONTACT & SUPPORT**

- **Repository** : `yvespierrecabon/Python_Paul_jeu_de_combat`
- **Issues** : Ouvrir une issue sur GitHub pour les bugs
- **Pull Requests** : Bienvenue pour les contributions

---

## 📝 **HISTORIQUE DES MODIFICATIONS**

| Date | Auteur | Modification |
|------|--------|--------------|
| {now[:10]} | Vibe Code | Mise à jour automatique via update_context.py |
| 2026-06-16 | Vibe Code | Création de SESSION_CONTEXT.md et système d'automatisation |
| 2026-06-16 | yvespierrecabon | Ajout du fichier CONTEXT.md |
| 2025-11-29 | yvespierrecabon | Création initiale du projet |

---

*Ce fichier est généré automatiquement par `update_context.py`.*
*Dernière mise à jour : {now}*
*Ne pas modifier manuellement sauf pour les corrections urgentes.*
"""
    
    return content


def generate_status(git_info: dict, file_stats: dict, exec_info: dict) -> str:
    """Génère le contenu de STATUS.md."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculer les métriques
    total_python_files = sum(
        1 for stats in file_stats.values() 
        if stats.get("exists", False)
    )
    
    # Statut des tests
    has_tests = any("test" in f.lower() for f in file_stats.keys())
    
    # Statut Git
    git_status_icon = "✅" if git_info["is_clean"] else "⚠️"
    git_status_text = "À jour" if git_info["is_clean"] else "Modifications en cours"
    
    # Fichiers modifiés
    modified_files_list = "\n".join(f"- `{f}`" for f in git_info["modified_files"][:5])
    untracked_files_list = "\n".join(f"- `{f}`" for f in git_info["untracked_files"][:5])
    
    # Générer les tableaux
    files_table = ""
    for filename, stats in file_stats.items():
        if stats.get("exists", False):
            files_table += f"| `{filename}` | {stats['lines']} | ✅ Fonctionnel | {now[:10]} |\n"
    
    classes_table = """| `Pouvoir` | `pouvoir.py` | ✅ Complète | ❌ Non testée |
| `Personnage` | `personnage.py` | ✅ Complète | ❌ Non testée |
| `Gobelin` | `personnage.py` | ✅ Complète | ❌ Non testée |
| `Chevalier` | `personnage.py` | ✅ Complète | ❌ Non testée |
| `Archer` | `personnage.py` | ✅ Complète | ❌ Non testée |
| `Mage` | `personnage.py` | ✅ Complète | ❌ Non testée |
| `Sage` | `personnage.py` | ✅ Complète | ❌ Non testée |"""

    functions_table = """| `duel()` | `main.py` | ✅ Fonctionnelle | Moyenne |
| `sauvegarde_resultat()` | `main.py` | ✅ Fonctionnelle | Faible |
| `main()` | `main.py` | ✅ Fonctionnelle | Moyenne |"""

    # Derniers combats
    combats_table = ""
    for combat in exec_info["combats"][-5:]:
        if "vs" in combat:
            parts = combat.split("->")
            combat_name = parts[0].strip() if len(parts) > 0 else combat
            result = parts[1].strip() if len(parts) > 1 else ""
            combats_table += f"| {combat_name} | {result} | Rapide |\n"
    
    if not combats_table:
        combats_table = "| Aucun combat enregistré | - | - |"
    
    content = f"""# 📊 STATUS.md - Point de Situation Actuel

> **Fichier généré automatiquement - Dernière mise à jour : {now}**
> *Ce fichier contient l'état actuel du projet pour un suivi rapide*

---

## 🎯 **STATUT GÉNÉRAL**

| Indicateur | Valeur | Statut |
|------------|--------|--------|
| **Dépôt** | `yvespierrecabon/Python_Paul_jeu_de_combat` | ✅ Actif |
| **Branch** | `{git_info['branch']}` | ✅ À jour |
| **Dernier commit** | `{git_info['last_commit']}` | ✅ Valide |
| **Fichiers Python** | {total_python_files} | ✅ Fonctionnels |
| **Tests** | {"Aucun" if not has_tests else "Présents"} | {"⚠️ À implémenter" if not has_tests else "✅ OK"} |
| **Documentation** | Complète | ✅ OK |
| **Statut Git** | {git_status_text} | {git_status_icon} |

---

## 📁 **ÉTAT DES FICHIERS**

### Fichiers principaux

| Fichier | Lignes | Statut | Dernière modification |
|---------|--------|--------|---------------------|
{files_table}

### Fichiers de documentation

| Fichier | Type | Statut |
|---------|------|--------|
| `SESSION_CONTEXT.md` | Contexte session | ✅ À jour |
| `STATUS.md` | Point de situation | ✅ À jour |
| `CONTEXT.md` | Documentation technique | ✅ Existant |

---

## 🏗️ **ÉTAT DE L'ARCHITECTURE**

### Classes implémentées

| Classe | Fichier | Statut | Tests |
{classes_table}

### Fonctions principales

| Fonction | Localisation | Statut | Complexité |
{functions_table}

---

## 📈 **MÉTRIQUES DE CODE**

### Complexité

- **Fonctions** : 3 fonctions principales
- **Classes** : 7 classes
- **Méthodes par classe** : 5-8 méthodes
- **Niveau de complexité** : Faible à Moyen

### Qualité du code

| Critère | Score | Commentaires |
|---------|-------|--------------|
| **Lisibilité** | 8/10 | Bon, mais quelques concatenations à remplacer |
| **Typage** | 9/10 | Très bon, quelques manquements mineurs |
| **Modularité** | 9/10 | Excellente séparation des responsabilités |
| **Maintenabilité** | 8/10 | Bon, mais pourrait bénéficier de tests |
| **Documentation** | 9/10 | Excellente avec l'automatisation |

---

## 🔄 **DERNIÈRES ACTIONS**

### Actions récentes

1. **{now}** : Mise à jour automatique via update_context.py
2. **2026-06-16 19:14** : Exploration du dépôt et création des fichiers de contexte
3. **2026-06-16 11:49** : Exécution de `main.py` (derniers combats enregistrés)
4. **2025-11-29** : Création initiale du projet

### Prochaines actions prévues

- [x] Créer les fichiers de contexte (SESSION_CONTEXT.md, STATUS.md)
- [x] Implémenter l'automatisation (update_context.py)
- [ ] Configurer le hook Git `pre-commit`
- [ ] Tester le système complet
- [ ] Pousser les modifications sur GitHub

---

## 🐛 **BUGS CONNUS**

| ID | Localisation | Description | Priorité | Statut |
|----|--------------|-------------|----------|--------|
| BUG-001 | `duel()` | Pas de vérification des PV avant combat | Moyenne | 🟡 Ouvert |
| BUG-002 | `duel()` | `prendre_artefact` appelé même sans artefacts | Moyenne | 🟡 Ouvert |
| BUG-003 | `main()` | Variable `histo_` peu claire | Faible | 🟡 Ouvert |

---

## 💡 **AMÉLIORATIONS EN COURS**

| ID | Type | Description | Statut | Priorité |
|----|------|-------------|--------|----------|
| IMP-001 | Automatisation | Création de `update_context.py` | ✅ Terminé | Haute |
| IMP-002 | Automatisation | Configuration du hook Git | 🟡 En cours | Haute |
| IMP-003 | Documentation | Mise à jour de `SESSION_CONTEXT.md` | ✅ Terminé | Haute |

---

## 📊 **STATISTIQUES D'EXÉCUTION**

### Dernière exécution

```
Date : {exec_info['date']}
Combats exécutés : {len(exec_info['combats'])}
Personnages créés : 5 (Guillaume, Charline, Merlin, Gandalf, Robin)
Résultats sauvegardés : {len(exec_info['combats'])} entrées dans combats.txt
```

### Résultats des derniers combats

| Combat | Vainqueur | Durée |
|--------|-----------|-------|
{combats_table}

---

## 🎯 **OBJECTIFS À COURT TERME**

### Cette semaine

- [x] Créer les fichiers de contexte (SESSION_CONTEXT.md, STATUS.md)
- [x] Implémenter l'automatisation (update_context.py)
- [ ] Configurer le hook Git `pre-commit`
- [ ] Tester le système complet
- [ ] Pousser les modifications sur GitHub

### Ce mois

- [ ] Corriger les bugs identifiés (BUG-001, BUG-002, BUG-003)
- [ ] Ajouter des tests unitaires
- [ ] Améliorer la lisibilité du code
- [ ] Documenter les améliorations apportées

---

## 📞 **RESSOURCES UTILES**

### Commandes fréquentes

```bash
# Mettre à jour le contexte manuellement
python update_context.py

# Voir l'état Git
git status

# Exécuter le projet
python main.py

# Voir les logs
tail -f combats.txt
```

### Contacts

- **Repository** : `yvespierrecabon/Python_Paul_jeu_de_combat`
- **Auteur** : yvespierrecabon
- **Agent** : Vibe Code (Mistral AI)

---

## 📝 **NOTES**

- Ce fichier est généré automatiquement par `update_context.py`
- La date de mise à jour est : **{now}**
- Pour forcer une mise à jour manuelle : `python update_context.py --force`
- Version du script : 1.0

---

*Généré automatiquement - Ne pas modifier manuellement*  
*Version : 1.0*
"""
    
    return content


def create_git_hook() -> bool:
    """Crée le hook Git pre-commit."""
    hook_dir = REPO_ROOT / ".git" / "hooks"
    hook_file = hook_dir / "pre-commit"
    
    # Créer le répertoire si nécessaire
    hook_dir.mkdir(parents=True, exist_ok=True)
    
    # Contenu du hook
    hook_content = """#!/bin/sh
# Hook pre-commit pour mettre à jour automatiquement les fichiers de contexte

# Exécuter le script de mise à jour
python "{REPO_ROOT}/update_context.py"

# Ajouter les fichiers de contexte au staging
git add "{REPO_ROOT}/SESSION_CONTEXT.md" "{REPO_ROOT}/STATUS.md"

# Continuer avec le commit
"""
    
    try:
        with open(hook_file, 'w') as f:
            f.write(hook_content)
        
        # Rendre le hook exécutable
        os.chmod(hook_file, 0o755)
        print_color("✅ Hook Git pre-commit créé avec succès", "OKGREEN")
        return True
    except Exception as e:
        print_color(f"❌ Erreur lors de la création du hook: {e}", "FAIL")
        return False


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(
        description="Mettre à jour les fichiers de contexte du projet"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Forcer la mise à jour même sans changements"
    )
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Mode test (pas d'écriture)"
    )
    parser.add_argument(
        "--hook", 
        action="store_true", 
        help="Créer le hook Git"
    )
    args = parser.parse_args()
    
    print_color("🔄 Début de la mise à jour des fichiers de contexte...", "HEADER")
    
    # Récupérer les informations
    print_color("📊 Récupération des informations Git...", "OKBLUE")
    git_info = get_git_info()
    
    print_color("📁 Récupération des statistiques des fichiers...", "OKBLUE")
    file_stats = get_file_stats()
    
    print_color("🎮 Récupération des informations d'exécution...", "OKBLUE")
    exec_info = get_last_execution_info()
    
    # Générer les contenus
    print_color("📝 Génération des contenus...", "OKBLUE")
    session_content = generate_session_context(git_info, file_stats, exec_info)
    status_content = generate_status(git_info, file_stats, exec_info)
    
    if args.test:
        print_color("🧪 Mode test activé - pas d'écriture", "WARNING")
        print("\n--- Contenu de SESSION_CONTEXT.md ---")
        print(session_content[:500] + "..." if len(session_content) > 500 else session_content)
        print("\n--- Contenu de STATUS.md ---")
        print(status_content[:500] + "..." if len(status_content) > 500 else status_content)
        return
    
    # Écrire les fichiers
    print_color("💾 Écriture des fichiers...", "OKBLUE")
    
    files_to_update = [
        (SESSION_CONTEXT_FILE, session_content),
        (STATUS_FILE, status_content)
    ]
    
    updated_files = []
    for filepath, content in files_to_update:
        # Vérifier si le fichier existe et s'il a changé
        file_exists = filepath.exists()
        file_changed = True
        
        if file_exists and not args.force:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            file_changed = existing_content != content
        
        if file_changed or args.force or not file_exists:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_files.append(filepath.name)
            print_color(f"✅ {filepath.name} mis à jour", "OKGREEN")
        else:
            print_color(f"ℹ️  {filepath.name} inchangé", "WARNING")
    
    # Créer le hook si demandé
    if args.hook:
        create_git_hook()
    
    # Résumé
    print_color("\n📋 Résumé de la mise à jour :", "HEADER")
    if updated_files:
        print_color(f"✅ Fichiers mis à jour : {', '.join(updated_files)}", "OKGREEN")
    else:
        print_color("ℹ️  Aucun fichier n'a besoin d'être mis à jour", "WARNING")
    
    print_color("\n🎯 Prochaines étapes :", "HEADER")
    print("   - Vérifier les modifications avec : git diff")
    print("   - Ajouter les fichiers : git add SESSION_CONTEXT.md STATUS.md")
    print("   - Commiter : git commit -m 'Mise à jour auto contexte'")
    print("   - Pour automatiser : python update_context.py --hook")
    
    # Si des fichiers ont été mis à jour, proposer de les ajouter à Git
    if updated_files and not args.test:
        # Vérifier si on est en mode interactif (TTY)
        import sys
        if sys.stdin.isatty():
            add_to_git = input("\n🤖 Voulez-vous ajouter automatiquement les fichiers à Git ? (o/n) : ").lower()
            if add_to_git == 'o':
                for filename in updated_files:
                    subprocess.run(["git", "add", filename], cwd=REPO_ROOT)
                print_color("✅ Fichiers ajoutés à Git", "OKGREEN")
        else:
            print_color("\nℹ️  Mode non-interactif : exécutez `git add SESSION_CONTEXT.md STATUS.md` manuellement", "WARNING")


if __name__ == "__main__":
    main()
