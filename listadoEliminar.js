// const URL = "http://127.0.0.1:5000/"

        //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
        const URL = "https://eosuna85.pythonanywhere.com/"
        

        //Vue.createApp para crear nuestra aplicación Vue.
        //Define una propiedad productos en el estado de la aplicación Vue. Inicialmente, es un array vacío que almacenará los datos de los productos obtenidos del servidor.
        const app = Vue.createApp({
            data() {
                return {
                    autos: []
                }
            },
            methods: {
                // El método obtenerProductos se utiliza para obtener los productos del servidor. 
                obtenerAutos() {
                    // Obtenemos el contenido del inventario
                    fetch(URL + 'autos') //Realiza una solicitud GET al servidor y obtener la lista de productos.
                        .then(response => {
                             // Si es exitosa (response.ok), convierte los datos de la respuesta de formato JSON a un objeto JavaScript.
                            if (response.ok) { return response.json();}
                        })

                        //Asigna los datos de los productos obtenidos a la propiedad productos del estado de Vue.
                        .then(data => {
                            // El código Vue itera este elemento para generar la tabla
                            this.autos = data;
                        })

                        //Captura y maneja errores, mostrando una alerta en caso de error al obtener los productos.
                        .catch(error => {
                            console.log('Error:', error);
                            alert('Error al obtener los autos.');
                        });
                },

                //Se utiliza para eliminar un producto.
                eliminarAuto(codigo) {
                    //Se muestra un diálogo de confirmación. Si el usuario confirma, se realiza una solicitud DELETE al servidor a través de fetch(URL + 'productos/${codigo}', {method: 'DELETE' }).
                    if (confirm('¿Estás seguro de que quieres eliminar este modelo?')) {
                        fetch(URL + `autos/${codigo}`, { method: 'DELETE' })
                            .then(response => {
                                if (response.ok) {
                                    // Si es exitosa (response.ok), elimina el producto y da mensaje de ok.
                                    this.autos = this.autos.filter(auto => auto.codigo !== codigo);
                                    alert('Modelo eliminado correctamente.');
                                }
                            })

                            // En caso de error, mostramos una alerta con un mensaje de error.
                            .catch(error => {
                                alert(error.message);
                            });
                    }
                }
            },

            //Una vez iniciada la app de Vue, se carga el método mounted()
            mounted() {
                //Se llama al método obtenerProductos para cargar la lista de productos cuando la página se carga por primera vez.
                this.obtenerAutos();
            }
        });

        //Monta la aplicación Vue en el elemento <body> del DOM. Esto activa Vue en la página, haciendo que sea reactivo y maneje el contenido dinámicamente según los datos y las interacciones del usuario.
        app.mount('body');