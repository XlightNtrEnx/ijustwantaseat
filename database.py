import pyrebase
from models.chair import Chair

class Database:
    def __init__(self):
        self.config = {
            "apiKey": "AIzaSyCqIcgH87xYVfmm_c74jGnXQ-evyQoJyxI",
            "authDomain": "ijustwantaseat.firebaseapp.com",
            "databaseURL": "https://ijustwantaseat-default-rtdb.asia-southeast1.firebasedatabase.app",
            "projectId": "ijustwantaseat",
            "storageBucket": "ijustwantaseat.appspot.com",
            "messagingSenderId": "218899778529",
            "appId": "1:218899778529:web:bd13d2ae727f2eedb8e0a0",
            "measurementId": "G-FQEMDXBPXK"
        }
        firebase = pyrebase.initialize_app(self.config)
        self.db = firebase.database()

db = Database().db

class DatabaseAPI:
    def __init__(self, db) -> None:
        self.db = db

    def seed_db(self):
        self.db.child("chairs").remove()
        if Chair.instances: 
            for i, chair in enumerate(Chair.instances):
                db.child("chairs").child(i + 1).set(chair.to_db())
        else: 
            raise Exception("Chair instances not created yet cannot push to db")
        
    def get_chairs(self):
        return self.db.child("chairs").get().each()
        
db_api = DatabaseAPI(db)

class DbSyncer:
    def __init__(self, db_api) -> None:
        self.db_api = db_api

    def handle_change(self, event):
        print('Event type: ', event["event"])  # can be: 'put', 'patch'
        print('Path: ', event["path"])  # path to the changed data
        print('Data: ', event["data"])  # the changed data
        splitted_path = event["path"].split('/')
        chair_id = splitted_path[-2]
        attribute_changed = event["path"].split('/')[-1]
        final_data = event["data"]
        for chair in Chair.instances:
            if chair_id and chair.id == int(chair_id):
                if attribute_changed == 'occupied':
                    chair.occupied = final_data
                elif attribute_changed == 'reserved':
                    chair.reserved = final_data
                elif attribute_changed == "sociable":
                    chair.sociable = final_data
                break

    def seed_db(self):
        self.db_api.seed_db()

    def sync(self):
        self.db_api.db.child("chairs").stream(self.handle_change)

db_syncer = DbSyncer(db_api)