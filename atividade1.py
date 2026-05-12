from flask import Flask

app = Flask(__name__)


@app.route('/decorator')
def ola_mundo():
    return 'Ele é usado para mapear a função, são funções que modificam ou aprimoram o comportamento de outras funções ou métodos sem alterar seu código-fonte original \n @app.route()'


if __name__ == '__main__':
    app.run(debug=True)