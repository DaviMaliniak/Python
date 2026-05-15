from flask import Flask, render_template


app = Flask(__name__) 

@app.route("/cotemig/curriculo")
def curriculo():
    return render_template("home.html")

@app.route('/cotemig/<nome>')
def cotemig(nome):
    return f'Olá, {nome}! Bem-vindo ao Cotemig.'

if __name__ == '__main__':
    app.run(debug=True) 
