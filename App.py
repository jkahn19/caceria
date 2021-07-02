from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_HOST'] = ''

mysql = MYSQL()


@app.route('/')
def Index():
    return 'Hello World'

@app.route('/add_player')
def add_player():
    return 'add player'

@app.route('/edit_player')
def edit_player():
    return 'edit player'

@app.route('/delete_player')
def delete_playr():
    return 'delete player'

app.run(port = 3000, debug = True)