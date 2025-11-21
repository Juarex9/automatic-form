import google.generativeai as genai

# Pega tu API Key aquí también
genai.configure(api_key="AIzaSyAwiSeNdG8507tzKLXsq3ooGSQxaFEQTWA")

print("--- Modelos Disponibles ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)