class UserData(object):
    def __init__(self):
        self.store = {}
    
    def set(self, user_id, place, latitude, longitude):
        self.store[user_id] = {
            city: city,
            latitude: latitude,
            longitude: longitude
        }

    def get(self, user_id):
        return self.store.get(user_id)
