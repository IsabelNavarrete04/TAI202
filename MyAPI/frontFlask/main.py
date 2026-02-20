from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

myAPI = "http://localhost:5001/v1/usuarios"

@app.route('/')
def vista():
    servidor = requests.get(myAPI)
    datos = servidor.json()
    return render_template('vista.html', usuarios=datos["usuarios"])

@app.route('/agregar', methods=["POST"])
def agregar():
    nuevo = {
        "id": int (request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int (request.form["edad"])
    }
    requests.post (myAPI, json = nuevo)
    return redirect("/")

@app.route('/eliminar/<int:id>')
def eliminar(id):
    requests.delete(myAPI + "/" + str(id))
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=500)