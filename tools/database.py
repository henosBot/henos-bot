from google.cloud import firestore

class db:
    def __init__(self):
        self.db = firestore.Client.from_service_account_json('firebase.json')
    
    async def open_account(self, user):
        user_db = self.db.collection('users').document(str(user.id))
        if not user_db:
            user
            return False
        else:
            return True