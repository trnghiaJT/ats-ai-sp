class DatabaseManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.dao = None 
        return cls._instance
    def set_dao(self, dao):
        self.dao = dao
    def get_dao(self):
        return self.dao
