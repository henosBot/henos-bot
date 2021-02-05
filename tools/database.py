from google.cloud import firestore

class db:
    def __init__(self):
        self.db = firestore.Client.from_service_account_json('firebase.json')
    
    @classmethod
    async def open_account(self, user):
        user_db = self.db.collection('users').document(str(user.id))
        if not user_db.get().exists:
            user_db.create({
                'wallet': 500,
                'bank': 0,
                'xp': 0,
                'level': 0
            })
            return False
        else:
            return True
    
    @classmethod
    async def set(self, user, type, amount):
        user_db = self.db.collection('users').document(str(user.id))
        ref = user_db.get().to_dict()
        wallet = ref['wallet']
        bank = ref['bank']
        xp = ref['xp']
        level = ref['level']
        if type == 'wallet':
            dicty = {
                'wallet': amount,
                'bank': bank,
                'xp': xp,
                'level': level
            }
        elif type == 'bank':
            dicty = {
                'wallet': wallet,
                'bank': amount,
                'xp': xp,
                'level': level
            }
        elif type == 'xp':
            dicty = {
                'wallet': wallet,
                'bank': bank,
                'xp': amount,
                'level': level
            }
        elif type == 'level':
            dicty = {
                'wallet': wallet,
                'bank': bank,
                'xp': xp,
                'level': amount
            }
        else:
            dicty = None
        user_db.set(dicty)
    
    @classmethod
    async def save(self, user, type, amount):
        user_db = self.db.collection('users').document(str(user.id))
        ref = user_db.get().to_dict()
        user_db.update({
            type: ref[type] + amount
        })
    
    @classmethod
    async def remove(self, user, type, amount):
        user_db = self.db.collection('users').document(str(user.id))
        ref = user_db.get().to_dict()
        user_db.update({
            type: ref[type] - amount
        })
    
    @classmethod
    async def ignored(self, guild, type):
        return