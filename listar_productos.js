
const URL = "https://127.0.0.1:5000/" //servidor donde se recuperan los datos de los prod

// Realizamos la solicitud GET al servidor para obtener todos los productos
fetch(URL + 'productos') //realiza una solicitud GET al servidor
    .then(function (response) { 
        if (response.ok) { //resp de exito
            return response.json(); // devuelv datos en JSON
        } else {
            // Si hubo un error, lanzar una excepción para poder solucionarla luego.
            throw new Error ('Error al obtener los productos.');      
        }
    }) 
    
    .then(function (data) { //maneja los datos convertidos
        let tablaProductos = document.getElementById('tablaProductos');
        // Iteramos sobre los productos y agregamos filas a la tabla
        for (let producto of data) {
            let fila = document.createElement('tr');
            fila.innerHTML = '<td>' + producto.codigo + '</td>' +
                '<td>' + producto.descripcion + '</td>' +
                '<td>' + producto.cantidad + '</td>' +
                '<td>' + producto.precio + '</td>' +
                '<td>' + producto.proveedor + '</td>' +
                // Mostrar miniatura de la imagen
                '<td><img src=static/imagen_producto/' + producto.imagen_url + '" alt = "Imagen del producto" style = "width: 100px;" ></td > ';
                
                //'<td><img src="https://www.pythonanywhere.com/user/ClaudiaVZ/files/home/ClaudiaVZ/mysite/static/imagenes_productos/' + producto.imagen_url + '" alt = "Imagen del producto" style = "width: 100px;" ></td > ';
                
            tablaProductos.appendChild(fila);
        } 
    })  //Una vez que se crea la fila con el contenido del producto, 
       //se agrega a la tabla utilizando el método appendChild del elemento tablaProductos.

    .catch(function (error) {
        alert('Error al obtener productos.');
        console.error('Error:', error);
    }) // En caso de error alerta y mje en pantalla

