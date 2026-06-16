# 🤖 Système d'Automatisation du Contexte

> **Guide pour le système de mise à jour automatique des fichiers de contexte**

---

## 📋 **Présentation**

Ce système permet de **maintenir automatiquement à jour** la documentation et le point de situation du projet `Python_Paul_jeu_de_combat`, évitant ainsi de devoir ré-expliquer le contexte à chaque nouvelle session.

---

## 🎯 **Fichiers du système**

| Fichier | Rôle | Mise à jour |
|---------|------|-------------|
| `SESSION_CONTEXT.md` | Contexte complet pour redémarrer une session | ✅ Automatique |
| `STATUS.md` | Point de situation actuel | ✅ Automatique |
| `update_context.py` | Script Python de mise à jour | ❌ Manuel |
| `.git/hooks/pre-commit` | Hook Git pour automatisation | ❌ Manuel |

---

## 🚀 **Comment ça fonctionne**

### 1️⃣ **Mécanisme de base**

```
Avant chaque commit :
    pre-commit hook → exécute update_context.py
    
update_context.py :
    - Récupère les infos Git (branch, dernier commit, statut)
    - Récupère les statistiques des fichiers
    - Récupère les infos d'exécution (derniers combats)
    - Génère SESSION_CONTEXT.md et STATUS.md
    - Met à jour les fichiers
    
Hook Git :
    - Ajoute automatiquement SESSION_CONTEXT.md et STATUS.md au staging
    - Continue le commit normalement
```

### 2️⃣ **Résultat**

- **SESSION_CONTEXT.md** : Toujours à jour avec la dernière date, les infos Git, et l'état du projet
- **STATUS.md** : Toujours à jour avec le statut actuel, les métriques, et les dernières actions
- **Pas de ré-explications** : À chaque nouvelle session, tout est déjà documenté !

---

## 🛠️ **Installation et Configuration**

### 1️⃣ **Prérequis**

- Python 3.6+
- Git installé
- Accès en écriture au dépôt

### 2️⃣ **Configuration initiale**

#### Cloner le dépôt (si ce n'est pas déjà fait)

```bash
cd /workspace
git clone https://github.com/yvespierrecabon/Python_Paul_jeu_de_combat.git
cd Python_Paul_jeu_de_combat
```

#### Créer le hook Git (si ce n'est pas déjà fait)

```bash
# Créer le répertoire des hooks
mkdir -p .git/hooks

# Créer le hook pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# Hook pre-commit pour mettre à jour automatiquement les fichiers de contexte

# Exécuter le script de mise à jour
python /workspace/yvespierrecabon__Python_Paul_jeu_de_combat/update_context.py

# Ajouter les fichiers de contexte au staging
git add /workspace/yvespierrecabon__Python_Paul_jeu_de_combat/SESSION_CONTEXT.md /workspace/yvespierrecabon__Python_Paul_jeu_de_combat/STATUS.md

# Continuer avec le commit
exit 0
EOF

# Rendre le hook exécutable
chmod +x .git/hooks/pre-commit
```

**⚠️ IMPORTANT** : Le hook Git n'est **pas versionné** par Git (il est dans `.git/`). Il doit être recréé manuellement sur chaque machine.

### 3️⃣ **Vérifier l'installation**

```bash
# Vérifier que le hook existe et est exécutable
ls -la .git/hooks/pre-commit

# Tester le script manuellement
python update_context.py

# Vérifier que les fichiers ont été mis à jour
cat SESSION_CONTEXT.md | head -10
cat STATUS.md | head -10
```

---

## 📖 **Utilisation**

### Utilisation normale (automatique)

1. **Faire des modifications** dans le code
2. **Commiter normalement** :
   ```bash
   git add .
   git commit -m "Votre message de commit"
   ```
3. **Le hook s'exécute automatiquement** et met à jour les fichiers de contexte
4. **Pousser sur GitHub** :
   ```bash
   git push origin main
   ```

### Utilisation manuelle

Si vous voulez mettre à jour les fichiers de contexte **sans faire de commit** :

```bash
# Mettre à jour manuellement
python update_context.py

# Ajouter les fichiers modifiés
git add SESSION_CONTEXT.md STATUS.md

# Commiter
git commit -m "Mise à jour manuelle du contexte"
```

### Options du script

```bash
# Mise à jour normale (détecte les changements)
python update_context.py

# Forcer la mise à jour (même sans changements)
python update_context.py --force

# Mode test (pas d'écriture, juste affichage)
python update_context.py --test

# Créer le hook Git
python update_context.py --hook
```

---

## 🎯 **Contenu des fichiers générés**

### SESSION_CONTEXT.md

Ce fichier contient :
- ✅ Informations clés pour démarrer rapidement
- ✅ Localisation du projet et accès
- ✅ État actuel du projet et fonctionnalités
- ✅ Architecture détaillée avec diagramme de classes
- ✅ Points d'amélioration identifiés
- ✅ Instructions pour redémarrer une session
- ✅ Historique des modifications

