from data.data_manager import DatabaseManager
from data.DAO.jobroleDAO import JobRoleDAO
class ApplicantDAO:
    _instance = None

    @staticmethod
    def get_instance():
        if ApplicantDAO._instance is None:
            ApplicantDAO._instance = ApplicantDAO()
        return ApplicantDAO._instance
    def __init__(self):
        if ApplicantDAO._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.db_dao = DatabaseManager().get_dao()
            if self.db_dao is None:
                raise Exception("DatabaseDAO wasn't create!")
    def insert_applicant(self, data):
        try:
            query = """
            INSERT INTO Applicant (name, phone, email, gpa, education, major, skill, project, exp, job_role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (
                data["Name"], data["Phone"], data["Email"], data["GPA"], 
                data["Education"], data["Major"], data["Skills"], data["Project"],
                data["Exp"], data["JobRole"]
            ))
            self.db_dao.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            if "unique constraint" in str(e):
                # print("Applicant already exists:", e)
                return False
            else:
                # print("Error inserting applicant:", e)
                return False
    def fetch_all_applicants(self):
        try:
            query = "SELECT name, phone, email, gpa, education, major, skill, project, exp, job_role, id FROM Applicant;"
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            # print(f"Error when get data: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
    def update_applicant(self, applicant_id, data):
        try:
            query = """
            UPDATE Applicant
            SET name = %s, phone = %s, email = %s, gpa = %s, 
                education = %s, major = %s, skill = %s, project = %s, 
                exp = %s, job_role = %s
            WHERE id = %s;
            """
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (
                data["Name"], data["Phone"], data["Email"], data["GPA"],
                data["Education"], data["Major"], data["Skill"], data["Project"],
                data["Exp"], data["JobRole"], applicant_id
            ))
            jrd = JobRoleDAO.get_instance()
            jrd.insert_job_role(data["JobRole"])
            self.db_dao.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.db_dao.connection.rollback()
            # print(f"Error update: {e}")
            return False
    def delete_applicant(self, applicant_id):
        try:
            query = "DELETE FROM Applicant WHERE id = %s;"
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (applicant_id,))
            self.db_dao.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            # print(f"Error delete: {e}")
            self.db_dao.connection.rollback()
            return False
    def fetch_applicant_by_job_role(self, job_role):
        try:
            query = "SELECT name, phone, email, gpa, exp, job_role FROM Applicant WHERE job_role = %s;"
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (job_role,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            # print(f"Error when get follow job role: {e}")
            return None
    def fetch_applicant_by_info(self, name, phone, job_role):
        try:
            query = """
            SELECT name, phone, email, gpa, education, major, exp, skill, project, job_role
            FROM Applicant 
            WHERE name = %s AND phone = %s AND job_role = %s;
            """
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (name, phone, job_role))
            result = cursor.fetchone() 
            cursor.close()
            return result
        except Exception as e:
            # print(f"Get applicant match with infomation: {e}")
            return None
    def fetch_by_filter(self, job_role, exp, gpa_from, gpa_to):
        try:
            query = """
                SELECT name, phone, email, gpa, education, major, exp, skill, project, job_role
                FROM Applicant
                WHERE (%s IS NULL OR job_role = %s)  
                AND (%s IS NULL OR exp = %s)               
                AND (gpa >= COALESCE(%s, 0))               
                AND (gpa <= COALESCE(%s, 4));              
                """
            job_role_param = job_role if job_role != "" else None
            exp_param = exp if exp != "" else None
            cursor = self.db_dao.connection.cursor()
            cursor.execute(query, (job_role_param, job_role_param, exp_param, exp_param, gpa_from, gpa_to))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            # print(f"Error when get data of applicant: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

