#importar modulos y liberias
from flask import Flask, request, jsonify

from flask_cors import CORS

import mysql.connector

from werkzeug.utils import secure_filename

import os
import time 

#inicializar Flask y habilitar Cors
app = Flask(__name__)
CORS(app)             #cors para todas las rutas

#clase catalogo 
class Catalogo: 
    
     #Metodo CONSTRUCTOR def __init__ 
    def __init__(self, host, user, password, database): #4 parametros

        self.conn = mysql.connector.connect(
            host = host,             
            user = user,             
            password = password,    
            #database = database      
        ) #inicializa la conexion sin especificar base de datos
    
        self.cursor = self.conn.cursor()  #se configura el cursor sin opc especificas

        try: #seleccionar la BDD
            self.cursor.execute(f"USE {database}") 
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}") # Si la base de datos no existe, la crea
                self.conn.database = database
            else:
                raise err
            
     #una vez establecida la BDD, crea la tabla si no existe.
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS productos (
            codigo INT PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),            
            proveedor INT)''') 
        self.conn.commit() #confirma la creacion de la tabla

        self.cursor.close() #cerramos el cursor inicial
        self.cursor = self.conn.cursor(dictionary = True) #abrimos cursor nuevo con parametro dicc true para que cada consulta sea devuelta como un diccionario


     #Metodo listar prodcuctos (muestra una lista de todos los productos) operacion de lectura.
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos") #consulta sobre todos los registros de la tabla
        productos = self.cursor.fetchall() # recupera y devuelve todos los productos de la consulta en una lista de dicc
        return productos
    

     #Metodo consultar productos por su Cod
    def consultar_producto(self, codigo):
        self.cursor.execute(f"SELECT * FROM pacientes WHERE codigo = {codigo}")
        return self.cursor.fetchone() # busca el producto y lo muestra, si no, retorna false

   
     #Metodo mostrar productos por su Cod
    def mostrar_producto(self, codigo):

        producto = self.consultar_producto(codigo) #si encuentra el producto, muestra los detalles
        if producto:
            print("-" * 50)  # linea de separacion
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción.....: {producto['descripcion']}")
            print(f"Cantidad.....: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
            print(f"Imagen_url.....: {producto['imagen_url']}")
            print(f"Proveedor.....: {producto['proveedor']}")
            print("-" * 50) 
        else:
            print("Producto NO encontado.") # si no encuentra el producto, imprime un mje.


     #Metodo agregar productos a la BDD MySQL (evita duplicados)
    def agregar_producto(self, codigo, descripcion, cantidad, precio, imagen, proveedor):
    
         #consulto si hay un producto con el mismo codigo
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone() #(ir a buscar)
        if producto_existe:
            return False   # si el producto ya existe, no se vuelve a agregar
    
         #si no existe, entonces lo agrega a la tabla con los valores proporcionados
        sql = "INSERT INTO productos (codigo, descripcion, cantidad, precio, imagen_url, proveedor) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (codigo, descripcion, cantidad, precio, imagen, proveedor)
        
        self.cursor.execute(sql, valores)  #guarda el producto nuevo
        self.conn.commit()   #cambios guardados de manera permanente en la BDD
        return True     #el producto se agrego con exito!        


     #Metodo eliminar producto (elimina un producto mediante su Cod)
    def eliminar_producto(self, codigo):
        #self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo}")
        sql = "DELETE FROM productos WHERE codigo = %s"
        valores = (codigo,) #evita ataques de vulneravilidad
        self.cursor.execute(sql, valores)
        self.conn.commit() #confirmar los cambios
        return self.cursor.rowcount > 0 #evalua si la eliminacion fue exitosa (>0 indica q se ha eliminado un producto; <0 indica q el producto no fue encontrado)


     #Metodo modificar producto por su Cod (actualizar los datos)
    def modificar_producto(self, codigo, descripcion_nueva, cantidad_nueva, precio_nuevo, imagen_nueva, proveedor_nuevo):
     #consulta para evitar inyecciones (vulneravilidad de seg)
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, imagen_url = %s, proveedor = %s WHERE codigo = %s" 
        valores = (descripcion_nueva, cantidad_nueva, precio_nuevo, imagen_nueva, proveedor_nuevo, codigo)
    
        self.cursor.execute(sql, valores) #busca el producto, aplica las modif 
        self.conn.commit()              #confirma los cambios
        return self.cursor.rowcount > 0 #num de filas afectadas


#CUERPO DEL PROGRAMA (crear catalogo)

#instancia de la clase catalogo (4 Argumentos)
#Catalogo = Catalogo(host='localhost', user='root', password='', database='miapp')

Catalogo = Catalogo(host= 'ClaudiaVZ.mysql.pythonanywhere-services.com', user= 'ClaudiaVZ', password= 'proyectocrud23', database= 'ClaudiaVZ$miapp')


#carpeta donde se guardan las imagenes 
#ruta_destino = './static/imagenes_productos/'
ruta_destino = '/home/ClaudiaVZ/mysite/static/imagenes_productos/' #cambio la ruta de las imagenes por la q me dá anywhere en files con slash al principio y fin sino, no carga las imagenes(aparecen rotas)

 #RUTAS

 #Ruta listar productos
@app.route("/productos", methods = ["GET"]) #asocia la funcion con la url, responde a solicitudes HTTP (web)
def listar_productos():
    productos = Catalogo.listar_productos() #devuelve una lista de dicc donde cada dicc representa 1 producto
    return jsonify(productos) #devuelve los datos en formato JSON(APIs)


 #Ruta mostrar producto
@app.route("/productos/<int:codigo>", methods = ["GET"]) #representa el num de codigo del prooducto
def mostrar_producto(codigo): #solicitud para dif codigos
    Catalogo.mostrar_producto(codigo)
    producto = Catalogo.consultar_producto(codigo) #llama al metodo, y busca en la BDD
    if producto:
        return jsonify(producto) #si encuentra el producto, muestra los detalles
    else:
        return "Producto NO encontrado", 404 #si no lo encuentra tira un mje de error.


 #Ruta agregar productos (ruta Flask -punto de acceso- permite registrar un nuevo producto a la base de datos)
@app.route("/productos", methods = ["POST"]) #solicitudes HTTP POST, URL es /productos.
def agragar_producto(): #se asocia a la url cuando se consulta por un producto y accede a los campos del form (recoge los datos)
    codigo = request.form['codigo']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    proveedor = request.form['proveedor']
    imagen = request.files['imagen']
    nombre_imagen = secure_filename (imagen.filename) #nombre del archivo seguro

    nombre_base, extension = os.path.splitext(nombre_imagen) #separa el nombre del archivo de su extension
    nombre_imagen = f"{nombre_base} _ {int(time.time())} {extension}" #genera un nuevo nombre a la imagen para evitar conflictos
    imagen.save(os.path.join(ruta_destino, nombre_imagen)) #guarda la imagen en el servidor

    if Catalogo.agregar_producto(codigo, descripcion, cantidad, precio, nombre_imagen, proveedor): #se llama a la funcion que intenta agregar el producto
        return jsonify({"mensaje": "Producto Agregado!"}), 201 #resp JSON HTTP 201 (creado)
    else:
        return jsonify({"mensaje": "El Producto ya Existe"}), 400  #resp JSON HTTP 400 (no creado)


 #Ruta eliminar producto (DELETE)
@app.route("/productos/<int:codigo>", methods = ["DELETE"])
def eliminar_producto(codigo):
     # Primero, obtiene la información del producto para encontrar la imagen
    producto = Catalogo.consultar_producto(codigo)
    if producto:
     # Elimina la imagen asociada, si existe
        ruta_imagen = os.path.join(ruta_destino, producto['imagen_url'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

     # Luego, elimina el producto del catálogo
        if Catalogo.eliminar_producto(codigo):
            return jsonify({"mensaje": "Producto Eliminado!"}), 200 #si lo encuentra muestra mje de exito
        else:
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500 #si no lo encuentra muestra mje ERROR
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
        #si el prod NO exite muestra mje de NO ENCONTRADO


 #Ruta modificar Producto
@app.route("/productos/<int:codigo>", methods = ["PUT"]) #Cod del producto a modif
def modificar_producto(codigo): #llama a la funcion cuando se realiza una consulta seguida de un num (Cod) recoge los datos
    descripcion_nueva = request.form.get("descripcion")
    cantidad_nueva = request.form.get("cantidad")
    precio_nuevo = request.form.get("precio")
    proveedor_nuevo = request.form.get("proveedor")

    #procesar imagen (actualiza la imagen en el servidor)
    imagen = request.files['imagen']
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    imagen.save(os.path.join(ruta_destino, nombre_imagen))

    #actualizar datos del producto de manera segura y controlada
    if Catalogo.modificar_producto(codigo, descripcion_nueva, cantidad_nueva, precio_nuevo, proveedor_nuevo, nombre_imagen):
        return jsonify({"mensaje": "Producto Modificado!"}), 200
    else:
        return jsonify({"mensaje": "Producto NO encontrado"}), 404


 #ejecutar la aplicacion (solo se ejecuta el servidor web flask cuando al hacer una consulta se ejecuta el script)
#if __name__ == "__main__":
    app.run(debug=True)

#finalizamos la implementacion de la API


