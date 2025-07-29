#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import datetime

def test_citas_agosto():
    """Prueba la función citas_dia con fechas del 1 al 8 de agosto"""
    
    print("🧪 Probando citas del 1 al 8 de agosto:")
    print("=" * 50)
    
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
        
        print(f"\n📅 Probando {fecha} ({nombre_dia}){' 🚫 DOMINGO' if es_domingo else ''}")
        
        if not es_domingo:
            try:
                # Hacer petición al endpoint
                response = requests.post('http://localhost:5000/citas_dia', 
                                      json={'dia': fecha},
                                      headers={'Content-Type': 'application/json'})
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Respuesta OK - {len(data['citas'])} citas encontradas")
                    
                    if data['citas']:
                        print("   Citas:")
                        for cita in data['citas']:
                            print(f"   ⏰ {cita['hora']} - {cita['nombre']} - {cita['servicio']}")
                    else:
                        print("   ❌ No hay citas para esta fecha")
                else:
                    print(f"❌ Error HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error de conexión: {e}")
        else:
            print("   ⏭️ Saltando domingo")
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")

if __name__ == "__main__":
    test_citas_agosto() 