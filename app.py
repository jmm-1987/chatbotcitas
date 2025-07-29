from flask import Flask, request, jsonify, render_template
# from openai import OpenAI  # Eliminado
# from dotenv import load_dotenv  # Eliminado
import os
import smtplib
from email.message import EmailMessage
import re
import sqlite3
import dateparser
import datetime

# load_dotenv()  # Eliminado

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Eliminado
app = Flask(__name__)

# Variables globales (simples, sin sesiones)
conversacion_log = []
nombre_usuario = ""
telefono_usuario = ""
correo_enviado = False

# Eliminado: modo_chatbot

# Función para enviar el correo con los datos
def enviar_correo(nombre, telefono, conversacion):
    try:
        print("✉️ Intentando enviar correo...")

        email_host = os.getenv("EMAIL_HOST")
        email_port = int(os.getenv("EMAIL_PORT", "587"))
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        email_receiver = os.getenv("EMAIL_RECEIVER")

        msg = EmailMessage()
        msg["Subject"] = "Nuevo lead captado desde el chatbot"
        msg["From"] = email_user
        msg["To"] = email_receiver

        cuerpo = f"""
Nuevo cliente potencial desde el chatbot de la web.

Nombre: {nombre}
Teléfono: {telefono}

Conversación completa:
{conversacion}
"""
        msg.set_content(cuerpo)

        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)

        print("✅ Correo enviado con éxito.")
    except Exception as e:
        print(f"❌ Error real al enviar correo: {e}")

# --- BASE DE DATOS PARA CITAS ---
DB_PATH = 'citas.db'

# Utilidad para normalizar fechas

def normalizar_fecha(texto):
    """Normaliza una fecha a formato YYYY-MM-DD"""
    if not texto:
        return None
    
    # Si ya está en formato YYYY-MM-DD, devolverlo tal cual
    if len(texto) == 10 and texto[4] == '-' and texto[7] == '-':
        try:
            datetime.datetime.strptime(texto, '%Y-%m-%d')
            return texto
        except:
            pass
    
    # Intentar con dateparser
    try:
        dt = dateparser.parse(texto, languages=['es'])
        if dt:
            return dt.strftime('%Y-%m-%d')
    except:
        pass
    
    # Si no se puede parsear, devolver el texto original
    return texto

def formatear_fecha_display(fecha_str):
    """Convierte fecha YYYY-MM-DD a DD/MM/AAAA"""
    try:
        dt = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return fecha_str

# Inicializar la base de datos (si no existe)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            servicio TEXT,
            dia DATE,
            hora TEXT,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Consultar horas ocupadas para un día
def horas_ocupadas(dia):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT hora FROM citas WHERE dia = ?', (dia,))
    ocupadas = [row[0] for row in c.fetchall()]
    conn.close()
    return ocupadas

# Guardar una cita
def guardar_cita(nombre, servicio, dia, hora, telefono):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO citas (nombre, servicio, dia, hora, telefono) VALUES (?, ?, ?, ?, ?)',
              (nombre, servicio, dia, hora, telefono))
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar
init_db()

