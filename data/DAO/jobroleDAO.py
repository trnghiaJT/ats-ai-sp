from data.data_manager import DatabaseManager

class JobRoleDAO:
    _instance = None
    @staticmethod
    def get_instance():
        if JobRoleDAO._instance is None:
            JobRoleDAO._instance = JobRoleDAO()
        return JobRoleDAO._instance
    def __init__(self):
        if JobRoleDAO._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.db_dao = DatabaseManager().get_dao()
            if self.db_dao is None:
                raise Exception("DatabaseDAO created!")
    def insert_job_role(self, job_role_name):
        try:
            query = """
            INSERT INTO JobRole (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (job_role_name,))
            self.db_dao.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            # print(f"Error when add role name: {e}")
            self.db_dao.connection.rollback()
            return False
