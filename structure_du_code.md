# 📁 STRUCTURE COMPLÈTE DU CODE SOURCE - ZamaPay Assistant IA

## 🎯 Objectif de ce Document

Ce document présente l'organisation complète du code source du projet ZamaPay Assistant IA avec :
- 🎯 **Rôle de chaque dossier/fichier**
- 🔧 **Technologies utilisées**
- 👤 **Responsable de maintenance** (conception initiale par KAFANDO W Fadel Adil)
- ⚠️ **Points critiques à connaître**
- 📝 **Exemples de code commentés**

---

## 📊 Vue d'Ensemble de l'Architecture
zamapay-platform/
├── backend/              # API Backend (FastAPI + Python 3.12)
├── frontend/             # Interface Utilisateur (React 18 + Vite)
├── docker/              # Configuration Docker & Nginx
├── scripts/             # Scripts d'automatisation
├── annexes/             # Documentation et diagrammes
├── .github/             # CI/CD Pipelines
└── storage/             # Stockage local (développement)

---

**Technologies Principales :**
- **Backend :** Python 3.12+, FastAPI 0.110+
- **Frontend :** React 18, Vite, Tailwind CSS
- **Base de données :** MongoDB Atlas
- **IA :** Google Gemini 2.0 Flash
- **Conteneurisation :** Docker, Docker Compose

---

## 📁 `/backend` - API Backend (FastAPI)

**Port d'écoute :** `8000`  
**Responsable conception :** KAFANDO W Fadel Adil  
**Point d'entrée :** `main.py`

---

### 📄 `main.py` - Point d'Entrée Principal
**Rôle :** Initialise l'application FastAPI, enregistre les routes, configure les middlewares.
**⚠️ Points Critiques :**
- Ne jamais exposer directement sans authentification JWT
- Modifier les origines CORS en production

---

### 📁 `config/` - Configuration Globale

#### 📄 `settings.py` - Variables d'Environnement
**Rôle :** Centralise toutes les configurations système.
**⚠️ Points Critiques :**
- Toujours utiliser un fichier `.env` pour les secrets
- Ne JAMAIS commiter le fichier `.env` dans Git
- Utiliser des variables d'environnement en production

---

#### 📄 `database.py` - Connexion MongoDB
**Rôle :** Gère la connexion et la session MongoDB.
**⚠️ Points Critiques :**
- Toujours fermer les connexions en fin de session
- Utiliser des index MongoDB pour optimiser les requêtes

---

#### 📄 `security.py` - JWT et Chiffrement
**Rôle :** Gère l'authentification, les tokens JWT et le chiffrement AES-256.
**⚠️ Points Critiques :**
- Utiliser bcrypt avec un cost factor minimum de 12
- Régénérer le JWT_SECRET_KEY en production
- Implémenter une rotation des tokens

---

#### 📄 `gemini_config.py` - Configuration LLM
**Rôle :** Configure le modèle Gemini 2.0 Flash et ses paramètres.
**⚠️ Points Critiques :**
- Ajuster `temperature` selon le niveau de créativité souhaité (0.0 = déterministe, 1.0 = créatif)
- Limiter `max_output_tokens` pour contrôler les coûts API
- Mettre à jour `SYSTEM_INSTRUCTION` si la politique de réponse change

---

### 📁 `core/` - Logique Métier

Cette section contient toute la logique d'intelligence artificielle et de traitement.

---

#### 📁 `core/rag/` - Système RAG (Retrieval-Augmented Generation)

**Objectif :** Permet à l'IA de rechercher des documents pertinents avant de générer une réponse.

---

##### 📄 `vector_store.py` - Stockage Vectoriel FAISS
**Rôle :** Gère l'index FAISS pour la recherche sémantique.
**⚠️ Points Critiques :**
- L'index FAISS doit être reconstruit après ajout/suppression de documents
- Toujours sauvegarder l'index après modifications majeures
- Utiliser `IndexIVFFlat` pour de très grandes bases (>100k documents)

