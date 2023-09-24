from flask import Flask, flash, render_template, request, redirect

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


@app.route("/manage", methods=('GET', 'POST'))
def manage():
    if request.method == 'POST':
        question_id = int(request.form.get("id"))
        if "authorized" in request.form:
            if request.form["authorized"] == '1':
                mysql_connection.authorize_question(question_id)
            else:
                mysql_connection.unauthorize_question(question_id)
        if "answered" in request.form:
            if request.form["answered"] == '1':
                mysql_connection.answer_question(question_id)
            else:
                mysql_connection.unanswer_question(question_id)
    questions = mysql_connection.get_all_questions()
    return render_template("manage.html", questions=questions)


@app.route("/show", methods=('GET',))
def show():
    question = mysql_connection.get_next_question_to_answer()
    return render_template("show.html", question=question)


@app.route("/delete", methods=(['POST']))
def delete():
    question_id = int(request.form.get("id"))
    mysql_connection.delete_question(question_id)

    return redirect("manage")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
