import mysql.connector


class MysqlConnection:

    def __init__(self, config):
        self.db = mysql.connector.connect(
            host="localhost",
            user=config["DATABASE"]["USER"],
            password=config["DATABASE"]["PASSWORD"],
            database=config["DATABASE"]["SCHEMA"]
        )

    def insert_question(self, question, author=None):
        if not self.db.is_connected():
            self.db.reconnect()
        cursor = self.db.cursor(buffered=True)
        sql = "INSERT INTO questions (question, author) VALUES (%s, %s)"
        val = (question, author)
        cursor.execute(sql, val)
        self.db.commit()
        print("new question asked")

    def authorize_question(self, question_id: int):
        self.set_authorize_question(question_id, 1)
        print(f"question {question_id} authorized")

    def unauthorize_question(self, question_id: int):
        self.set_authorize_question(question_id, 0)
        print(f"question {question_id} unauthorized")

    def set_authorize_question(self, question_id: int, authorize: int):
        if not self.db.is_connected():
            self.db.reconnect()
        cursor = self.db.cursor(buffered=True)
        sql = "UPDATE questions SET authorized = %s WHERE id = %s"
        val = (authorize, question_id)
        cursor.execute(sql, val)
        self.db.commit()

    def answer_question(self, question_id: int):
        self.set_answered_question(question_id, 1)
        print(f"question {question_id} answered")

    def unanswer_question(self, question_id: int):
        self.set_answered_question(question_id, 0)
        print(f"question {question_id} unanswered")

    def set_answered_question(self, question_id: int, answer: int):
        if not self.db.is_connected():
            self.db.reconnect()
        cursor = self.db.cursor(buffered=True)
        sql = "UPDATE questions SET answered = %s WHERE id = %s"
        val = (answer, question_id)
        cursor.execute(sql, val)
        self.db.commit()

    def get_next_question_to_answer(self):
        if not self.db.is_connected():
            self.db.reconnect()
        cursor = self.db.cursor(buffered=True, dictionary=True)
        sql = "SELECT * FROM questions WHERE authorized=1 AND answered=0 ORDER BY date"
        cursor.execute(sql)
        return cursor.fetchone()

    def get_all_questions(self):
        if not self.db.is_connected():
            self.db.reconnect()
        cursor = self.db.cursor(buffered=True, dictionary=True)
        sql = "SELECT * FROM questions ORDER BY date DESC"
        cursor.execute(sql)
        return cursor.fetchall()


if __name__ == "__main__":
    conn = MysqlConnection()
