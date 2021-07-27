from flask import Flask

app = Flask(__name__)
app.secret_key = 'carro2021'
#db = psycopg2.connect('dbname=projeto user=postgres password=postgres host=127.0.0.1')

from views import *

if __name__ == '__main__':
    app.run(debug=True)