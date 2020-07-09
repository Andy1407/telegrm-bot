from database import Database

db = Database()
db.add_table(name_table="messages", ID="INT", DATE="TEXT", TYPE="TEXT", MESSAGE1="TEXT", MESSAGE2="TEXT",
             SHOW_MESSAGE="TEXT", NUMBER="INT")
db.add_table(name_table="users", ID="INT", TIMEZONE="TEXT", language='TEXT')
