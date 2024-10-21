import psycopg2
from data.DTO.databaseDTO import DatabaseDTO

class DatabaseDAO:
    def connect(self, db_dto: DatabaseDTO):
        try:
            self.connection = psycopg2.connect(
                dbname=db_dto.dbname,
                user=db_dto.dbuser,
                password=db_dto.dbpassword,
                host=db_dto.dbhost,
                port=db_dto.dbport
            )
            # print("Connected database!")
            return True
        except Exception as error:
            # print(f"Error: {error}")
            return False
    def create_job_role_table(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Hasn't connected db.")
            cursor = self.connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS JobRole (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE
            );
            """
            cursor.execute(create_table_query)
            self.connection.commit()
            # print("'JobRole' Created(If not exist).")
        except Exception as e:
            self.connection.rollback()
            # print(f"Error create 'JobRole': {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def create_exp_type(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Hasn't connected db.")

            cursor = self.connection.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS ExpType (
                name VARCHAR(20) PRIMARY KEY
            );
            """
            cursor.execute(create_table_query)
            insert_exptypes_query = """
            INSERT INTO ExpType (name) VALUES
            ('No experience'),
            ('< 1 year'),
            ('1-2 years'),
            ('2-5 years'),
            ('> 5 years')
            ON CONFLICT (name) DO NOTHING;
            """
            cursor.execute(insert_exptypes_query)

            self.connection.commit()
            # print("'ExpType' created (if not exist).")
        except Exception as e:
            self.connection.rollback()
            # print(f"Error create Exptype table: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    def create_applicant_table(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Hasn't connected db.")
            cursor = self.connection.cursor()
            cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Applicant (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,  -- Thay SERIAL bằng UUID
                name VARCHAR(100) NULL, 
                phone VARCHAR(15) NULL,
                email VARCHAR(100) NULL,
                gpa FLOAT NULL,
                education VARCHAR(100) NULL,
                major VARCHAR(100) NULL,
                exp VARCHAR(20) NULL, 
                skill TEXT NULL,
                project TEXT NULL,
                job_role VARCHAR(50) NULL,
                CONSTRAINT unique_applicant UNIQUE (name, phone, job_role),
                FOREIGN KEY (exp)
                REFERENCES ExpType(name)
                ON DELETE SET NULL
            );
            """
            cursor.execute(create_table_query)
            self.connection.commit()
            # print("'Applicant' created (if not exist).")
        except Exception as e:
            self.connection.rollback()
            # print(f"Error create 'Applicant': {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    def fetch_applicants(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Hasn't connected db.")
            cursor = self.connection.cursor()
            cursor.execute("SELECT name, phone, email, gpa, exp, job_role FROM Applicant")
            applicants = cursor.fetchall()
            return applicants
        except Exception as e:
            # print(f"Error get data: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
    def fetch_exp_and_job_role(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Hasn't connect")
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM ExpType")
            exp_data = cursor.fetchall()
            cursor.execute("SELECT name FROM JobRole")
            job_role_data = cursor.fetchall()
            return {
                "exp_types": [row[0] for row in exp_data],
                "job_roles": [row[0] for row in job_role_data]
            }
        except Exception as e:
            # print(f"Error get data: {e}")
            return {
                "exp_types": [],
                "job_roles": []
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
    def add_foreign_key_to_applicant(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Hasn't connect")
            cursor = self.connection.cursor()
            check_constraint_query = """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'Applicant' AND constraint_name = 'fk_job_role';
            """
            cursor.execute(check_constraint_query)
            result = cursor.fetchone()
            if result is None:
                alter_table_query = """
                ALTER TABLE Applicant
                ADD CONSTRAINT fk_job_role
                FOREIGN KEY (job_role)
                REFERENCES JobRole(name)
                ON DELETE SET NULL;
                """
                cursor.execute(alter_table_query)
                self.connection.commit()
                # print("Added foreigh key for 'Applicant'.")
            else:
                return
                # print("'fk_job_role' is existing in table 'Applicant'.")
        except Exception as e:
            self.connection.rollback()
            # print(f"Error add fgk: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
    def create_delete_jobrole_trigger(self):
        try:
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Database connection has not been established.")          
            cursor = self.connection.cursor()
            create_function_query = """
            CREATE OR REPLACE FUNCTION delete_jobrole_if_no_applicant()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM Applicant WHERE job_role = OLD.job_role) THEN
                    DELETE FROM JobRole WHERE name = OLD.job_role;
                END IF;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
            """
            cursor.execute(create_function_query)
            create_trigger_query = """
            CREATE TRIGGER trg_delete_jobrole
            AFTER DELETE ON Applicant
            FOR EACH ROW
            EXECUTE FUNCTION delete_jobrole_if_no_applicant();
            """
            cursor.execute(create_trigger_query)
            self.connection.commit()
            # print("Trigger and function created successfully.")
        except Exception as e:
            self.connection.rollback()
            # print(f"Error creating trigger: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()