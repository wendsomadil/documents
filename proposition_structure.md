# Proposition de la structure complete du chatbot

zamapay-platform/
│
├── backend/                           # API principale (FastAPI)
│   ├── main.py                        # Point d'entrée
│   ├── config/                        # Configuration globale
│   │   ├── settings.py                # Variables config
│   │   ├── database.py                # Connexion MongoDB
│   │   ├── security.py                # JWT, cryptage, ACL
│   │   └── gemini_config.py           # Config LLM
│   │
│   ├── core/                          # Logique métier
│   │   ├── rag/                       # Système RAG
│   │   │   ├── vector_store.py        # FAISS/Chroma
│   │   │   ├── embeddings.py          # Embeddings LLM
│   │   │   ├── retriever.py           # Recherche contextuelle
│   │   │   ├── document_processor.py  # Parsing + chunking
│   │   │   └── knowledge_base.py      # Gestion KB interne
│   │   │
│   │   ├── ai/                        # Gestion IA/LLM
│   │   │   ├── gemini_client.py       # Client modèle
│   │   │   ├── prompt_templates.py    # Templates prompts
│   │   │   ├── context_manager.py     # Gestion historique
│   │   │   └── response_validator.py  # Vérification finances
│   │   │
│   │   ├── multimedia/                # Audio + fichiers
│   │   │   ├── audio/
│   │   │   │   ├── speech_to_text.py  # STT
│   │   │   │   ├── text_to_speech.py  # TTS
│   │   │   │   ├── audio_processor.py # Conversion & compression
│   │   │   │   └── audio_storage.py   # S3/local
│   │   │   ├── files/
│   │   │   │   ├── pdf_extractor.py
│   │   │   │   ├── docx_extractor.py
│   │   │   │   ├── excel_extractor.py
│   │   │   │   ├── image_ocr.py
│   │   │   │   └── file_storage.py
│   │   │   └── text/
│   │   │       ├── text_cleaner.py
│   │   │       └── text_chunker.py
│   │   │
│   │   └── security/
│   │       ├── content_filter.py      # Mots bloqués
│   │       ├── financial_context.py   # Anti-fraude logique
│   │       └── rate_limiter.py        # Limitation requêtes
│   │
│   ├── database/                      # DB Mongo + repos
│   │   ├── mongodb.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── ticket.py
│   │   │   ├── metrics.py
│   │   │   ├── message.py
│   │   │   └── admin.py
│   │   └── repositories/
│   │       ├── user_repository.py
│   │       ├── ticket_repository.py
│   │       ├── message_repository.py
│   │       ├── metrics_repository.py
│   │       └── keyword_repository.py
│   │
│   ├── services/                      # Services métier
│   │   ├── chat_service.py
│   │   ├── rag_service.py
│   │   ├── audio_service.py
│   │   ├── file_service.py
│   │   ├── metrics_service.py
│   │   ├── ticket_service.py
│   │   ├── admin_service.py
│   │   ├── report_service.py
│   │   └── account_service.py         # ⚠️ GESTION MODE
│   │                                  #    DÉMO/UTILISATEUR ENREGISTRÉ
│   │
│   ├── api/                           # Endpoints REST
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── audio.py
│   │   │   ├── tickets.py
│   │   │   ├── files.py
│   │   │   ├── users.py
│   │   │   ├── metrics.py
│   │   │   └── admin/
│   │   │       ├── dashboard.py
│   │   │       ├── reports.py
│   │   │       ├── users_admin.py
│   │   │       └── knowledge_base.py
│   │   └── middleware/
│   │       ├── auth.py
│   │       ├── cors.py
│   │       ├── logging.py
│   │       ├── error_handler.py
│   │       └── rate_limit.py
│   │
│   ├── utils/
│   │   ├── token_counter.py
│   │   ├── crypto.py
│   │   ├── validators.py
│   │   ├── exceptions.py
│   │   └── logger.py
│   │
│   └── tests/
│       ├── test_api/
│       ├── test_services/
│       └── test_core/
│
├── frontend/                          # Interface React
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   ├── admin/
│   │   │   └── tickets/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── store/
│   │   └── styles/
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── scripts/                           # Automatisation
│   ├── migration/
│   ├── deployment/
│   ├── monitoring/
│   └── dev/
│
├── docker/                            # Docker & Nginx
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── nginx/
│       └── nginx.conf
│
├── .github/                            # CI/CD
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── deploy-dev.yml
│   │   ├── deploy-prod.yml
│   │   └── code-quality.yml
│
├── docs/                               # Documentation
│   ├── API.md
│   ├── SECURITY.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
│
├── storage/
├── logs/
├── .env.example
└── README.md
