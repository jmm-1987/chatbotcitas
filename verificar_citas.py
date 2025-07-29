#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime

# Configuración de la base de datos
DB_PATH = 'citas.db'

def verificar_citas():
    """Verifica las citas en la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Obtener todas las citas
    c.execute('SELECT dia, hora, nombre, servicio FROM citas ORDER BY dia, hora')
    rows = c.fetchall()
    conn.close()
    
    print(f"📊 Total de citas en la base de datos: {len(rows)}")
    print("=" * 50)
    
    if not rows:
        print("❌ No hay citas en la base de datos")
        return
    
    # Agrupar por día
    citas_por_dia = {}
    for row in rows:
        dia, hora, nombre, servicio = row
        if dia not in citas_por_dia:
            citas_por_dia[dia] = []
        citas_por_dia[dia].append((hora, nombre, servicio))
    
    # Mostrar citas por día
    for dia in sorted(citas_por_dia.keys()):
        fecha = datetime.datetime.strptime(dia, '%Y-%m-%d')
        nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha.weekday()]
        print(f"\n📅 {nombre_dia} {dia} ({len(citas_por_dia[dia])} citas):")
        
        for hora, nombre, servicio in sorted(citas_por_dia[dia]):
            print(f"   ⏰ {hora} - {nombre} - {servicio}")

if __name__ == "__main__":
    verificar_citas() 