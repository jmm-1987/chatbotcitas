#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime

def verificar_fecha_actual():
    """Verifica las fechas actuales y el problema con las citas del 1 al 8 de agosto"""
    
    print("🔍 Verificación de fechas y citas:")
    print("=" * 50)
    
    # Verificar fecha actual
    hoy = datetime.date.today()
    print(f"📅 Fecha actual: {hoy}")
    print(f"📅 Fecha actual formato: {hoy.strftime('%Y-%m-%d')}")
    
    # Conectar a la base de datos
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    # Verificar todas las fechas en la base de datos
    c.execute('SELECT DISTINCT dia FROM citas ORDER BY dia')
    fechas = c.fetchall()
    
    print(f"\n📊 Total de fechas únicas en la base de datos: {len(fechas)}")
    
    # Verificar específicamente las fechas del 1 al 8 de agosto
    print("\n🔍 Verificando fechas del 1 al 8 de agosto:")
    for dia in range(1, 9):
        fecha = f"2025-08-{dia:02d}"
        c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (fecha,))
        count = c.fetchone()[0]
        
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha_obj.weekday()]
            es_domingo = fecha_obj.weekday() == 6
        except:
            nombre_dia = "ERROR"
            es_domingo = False
        
        print(f"  {fecha} ({nombre_dia}): {count} citas {'🚫 DOMINGO' if es_domingo else ''}")
        
        # Si hay citas, mostrar algunas
        if count > 0:
            c.execute('SELECT hora, nombre, servicio FROM citas WHERE dia = ? ORDER BY hora LIMIT 3', (fecha,))
            citas = c.fetchall()
            for hora, nombre, servicio in citas:
                print(f"    ⏰ {hora} - {nombre} - {servicio}")
            if count > 3:
                print(f"    ... y {count - 3} citas más")
    
    # Verificar si hay fechas con formato incorrecto
    print("\n🔍 Verificando formato de fechas:")
    for (fecha,) in fechas:
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha_obj.weekday()]
            print(f"  ✅ {fecha} ({nombre_dia})")
        except Exception as e:
            print(f"  ❌ {fecha} - Error: {e}")
    
    # Verificar citas de agosto específicamente
    print("\n🔍 Citas de agosto:")
    c.execute("SELECT dia, COUNT(*) FROM citas WHERE dia LIKE '2025-08-%' GROUP BY dia ORDER BY dia")
    agosto = c.fetchall()
    
    for dia, count in agosto:
        try:
            fecha_obj = datetime.datetime.strptime(dia, '%Y-%m-%d')
            nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha_obj.weekday()]
            print(f"  {dia} ({nombre_dia}): {count} citas")
        except:
            print(f"  {dia}: {count} citas (formato incorrecto)")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("✅ Verificación completada")

if __name__ == "__main__":
    verificar_fecha_actual() 