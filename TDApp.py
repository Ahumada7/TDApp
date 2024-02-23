from flask import Flask, render_template, request, jsonify
import json
import openai


app = Flask(__name__)

# Usa una variable de entorno para la clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/analizar', methods=['POST'])
def analizar_tareas():
    descripcion = request.form['descripcion']
    
    tareas_organizadas_json = analyze(descripcion)
    tareas_organizadas = json.loads(tareas_organizadas_json)  # Convertir de JSON a dict de Python
    
    # Pasar las tareas a la plantilla HTML
    return render_template('mostrar_tareas.html', tareas=tareas_organizadas["tareas"])

def analyze(descripcion):
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil que se especializa en ayudar a las personas con TDAH a organizar sus listas de tareas pendientes. Tu objetivo es ayudar a los usuarios a administrar sus tareas de manera efectiva. Sé proactivo, empático, paciente y adaptable. Prioriza la simplicidad y la claridad mientras mantienes un tono de apoyo. Divide minuciosamente cada tarea en sub-tareas pequeñas alcanzables en diez minutos y que al acabarlas sean recompensantes para el usuario. Responde con una lista de todas las tareas y sub-tareas en formato JSON, como sigue: {\"tareas\": [{\"nombre\": \"Tarea 1\", \"subtareas\": [\"Subtarea 1.1\", \"Subtarea 1.2\"]}, {\"nombre\": \"Tarea 2\", \"subtareas\": [\"Subtarea 2.1\", \"Subtarea 2.2\"]}]}."},
                {"role": "user", "content": descripcion},
            ]
        )
        tareas = respuesta.choices[0].message['content']
        return tareas
    except Exception as e:
        # Considera devolver una respuesta JSON con estado de error
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500

@app.route('/')
def home():
    # Asegúrate de que el archivo 'index.html' exista en la carpeta 'templates'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=8157, debug=True)
