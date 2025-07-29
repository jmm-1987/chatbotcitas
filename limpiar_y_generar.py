#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import random

def limpiar_y_generar():
    """Limpia todas las citas y las regenera correctamente"""
    
    print("🧹 Limpiando y regenerando citas...")
    print("=" * 50)
    
    # Conectar a la base de datos
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    # Limpiar todas las citas
    c.execute('DELETE FROM citas')
    print("🗑️ Todas las citas han sido eliminadas")
    
    # Nombres realistas de clientes
    nombres = [
        "María García", "Ana López", "Carmen Rodríguez", "Isabel Martínez", "Rosa Sánchez",
        "Elena Pérez", "Laura González", "Sofia Fernández", "Patricia Jiménez", "Mónica Ruiz",
        "Cristina Moreno", "Beatriz Díaz", "Nuria Martín", "Victoria Alonso", "Teresa Gutiérrez",
        "Pilar Romero", "Angeles Navarro", "Dolores Torres", "Concepción Domínguez", "Isabel Vázquez",
        "Lucía Hernández", "Paula Castro", "Adriana Morales", "Claudia Silva", "Valentina Rojas",
        "Camila Mendoza", "Sara Herrera", "Daniela Vega", "Gabriela Fuentes", "Carolina Reyes",
        "Andrea Morales", "Natalia Jiménez", "Valeria Torres", "Mariana Silva", "Fernanda Castro"
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
    
    citas_generadas = 0
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
            c.execute('INSERT INTO citas (nombre, servicio, dia, hora, telefono) VALUES (?, ?, ?, ?, ?)',
                      (nombre, servicio, fecha_str, hora, telefono))
            citas_generadas += 1
        
        fecha_actual += datetime.timedelta(days=1)
    
    # Confirmar cambios
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Total de citas generadas: {citas_generadas}")
    print("✅ Base de datos regenerada correctamente")

if __name__ == "__main__":
    limpiar_y_generar() 