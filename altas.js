// const URL = "http://127.0.0.1:5000/"

        //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
        const URL = "https://eosuna85.pythonanywhere.com/"
        

        // Capturamos el evento de envío del formulario
        document.getElementById('formulario').addEventListener('submit', function (event) {
            event.preventDefault(); // Evitamos que se envie el form 

            var formData = new FormData();
            formData.append('codigo', document.getElementById('codigo').value);
            formData.append('marca', document.getElementById('marca').value);
            formData.append('cantidad', document.getElementById('cantidad').value);
            formData.append('precio', document.getElementById('precio').value);
            formData.append('imagen', document.getElementById('imagenAuto').files[0]);
            formData.append('modelo', document.getElementById('modeloAuto').value);
            formData.append('anio', document.getElementById('anio').value);
            formData.append('km', document.getElementById('km').value);
            formData.append('motor', document.getElementById('motor').value);
            formData.append('transmision', document.getElementById('transmision').value);
            
            // Realizamos la solicitud POST al servidor. El método POST se usa para enviar y crear nuevos datos en el servidor.
            fetch(URL + 'autos', {
                method: 'POST',
                body: formData // Aquí enviamos formData. Dado que formData puede contener archivos, no se utiliza JSON.
            })

                //Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.
                .then(function (response) {
                    if (response.ok) { 
                        //Si la respuesta es exitosa, convierte los datos de la respuesta a formato JSON.
                        return response.json(); 
                    } else {
                        // Si hubo un error, lanzar explícitamente una excepción
                        // para ser "catcheada" más adelante
                        throw new Error('Error al agregar el Artículo.');
                    }
                })

                //Respuesta OK, muestra una alerta informando que el producto se agregó correctamente y limpia los campos del formulario para que puedan ser utilizados para un nuevo producto.
                .then(function (data) {
                    alert('Artículo agregado correctamente.');
                })

                // En caso de error, mostramos una alerta con un mensaje de error.
                .catch(function (error) {
                    alert('Error al agregar el Artículo');
                })

                // Limpiar el formulario en ambos casos (éxito o error)
                .finally(function () {
                    document.getElementById('codigo').value = "";
                    document.getElementById('marca').value = "";
                    document.getElementById('cantidad').value = "";
                    document.getElementById('precio').value = "";
                    document.getElementById('imagenAuto').value = "";
                    document.getElementById('modeloAuto').value = "";
                    document.getElementById('anio').value = "";
                    document.getElementById('km').value = "";
                    document.getElementById('motor').value = "";
                    document.getElementById('transmision').value = "";
                });
        })