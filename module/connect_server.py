from data.DAO.data_provider import DatabaseDAO
from data.DTO.databaseDTO import DatabaseDTO
from data.data_manager import DatabaseManager
from gui import home
import tkinter as tk
def connect_to_database(datasetup_frame, root,name, user, password, host, port):
        dbname = name
        dbuser = user 
        dbpassword = password
        dbhost =  host
        dbport =  port
        global dao
        # Create DTO
        db_dto = DatabaseDTO(dbname, dbuser, dbpassword, dbhost, dbport)
        # Create DAO
        dao = DatabaseDAO()
        if dao.connect(db_dto): 
            datasetup_frame.destroy()
            main_frame = home.create_main_frame(root) 
            try:
                dao.create_exp_type()
                dao.create_job_role_table()
                dao.create_applicant_table()
                dao.create_delete_jobrole_trigger()
                DatabaseManager().set_dao(dao)
            except Exception as error:
                dao.connection.rollback()
                # print(f"Error: {error}")
                tk.messagebox.showerror("Error", "Failed to create tables or perform actions.")
        else:
            tk.messagebox.showerror("Error", "Connection failed. Please check your credentials.")