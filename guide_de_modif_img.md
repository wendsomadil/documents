# Guide de Modification et de Maintenance - ZamaPay Assistant IA

Ce document est le guide de référence pour les équipes de développement souhaitant effectuer la maintenance, l'évolution et la mise à jour du projet ZamaPay Assistant IA. Il définit les procédures standard pour mettre à jour les composants techniques et la Documentation Technique Complète (`DOCUMENTATION_TECHNIQUE_COMPLETE.docx`).

## 1\. Processus de Documentation (Action 6)

Toute modification majeure de l'architecture, du flux de travail ou de l'infrastructure **doit** être répercutée dans la documentation technique.

### 1.1. Mise à jour des Diagrammes

Les diagrammes sont stockés en format **Mermaid** (`.mmd`) pour faciliter la modification du code source.

**1. Éditer le Code Source** 
    Ouvrir et modifier le fichier `.mmd` concerné. 
    `annexes/diagrammes/mermaid/`
**2. Générer les Images** 
    Exécuter la commande manuelle dans le terminal PowerShell pour convertir le `.mmd` en `.png` et `.svg`. 
    **Cette étape est critique pour l'exactitude des documents.** 
    `annexes/diagrammes/exports/` 
**3. Mettre à jour le Document**
    Remplacer l'ancienne image (PNG) dans le document Word par le nouveau fichier généré.
    `DOCUMENTATION_TECHNIQUE_COMPLETE.docx`
**4. Exemple de commande pour régénérer l'Architecture Globale :**
    *(Adaptez le chemin `mmdc.cmd` si l'environnement d'un nouveau développeur est différent)*

```bash
& "C:/Users/user/AppData/Roaming/npm/mmdc.cmd" -i "annexes/diagrammes/mermaid/01_architecture_globale.mmd" -o "annexes/diagrammes/exports/png/01_architecture_globale.png" -t dark --width 1600
````

### 1.2. Mettre à jour l'Infrastructure

Toute modification aux services de déploiement (ports, volumes, dépendances) doit être mise à jour dans :
    *1. Le fichier de configuration **`annexes/code-source/docker/docker-compose.yml`**.
    *2. La **Section 5 (Infrastructure et Déploiement)** du document Word.

## 2\. Maintenance du Code et des Dépendances

### 2.1. Backend (Python/FastAPI)

Le backend utilise des dépendances listées dans `requirements.txt` (et gérées par `pyproject.toml`).

  *1. **Ajout/Modification de librairie :** Mettre à jour `requirements.txt`.
  *2. **Conteneurisation :** Après mise à jour des dépendances Python, le `Dockerfile` du backend doit être revu si des dépendances système (`apt-get install` ou équivalent) sont ajoutées.
  *3. **Mise à jour de l'API Gemini :** Le fichier `backend/config/gemini_config.py` est le point de configuration central pour les versions de modèles, les températures, et les fonctions d'outillage (tool-calling).

### 2.2. Frontend (React)

  *1. **Dépendances :** Mettre à jour `frontend/package.json`.
  *2. **Connexion API :** Le Frontend doit toujours pointer vers le service `backend:8000` (FastAPI) pour garantir la communication à l'intérieur de l'environnement Docker.

### 2.3. Gestion de la Base de Connaissances (RAG)

Le système repose sur une base de connaissances vectorielle (FAISS).

  *1. **Mise à jour des documents :** Les nouveaux documents de référence (règles, FAQ, procédures) doivent être ajoutés au répertoire source du *pipeline* d'indexation.
  *2. **Reconstruction de l'Index :** Après ajout/suppression de documents, l'index vectoriel doit être reconstruit pour que le moteur RAG puisse les retrouver. La procédure se fait via un script dédié (ex: `python scripts-automatisation/rebuild_faiss.py`).

## 3\. Gestion des Environnements (Docker)

L'environnement de développement complet est géré par **Docker Compose**.

### 3.1. Commandes de Base

Toutes les commandes Docker Compose doivent être exécutées à la racine du projet (`ZAMAPAY_IA_DOCUMENTATION_V2.1`).

  **1. Démarrage (Mode Détaché)**  `docker compose up -d` : Lance tous les services (backend, db, cache, frontend) en arrière-plan.
  **2. Arrêt des Services**  `docker compose down` : Arrête et supprime les conteneurs (mais conserve le volume de données `mongo_data`).
  **3. Reconstruction d'un Service**  `docker compose up -d --build [NOM_SERVICE]` : Nécessaire après toute modification dans un `Dockerfile` ou les dépendances. Ex: `--build backend`.
  **4. Afficher les Logs**  `docker compose logs -f [NOM_SERVICE]` : Afficher les logs en temps réel. Ex: `logs -f backend`. 

### 3.2. Volumes et Persistance

Le volume nommé **`mongo_data`** est crucial. Il garantit que les données de MongoDB ne sont pas perdues lorsque les conteneurs sont arrêtés ou recréés.

## 4\. Workflow de Validation

Avant de fusionner tout changement avec la branche principale (`main`), les étapes suivantes sont **obligatoires** :

1.  **Tests Locaux :** Vérification du fonctionnement de l'application via `docker compose up`.
2.  **Tests Unitaires/Intégration :** Réussite de tous les tests situés dans `backend/tests/`.
3.  **Revue de Code (Code Review) :** Validation par un développeur senior ou le Lead Architecte.
4.  **Conformité Documentaire :** Vérification finale que ce guide et la Documentation Technique Complète reflètent les modifications apportées.

<!-- end list -->
