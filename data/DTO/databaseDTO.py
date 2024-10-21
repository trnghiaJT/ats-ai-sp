class DatabaseDTO:
    def __init__(self, dbname, dbuser, dbpassword, dbhost, dbport):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbhost = dbhost
        self.dbport = dbport
    def __str__(self):
        return f"Database: {self.dbname}, User: {self.dbuser}, Host: {self.dbhost}, Port: {self.dbport}"
