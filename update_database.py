from database import Database

db = Database()
db.add_table(name_table="messages", user_id="INT", date="TEXT", type="TEXT", message1="TEXT", message2="TEXT",
             description="TEXT", id="INT")
db.add_table(name_table="users", id="INT", timezone="TEXT", language='TEXT')