# Función para generar citas de prueba realistas
def generar_citas_prueba():
    """Genera citas de prueba realistas desde hoy hasta final de agosto"""
    import random
    
    # Nombres realistas de clientes
    nombres = [
        "María García", "Ana López", "Carmen Rodríguez", "Isabel Martínez", "Rosa Sánchez",
        "Elena Pérez", "Laura González", "Sofia Fernández", "Patricia Jiménez", "Mónica Ruiz",
        "Cristina Moreno", "Beatriz Díaz", "Nuria Martín", "Victoria Alonso", "Teresa Gutiérrez",
        "Pilar Romero", "Angeles Navarro", "Dolores Torres", "Concepción Domínguez", "Isabel Vázquez",
        "Lucía Hernández", "Paula Castro", "Adriana Morales", "Claudia Silva", "Valentina Rojas",
        "Camila Mendoza", "Sara Herrera", "Daniela Vega", "Gabriela Fuentes", "Carolina Reyes",
        "Andrea Morales", "Natalia Jiménez", "Valeria Torres", "Mariana Silva", "Fernanda Castro",
        "Isabella Rojas", "Sofía Mendoza", "Emma Herrera", "Olivia Vega", "Ava Fuentes",
        "Mia Reyes", "Charlotte Morales", "Amelia Jiménez", "Harper Torres", "Evelyn Silva"
    ]
    
    # Servicios disponibles
    servicios = [
        "Corte de mujer", "Corte de hombre", "Peinado", "Tinte raíz", "Mechas", "Lavado y secado",
        "Corte y color", "Peinado de fiesta", "Tinte completo", "Mechas californianas", "Brushing",
        "Corte degradado", "Peinado recogido", "Color fantasía", "Mechas balayage", "Tratamiento capilar",
        "Corte bob", "Peinado casual", "Tinte natural", "Mechas lowlights", "Secado profesional"
    ]
    
    # Horarios disponibles
    horas = [
        '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30',
        '16:00', '16:30', '17:00', '17:30',
        '18:00', '18:30', '19:00', '19:30'
    ]
    
    # Calcular fechas desde hoy hasta final de agosto
    hoy = datetime.date.today()
    fin_agosto = datetime.date(2025, 8, 31)  # 31 de agosto de 2025
    
    citas_generadas = []
    fecha_actual = hoy
    
    print(f"🎯 Generando citas desde {hoy.strftime('%d/%m/%Y')} hasta {fin_agosto.strftime('%d/%m/%Y')}")
    
    # Generar citas para cada día desde hoy hasta final de agosto
    while fecha_actual <= fin_agosto:
        fecha_str = fecha_actual.strftime('%Y-%m-%d')
        dia_semana = fecha_actual.weekday()
        nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana]
        
        # Domingo no hay citas
        if dia_semana == 6:  # Domingo
            fecha_actual += datetime.timedelta(days=1)
            continue
            
        # Generar entre 3-15 citas por día (más ocupado los miércoles, jueves y viernes)
        num_citas = random.randint(3, 10)
        if dia_semana == 2:  # Miércoles más ocupado
            num_citas = random.randint(8, 14)
            print(f"🎯 Miércoles {fecha_str}: {num_citas} citas")
        elif dia_semana == 3:  # Jueves ocupado
            num_citas = random.randint(6, 12)
            print(f"📅 Jueves {fecha_str}: {num_citas} citas")
        elif dia_semana == 4:  # Viernes muy ocupado
            num_citas = random.randint(10, 16)
            print(f"🔥 Viernes {fecha_str}: {num_citas} citas")
        elif dia_semana == 5:  # Sábado ocupado
            num_citas = random.randint(8, 14)
            print(f"🌟 Sábado {fecha_str}: {num_citas} citas")
        else:
            print(f"📅 {nombre_dia} {fecha_str}: {num_citas} citas")
        
        # Seleccionar horas aleatorias para las citas
        horas_disponibles = horas.copy()
        random.shuffle(horas_disponibles)
        horas_seleccionadas = horas_disponibles[:num_citas]
        
        for hora in horas_seleccionadas:
            nombre = random.choice(nombres)
            servicio = random.choice(servicios)
            telefono = f"6{random.randint(10000000, 99999999)}"  # Teléfono móvil español
            
            # Guardar la cita en la base de datos
            guardar_cita(nombre, servicio, fecha_str, hora, telefono)
            citas_generadas.append({
                'fecha': fecha_str,
                'hora': hora,
                'nombre': nombre,
                'servicio': servicio,
                'telefono': telefono
            })
        
        fecha_actual += datetime.timedelta(days=1)
    
    print(f"\n🎉 Total de citas generadas: {len(citas_generadas)}")
    return citas_generadas

# Endpoint para generar citas de prueba
@app.route('/generar_citas_prueba', methods=['POST'])
def generar_citas_prueba_endpoint():
    try:
        citas = generar_citas_prueba()
        return jsonify({
            'ok': True, 
            'mensaje': f'Se han generado {len(citas)} citas de prueba desde hoy hasta final de agosto',
            'citas': citas
        })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

# Endpoint para limpiar todas las citas (solo para desarrollo)
@app.route('/limpiar_citas', methods=['POST'])
def limpiar_citas():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM citas')
        conn.commit()
        conn.close()
        return jsonify({'ok': True, 'mensaje': 'Todas las citas han sido eliminadas'})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

@app.route("/")
def index():
    return render_template("index.html")

# Panel de control de citas
@app.route("/panel")
def panel():
    return render_template("panel.html")