---

##### 📄 `embeddings.py` - Génération d'Embeddings
**Rôle :** Transforme le texte en vecteurs numériques pour la recherche sémantique.

**⚠️ Points Critiques :**
- Utiliser `task_type="retrieval_document"` pour indexer des documents
- Utiliser `task_type="retrieval_query"` pour les requêtes utilisateur
- Limite de 2048 tokens par appel API

---

##### 📄 `retriever.py` - Recherche Contextuelle
**Rôle :** Orchestre la recherche de documents pertinents.

**⚠️ Points Critiques :**
- Toujours vérifier que des résultats ont été trouvés
- Limiter la taille du contexte pour éviter de dépasser les limites de tokens

---

##### 📄 `document_processor.py` - Traitement de Documents
**Rôle :** Parse et découpe les documents en chunks optimaux.

**⚠️ Points Critiques :**
- Un bon chunking améliore drastiquement la qualité des réponses
- Tester différentes valeurs de `chunk_size` selon vos documents
- Conserver les métadonnées pour traçabilité

---

##### 📄 `knowledge_base.py` - Gestion Base de Connaissances
**Rôle :** Interface de haut niveau pour gérer la base de connaissances.

**⚠️ Points Critiques :**
- Toujours sauvegarder l'index après des ajouts importants
- Prévoir un script de reconstruction automatique (voir `scripts/`)
- Monitorer la taille de l'index (performance)

---

#### 📁 `core/ai/` - Gestion IA/LLM

##### 📄 `gemini_client.py` - Client Gemini
**Rôle :** Interface avec l'API Gemini 2.0 Flash.

**⚠️ Points Critiques :**
- Toujours capturer les exceptions API (quota, timeout, etc.)
- Monitorer l'utilisation des tokens pour contrôler les coûts
- Utiliser `chat_session` pour préserver l'historique des conversations

---

##### 📄 `prompt_templates.py` - Templates de Prompts
**Rôle :** Centralise les prompts système pour cohérence et maintenance.

**⚠️ Points Critiques :**
- Centraliser les prompts facilite les tests A/B
- Versionner les prompts pour suivre l'évolution des performances

---

##### 📄 `context_manager.py` - Gestion Historique
**Rôle :** Gère l'historique des conversations pour maintenir le contexte.

