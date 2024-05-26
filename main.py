from flask import Flask, request, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assicurati che la cartella esista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        processed_file_path = process_csv(file_path)
        return send_file(processed_file_path, as_attachment=True)

def process_csv(file_path):
    data = pd.read_csv(file_path, delimiter=';')
    # Filtro per status 'Online'
    filtered_data = data[data['status'] == 'Online']

    # Calcolo del 10% in meno del prezzo del buybox
    filtered_data['price'] = filtered_data['buybox_price'] * 0.90

    new_data = pd.DataFrame({
        'product_id': filtered_data['product_uuid'],
        'listing_id': filtered_data['listing_id'],
        'market': 'fr-fr',
        'price': filtered_data['price'],
        'sku': filtered_data['sku'].where(pd.notnull(filtered_data['sku']), None),
        'grade_code': filtered_data['grade_code']
    })

    # Formattare la colonna 'price' per avere due cifre decimali
    new_data['price'] = new_data['price'].apply(lambda x: format(float(x), '.2f'))

    new_file_path = file_path.replace('.csv', '_processed.csv')
    new_data.to_csv(new_file_path, index=False)
    return new_file_path

if __name__ == '__main__':
    app.run(debug=True)

