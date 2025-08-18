# Curso de Big Data

Este repositorio aborda algunos ejercicios del curso de Big Data de la Maestría en Ciencias de la Información y las Comunicaciones
de la Universidad Distrital Francisco José de Caldas.

NOTA: Todos los comandos a ejecutar en consola pueden ejecutarse en la consola bash o PowerShell.

## Contenido

- Clonar repositorio
- Crear y activar el entorno virtual
- Instalar dependencias

### Clonar repositorio

Abre una consola de comandos y muevete hasta el lugar (MI_RUTA) donde deseas descargar este repositorio. En la consola ejecuta lo siguiente:

```bash
cd MI_RUTA
```

Debes tener instalado Git para el control de versiones, así como poseer una cuenta en Github, sino tienes instalado Git ni una cuenta de Github, te recomiendo consultar estos enlaces:

1. [Descargar Git](https://git-scm.com/downloads/win)
2. [Crear una cuenta en Github](https://docs.github.com/es/get-started/start-your-journey/creating-an-account-on-github)

En cuanto a la instalación de Git en caso de que no lo tengas ya instalado, para revisar ejecuta en una consola lo siguiente:

```bash
git --version
```

Conforme lo indicado en la salida de la consola, si no lo tienes instalado, ve al enlace inde descarga indicado arriba, posterior a la descarga ejecutar el archivo .exe, ejecutar como administrador y seguir todos los pasos de la instalación que vienen por defecto.

Sino tienes una cuenta Github arriba está el enlace que puedes llegar a requerir. Puedes configurar tu conexión a Github con SSH o http, por facilidad, puedes clonar este repositorio ejecutando el sigueinte comando en la consola en la que has venido trabajando:

```bash
git clone https://github.com/HaesslerOrtiz/bigdata
```
Muevete a la dirección del repositorio local que se acaba de crear en tu PC local. Ejecuta el siguiente comando en consola:

```bash
cd big_data
```
El entorno virtual se crea a partir del interprete instalado y se añaden las librerías y complementos deseados.

### Crear y activar el entorno virtual

En la misma dirección deonde se clonó el repositorio muevete hacia el directorio creado y ejecuta los siguientes comandos:

1. Crear el entorno virtual
```bash
python -m venv big_data
```

2. Activar entorno virtual

- Activar en Windows (si usas PowerShell, sin .ps1 si usas CMD)
```bash
big_data\Scripts\Activate.ps1
```

- Activar en Linux/Mac
```bash
source big_data/bin/activate
```

Con el entrono activo deberías ver algo similar a "(big_data) C:\ruta\al\proyecto>" en la dirección donde se encuenta tu consola

3. Desactivar entorno virtual

Para desactivar el entorno virtual puedes correr el siguiente comando en consola:

```bash
deactivate
```

### Instalar dependencias

Se refiere a todos los complementos necesarios para que funcionen todos los métodos y clases requeridos en los diferentes códigos 
impelmentados en este curso.

```bash
pip install -r requirements.txt
```