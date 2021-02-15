from google.cloud import firestore
from tools.amounts import amounts

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
    async def open_guild_account(self, guild):
        guild_db = self.db.collection('users').document(str(guild.id))
        if not guild_db.get().exists:
            guild_db.create({
                'bad_word_checker': True,
                'ban_infringments': 3,
                'log_channel': None,
                'warn_infringments': 1,
                'warn_role': None,
                'lvl_ msgs': True ,
                'welcome_msgs': True
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
        user_db = self.db.collection('users').document(str(user.id))
        ref = user_db.get().to_dict()
        return ref[type]
    
    @classmethod
    async def buy_item(self, user, item):
        item_db = self.db.collection('users').document(str(user.id))
        if not item_db.get().exists:
            item_db.create({
                'cookie': 0,
                'chocolate': 0,
                'coin': 0,
                'rare coin': 0,
                'medal': 0,
                'rare medal': 0,
                'trophy': 0,
                'rare trophy': 0,
                'ultra collectable thingy': 0,
            })
        await self.remove(user, 'wallet', amounts(item))
        ref = item_db.get().to_dict()
        item_db.update({
            item: ref[item] + 1
        })