@app.route("/chat", methods=["POST"])
def chat():
    global nombre_usuario, telefono_usuario, correo_enviado, conversacion_log

    user_message = request.get_json().get("message", "").strip().lower()
    respuesta = ""

    # Guardamos la conversación
    conversacion_log.append(f"Usuario: {user_message}")

    # Flujo simple de preguntas y respuestas
    if any(saludo in user_message for saludo in ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches"]):
        respuesta = "¡Hola! ¿Qué servicio deseas reservar? (corte, peinado, tinte, lavado)"
    elif any(serv in user_message for serv in ["corte", "peinado", "tinte", "lavado"]):
        # Guardar el servicio elegido
        servicio = next((serv for serv in ["corte", "peinado", "tinte", "lavado"] if serv in user_message), None)
        respuesta = f"Perfecto, has elegido {servicio}. ¿Para qué día quieres la cita? (por ejemplo: 2024-07-25)"
    elif re.match(r"\d{4}-\d{2}-\d{2}", user_message):
        # El usuario ha escrito una fecha
        dia = normalizar_fecha(user_message)
        # Consultar horas disponibles
        todas = [
            '10:00', '10:30', '11:00', '11:30',
            '12:00', '12:30', '13:00', '13:30',
            '16:00', '16:30', '17:00', '17:30',
            '18:00', '18:30', '19:00', '19:30'
        ]
        ocupadas = horas_ocupadas(dia)
        libres = [h for h in todas if h not in ocupadas]
        if libres:
            respuesta = f"Estas son las horas disponibles para {dia}: {', '.join(libres)}. ¿Qué hora prefieres?"
        else:
            respuesta = f"Lo siento, no hay horas disponibles para ese día. Por favor, elige otro día."
    elif re.match(r"\d{2}:\d{2}", user_message):
        # El usuario ha escrito una hora
        respuesta = "Por favor, indícame tu nombre para completar la reserva."
    elif any(palabra in user_message for palabra in ["me llamo", "soy", "nombre"]):
        # Extraer nombre
        nombre = user_message.replace("me llamo","").replace("soy","").replace("nombre","").strip().title()
        nombre_usuario = nombre
        respuesta = "Gracias. Ahora, por favor, indícame tu número de teléfono."
    elif re.match(r"\d{9,}", user_message):
        telefono_usuario = user_message
        respuesta = "¡Reserva completada! Te hemos registrado para la cita. Si necesitas cambiar algo, avísanos."
        correo_enviado = False  # Permitir enviar correo si es necesario
    else:
        respuesta = "No he entendido tu mensaje. Por favor, sigue las instrucciones para reservar tu cita."

    conversacion_log.append(f"Asistente: {respuesta}")

    # Enviar correo si ya tenemos nombre y teléfono y aún no se envió
    if nombre_usuario and telefono_usuario and not correo_enviado:
        texto_conversacion = "\n".join(conversacion_log)
        enviar_correo(nombre_usuario, telefono_usuario, texto_conversacion)
        correo_enviado = True

    return jsonify({"reply": respuesta})

# --- ENDPOINT PARA HORAS DISPONIBLES ---
@app.route('/horas_disponibles', methods=['POST'])
def horas_disponibles():
    data = request.get_json()
    dia = normalizar_fecha(data.get('dia'))
    # Horas posibles (puedes ajustar este rango)
    todas = [
        '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30',
        '16:00', '16:30', '17:00', '17:30',
        '18:00', '18:30', '19:00', '19:30'
    ]
    ocupadas = horas_ocupadas(dia)
    libres = [h for h in todas if h not in ocupadas]
    return jsonify({'libres': libres})

# --- ENDPOINT PARA RESERVAR CITA ---
@app.route('/reservar_cita', methods=['POST'])
def reservar_cita():
    data = request.get_json()
    nombre = data.get('nombre')
    servicio = data.get('servicio')
    dia = normalizar_fecha(data.get('dia'))
    hora = data.get('hora')
    telefono = data.get('telefono', '')
    # Comprobar si la hora sigue libre
    if hora in horas_ocupadas(dia):
        return jsonify({'ok': False, 'msg': 'La hora ya está ocupada'})
    guardar_cita(nombre, servicio, dia, hora, telefono)
    return jsonify({'ok': True, 'msg': 'Cita reservada correctamente'})

# --- ENDPOINT PARA CONSULTAR CITAS DE UN DÍA (panel de control) ---
@app.route('/citas_dia', methods=['POST'])
def citas_dia():
    data = request.get_json()
    dia_original = data.get('dia')
    dia = normalizar_fecha(dia_original)
    print(f"🔍 Consultando citas para: {dia_original} -> {dia}")
    
    if not dia:
        print(f"❌ Error: fecha inválida '{dia_original}'")
        return jsonify({'ocupadas': [], 'citas': [], 'error': 'Fecha inválida'})
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verificar si hay citas para esta fecha
    c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (dia,))
    total_citas = c.fetchone()[0]
    print(f"📊 Total de citas en BD para {dia}: {total_citas}")
    
    c.execute('SELECT hora, nombre, servicio, telefono FROM citas WHERE dia = ?', (dia,))
    rows = c.fetchall()
    conn.close()
    
    ocupadas = [row[0] for row in rows]
    citas = [
        {'hora': row[0], 'nombre': row[1], 'servicio': row[2], 'telefono': row[3], 'dia': formatear_fecha_display(dia)} for row in rows
    ]
    
    print(f"📅 Encontradas {len(citas)} citas para {dia}: {[c['hora'] for c in citas]}")
    return jsonify({'ocupadas': ocupadas, 'citas': citas})

