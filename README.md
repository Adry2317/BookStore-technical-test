
# Guía para la Ejecución del Proyecto con Docker y Docker Compose

Este proyecto está configurado para ejecutarse utilizando Docker y Docker Compose. Asegúrate de tener Docker y Docker Compose instalados en tu máquina antes de continuar.

## Prerrequisitos

1. **Instalar Docker**  
   Sigue las instrucciones oficiales para instalar Docker en tu sistema operativo: [Instalación de Docker](https://docs.docker.com/get-docker/).

2. **Instalar Docker Compose**  
   Docker Compose generalmente viene incluido con Docker Desktop. En caso contrario, sigue las instrucciones oficiales: [Instalación de Docker Compose](https://docs.docker.com/compose/install/).

3. **Clonar el repositorio**  
   Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/Adry2317/BookStore-technical-test.git
   cd BookStore-technical-test/BookStore


## Pasos para la Ejecución
1. **Construir y levantar los contenedores**  
Usa el siguiente comando para construir y levantar los servicios definidos en el archivo `docker-compose.yml`:

	bash

	```
	docker-compose up --build

	```

Esto hará lo siguiente:

-   Construirá las imágenes de Docker necesarias.
-   Levantará los contenedores del archivo: `docker-compose.yml`.
- El proyecto estará disponible en `http://localhost:8000`


## Ejecución de test

Al encontraese dockerizada la aplicación, debemos de ingresar dentro del contenedor para lanzar los test.

Localizamos el contenedor que contenga el nombre django, copia el id del contenedor y ejecuta el siguiente comando.


**Linux**

	docker exec -it <contenedor_id> bash

	

**Windows**

	docker exec -it <contenedor_id> sh

	
Una vez dentro utilice el siguiente comando para ejecutar los test.


	python manage.py test
