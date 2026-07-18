import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpeta para guardar las imágenes subidas
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Lista donde guardaremos todas las noticias y sus comentarios
noticias = []

@app.route('/')
def index():
    return render_template('index.htm', noticias=noticias)

@app.route('/publicar', methods=['POST'])
def publicar():
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    autor = request.form.get('autor')
    
    # Manejo de la imagen
    imagen = request.files.get('imagen')
    nombre_imagen = None
    if imagen and imagen.filename != '':
        nombre_imagen = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))
    
    # Crear la nueva noticia con una lista vacía para comentarios
    nueva_noticia = {
        'titulo': titulo,
        'contenido': contenido,
        'autor': autor,
        'imagen': nombre_imagen,
        'comentarios': []
    }
    noticias.append(nueva_noticia)
    
    return redirect(url_for('index'))

@app.route('/comentar', methods=['POST'])
def comentar():
    # Obtener el índice de la noticia y el texto del comentario
    noticia_id = int(request.form.get('noticia_id'))
    texto = request.form.get('texto_comentario')
    
    # Guardar el comentario en la noticia correspondiente
    if noticia_id < len(noticias):
        noticias[noticia_id]['comentarios'].append(texto)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Crear carpeta de subida si no existe
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)