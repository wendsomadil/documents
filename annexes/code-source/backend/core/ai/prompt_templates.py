# core/ai/prompt_templates.py

class PromptTemplates:
    """Templates de prompts réutilisables"""
    
    FINANCIAL_QUERY = """
Tu es un assistant spécialisé en services financiers pour ZamaPay.

Contexte fourni :
{context}

Question de l'utilisateur :
{query}

Instructions :
- Fournis une réponse claire et professionnelle
- Base-toi uniquement sur le contexte fourni
- Si l'information n'est pas disponible, recommande de contacter le support
- Utilise des exemples concrets si pertinent
- Format : Markdown si nécessaire
"""
    
    TRANSACTION_HELP = """
L'utilisateur a une question sur une transaction.

Détails de la transaction :
{transaction_details}

Question :
{query}

Aide l'utilisateur à comprendre ou résoudre son problème de manière simple et rassurante.
"""
    
    DEMO_MODE_RESPONSE = """
L'utilisateur est en MODE DÉMO (sans compte ZamaPay).

Question :
{query}

Instructions :
- Fournis une réponse partielle et limitée
- Indique clairement que la réponse complète nécessite un compte
- Encourage l'inscription tout en restant utile
"""

    @staticmethod
    def format_prompt(template: str, **kwargs) -> str:
        """Formate un template avec les variables fournies"""
        return template.format(**kwargs)
    