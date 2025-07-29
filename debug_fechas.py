#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime

def debug_fechas():
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    print("🔍 Debug de fechas del 1 al 8 de agosto:")
    print("=" * 50)
    
    # Verificar citas específicas del 1 al 8 de agosto
    for dia in range(1, 9):
        fecha = f"2025-08-{dia:02d}"
        c.execute('SELECT COUNT(*) FROM citas WHERE dia = ?', (fecha,))
        count = c.fetchone()[0]
        
        # Verificar si la fecha es válida
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha_obj.weekday()]
            es_domingo = fecha_obj.weekday() == 6
        except:
            nombre_dia = "ERROR"
            es_domingo = False
        
        print(f"📅 {fecha} ({nombre_dia}): {count} citas {'🚫 DOMINGO' if es_domingo else ''}")
        
        # Si hay citas, mostrar detalles
        if count > 0:
            c.execute('SELECT hora, nombre, servicio FROM citas WHERE dia = ? ORDER BY hora', (fecha,))
            citas = c.fetchall()
            for hora, nombre, servicio in citas:
                print(f"   ⏰ {hora} - {nombre} - {servicio}")
    
    print("\n" + "=" * 50)
    print("🔍 Verificando formato de fechas en la base de datos:")
    
    # Verificar todas las fechas en la base de datos
    c.execute('SELECT DISTINCT dia FROM citas ORDER BY dia')
    fechas = c.fetchall()
    
    for (fecha,) in fechas:
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
            nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha_obj.weekday()]
            print(f"✅ {fecha} ({nombre_dia}) - Formato correcto")
        except Exception as e:
            print(f"❌ {fecha} - Error de formato: {e}")
    
    conn.close()

if __name__ == "__main__":
    debug_fechas() 