const URL = "http://127.0.0.1:5000/" //serv local

const app = Vue.createApp({ //define un objeto crea una Vue dentro de otra
    data() { //variables reactivas para cambiar valores
        return {
            codigo: '',
            descripcion: '',
            cantidad: '',
            precio: '',
            proveedor: '',
            imagen_url: '',
            imagenUrlTemp: null,
            mostrarDatosProducto: false,
        };
    },
    methods: { //define las funciones para ser usadas
        obtenerProducto() { //obtener detalles de un producto
            fetch(URL + 'productos/' + this.codigo)
                .then(response => {
                    if (response.ok) {
                        return response.json() // los convierte de JSON a OB JS
                    } else {
                        //Si la respuesta es un error, lanzamos una excepción para ser "catcheada" más adelante en el catch.
                        throw new Error('Error al obtener los datos del producto.')
                    }
                })

                .then(data => {//se asignan los datos a las variables
                    this.descripcion = data.descripcion;
                    this.cantidad = data.cantidad;
                    this.precio = data.precio;
                    this.proveedor = data.proveedor;
                    this.imagen_url = data.imagen_url;
                    this.mostrarDatosProducto = true;
                })

                .catch(error => {
                    console.log(error);
                    alert('Código no encontrado.');
                }) // se alerta un error
        },

        seleccionarImagen(event) {
            const file = event.target.files[0];
            this.imagenSeleccionada = file;
            this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
        }, // se activa cuando el usuarion selecciona una img para cargar

        guardarCambios() { //enviar datos modif al servidor
            const formData = new FormData();
            formData.append('codigo', this.codigo);
            formData.append('descripcion', this.descripcion);
            formData.append('cantidad', this.cantidad);
            formData.append('proveedor', this.proveedor);
            formData.append('precio', this.precio);
            if (this.imagenSeleccionada) {
                formData.append('imagen', this.imagenSeleccionada,
                this.imagenSeleccionada.name);
            }
            //Utilizamos fetch para realizar una solicitud PUT a la API y
            //guardar los cambios.
            fetch(URL + 'productos/' + this.codigo, {
                method: 'PUT',
                body: formData,
            })

            .then(response => {
                    //Si la respuesta es exitosa, convierte la resp a un OB JS
                if (response.ok) {
                    return response.json()
                } else {
                        //Si la respuesta es un error, lanzamos una excepción.
                    throw new Error('Error al guardar los cambios del producto.')
                }
            })

            .then(data => { //mje de actualizacion
                alert('Producto actualizado correctamente.');
                this.limpiarFormulario();
            })

            .catch(error => { //mje de error
                console.error('Error:', error);
                alert('Error al actualizar el producto.');
            });
        },
        limpiarFormulario() { //restablece las variables, limpia el form
            this.codigo = '';
            this.descripcion = '';
            this.cantidad = '';
            this.precio = '';
            this.imagen_url = '';
            this.imagenSeleccionada = null;
            this.imagenUrlTemp = null;
            this.mostrarDatosProducto = false;
        }
    }
});
app.mount('#app'); //activa la aplicacion Vue en el DOM del navegador

