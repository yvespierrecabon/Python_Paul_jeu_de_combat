# 📜 Contexte du Projet : Python_Paul_jeu_de_combat

---

## 📌 **Description du Projet**
Un jeu de combat en Python où des personnages (Gobelin, Chevalier, Mage, Sage, Archer) s'affrontent en utilisant des pouvoirs et des artefacts.
Le projet utilise :
- **L'héritage** pour spécialiser les personnages.
- **La gestion des combats** via une fonction `duel()`.
- **La sauvegarde des résultats** dans un fichier `combats.txt` avec horodatage.

---

---

## 🏗️ **Architecture du Projet**

### **Fichiers Principaux**
| Fichier          | Rôle                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| `personnage.py`  | Contient les classes `Personnage`, `Gobelin`, `Chevalier`, `Archer`, `Mage`, `Sage`.      |
| `pouvoir.py`     | Contient la classe `Pouvoir` (nom + dégâts).                                              |
| `main.py`        | Contient la logique des combats (`duel()`), la sauvegarde des résultats, et la fonction `main()`. |
| `combats.txt`    | Fichier de log où sont sauvegardés les résultats des combats avec horodatage.              |

---

### **Classes et Hiérarchie**
```mermaid
classDiagram
    Personnage <|-- Gobelin
    Personnage <|-- Chevalier
    Personnage <|-- Archer
    Personnage <|-- Mage
    Personnage <|-- Sage
    Personnage : +str nom
    Personnage : +str _categorie
    Personnage : +int _pv
    Personnage : +list[Pouvoir] pouvoirs
    Personnage : +list[str] artefacts
    Personnage : +est_vivant() bool
    Personnage : +recevoir_degats(dmg: int) None
    Personnage : +soigner(pts: int) None
    Personnage : +attaquer(cible: Personnage) str
    Personnage : +prendre_artefact(perdant: Personnage) str
    Chevalier : +float _resistance
    Chevalier : +recevoir_degats(dmg: int) None
    Mage : +int puissance_magique
    Mage : +attaquer(cible: Personnage) str
    Sage : +float pouvoir
    Sage : +int potion
    Sage : +boire_potion() None
    Sage : +attaquer(cible: Personnage) str
```

---

---

## ✅ **Points Forts du Code**
1. **Structure Modulaire** :
   - Séparation claire entre les classes (`Personnage`, `Pouvoir`) et la logique (`main.py`).
   - Utilisation de l'**héritage** pour spécialiser les personnages.

2. **Typage** :
   - Utilisation de `-> type` pour les méthodes.
   - Typage des paramètres (ex: `p1: Personnage`).

3. **Gestion des Fichiers** :
   - Sauvegarde des résultats dans `combats.txt` avec horodatage (`datetime.now()`).
   - Utilisation de `with open(...)` pour une gestion sécurisée des fichiers.

4. **Logique de Combat** :
   - Fonction `duel()` bien structurée pour gérer les tours et les conditions de victoire.
   - Gestion des artefacts via `prendre_artefact()`.

5. **Affichage Lisible** :
   - Utilisation de f-strings pour les chaînes dynamiques.
   - Affichage des artefacts sans crochets (`", ".join(self.artefacts)`).

---

---

## 🔧 **Points à Améliorer (Optionnels)**

| Fichier/Classe       | Problème                          | Suggestion                                                                 |
|----------------------|-----------------------------------|-----------------------------------------------------------------------------|
| `duel()`             | Pas de vérification initiale      | Ajouter une vérification pour éviter les combats avec des personnages déjà morts. |
| `duel()`             | `prendre_artefact` appelé même si le perdant n'a pas d'artefacts | Vérifier si `perdant.artefacts` n'est pas vide avant d'appeler la méthode. |
| `main.py`            | `histo_` peu clair                 | Utiliser `histo[-1]` pour sauvegarder le dernier message.                  |
| `Personnage.attaquer`| Concatenations de chaînes          | Remplacer par des f-strings pour plus de lisibilité.                     |
| `pouvoir.py`         | Typage de `__str__` manquant        | Ajouter `-> str` à la méthode `__str__`.                                  |

