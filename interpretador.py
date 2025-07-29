from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/chatemmap')
def chatemmap():
    return render_template("chatemmap.html")

@app.route('/problematicas')
def problematicas():
    return render_template('problematicas.html')

@app.route('/flujoagua')
def flujoagua():
    return render_template('flujoagua.html')

# Prompt base de comportamiento (contexto)
PROMPT_BASE = """
Eres un asistente inteligente especializado en temas de agua potable, monitoreo hidrológico y gestión de estaciones de medición en Quito, especialmente en Calderón.

Debes responder de forma clara, técnica pero comprensible, sobre:
- estaciones como DQS01HC01, H5006, H5026;
- variables como el caudal máximo;
- interpretación de indicadores;
- adicional tienes estas urls: https://www.ambiente.gob.ec/wp-content/uploads/downloads/2014/07/Estudio-de-Red-hidrometeorol%C3%B3gica.pdf, https://www.fonag.org.ec/web/wp-content/uploads/2024/06/Anuario-hidroclimatico-2020.pdf

No inventes datos, responde sólo dentro del contexto de análisis ambiental, hidrológico y técnico del proyecto en no más de 8 líneas.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "❗Mensaje vacío. Intenta escribir algo."})

        prompt_total = f"{PROMPT_BASE}\n\nUsuario: {user_message}"
        response = model.generate_content(prompt_total)

        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "⚠️ Ocurrió un error. Verifica tu conexión o vuelve a intentar más tarde."})

if __name__ == '__main__':
    is_local = os.environ.get("RENDER", "") == ""  # RENDER env var está vacía en local
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000)),
        debug=is_local
    )