### STATUS.md

Ce fichier contient :
- ✅ Statut général du projet
- ✅ État des fichiers (lignes, statut)
- ✅ État de l'architecture (classes, fonctions)
- ✅ Métriques de code (qualité, complexité)
- ✅ Dernières actions et prochaines étapes
- ✅ Bugs connus et améliorations en cours
- ✅ Statistiques d'exécution

---

## 🔧 **Personnalisation**

### Modifier le contenu généré

Éditez le fichier `update_context.py` et modifiez les fonctions :
- `generate_session_context()` : Pour modifier SESSION_CONTEXT.md
- `generate_status()` : Pour modifier STATUS.md

### Ajouter de nouvelles métriques

Dans `get_file_stats()` et `get_git_info()`, vous pouvez ajouter :
- Compte de tests unitaires
- Couverture de code
- Complexité cyclomatique
- Autres métriques pertinentes

### Changer la fréquence de mise à jour

Par défaut, la mise à jour se fait à chaque commit. Vous pouvez :
- **Désactiver le hook** : Supprimez `.git/hooks/pre-commit`
- **Mettre à jour moins souvent** : Modifiez le hook pour n'exécuter que sur certains commits
- **Mettre à jour manuellement** : Utilisez `python update_context.py` quand nécessaire

---

## 🐛 **Dépannage**

### Problème : Le hook ne s'exécute pas

**Solutions** :
1. Vérifiez que le hook existe : `ls -la .git/hooks/pre-commit`
2. Vérifiez qu'il est exécutable : `chmod +x .git/hooks/pre-commit`
3. Vérifiez le contenu du hook
4. Testez manuellement : `bash .git/hooks/pre-commit`

### Problème : Les fichiers ne sont pas mis à jour

**Solutions** :
1. Exécutez manuellement : `python update_context.py --force`
2. Vérifiez les permissions : `chmod +x update_context.py`
3. Vérifiez les dépendances Python

### Problème : Erreurs lors de l'exécution

**Solutions** :
1. Vérifiez que Python 3 est installé
2. Vérifiez que vous êtes dans le bon répertoire
3. Exécutez en mode test : `python update_context.py --test`

---

## 📊 **Exemple de workflow**

### Scénario 1 : Développement normal

```bash
# 1. Faire des modifications
vim main.py

# 2. Tester les modifications
python main.py

# 3. Commiter (le hook s'exécute automatiquement)
git add main.py
git commit -m "Amélioration de la fonction duel"

# 4. Pousser
git push origin main

# Résultat : SESSION_CONTEXT.md et STATUS.md sont automatiquement mis à jour !
```

### Scénario 2 : Nouvelle session

```bash
# 1. Cloner le dépôt
git clone https://github.com/yvespierrecabon/Python_Paul_jeu_de_combat.git
cd Python_Paul_jeu_de_combat

# 2. Configurer le hook (une seule fois par machine)
python update_context.py --hook

# 3. Lire le contexte
cat SESSION_CONTEXT.md

# 4. Commencer à travailler (le hook fonctionnera automatiquement)
```

---

## 🎉 **Bénéfices**

### Pour les développeurs

- ✅ **Gain de temps** : Pas besoin de ré-expliquer le contexte
- ✅ **Documentation toujours à jour** : Pas de documentation obsolète
- ✅ **Suivi automatique** : L'historique et le statut sont toujours actuels
- ✅ **Meilleure collaboration** : Tout le monde a accès aux mêmes informations

### Pour le projet

- ✅ **Meilleure maintenabilité** : Le code et la documentation évoluent ensemble
- ✅ **Transparence** : Tout le monde voit l'état actuel du projet
- ✅ **Traçabilité** : Historique complet des modifications et du contexte
- ✅ **Professionnalisme** : Documentation toujours à jour

---

## 📞 **Support**

### Questions fréquentes

**Q : Pourquoi les fichiers de contexte changent à chaque commit ?**
R : Parce que le hook Git les met à jour automatiquement avec la date, les infos Git, et l'état actuel.

**Q : Puis-je désactiver l'automatisation ?**
R : Oui, supprimez simplement `.git/hooks/pre-commit`.

**Q : Comment mettre à jour manuellement ?**
R : Exécutez `python update_context.py`.

**Q : Les fichiers de contexte sont-ils versionnés ?**
R : Oui, SESSION_CONTEXT.md, STATUS.md et update_context.py sont versionnés. Seul le hook Git ne l'est pas.

---

## 📝 **Historique**

| Date | Version | Modification |
|------|---------|--------------|
| 2026-06-16 | 1.0 | Création initiale du système |
| 2026-06-16 | 1.0 | Premier commit avec automatisation |

---

*Ce système a été créé par Vibe Code (Mistral AI) pour le projet Python_Paul_jeu_de_combat.*
*Dernière mise à jour : 2026-06-16*
