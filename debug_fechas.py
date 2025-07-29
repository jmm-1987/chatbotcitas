#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

def mostrar_fechas_panel():
    """Muestra las fechas que está consultando el panel"""
    
    # Calcular la semana actual (como lo hace el panel)
    hoy = datetime.date.today()
    lunes = hoy - datetime.timedelta(days=hoy.weekday())  # Lunes de esta semana
    
    print("📅 Fechas que está consultando el panel:")
    print("=" * 50)
    
    for i in range(7):  # 7 días (domingo a sábado)
        fecha = lunes + datetime.timedelta(days=i)
        fecha_str = fecha.strftime('%Y-%m-%d')
        fecha_display = fecha.strftime('%d/%m/%Y')
        nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha.weekday()]
        
        print(f"  {i}: {fecha_str} ({fecha_display}) - {nombre_dia}")
    
    print(f"\n📊 Resumen:")
    print(f"  Hoy: {hoy}")
    print(f"  Lunes de esta semana: {lunes}")
    print(f"  Viernes de esta semana: {lunes + datetime.timedelta(days=4)}")

if __name__ == "__main__":
    mostrar_fechas_panel() 