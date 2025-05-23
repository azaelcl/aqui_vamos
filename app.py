from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Cargar datos
file_path = os.path.join(os.path.dirname(__file__), 'data.xlsx')
df = pd.read_excel(file_path)

# Asegurarnos de que la columna 'Número' sea de tipo entero
df['Número'] = df['Número'].fillna(0).astype(int)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Definir categorías
CATEGORIES = ["Ilustración", "Poesía", "Narrativa", "Ensayo/Artículo", "Textos Periodísticos",
              "Reseñas", "Correo", "Varia", "No especificada"]

# Ruta para la base de datos
@app.route('/database', methods=['GET'])
def database():
    # Obtener filtros de la solicitud
    author_filter = request.args.get('author', '')
    title_filter = request.args.get('title', '')
    date_filter = request.args.get('date', '')
    number_filter = request.args.get('number', '')
    year_filter = request.args.get('year', '')
    category_filter = request.args.get('category', '')

    # Aplicar filtros a DataFrame
    filtered_df = df.copy()

    if author_filter:
        filtered_df = filtered_df[filtered_df['Autor'].str.contains(author_filter, case=False, na=False)]
    if title_filter:
        filtered_df = filtered_df[filtered_df['Título'].str.contains(title_filter, case=False, na=False)]
    if date_filter:
        filtered_df = filtered_df[filtered_df['Fecha'] == date_filter]
    if number_filter:
        filtered_df = filtered_df[filtered_df['Número'] == int(number_filter)]
    if year_filter:
        filtered_df = filtered_df[filtered_df['Año'] == int(year_filter)]
    if category_filter:
        # Buscar registros donde 'Categoría' contenga la categoría seleccionada
        filtered_df = filtered_df[filtered_df['Categoría'].str.contains(category_filter, case=False, na=False)]

    # Calcular el total de filas después de aplicar los filtros
    total_rows = len(filtered_df)

    # Convertir a diccionario para enviarlo a la plantilla
    data = filtered_df.to_dict(orient='records')
    return render_template('database.html', data=data, categories=CATEGORIES, total_rows=total_rows)

# Ruta para los gráficos
@app.route('/charts')
def charts():
    return render_template('charts.html')

# Ruta para el contacto
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Ruta para enviar datos en formato JSON
@app.route('/data')
def get_data():
    data = {
        "years": df['Año'].tolist(),
        "authors": df['Autor'].tolist(),
        "numbers": df['Número'].tolist()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
