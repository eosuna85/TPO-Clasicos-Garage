// const URL = "http://127.0.0.1:5000/"

        //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
        const URL = "https://eosuna85.pythonanywhere.com/"
        

        //Vue.createApp para crear nuestra aplicación Vue.
        const app = Vue.createApp({
            
            //La función data devuelve un objeto que contiene las siguientes propiedades: 
            data() {
                return {
                    codigo: '',
                    marca: '',
                    cantidad: '',
                    precio: '',
                    modelo: '',
                    imagen: '',
                    imagenSeleccionada: null,
                    imagenUrlTemp: null,
                    anio: '',
                    km: '',
                    motor:'',
                    transmision:'',
                    mostrarDatosAuto: false, //mostrarDatosProducto para controlar la visibilidad del formulario de modificación.
                };
            },

            methods: {
                //Se ejecuta cuando se envía el formulario de consulta. En este método, utilizamos fetch para realizar una solicitud GET a la API y obtener los datos del producto correspondiente al código ingresado.
                obtenerAuto() {
                    fetch(URL + 'autos/' + this.codigo)
                    //Realiza una solicitud de red al servidor para obtener los datos del producto. Usa la URL definida anteriormente y añade 'productos/' seguido del código del producto.
                        
                        //Verificamos si la respuesta de la solicitud es exitosa (código de respuesta 200-299). 
                        .then(response =>  {
                            //Si es así, utilizamos response.json() para parsear la respuesta en formato JSON.
                            if (response.ok) {
                                return response.json() //Una vez que la respuesta llega del servidor, se convierte de formato JSON a un objeto JavaScript.
                            } else {
                                //Si la respuesta es un error, lanzamos una excepción para ser "catcheada" más adelante en el catch.
                                throw new Error('Error al obtener los datos del auto.')
                            }
                        })

                        //En este bloque, se asignan los datos obtenidos a las variables correspondientes de la aplicación Vue.
                        .then(data => {
                            this.cantidad = data.cantidad;
                            this.precio = data.precio;
                            this.imagen =  data.imagen;
                            this.mostrarDatosAuto = true;
                        })

                        //Si ocurre un error durante la solicitud, se captura y se imprime en la consola.
                        .catch(error => {
                            alert('Código no encontrado.')
                        })
                },

                //Se activa cuando el usuario selecciona una imagen para cargar.
                seleccionarImagen(event) {
                    const file = event.target.files[0];
                    this.imagenSeleccionada = file;
                    this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
                },

                //Se usa para enviar los datos modificados del producto al servidor.
                guardarCambios() {
                    const formData = new FormData();
                    formData.append('codigo', this.codigo);
                    formData.append('cantidad', this.cantidad);
                    formData.append('precio', this.precio);

                    //Si se ha seleccionado una imagen nueva, la añade al formData. 
                    if (this.imagenSeleccionada) {
                        formData.append('imagen', this.imagenSeleccionada, this.imagenSeleccionada.name);
                    }

                    //Utilizamos fetch para realizar una solicitud PUT a la API y guardar los cambios.
                    fetch(URL + 'autos/' + this.codigo, {
                        method: 'PUT',
                        body: formData, //Dado que formData puede contener archivos, no se utiliza JSON.
                    })
                        .then(response => {
                            //Si la respuesta es exitosa, utilizamos response.json() para parsear la respuesta en formato JSON.
                            if (response.ok) {
                                return response.json()
                            } else {
                                //Si la respuesta es un error, lanzamos una excepción.
                                throw new Error('Error al guardar los cambios del modelo.')
                            }
                        })

                        //Respuesta OK, muestra una alerta informando que el producto se agregó correctamente y limpia los campos del formulario para que puedan ser utilizados para un nuevo producto.
                        .then(data => {
                            alert('Modelo actualizado Exitosamente.');
                            this.limpiarFormulario();
                        })

                        // En caso de error, mostramos una alerta con un mensaje de error.
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Error al actualizar el modelo.');
                        });
                },

                //Restablece todas las variables relacionadas con el formulario a sus valores iniciales, lo que efectivamente "limpia" el formulario.
                limpiarFormulario() {
                    this.codigo = '';
                    this.cantidad = '';
                    this.precio = '';
                    this.imagen = '';
                    this.imagenSeleccionada = null;
                    this.imagenUrlTemp = null;
                    this.mostrarDatosAuto = false;
                }
            }
        });

        //Cuando se llama a app.mount('#app'), Vue busca en el documento HTML un elemento con el id app. Vue entonces toma el control de este elemento y de todo su contenido. Esto significa que Vue puede reaccionar a los cambios en sus datos y actualizar automáticamente el HTML en este elemento. También maneja eventos, como clicks o entradas de formulario, y actualiza los datos según las interacciones del usuario.

        app.mount('#app');