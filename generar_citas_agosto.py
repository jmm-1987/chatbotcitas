import sqlite3
import datetime
import random

def generar_citas_agosto():
    """Genera citas específicamente para las fechas del 1 al 8 de agosto"""
    
    # Nombres realistas de clientes
    nombres = [
        "María García", "Ana López", "Carmen Rodríguez", "Isabel Martínez", "Rosa Sánchez",
        "Elena Pérez", "Laura González", "Sofia Fernández", "Patricia Jiménez", "Mónica Ruiz",
        "Cristina Moreno", "Beatriz Díaz", "Nuria Martín", "Victoria Alonso", "Teresa Gutiérrez",
        "Pilar Romero", "Angeles Navarro", "Dolores Torres", "Concepción Domínguez", "Isabel Vázquez"
    ]
    
    # Servicios disponibles
    servicios = [
        "Corte de mujer", "Corte de hombre", "Peinado", "Tinte raíz", "Mechas", "Lavado y secado",
        "Corte y color", "Peinado de fiesta", "Tinte completo", "Mechas californianas", "Brushing",
        "Corte degradado", "Peinado recogido", "Color fantasía", "Mechas balayage", "Tratamiento capilar"
    ]
    
    # Horarios disponibles
    horas = [
        '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30',
        '16:00', '16:30', '17:00', '17:30',
        '18:00', '18:30', '19:00', '19:30'
    ]
    
    # Conectar a la base de datos
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    print("🎯 Generando citas para agosto (1-8):")
    print("=" * 50)
    
    citas_generadas = 0
    
    # Generar citas para cada día del 1 al 8 de agosto
    for dia in range(1, 9):
        fecha = f"2025-08-{dia:02d}"
        
        # Verificar si la fecha es válida
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha_obj.weekday()]
            es_domingo = fecha_obj.weekday() == 6
        except:
            nombre_dia = "ERROR"
            es_domingo = False
        
        print(f"\n📅 {fecha} ({nombre_dia}){' 🚫 DOMINGO' if es_domingo else ''}")
        
        if not es_domingo:
            # Verificar si ya hay citas para esta fecha
            c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (fecha,))
            citas_existentes = c.fetchone()[0]
            
            if citas_existentes > 0:
                print(f"  ⚠️ Ya hay {citas_existentes} citas para esta fecha")
                continue
            
            # Generar entre 5-12 citas por día
            num_citas = random.randint(5, 12)
            if fecha_obj.weekday() == 4:  # Viernes
                num_citas = random.randint(10, 16)
                print(f"  🔥 Viernes - {num_citas} citas")
            elif fecha_obj.weekday() == 2:  # Miércoles
                num_citas = random.randint(8, 14)
                print(f"  🎯 Miércoles - {num_citas} citas")
            else:
                print(f"  📅 {nombre_dia} - {num_citas} citas")
            
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
                          (nombre, servicio, fecha, hora, telefono))
                
                print(f"    ⏰ {hora} - {nombre} - {servicio}")
                citas_generadas += 1
        else:
            print("  ⏭️ Saltando domingo")
    
    # Confirmar cambios
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Total de citas generadas: {citas_generadas}")
    print("✅ Citas de agosto generadas correctamente")

if __name__ == "__main__":
    generar_citas_agosto() 