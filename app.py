#--------------------------------------------------------------------
# !Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
# from flask import request

# !Instalar con pip install flask-cors
from flask_cors import CORS

# !Instalar con pip intall mysql-connector-python
import mysql.connector

# !Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# !No es necesario instalar, es parte del sistema standar de Python

import os
import time

app = Flask(__name__)
CORS(app) # +Esto habilitará CORS para todas las rutas

# !Definimos la clase Catalogo
class Catalogo: # +Primero, se establece una conexión sin especificar la base de datos
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        # !Intentamos Selecionar la base de Datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # !Si la base de Datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor = self.conn.cursor(dictionary=True)
        # Si la tabla 'autos' no existe, la creamos
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS autos (
            codigo INT,
            marca VARCHAR(50) NOT NULL,
            cantidad INT(4),
            precio INT(20),
            imagen VARCHAR(500) NOT NULL,
            modelo VARCHAR(50) NOT NULL,
            anio INT(5),
            km INT(7),
            motor VARCHAR(255) NOT NULL,
            transmision VARCHAR(255) NOT NULL)''')
        self.conn.commit()
        
        # !Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary = True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        

    # !Método para agregar un auto a la tabla (Catalogo)
    def agregar_auto(self, codigo, marca, cantidad, precio, imagen, modelo, anio, km, motor, transmision):
        # +Verificamos si el auto ya existe en la tabla
        self.cursor.execute(f"SELECT * FROM autos WHERE codigo = {codigo}")
        auto_existe = self.cursor.fetchone() #+Devuelve un único resgistro
        
        if auto_existe:
            return False
        #+Si no existe agregamos el nuevo auto a la tabla
        sql = f"INSERT INTO autos \
                (codigo, marca, cantidad, precio, imagen, modelo, anio, km, motor, transmision) \
                VALUES \
                ({codigo}, '{marca}', {cantidad}, {precio}, '{imagen}', '{modelo}', {anio}, {km}, '{motor}', '{transmision}')"
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    # !Método para consultar un auto a partir de su codigo
    def consultar_auto(self, codigo):
        # +Se busca el auto en la tabla de autos a partir de su codigo
        self.cursor.execute(f"SELECT * FROM autos WHERE codigo = {codigo}")
        return self.cursor.fetchone() #+fetchone retorna un unico registro
        

    # !Método para modificar los detalles de un auto
    def modificar_auto(self, codigo, nueva_cantidad, nuevo_precio, nueva_imagen):
        # +Modficamos los datos del auto a partir de su codigo
        sql = f"UPDATE autos SET \
                    cantidad = {nueva_cantidad}, \
                    precio = {nuevo_precio}, \
                    imagen = '{nueva_imagen}'\
                WHERE codigo = {codigo}"
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.rowcount > 0 #+ el metodo rowcount devuelve el numero de filas afectadas por la consulta
        
    # !Método para mostrar los detalles de un auto por código
    def mostrar_auto(self, codigo):
        # +Consultamos el auto por su codigo
        auto = self.consultar_auto(codigo)
        if auto:
            # +Vemos los detalles del auto en la pantalla
            print("=" * 50)
            print(f"Código.....: {auto['codigo']}")
            print(f"Marca......: {auto['marca']}")
            print(f"Cantidad...: {auto['cantidad']}")
            print(f"Precio.....: {auto['precio']}")
            print(f"Imagen.....: {auto['imagen']}")
            print(f"Modelo.....: {auto['modelo']}")
            print(f"Año........: {auto['anio']}")
            print(f"Kilometraje: {auto['km']}")
            print(f"Motor......: {auto['motor']}")
            print(f"Transmision: {auto['transmision']}")
            print("=" * 50)
        else:
            print("Modelo no encontrado.")

    # !Método para obtener un listado de los autos
    def listar_autos(self):
        # +Mostramos en pantalla un listado de todos los autos de la tabla
        self.cursor.execute(f"SELECT * FROM autos")
        autos = self.cursor.fetchall() #+ Muestra todos los resgistros en una consulta de SQL
        return autos
        

    # !Método para eliminar un auto por codigo
    def eliminar_auto(self, codigo):
        # +eliminamos un auto de la tabla a partir del codigo
        self.cursor.execute(f"DELETE FROM autos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0 #+ el metodo rowcount devuelve el numero de filas afectadas por la consulta

# !Programa Principal
# +Verificación
# catalogo = Catalogo(host='localhost', user='root', password='', database='miapp')
catalogo = Catalogo(host='', user='', password='', database='')


# !Carpeta para guardar las imagenes
# RUTA_DESTINO = './static/imagenes/'

#+Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
RUTA_DESTINO = '/home/eosuna85/mysite/static/imagenes'

# # +Agregamos productos a la tabla
# catalogo.agregar_auto(123, 'Ford', 1, 13000, 'Falcon.jpg', 'Falcon', 1980, 140000, '6 Cilindros', 'Manual')
# catalogo.agregar_auto(223, 'Ford', 1, 7000, 'Fairlane.jpg', 'Fairlane', 1972, 98000, 'V8', 'Manual')
# catalogo.agregar_auto(345, 'Ford', 1, 110000, 'Mustang.jpg', 'Mustang', 1965, 46639, 'V8', 'Manual')
# catalogo.agregar_auto(456, 'Chevrolet', 1, 95000, 'ChevySSChevelle.jpg', 'Chevy SS', 1966, 40000, 'V8', 'Manual')
# catalogo.agregar_auto(578, 'Chevrolet', 1, 110000, 'CoupeSSCamaro.jpg', 'Camaro', 2019, 21000, 'V8', 'Manual')
# catalogo.agregar_auto(652, 'Chevrolet', 1, 6000, 'Nova.jpg', 'Nova', 1969, 100000, '6 Cilindros', 'Automatica')
# catalogo.agregar_auto(725, 'Dodge', 1, 99800, 'ScatPack.jpg', 'Charllenger', 2016, 30000, 'V8', 'Automatica Secuencial')
# catalogo.agregar_auto(811, 'Dodge', 1, 109000, 'ChargerSRT392.jpg', 'Charger', 2015, 21000, 'V8', 'Automatica')
# catalogo.agregar_auto(996, 'Dodge', 1, 75000, 'GTSViper.jpg', 'Viper', 1996, 30000, 'V8', 'Manual')

# # +Modificamos un auto
# # catalogo.modificar_auto(996, 3, 75000, 'GTS_Viper.jpg', 36000)


# # +Eliminamos un auto
# # catalogo.eliminar_auto(996)


# !Construimos la ruta para ejecutar el método listar artículo
@app.route("/autos", methods = ["GET"]) # +GET: método para obtener respuesta a una petición.
def listar_autos():
    autos = catalogo.listar_autos()
    return jsonify(autos)

# !Mostrar un sólo auto según su código
@app.route("/autos/<int:codigo>", methods=["GET"])
def mostrar_auto(codigo):
    auto = catalogo.consultar_auto(codigo)
    if auto:
        return jsonify(auto), 201
    else:
        return "Auto no encontrado.", 404

# !Agregar un auto
@app.route("/autos", methods=["POST"])
def agregar_auto():
    # +Recojo los datos del form
    codigo = request.form['codigo']
    marca = request.form['marca']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    imagen = request.files['imagen']
    modelo = request.form['modelo']
    anio = request.form['anio']
    km = request.form['km']
    motor = request.form['motor']
    transmision = request.form['transmision']  
    nombre_imagen=""

#+ Me aseguro que el auto exista en la lista del stock
    auto = catalogo.consultar_auto(codigo)
    if not auto: # +Si no existe el auto...
        # +Genero el nombre de la imagen
        nombre_imagen = secure_filename(imagen.filename) #+Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #+Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #+Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.
        
        #+Se agrega el auto a la base de datos
        if  catalogo.agregar_auto(codigo, marca, cantidad, precio, nombre_imagen, modelo, anio, km, motor, transmision):
            imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

            #+Si el Auto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
            return jsonify({"mensaje": "Auto agregado correctamente.", "imagen": nombre_imagen}), 201
        else:
            #+Si el Auto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
            return jsonify({"mensaje": "Error al agregar el Auto."}), 500

    else:
        #+Si el Auto ya existe (basado en el código), se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 400 (Solicitud Incorrecta).
        return jsonify({"mensaje": "Auto ya existe en la lista."}), 400


# !Modificar un auto según su código
@app.route("/autos/<int:codigo>", methods=["PUT"])
#+La ruta Flask /autos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un auto existente en la base de datos, identificado por su código.
#+La función modificar_auto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /autos/ seguido de un número (el código del auto).

def modificar_auto(codigo):
    #+Se recuperan los nuevos datos del formulario
    nueva_cantidad = request.form.get("cantidad")
    nuevo_precio = request.form.get("precio")
    imagen = request.files['imagen']

    #+Procesamiento de la imagen
    nombre_imagen = secure_filename(imagen.filename) #+Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #+Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #+Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    #+Busco el auto guardado
    auto = auto = catalogo.consultar_auto(codigo)
    if auto: #+Si existe el auto...
        imagen_vieja = auto["imagen"]
        #+Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        #+Y si existe la borro.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
    
    #+Se llama al método modificar_auto pasando el codigo del auto y los nuevos datos.
    if catalogo.modificar_auto(codigo, nueva_cantidad, nuevo_precio, nombre_imagen):
        #+La imagen se guarda en el servidor.
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #+Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Auto modificado"}), 200
    else:
        #+Si el auto no se encuentra (por ejemplo, si no hay ningún auto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Auto no encontrado"}), 403


# !Eliminar un auto según su código
@app.route("/autos/<int:codigo>", methods=["DELETE"])
#+La ruta Flask /autos/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un auto específico de la base de datos, utilizando su código como identificador.
#+La función eliminar_auto se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /autos/ seguido de un número (el código del auto).

def eliminar_auto(codigo):
    #+Busco el auto en la base de datos
    auto = catalogo.consultar_auto(codigo)
    if auto: #+Si el auto existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = auto["imagen"]
        #+Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        #+Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        #+Luego, elimina el auto del catálogo
        if catalogo.eliminar_auto(codigo):
            #+Si el auto se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Auto eliminado"}), 200
        else:
            #+Si ocurre un error durante la eliminación (por ejemplo, si el auto no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error Scon un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el auto"}), 500
    else:
        #+Si el auto no se encuentra (por ejemplo, si no existe un auto con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Auto no encontrado"}), 404

# ! para que se muestre el archivo json y corra en el debug si hay un error
if __name__ == "__main__":
    app.run(debug = True)
