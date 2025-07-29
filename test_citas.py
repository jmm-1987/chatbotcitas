#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

# Configuración de la base de datos
DB_PATH = 'citas.db'

def guardar_cita(nombre, servicio, dia, hora, telefono):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO citas (nombre, servicio, dia, hora, telefono) VALUES (?, ?, ?, ?, ?)',
              (nombre, servicio, dia, hora, telefono))
    conn.commit()
    conn.close()

def limpiar_citas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM citas')
    conn.commit()
    conn.close()
    print("🗑️ Todas las citas han sido eliminadas")

def generar_citas_prueba():
    """Genera citas de prueba realistas para esta semana"""
    
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
    
    # Generar fechas de esta semana (lunes a sábado)
    hoy = datetime.date.today()
    lunes = hoy - datetime.timedelta(days=hoy.weekday())  # Lunes de esta semana
    
    print(f"📅 Generando citas para la semana del {lunes} al {lunes + datetime.timedelta(days=6)}")
    
    citas_generadas = []
    
    # Generar citas para cada día de la semana (lunes a sábado)
    for i in range(6):  # 6 días (lunes a sábado)
        fecha = lunes + datetime.timedelta(days=i)
        fecha_str = fecha.strftime('%Y-%m-%d')
        dia_semana = fecha.weekday()
        nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana]
        
        # Domingo no hay citas
        if dia_semana == 6:  # Domingo
            continue
            
        # Generar entre 4-12 citas por día (más ocupado los miércoles y viernes)
        num_citas = random.randint(4, 12)
        if dia_semana == 2:  # Miércoles más ocupado
            num_citas = random.randint(8, 14)
            print(f"🎯 Miércoles {fecha_str}: {num_citas} citas")
        elif dia_semana == 4:  # Viernes muy ocupado
            num_citas = random.randint(12, 18)  # Aumentado para asegurar muchas citas
            print(f"🔥 Viernes {fecha_str}: {num_citas} citas")
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
    
    print(f"\n🎉 Total de citas generadas: {len(citas_generadas)}")
    return citas_generadas

if __name__ == "__main__":
    print("🎲 Generador de Citas de Prueba")
    print("=" * 40)
    
    # Preguntar qué acción realizar
    print("1. Generar citas de prueba")
    print("2. Limpiar todas las citas")
    print("3. Generar y luego limpiar (para testing)")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion == "1":
        generar_citas_prueba()
    elif opcion == "2":
        confirmar = input("¿Estás seguro de que quieres eliminar todas las citas? (s/n): ").strip().lower()
        if confirmar == 's':
            limpiar_citas()
        else:
            print("Operación cancelada.")
    elif opcion == "3":
        print("\n🎲 Generando citas...")
        generar_citas_prueba()
        print("\n🗑️ Limpiando citas...")
        limpiar_citas()
    else:
        print("Opción no válida.") 