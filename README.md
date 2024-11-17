# Generador de Documentos

Este proyecto es un generador de documentos que permite crear recibos basados en datos de un archivo Excel. Está diseñado para ayudar a gestionar ayudas y beneficios sociales, facilitando la entrada de datos y la generación de documentos en formato Word.

## Características

- Carga datos desde un archivo Excel.
- Interfaz gráfica de usuario (GUI) utilizando Tkinter.
- Generación de documentos en formato .docx utilizando plantillas.
- Validación de datos de entrada.
- Cálculo automático de copagos según la ayuda seleccionada.

## Requisitos

Asegúrate de tener instalados los siguientes paquetes de Python:

- `pandas`: Para la manipulación y análisis de datos, especialmente para leer y procesar archivos Excel.
- `docxtpl`: Para la creación y manipulación de documentos de Word basados en plantillas.
- `tkinter`: Para la creación de la interfaz gráfica de usuario.
- `dateutil`: Para el manejo de fechas y cálculos relacionados, como la edad.

Puedes instalar las dependencias necesarias utilizando pip:

bash
pip install pandas docxtpl python-dateutil


## Funcionamiento Interno

El script `generar_recibi.py` funciona de la siguiente manera:

1. **Carga de Recursos**: Utiliza la función `resource_path` para obtener la ruta absoluta de los recursos necesarios, como el icono de la aplicación.

2. **Inicialización de la Clase `DocumentGenerator`**: Esta clase es el núcleo de la aplicación. En su constructor (`__init__`), se configuran las constantes, se inicializa la interfaz de usuario y se establece el idioma para las fechas.

3. **Carga de Archivos Excel**: La función `load_excel_file` permite al usuario seleccionar un archivo Excel y carga los datos en un DataFrame de pandas. También carga una hoja oculta con valores profesionales.

4. **Interfaz de Usuario**: La función `init_ui` configura la ventana principal y los elementos de la interfaz, como campos de entrada y botones.

5. **Validación de Datos**: Antes de generar un documento, se valida la entrada del usuario mediante la función `validate_input`, asegurando que todos los campos requeridos estén completos y que las cuantías no excedan los límites establecidos.

6. **Generación de Documentos**: La función `generate_document` recopila los datos ingresados, calcula la información necesaria (como la edad y el copago), y utiliza `docxtpl` para renderizar un documento basado en una plantilla.

7. **Cálculo de Copagos**: La función `calculate_copago` calcula el copago si la ayuda seleccionada lo requiere, actualizando la interfaz con la información correspondiente.

## Uso

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/tu_usuario/generar_recibi.git
   cd generar_recibi
   ```

2. Asegúrate de tener un archivo Excel con los datos necesarios. El archivo debe tener una hoja con los datos de beneficiarios y otra hoja oculta con valores profesionales.

3. Ejecuta el script:
   ```bash
   python generar_recibi.py
   ```

4. Sigue las instrucciones en la interfaz gráfica para cargar el archivo Excel y generar el recibo.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
