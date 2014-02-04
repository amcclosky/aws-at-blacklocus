from bottle import route
from bottle import run

@route('/chaos')
def index():
    return 'Monitored Chaos!'


def main():
    run(host='localhost', port=8080, debug=True)


if __name__ == '__main__':
    main()



