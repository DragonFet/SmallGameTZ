import sqlite3
class GameDatabase:
    def __init__(self, db_name="game.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                score INTEGER
            )
        ''')
        self.conn.commit()
    def insert_score(self, player_name, score):
        self.cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
        self.conn.commit()
    def get_top_scores(self, limit=5):
        self.cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()