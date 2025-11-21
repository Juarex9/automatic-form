import os
import time
import json
import pandas as pd
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN ---
API_KEY = "PEGA_TU_API_KEY_AQUI"  # <--- ¡No olvides tu clave!
CARPETA_IMAGENES = "img"          # <--- AHORA BUSCA AQUÍ
ARCHIVO_SALIDA = "base_datos_completa.csv"

# Configuramos la API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={"response_mime_type": "application/json"}
)

def analizar_formulario(path_frente, path_dorso):    
    try:
        img_frente = Image.open(path_frente)
        imagenes_prompt = [img_frente]
        
        texto_dorso = "No se encontró imagen del dorso."
        if path_dorso and os.path.exists(path_dorso):
            img_dorso = Image.open(path_dorso)
            imagenes_prompt.append(img_dorso)
            texto_dorso = "La segunda imagen es el dorso (preguntas 5 a 8)."

        # PROMPT 
        prompt = f"""
        Actúa como un digitalizador de datos experto. Tienes dos imágenes del mismo formulario (frente y dorso).
        Tu tarea es extraer las respuestas marcadas con 'X' y el texto manuscrito.
        
        INSTRUCCIONES DE LECTURA:
        - La primera imagen contiene las secciones 1, 2, 3 y 4.
        - {texto_dorso}
        - Si hay una opción 'Otra' con texto manuscrito, transcribe el texto.
        - Devuelve SOLO un objeto JSON con las siguientes claves:

        {{
          "archivo": "nombre_archivo",
          
          "escuela_nro": "Texto manuscrito en el recuadro superior 'Escuela Nro'",
          "1.1_genero": "Opción marcada en 1.1",
          "1.2_edad": "Opción marcada en 1.2",
          "2.1_primer_contacto": "Opción marcada en 2.1",
          "2.2_primer_propio": "Opción marcada en 2.2",
          "2.3_horas_pantalla": "Opción marcada en 2.3",
          "2.4_con_quien_usa": "Opción marcada en 2.4 (puede ser múltiple)",
          "3.1_reto_viral": "Opción marcada en 3.1",
          "3.2_apps_frecuentes": ["Lista de opciones marcadas en 3.2"],
          "3.3_juegos": ["Lista de opciones marcadas en 3.3"],
          "4.1_habla_desconocidos": "Opción marcada en 4.1",
          "4.2_reglas_casa": "Opción marcada en 4.2",
          "4.3_app_desconocidos": "Opción marcada en 4.3 o null",
          "4.4_padres_conocen": "Opción marcada en 4.4",
          "5.1_apuestas_casino": "Opción marcada en 5.1",
          "5.2_enterado_apuestas": "Opción marcada en 5.2",
          "5.3_pedido_noviazgo": "Opción marcada en 5.3",
          "5.4_app_noviazgo": "Opción marcada en 5.4 (o texto si escribió en Otra)",
          "6.1_adulto_comparte": "Opción marcada en 6.1",
          "6.2_privacidad_redes": "Opción marcada en 6.2",
          "6.3_quien_ve_fotos": "Opción marcada en 6.3",
          "6.4_aceptaste_desconocidos": "Opción marcada en 6.4",
          "6.5_sabe_sexting": "Opción marcada en 6.5",
          "6.6_sabe_grooming": "Opción marcada en 6.6",
          "7.1_compartiste_intimo": "Opción marcada en 7.1",
          "7.2_pidieron_intimo": "Opción marcada en 7.2",
          "7.3_conocias_persona": "Opción marcada en 7.3",
          "7.4_sentir_mal_hiciste": "Opción marcada en 7.4",
          "7.5_sabe_denunciar": "Opción marcada en 7.5",
          "8.1_sentimiento_online": "Opción marcada en 8.1",
          "8.2_sentiste_mal_visto": "Opción marcada en 8.2",
          "8.3_sabe_mas_tecnologia": "Opción marcada en 8.3",
          "8.4_sabe_proteger_pass": "Opción marcada en 8.4"
        }}
        """

        response = model.generate_content([prompt, *imagenes_prompt])
        return json.loads(response.text)

    except Exception as e:
        print(f"Error procesando {path_frente}: {e}")
        return None

def main():
    datos_extraidos = []
    
    # Verificamos que la carpeta exista
    if not os.path.exists(CARPETA_IMAGENES):
        print(f"ERROR: No encuentro la carpeta '{CARPETA_IMAGENES}'.")
        return

    print(f"Buscando imágenes en la carpeta: '{CARPETA_IMAGENES}'")
    archivos = os.listdir(CARPETA_IMAGENES)
    
    # Filtramos solo los que dicen "-frente"
    frentes = [f for f in archivos if "-frente" in f.lower() and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    total = len(frentes)
    
    if total == 0:
        print("No encontré archivos con '-frente' en la carpeta img.")
        return

    print(f"--- Iniciando proceso para {total} formularios ---")

    for i, archivo_frente in enumerate(frentes):
        # Construimos la ruta completa (img/archivo.jpg)
        path_frente = os.path.join(CARPETA_IMAGENES, archivo_frente)
        
        # Buscamos la pareja (dorso) reemplazando -frente por -dorso
        archivo_dorso = archivo_frente.lower().replace("-frente", "-dorso")
        path_dorso = os.path.join(CARPETA_IMAGENES, archivo_dorso)
        
        # Verificación visual
        estado_dorso = "Con Dorso" if os.path.exists(path_dorso) else "Sin Dorso"
        print(f"Procesando [{i+1}/{total}]: {archivo_frente} -> {estado_dorso}")
        
        resultado = analizar_formulario(path_frente, path_dorso)
        
        if resultado:
            resultado['archivo'] = archivo_frente
            datos_extraidos.append(resultado)
        else:
            print(f"FALLÓ: {archivo_frente}")
        
        time.sleep(2) 

    # Exportar
    if datos_extraidos:
        df = pd.DataFrame(datos_extraidos)
        df.to_csv(ARCHIVO_SALIDA, index=False, encoding='utf-8-sig', sep=';') 
        print(f"\n¡ÉXITO! {len(datos_extraidos)} formularios guardados en '{ARCHIVO_SALIDA}'")
    else:
        print("\nNo se generaron datos.")

if __name__ == "__main__":
    main()