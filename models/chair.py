class Chair():
    instances = []

    def __init__(self, id, user: int, occupied = False, reserved = False, sociable = False)-> None:
        self.id = id
        self.user = user
        self.occupied = occupied
        self.reserved = reserved
        self.sociable = sociable

    def to_db(self):
        return {
            "id": self.id,
            "user": self.user,
            "occupied": self.occupied,
            "reserved": self.reserved
        }