# config/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

class Database:
    client: AsyncIOMotorClient = None
    
    async def connect_db(self):
        """Établit la connexion à MongoDB Atlas"""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        print("✅ Connexion MongoDB établie")
    
    async def close_db(self):
        """Ferme la connexion proprement"""
        self.client.close()
        print("🔌 Connexion MongoDB fermée")
    
    def get_database(self):
        """Retourne l'instance de la base de données"""
        return self.client[settings.DATABASE_NAME]

db = Database()