**⚠️ Points Critiques :**
- Ne pas dépasser les limites de tokens du modèle (limiter l'historique)
- Sauvegarder l'historique en base de données pour persistance

---

##### 📄 `response_validator.py` - Validation Financière
**Rôle :** Vérifie que les réponses sont cohérentes et sûres pour le contexte financier.

**⚠️ Points Critiques :**
- Adapter les règles de validation selon la réglementation BCEAO
- Logger toutes les réponses rejetées pour analyse
- Mise à jour régulière des patterns interdits

---

#### 📁 `core/multimedia/` - Gestion Multimédia

##### 📁 `core/multimedia/audio/` - Traitement Audio

###### 📄 `speech_to_text.py` - Transcription Audio
**Rôle :** Convertit les messages vocaux en texte avec Google Cloud Speech-to-Text.

**⚠️ Points Critiques :**
- Fichiers audio > 1 minute nécessitent une transcription asynchrone
- Coût : ~0.006 $ par 15 secondes audio
- Toujours nettoyer les fichiers temporaires après traitement

---

###### 📄 `text_to_speech.py` - Synthèse Vocale
**Rôle :** Convertit les réponses textuelles en audio avec Google Cloud TTS.

**⚠️ Points Critiques :**
- Implémenter un système de cache pour éviter de régénérer les mêmes textes
- Coût : ~4 $ par million de caractères (WaveNet)
- Nettoyer régulièrement les fichiers audio anciens

---

##### 📁 `core/multimedia/files/` - Traitement de Fichiers

###### 📄 `pdf_extractor.py` - Extraction PDF
**Rôle :** Extrait le texte des fichiers PDF uploadés.

**⚠️ Points Critiques :**
- Certains PDF protégés ou scannés ne peuvent pas être extraits directement
- Utiliser OCR (Tesseract) pour les PDF scannés
- Valider la taille des fichiers avant traitement (limite : 10 MB)

---

#### 📁 `core/security/` - Sécurité

##### 📄 `content_filter.py` - Filtrage de Contenu
**Rôle :** Filtre les messages inappropriés ou dangereux.

**⚠️ Points Critiques :**
- Mettre à jour régulièrement la liste des mots bloqués
- Logger toutes les tentatives bloquées pour analyse de sécurité
- Équilibrer entre sécurité et faux positifs

---

### 📁 `database/` - Gestion Base de Données

#### 📁 `database/models/` - Modèles de Données

##### 📄 `user.py` - Modèle Utilisateur


**⚠️ Points Critiques :**
- Ne JAMAIS stocker les mots de passe en clair
- Toujours utiliser `hashed_password` avec bcrypt
- Implémenter un système de vérification email/téléphone

---

##### 📄 `ticket.py` - Modèle Ticket

**⚠️ Points Critiques :**
- Générer automatiquement `ticket_number` pour traçabilité
- Calculer automatiquement les métriques de performance (temps de réponse)
- Implémenter un système d'escalade automatique pour tickets urgents

---

### 📁 `services/` - Services Métier

#### 📄 `chat_service.py` - Service de Chat Principal

**⚠️ Points Critiques :**
- Le flux complet doit être robuste à chaque étape
- Logger chaque étape pour debugging
- Implémenter des timeouts pour éviter les blocages
- Gérer les erreurs API de manière gracieuse

---

### 📁 `api/` - Endpoints REST

#### 📁 `api/routes/` - Routes API

##### 📄 `chat.py` - Endpoints de Chat

**⚠️ Points Critiques :**
- Toujours vérifier l'authentification JWT
- Limiter le nombre de requêtes par utilisateur (rate limiting)
- Retourner des erreurs explicites pour debugging frontend

---

## 📁 `/frontend` - Interface Utilisateur (React)

**Port d'écoute :** `3000` (développement), `80` (production via Nginx)  
**Responsable conception :** KAFANDO W Fadel Adil

### Structure Interne

frontend/
├── public/              # Fichiers statiques
├── src/
│   ├── components/      # Composants React réutilisables
│   │   ├── chat/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── InputBar.jsx
│   │   ├── admin/
│   │   └── tickets/
│   ├── services/        # Clients API
│   │   └── api.js
│   ├── hooks/           # Custom React Hooks
│   ├── store/           # État global (Redux/Context)
│   ├── styles/          # Styles Tailwind
│   └── App.jsx          # Point d'entrée
├── package.json
├── tailwind.config.js
└── vite.config.js

### 📄 `src/services/api.js` - Client API

**⚠️ Points Critiques :**
- Toujours utiliser des variables d'environnement pour l'URL API
- Gérer les erreurs réseau de manière globale
- Implémenter un refresh automatique des tokens JWT

---

### 📄 `src/components/chat/ChatWindow.jsx` - Composant de Chat

**⚠️ Points Critiques :**
- Implémenter un système de retry en cas d'échec réseau
- Optimiser le rendu avec `React.memo` pour grandes conversations
- Afficher un indicateur de typing pour meilleure UX

---

## 📁 `/docker` - Configuration Docker

### 📄 `docker-compose.yml` - Développement

**⚠️ Points Critiques :**
- Ne JAMAIS commiter les variables d'environnement sensibles
- Utiliser `docker-compose.prod.yml` pour la production (sans `--reload`)
- Toujours définir des volumes pour persister les données

---

### 📄 `Dockerfile.backend` - Image Backend

**⚠️ Points Critiques :**
- Utiliser des images slim pour réduire la taille
- Multi-stage builds pour optimiser en production
- Ne pas copier le dossier `.git` (utiliser `.dockerignore`)

---

## 📁 `/scripts` - Scripts d'Automatisation

### 📄 `scripts/rebuild_faiss.py` - Reconstruction Index RAG

**⚠️ Points Critiques :**
- Toujours faire une sauvegarde de l'index avant reconstruction
- Planifier cette tâche via cron ou GitHub Actions
- Notifier l'équipe en cas d'échec

---

## 📁 `/.github/workflows` - CI/CD Pipelines

### 📄 `.github/workflows/ci.yml` - Tests Automatiques

**⚠️ Points Critiques :**
- Toujours exécuter les tests avant merge
- Bloquer le merge si les tests échouent
- Monitorer la couverture de code (objectif : >80%)

---

## 🔑 Fichiers Critiques à NE JAMAIS Modifier Sans Validation

| Fichier | Raison | Responsable Validation |
|---------|--------|----------------------|
| `config/security.py` | Sécurité JWT | Lead Architecte |
| `config/gemini_config.py` | Configuration IA | Lead IA |
| `docker-compose.prod.yml` | Environnement production | DevOps |
| `core/rag/vector_store.py` | Index RAG | Lead IA |
| `.github/workflows/deploy-prod.yml` | Déploiement production | Chef de Projet |

---

## 📝 Convention de Nommage

### Fichiers Python
- **Modules** : `snake_case.py` (ex: `chat_service.py`)
- **Classes** : `PascalCase` (ex: `ChatService`)
- **Fonctions** : `snake_case()` (ex: `process_message()`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `MAX_TOKENS`)

### Fichiers JavaScript/React
- **Composants** : `PascalCase.jsx` (ex: `ChatWindow.jsx`)
- **Services** : `camelCase.js` (ex: `apiService.js`)
- **Fonctions** : `camelCase()` (ex: `handleSendMessage()`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `API_BASE_URL`)

---

## 🚨 Gestion des Erreurs Courantes

### Erreur : "ModuleNotFoundError: No module named 'core'"
**Cause :** Python ne trouve pas le module  
**Solution :**
```bash
# S'assurer d'être dans le dossier backend/
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py


### Erreur : "Connection refused to MongoDB"
**Cause :** MongoDB n'est pas démarré  
**Solution :**
```bash
# Vérifier que le conteneur Docker est actif
docker ps | grep mongo

# Si absent, démarrer les services
docker compose up -d mongo
```

### Erreur : "Gemini API Key not found"
**Cause :** Variable d'environnement manquante  
**Solution :**
```bash
# Créer un fichier .env dans backend/
echo "GEMINI_API_KEY=votre_clé_api" > backend/.env
```

---

## 📚 Ressources Complémentaires

- **Documentation FastAPI :** https://fastapi.tiangolo.com
- **Documentation Gemini :** https://ai.google.dev/docs
- **Documentation FAISS :** https://github.com/facebookresearch/faiss/wiki
- **Documentation MongoDB :** https://www.mongodb.com/docs
- **Documentation React :** https://react.dev

---

## ✅ Checklist de Vérification

Avant de considérer une modification comme terminée :

- [ ] Le code suit les conventions de nommage
- [ ] Les tests unitaires passent (`pytest` ou `npm test`)
- [ ] La documentation est mise à jour
- [ ] Les secrets ne sont pas exposés dans Git
- [ ] Les logs de debugging sont retirés
- [ ] Le code a été revu par un pair (code review)
- [ ] Les diagrammes sont régénérés si nécessaire
- [ ] Les variables d'environnement sont documentées

---

**Document maintenu par :** KAFANDO W Fadel Adil  
**Dernière mise à jour :** Décembre 2025  
**Version :** 1.0
