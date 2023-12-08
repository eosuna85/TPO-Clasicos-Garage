// const URL = "http://127.0.0.1:5000/"

        // Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
        const URL = "https://eosuna85.pythonanywhere.com/"
        

        // Realizamos la solicitud GET al servidor para obtener todos los productos.
        fetch(URL + 'autos')
            .then(function (response) {
                if (response.ok) {
                    //Si la respuesta es exitosa (response.ok), convierte el cuerpo de la respuesta de formato JSON a un objeto JavaScript y pasa estos datos a la siguiente promesa then.
                    return response.json(); 
            } else {
                    // Si hubo un error, lanzar explícitamente una excepción para ser "catcheada" más adelante
                    throw new Error('Error al obtener el listado del stock.');
                }
            })

            //Esta función maneja los datos convertidos del JSON.
            .then(function (data) {
                let tablaAutos = document.getElementById('tablaAutos'); //Selecciona el elemento del DOM donde se mostrarán los productos.

                // Iteramos sobre cada producto y agregamos filas a la tabla
                for (let auto of data) {
                    let fila = document.createElement('tr'); //Crea una nueva fila de tabla (<tr>) para cada producto.
                    fila.innerHTML = '<td>' + auto.codigo + '</td>' +
                        '<td>' + auto.marca + '</td>' +
                        '<td>' + auto.cantidad + '</td>' +
                        '<td>' + auto.precio + '</td>' +
                        // Mostrar miniatura de la imagen
                        // '<td><img id="img_auto" src=./static/imagenes/' + auto.imagen +' alt="Imagen del auto" style="width: 100px;"></td>' + '<td>' + auto.modelo + '</td>' +'<td>' + auto.anio + '</td>' + '<td>' + auto.km + '</td>' + '<td>' + auto.motor + '</td>' + '<td>' + auto.transmision + '</td>';
                        
                        //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
                        '<td><img id="img_auto" src=https://www.pythonanywhere.com/user/eosuna85/files/home/eosuna85/mysite/static/imagenes/' + auto.imagen +' alt="Imagen del auto" style="width: 100px;"></td>' + '<td>' + auto.modelo + '</td>' +'<td>' + auto.anio + '</td>' + '<td>' + auto.km + '</td>' + '<td>' + auto.motor + '</td>' + '<td>' + auto.transmision + '</td>';
                    
                    //Una vez que se crea la fila con el contenido del producto, se agrega a la tabla utilizando el método appendChild del elemento tablaProductos.
                    tablaAutos.appendChild(fila);
                }
            })

            //Captura y maneja errores, mostrando una alerta en caso de error al obtener los productos.
            .catch(function (error) {
                // Código para manejar errores
                alert('Error al obtener el listado del stock');
            });