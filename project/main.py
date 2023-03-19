import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_security.decorators import roles_accepted,roles_required
from werkzeug.utils import secure_filename

from project import baseD
from project.models import Game
from . import db


main = Blueprint('main',__name__)

#Definimos las rutas

#Definimos la ruta para la página principal
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

#Definimos la ruta para la página de perfil de usuairo
@main.route('/profile')
#@roles_required('')
@login_required
def profile():
        
    return render_template('profile.html', name = current_user.name)

#Ruta para galeria de productos
@main.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    connection = baseD.get_connection()

    with connection.cursor() as cursor:
                cursor.execute('call getAllGames()')
                games= cursor.fetchall()
                
    connection.commit()
    connection.close()


    return render_template('products.html', games = games)

#Agregar productos
@main.route('/addGame', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def addGame():
    
    if request.method == 'POST':     
   
        name = request.form.get('nameG')
        price = request.form.get('price')
        gender = request.form.get('gender')
        platform = request.form.get('platform')
        
        img=str(uuid.uuid4())+'.png'
        imagen=request.files['image']
        ruta_imagen = os.path.abspath('project\\static\\img')
        imagen.save(os.path.join(ruta_imagen,img))
   
        try:
            connection = baseD.get_connection()

            with connection.cursor() as cursor:
                cursor.execute('call insertGame(%s,%s,%s,%s,%s)',
                               (name, price, gender, platform, img))
                resultset = cursor.fetchall()

            connection.commit()
            connection.close()
            return redirect(url_for('main.ABCGames'))
            
        except Exception as ex:
                print(ex)
    return render_template('gamesForm.html')

@main.route("/updateG", methods=['GET', 'POST'])
def updateG():    
    if request.method == 'GET':
        id = request.args.get('id')
        game = Game.query.get(id)
        print(game)
        return render_template('modificar.html', game=game,id=id)
        
    if request.method == 'POST':
        id = request.args.get('id')
        game = Game.query.get(id)
        game.name = request.form.get('nameG')
        game.price = request.form.get('price')
        game.gender = request.form.get('gender')
        game.platform = request.form.get('platform')
        imagen = request.files.get('image')
        ruta_imagen = os.path.abspath('project\\static\\img')
        if imagen:
            # Eliminar la imagen anterior
            os.remove(os.path.join(ruta_imagen, game.image))
            # Guardar la nueva imagen
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(ruta_imagen, filename))
            game.image = filename
        db.session.commit()
        flash("El registro se ha modificado exitosamente.", "exito")
            
    return redirect(url_for('main.ABCGames'))

@main.route("/deleteG", methods=['GET', 'POST'])
def deleteG():    
    if request.method == 'GET':
        id = request.args.get('id')
        game = Game.query.get(id)
        print(game)
        return render_template('eliminar.html', game=game,id=id)
        
    if request.method == 'POST':
        id = request.args.get('id')
        game = Game.query.get(id)
        game.name = request.form.get('nameG')
        game.price = request.form.get('price')
        game.gender = request.form.get('gender')
        game.platform = request.form.get('platform')
        imagen = request.files.get('image')
        ruta_imagen = os.path.abspath('project\\static\\img')
        if imagen:
            # Eliminar la imagen anterior
            os.remove(os.path.join(ruta_imagen, game.image))
            # Guardar la nueva imagen
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(ruta_imagen, filename))
            game.image = filename
        db.session.delete(game)
        db.session.commit()
        return redirect(url_for('main.ABCGames'))
    #flash("El registro se ha modificado exitosamente.", "exito")
            
    return redirect(url_for('main.ABCGames'))


#ABC de productos
@main.route('/ABCGames', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def ABCGames():
    
    connection = baseD.get_connection()

    with connection.cursor() as cursor:
                cursor.execute('call getAllGames()')
                games= cursor.fetchall()
                
    connection.commit()
    connection.close()


    return render_template('gamesList.html', games = games)
