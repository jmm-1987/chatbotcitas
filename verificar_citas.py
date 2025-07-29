#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime

def verificar_citas():
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()
    
    # Verificar total de citas
    c.execute('SELECT COUNT(*) FROM citas')
    total = c.fetchone()[0]
    print(f"📊 Total de citas en la base de datos: {total}")
    
    # Verificar citas por día
    c.execute('SELECT dia, COUNT(*) as total FROM citas GROUP BY dia ORDER BY dia')
    dias = c.fetchall()
    
    print("\n📅 Citas por día:")
    for dia, count in dias:
        fecha = datetime.datetime.strptime(dia, '%Y-%m-%d')
        nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha.weekday()]
        print(f"  {dia} ({nombre_dia}): {count} citas")
    
    # Verificar citas de viernes específicamente
    c.execute("SELECT dia, COUNT(*) FROM citas WHERE dia LIKE '%-%-%' AND strftime('%w', dia) = '5' GROUP BY dia ORDER BY dia")
    viernes = c.fetchall()
    
    print(f"\n🔥 Citas de viernes: {len(viernes)} días")
    for dia, count in viernes:
        print(f"  {dia}: {count} citas")
    
    conn.close()

if __name__ == "__main__":
    verificar_citas() 