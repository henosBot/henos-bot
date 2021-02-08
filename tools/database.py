from google.cloud import firestore

class database:
    db = firestore.Client.from_service_account_json('tools/firebase.json')
    
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
        user_db.update({
            type: amount
        })
    
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
    def ignored(self, guild, type):
        guild_db = self.db.collection('guilds').document(str(guild.id))
        ref = guild_db.get().to_dict()
        return ref[type]
    
    @classmethod
    async def get(self, user, type):
        return self.db.collection('user').document(str(user.id)).get().to_dict()[type]