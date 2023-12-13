
//const URL = "https://claudiavz.pythonanywhere.com/"
const URL = "http://127.0.0.1:5000/"

const app = Vue.createApp({
    data() { //almacenará los datos en el servidor
        return {
            productos: []
        }
    },
    methods: {
        obtenerProductos() {
            // Obtenemos el contenido del inventario del servidor
            fetch(URL + 'productos')
                .then(response => {
                    // Parseamos la respuesta JSON
                    if (response.ok) { return response.json(); }
                })

                .then(data => {
                    // El código Vue itera este elemento para generar la tabla con los datos obtenidos
                    this.productos = data;
                })

                .catch(error => {
                    console.log('Error:', error);
                    alert('Error al obtener los productos.');
                }); //captura y maneja errores
        },
        
        eliminarProducto(codigo) { //se elimina un prod mediante un dialogo de confirmacion
            if (confirm('¿Estás seguro de que quieres eliminar este producto ? ')) {
                fetch(URL + `productos/${codigo}`, { method: 'DELETE' })
                    .then(response => {
                        if (response.ok) {
                            this.productos =
                            this.productos.filter(producto => producto.codigo !== codigo);
                            alert('Producto eliminado correctamente.');
                        }
                    })

                    .catch(error => {
                        alert(error.message);
                    }); //mje de error al querer eliminar
        }
    }
},

mounted() {
    //Al cargar la página por primera vez, obtenemos la lista de productos
    this.obtenerProductos();
}
});

app.mount('body'); //monta el elemento boby del DOM y activa Vue en la pag


