from google.cloud import firestore

class db:
    def __init__(self):
        self.db = firestore.Client.from_service_account_json('firebase.json')
    
    @classmethod
    async def open_account(self, user):
        user_db = self.db.collection('users').document(str(user.id))
        if not user_db:
            return False
        else:
            return True
    
    @classmethod
    async def set(self, user, type, amount):
        return
    
    @classmethod
    async def save(self, user, type, amount):
        return
    
    @classmethod
    async def remove(self, user, type, amount):
        return
    
    @classmethod
    async def ignored(self, guild, type):
        return