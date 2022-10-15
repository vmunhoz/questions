from flask import Flask, flash, render_template, request

from configuration import config
from connections.mysql_connection import MysqlConnection

mysql_connection = MysqlConnection(config)

app = Flask(__name__)
app.secret_key = config["FLASK"]["SECRET_KEY"]


@app.route("/", methods=('GET', 'POST'))
def ask():
    if request.method == 'POST':
        author = request.form.get("author")
        question = request.form.get("question")
        mysql_connection.insert_question(question, author)
        flash('Pergunta realizada com sucesso!')

    return render_template("ask.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
