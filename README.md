# Digitalizador de Formularios con IA (Gemini API)

Herramienta automatizada en Python diseñada para procesar masivamente formularios físicos (manuscritos y check-boxes). Utiliza la API de **Google Gemini 1.5 Flash** para interpretar imágenes, realizar OMR (Reconocimiento Óptico de Marcas) y OCR (Reconocimiento de Texto) simultáneamente, exportando los resultados a un formato estructurado.

## Características

- **Visión Computacional con LLMs:** A diferencia del OCR tradicional, utiliza IA generativa para entender el contexto, lo que permite procesar imágenes rotadas, con mala iluminación o en perspectiva sin necesidad de pre-procesamiento complejo.
- **Procesamiento de Frente y Dorso:** Algoritmo inteligente que empareja automáticamente las imágenes del anverso y reverso de cada formulario basándose en la nomenclatura del archivo.
- **Salida Estructurada (JSON a CSV):** Convierte respuestas no estructuradas (fotos) en una base de datos limpia (.csv), manejando listas de opciones múltiples y texto manuscrito.
- **Seguridad:** Gestión de credenciales mediante variables de entorno (`.env`).

## Stack Tecnológico

- **Python 3.13**
- **Google Generative AI SDK** (Gemini 2.0 Flash)
- **Pandas** (Estructuración y exportación de datos)
- **Pillow** (Manipulación de imágenes)
- **Python-dotenv** (Gestión de variables de entorno)

## Estructura del Proyecto

```text
├── img/                     # Carpeta donde se colocan las fotos (Ignorada por git)
├── .env                     # Archivo de variables de entorno (API KEY)
├── form.py                  # Script principal
├── requirements.txt         # Dependencias del proyecto
├── base_datos_completa.csv  # Archivo de salida (Generado automáticamente)
└── README.md                # Documentación
Instalación y ConfiguraciónClonar el repositorio:Bashgit clone [https://github.com/TU_USUARIO/nombre-del-repo.git](https://github.com/TU_USUARIO/nombre-del-repo.git)
cd nombre-del-repo
Instalar dependencias:Se recomienda usar un entorno virtual.Bashpip install -r requirements.txt
Configurar la API Key:Obtén tu API Key en Google AI Studio.Crea un archivo llamado .env en la raíz del proyecto.Agrega tu clave de la siguiente manera:Fragmento de códigoAPI_KEY=tu_clave_secreta_aqui
📸 UsoPreparar las imágenes:Coloca las fotos de los formularios en la carpeta img/. Es crucial respetar la nomenclatura para que el script detecte los pares:formulario_01-frente.jpgformulario_01-dorso.jpg(El script busca archivos que terminen en -frente y busca su pareja -dorso automáticamente).Ejecutar el script:Bashpython form.py
Resultados:El script generará un archivo base_datos_completa.csv en la raíz.Nota: El CSV utiliza punto y coma (;) como separador para asegurar compatibilidad directa con Excel en español.📝 Ejemplo de Salida (CSV)archivoescuela_nro1.1_genero3.3_juegos...form1-frente.jpg4459Femenino['Roblox', 'Minecraft']...📄 LicenciaEste proyecto es de código abierto y está disponible bajo la Licencia MIT.
---

### Recordatorio final para antes de subir:

Asegúrate de generar el archivo `requirements.txt` para que la sección de instalación sea real. Ejecuta esto en tu terminal antes de hacer el commit:

```powershell
pip freeze > requirements.txt