---

---

## 📂 **Exemple de Code Clé**

### **Classe `Personnage`**
```python
class Personnage:
    def __init__(self, nom: str, _categorie: str, _pv: int, pouvoirs: list[Pouvoir] | None = None, artefacts: List[str] | None = None):
        if artefacts is None:
            artefacts = ['Artefact initial']
        self.nom = nom
        self._categorie = _categorie
        self._pv = _pv
        self._pv_max = _pv
        self.pouvoirs = pouvoirs or []
        self.artefacts = artefacts

    def __str__(self) -> str:
        artefacts_str = ", ".join(self.artefacts) if self.artefacts else "aucun"
        return f"{self.nom}({self._categorie}) PV {self._pv} Artefacts ({artefacts_str})"
```

### **Fonction `duel()`**
```python
def duel(p1: Personnage, p2: Personnage):
    historique = []
    print(f'\n--- Début du combat : {p1.nom} vs {p2.nom} ---')
    while p1.est_vivant() and p2.est_vivant():
        historique.append(p1.attaquer(p2))
        if not p2.est_vivant():
            break
        historique.append(p2.attaquer(p1))
        if not p1.est_vivant():
            break
    if not p2.est_vivant() and p1.est_vivant():
        historique.append(p1.prendre_artefact(p2))
        historique.append(f'Vainqueur : {p1.nom}')
        return p1.nom, historique
    elif not p1.est_vivant() and p2.est_vivant():
        historique.append(p2.prendre_artefact(p1))
        historique.append(f'Vainqueur : {p2.nom}')
        return p2.nom, historique
    else:
        historique.append(f'Aucun vainqueur : {p1.nom} et {p2.nom} sont morts')
        return 'Aucun vainqueur', historique
```

---

---

## 🚀 **Comment Redémarrer une Session**

### **1. Cloner le Dépôt**
```bash
git clone https://github.com/yvespierrecabon/Python_Paul_jeu_de_combat.git
cd Python_Paul_jeu_de_combat
```

### **2. Exécuter le Projet**
```bash
python main.py
```

### **3. Vérifier les Logs**
Les résultats des combats sont sauvegardés dans `combats.txt`.

---

---

## 🤖 **Automatisation de la Mise à Jour du Contexte**

### **Option 1 : Script Python pour Générer `CONTEXT.md`**
Crée un fichier `update_context.py` :
```python
import os
from datetime import datetime

def generate_context():
    context = f"""# 📜 Contexte du Projet : Python_Paul_jeu_de_combat

---
## 📅 **Dernière Mise à Jour : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**

### **Fichiers Modifiés Récemment**
```bash
git log --oneline -5
```

### **Structure Actuelle**
- Fichiers : {os.listdir('.')}

### **Points Clés**
- Voir le fichier `CONTEXT.md` pour plus de détails.
"""
    with open("CONTEXT.md", "w", encoding="utf-8") as f:
        f.write(context)

if __name__ == "__main__":
    generate_context()
```

**Exécution** :
```bash
python update_context.py
git add CONTEXT.md
git commit -m "Mise à jour du contexte"
git push origin main
```

---

### **Option 2 : Utiliser un Hook Git (Automatisé)**
1. Crée un fichier `.git/hooks/pre-commit` (rends-le exécutable avec `chmod +x .git/hooks/pre-commit`) :
   ```bash
   #!/bin/sh
   python update_context.py
   git add CONTEXT.md
   ```

2. À chaque `git commit`, le fichier `CONTEXT.md` sera **automatiquement mis à jour**.

---

---

## 📝 **Historique des Modifications**
| Date               | Modification                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| 2025-11-29         | Création des classes `Personnage`, `Pouvoir`, et des classes dérivées.     |
| 2025-11-29         | Ajout de la fonction `duel()` et sauvegarde des résultats dans `combats.txt`. |
| 2025-11-29         | Amélioration de l'affichage des artefacts et typage des méthodes.          |
