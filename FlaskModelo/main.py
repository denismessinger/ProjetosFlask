from flask import Flask, render_template, request, redirect, session, flash, url_for

from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key='alura'

test_dir = 'static/test'
batch_size = 12
image_shape = (200,200,3)

image_gen = ImageDataGenerator(rotation_range=30, # rotaciona a imagem 30 graus
                               width_shift_range=0.1, # Desloca a imagem lateralmente por um máximo de 10%
                               height_shift_range=0.1, # Desloca a imagem verticalmente por um máximo de 10%
                               rescale=1/255, # Normaliza a imagem
                               shear_range=0.2, # Recorta a imagem em no máximo 20%
                               zoom_range=0.2, # Da um zoom em no máximo 20 %
                               horizontal_flip=True, # Permite inverter a imagem horizontalmente
                               fill_mode='nearest') # Preenche pixels faltantes baseado nos pixels a volta)

prefixo = " "
test_image_gen = image_gen.flow_from_directory(test_dir,
                                               target_size=image_shape[:2],
                                               batch_size=batch_size,
                                               class_mode='categorical',
                                               save_prefix= True,
                                               shuffle=True)

image_paths = test_image_gen.filepaths
modelo = load_model('model/modelo_treinado.h5')
metal_defects_labels = ['Crazing', 'Inclusion', 'Patches', 'Pitted', 'Rolled', 'Scratches']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():

    prefixo = test_image_gen.batch_index * 12
    X, y = test_image_gen.next()
    cnn_prediction = modelo.predict(X)

    pred_idx = np.argmax(cnn_prediction[0])
    true_idx = np.argmax(y)

    predicao = metal_defects_labels[pred_idx]
    real = metal_defects_labels[true_idx]

    if 'acertos' not in session:
        session['acertos'] = 0
    if 'erros' not in session:
        session['erros'] = 0

    for i, label in enumerate(metal_defects_labels):
        if i == true_idx:
            session[label] = session.get(label, 0) + 1
        else:
            session[label] = session.get(label, 0)

    if predicao == real:
        session['acertos'] += 1
    else:
        session['erros'] += 1

    # Generate a bar chart
    fig, ax = plt.subplots(figsize=(4, 4), dpi=80)
    ax.bar(['Acertos', 'Erros'], [session['acertos'], session['erros']])
    ax.set_ylabel('Quantidade')
    ax.set_title('Gráfico de Acertos e Erros')

    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the chart as a base64 string
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    filtered_labels = [label for label in session.keys() if label not in ['acertos', 'erros']]
    filtered_counts = [session[label] for label in filtered_labels]

    # Generate a horizontal bar chart for labels excluding 'acertos' and 'erros'
    fig, ax = plt.subplots(figsize=(4, 4))  # Adjust size if needed
    ax.barh(filtered_labels, filtered_counts)
    ax.set_xlabel('Quantidade')
    ax.set_title('Quantidade por Defeito')

    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the chart as a base64 string
    chart_data_side = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('index.html',
                           image_path=test_image_gen.filepaths[test_image_gen.index_array[prefixo]],
                           prediction=predicao,
                           type=real,
                           acertos=session['acertos'],
                           erros=session['erros'],
                           chart_data=chart_data,
                           chart_side=chart_data_side)

app.run(debug=True)
