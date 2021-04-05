import google_t

from flask import Flask, render_template, request, url_for, jsonify
from werkzeug.utils import redirect
from csv_manager import CsvManager
import mydb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjbcbkjsFGG(0knsdpcp887364hh*ˆˆghe'

user_id = 'stishechko'
buckets = ['zero', 'one', 'two', 'three', 'four']


def upload_csv(user):
    db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
    # csvfile = 'static/files/words.csv'
    csvfile = 'static/files/verben_prap.csv'
    csv_man = CsvManager(csvfile)
    words = csv_man.get_all_words()
    for word in words:
        query = f"INSERT INTO words_{user}(source, target, zero, one, two, three, four) " \
                f"VALUES ('{word[0]}','{word[1]}', 1, 0, 0, 0, 0);"
        db.execute_query(query)


# all Flask routes below
@app.route("/")
def home():
    db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
    # get buckets
    query = f"SELECT sum(zero), sum(one), sum(two), sum(three), sum(four) " \
            f"from words_{user_id} "
    dataset = db.return_rows(query)
    temp_list_set = list(dataset[0])
    # converting None to 0
    list_set = [0 if j is None else j for j in temp_list_set]
    # get settings
    query = f"SELECT randomize, round_size " \
            f"from settings_{user_id} "
    settings_list = list(db.return_rows(query)[0])
    return render_template("index.html", dataset=list_set, settings=settings_list)


@app.route("/bucket/<bucket>")
def serve_bucket(bucket):
    db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
    # get settings
    query = f"SELECT randomize, round_size " \
            f"from settings_{user_id} "
    settings_list = list(db.return_rows(query)[0])
    groupby = ""
    if settings_list[0] == 1:
        groupby = "GROUP by RANDOM()"

    query = f"SELECT * from words_{user_id} " \
            f"WHERE {bucket} = 1 " \
            f"{groupby}" \
            f"LIMIT {settings_list[1]}"
    pairs = db.return_rows(query)
    if len(pairs) == 0:
        return redirect(url_for('home'))

    return render_template("stack.html", words=pairs, count=len(pairs), bucket=bucket)


@app.route("/trans", methods=["POST"])
def translate():
    if request.method == "POST":
        translated = google_t.translate_text('ru', request.get_json()['deu'])
        return translated


@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
        deu = request.get_json()['deu']
        rus = request.get_json()['rus']
        deu = deu.lower().strip()
        rus = rus.lower().strip()
        # check for duplicates. if both deu and rus exist - return 'NOK'
        query = f"SELECT * FROM words_{user_id} where source = '{deu}' AND target = '{rus}'"
        f = db.return_rows(query)
        if len(f) != 0:
            return 'NOK'

        query = f"INSERT INTO words_{user_id}(source, target, zero, one, two, three, four) " \
                f"VALUES ('{deu}','{rus}', 1, 0, 0, 0, 0);"
        db.execute_query(query)

        return 'OK', 200


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
        deu = request.get_json()['deu']
        rus = request.get_json()['rus']
        w_id = request.get_json()['w_id']
        deu = deu.lower().strip()
        rus = rus.lower().strip()
        w_id = int(w_id.lower().strip())
        # check for duplicates. if both deu and rus exist - return 'NOK'
        query = f"SELECT * FROM words_{user_id} where source = '{deu}' AND target = '{rus}'"
        f = db.return_rows(query)
        if len(f) != 0:
            return 'NOK'

        query = f"UPDATE words_{user_id} " \
                f"SET source = '{deu}' , target = '{rus}' " \
                f"WHERE id = {w_id}"
        db.execute_query(query)

        return 'OK', 200


@app.route("/mark", methods=["POST"])
def mark():
    if request.method == "POST":
        bucket = request.get_json()['bucket']
        if bucket == 'four':
            return 'OK'
        next_bucket = buckets[buckets.index(bucket) + 1]
        db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
        word_id = int(request.get_json()['id'])
        query = f"UPDATE words_{user_id} SET {bucket} = 0, {next_bucket} = 1 WHERE id = {word_id}"
        db.execute_query(query)

        return 'OK'


@app.route("/settings", methods=["POST"])
def settings():
    if request.method == "POST":
        randomize = 0
        if request.get_json()['randomize']:
            randomize = 1
        round_size = int(request.get_json()['round_size'])
        db = mydb.MyDatabase(dbtype=mydb.SQLITE, dbname='wortkarte.sqlite')
        query = f"UPDATE settings_{user_id} SET randomize = {randomize}, round_size = {round_size}"
        db.execute_query(query)

        return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