# --- ENDPOINT: Próximos 20 días laborables y disponibilidad ---
@app.route('/proximos_dias_disponibles', methods=['GET'])
def proximos_dias_disponibles():
    HORAS = [
        '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30',
        '16:00', '16:30', '17:00', '17:30',
        '18:00', '18:30', '19:00', '19:30'
    ]
    dias = []
    hoy = datetime.date.today()
    hasta = hoy + datetime.timedelta(days=31)
    dia = hoy
    while dia <= hasta:
        dia_str = dia.strftime('%Y-%m-%d')
        ocupadas = horas_ocupadas(dia_str)
        libres = [h for h in HORAS if h not in ocupadas]
        dias.append({
            'fecha': dia_str,
            'fecha_display': formatear_fecha_display(dia_str),
            'disponibles': len(libres),
            'weekday': dia.weekday()  # 0=lunes, 6=domingo
        })
        dia += datetime.timedelta(days=1)
    return jsonify({'dias': dias})

@app.route('/enviar_recordatorio', methods=['POST'])
def enviar_recordatorio():
    data = request.get_json()
    email = data.get('email')
    fecha = data.get('fecha')
    hora = data.get('hora')
    servicio = data.get('servicio')
    nombre_peluqueria = 'Peluquería JM'  # Puedes cambiarlo por el nombre real
    try:
        # Configuración de email
        email_host = os.getenv("EMAIL_HOST")
        email_port = int(os.getenv("EMAIL_PORT", "587"))
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        msg = EmailMessage()
        msg["Subject"] = f"Recordatorio de tu cita en {nombre_peluqueria}"
        msg["From"] = email_user
        msg["To"] = email  # El destinatario es el email del usuario
        cuerpo = f"""
Hola,

Te recordamos tu cita en {nombre_peluqueria}:

- Servicio: {servicio}
- Fecha: {fecha}
- Hora: {hora}

¡Te esperamos!
"""
        msg.set_content(cuerpo)
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})

@app.route('/actualizar_telefono', methods=['POST'])
def actualizar_telefono():
    data = request.get_json()
    dia = data.get('dia')
    hora = data.get('hora')
    telefono = data.get('telefono')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE citas SET telefono = ? WHERE dia = ? AND hora = ?', (telefono, dia, hora))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/citas_por_telefono', methods=['POST'])
def citas_por_telefono():
    data = request.get_json()
    telefono = data.get('telefono')
    hoy = datetime.date.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT servicio, dia, hora, nombre FROM citas WHERE telefono = ? AND dia >= ?', (telefono, hoy))
    rows = c.fetchall()
    conn.close()
    citas = [
        {'servicio': row[0], 'dia': row[1], 'hora': row[2], 'nombre': row[3]} for row in rows
    ]
    return jsonify({'citas': citas})

@app.route('/borrar_cita', methods=['POST'])
def borrar_cita():
    data = request.get_json()
    fecha = normalizar_fecha(data.get('fecha'))
    hora = data.get('hora')
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM citas WHERE dia = ? AND hora = ?', (fecha, hora))
        conn.commit()
        conn.close()
        
        if c.rowcount > 0:
            return jsonify({'ok': True, 'msg': 'Cita borrada correctamente'})
        else:
            return jsonify({'ok': False, 'msg': 'No se encontró la cita'})
    except Exception as e:
        return jsonify({'ok': False, 'msg': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
