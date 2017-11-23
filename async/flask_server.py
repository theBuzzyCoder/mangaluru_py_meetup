import time
from flask import Flask, Response, Markup

app = Flask(__name__)
N_CHUNKS = 100


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return Markup('''
        <html>
            <head>  
                <title> Flask Server </title>
            </head>
            <body>
                <ul>
                    <li> <a href='/getServerCode'> Get Server Code </a> </li>
                </ul>
            </body>
        </html>
    ''')


@app.route('/getServerCode')
def get_server_code():
    with open(__file__, mode='r') as f:
        data = f.read()
        chunk_len = (len(data) // N_CHUNKS)

    def generate():
        i = 0
        while True:
            end = i + chunk_len
            rdata = data[i:end]
            if not rdata:
                break
            else:
                yield rdata
                time.sleep(0.877 / N_CHUNKS)
                i = end

    return '<pre>' + Response(response=generate()).data.decode()


if __name__ == '__main__':
    app.run(threaded=True)
