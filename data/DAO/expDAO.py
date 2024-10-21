from data.data_manager import DatabaseManager

class expDAO:
    _instance = None
    @staticmethod
    def get_instance():
        if expDAO._instance is None:
            expDAO._instance = expDAO()
        return expDAO._instance

    def __init__(self):
        if expDAO._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.db_dao = DatabaseManager().get_dao()
            if self.db_dao is None:
                raise Exception("DatabaseDAO created!")
    def fetch_exp_name(self):
        try:
            query = "SELECT name FROM ExpType;"
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            # print(f"Error: {e}")
            return None