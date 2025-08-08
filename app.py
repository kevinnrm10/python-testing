from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecreto"  # Necesario para usar flash()

DATA_PATH = 'data/tickets.csv'

@app.route('/')
def dashboard():
    df = pd.read_csv(DATA_PATH)
    prioridad = request.args.get('prioridad')
    if prioridad:
        df = df[df['prioridad'] == prioridad]
    estado = request.args.get('estado')
    if estado:
        df = df[df['estado'] == estado]
    conteo = df['prioridad'].value_counts().to_dict()
    return render_template(
        "dashboard.html",
        data=df.to_dict(orient="records"),
        filtro=prioridad,
        filtro_estado=estado,
        conteo=conteo
)

@app.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        prioridad = request.form['prioridad']
        estado = request.form['estado']

        # Validaciones simples
        if not nombre:
            flash("El nombre no puede estar vacío", "danger")
            return render_template('nueva.html')

        if prioridad not in ['alta', 'media', 'baja']:
            flash("Prioridad inválida", "danger")
            return render_template('nueva.html')

        if estado not in ['abierta', 'cerrada']:
            flash("Estado inválido", "danger")
            return render_template('nueva.html')

        # Guardar si todo es correcto
        df = pd.read_csv(DATA_PATH)
        nuevo = pd.DataFrame([{
            'nombre': nombre,
            'prioridad': prioridad,
            'estado': estado
        }])
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        flash("Ticket guardado correctamente ✅", "success")
        return redirect('/')

    return render_template('nueva.html')

if __name__ == '__main__':
    app.run(debug=True)
