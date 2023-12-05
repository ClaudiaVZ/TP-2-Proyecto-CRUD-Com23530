//CODIGO DE ALTAS

const URL = "http://127.0.0.1:5000/" //url del servidor (desarrollo local)

// reacciona el evento de envío del formulario (lo envia)
document.getElementById('formulario').addEventListener('submit', function
(event) {
    event.preventDefault(); // Evita q el nav recargue la pag
    
    var formData = new FormData(); //crea el OBJETO para enviar dts de formulario al servidor
    formData.append('codigo',    //agrega clave/valor al OBJETO
    document.getElementById('codigo').value); //valor del campo de entrada que ingresa el usuario
    formData.append('descripcion', 
    document.getElementById('descripcion').value);
    formData.append('cantidad', 
    document.getElementById('cantidad').value);
    formData.append('precio', 
    document.getElementById('precio').value);
    formData.append('imagen', 
    document.getElementById('imagenProducto').files[0]);
    formData.append('proveedor', 
    document.getElementById('proveedorProducto').value);
    
    //solicitud POST al servidor
    fetch(URL + 'productos', {
        method: 'POST', //define el met HTML como POST
        body: formData  //establece el cuerpo de la solic HTML como OBJ
    }) // Aquí enviamos formData en lugar de JSON

    //Después de realizar la solicitud POST, se utiliza el método then() 
    //maneja la respuesta del servidor.
    .then(function (response) { 
        if (response.ok) {
            return response.json();} //si la resp es exitosa, convierte los datos en JSON
        else {
            // Si hubo un error, lanzar explícitamente una excepción (throw) que detiene la ejecucion normal del codigo; para poder identificar el error.
            throw new Error('Error al agregar el producto.');
            } // mje de error
    }) 

    // Respuesta OK
    .then(function () {
         // En caso de que el prod se agregó
        alert('Producto agregado correctamente.');
    }) //mje de exito

    .catch(function (error) {
        // En caso de error
        alert('Error al agregar el producto.');
        console.error('Error:', error);
    }) //captura y maneja cualq error que pueda ocurrir durante la solic fetch
    
    //se limpian los campos para que puedan ser utilizados para un nuevo producto
    .finally(function () {
        // Limpiar el formulario en ambos casos (éxito o error)
        document.getElementById('codigo').value = "";
        document.getElementById('descripcion').value = "";
        document.getElementById('cantidad').value = "";
        document.getElementById('precio').value = "";
        document.getElementById('imagenProducto').value = "";
        document.getElementById('proveedorProducto').value = "";});
    })



