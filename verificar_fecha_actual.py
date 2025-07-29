#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

def verificar_fecha():
    hoy = datetime.date.today()
    lunes = hoy - datetime.timedelta(days=hoy.weekday())
    
    print(f"📅 Fecha actual del sistema: {hoy}")
    print(f"📅 Lunes de esta semana: {lunes}")
    print(f"📅 Viernes de esta semana: {lunes + datetime.timedelta(days=4)}")
    
    print(f"\n📊 Semana completa:")
    for i in range(7):
        fecha = lunes + datetime.timedelta(days=i)
        nombre = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][fecha.weekday()]
        print(f"  {nombre}: {fecha}")

if __name__ == "__main__":
    verificar_fecha() 