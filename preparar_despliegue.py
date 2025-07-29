#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def limpiar_archivos_desarrollo():
    """Limpia archivos de desarrollo antes del despliegue"""
    
    archivos_a_eliminar = [
        'verificar_fecha_actual.py',
        'debug_fechas.py',
        'test_citas.py',
        'verificar_citas.py',
        'limpiar_y_generar.py',
        'generar_citas.py',
        'preparar_despliegue.py'
    ]
    
    print("🧹 Limpiando archivos de desarrollo...")
    
    for archivo in archivos_a_eliminar:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"  ✅ Eliminado: {archivo}")
        else:
            print(f"  ⚠️ No encontrado: {archivo}")
    
    print("\n📋 Archivos que se subirán a GitHub:")
    archivos_importantes = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'README.md',
        '.gitignore',
        'citas.db',
        'static/',
        'templates/'
    ]
    
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            if os.path.isdir(archivo):
                print(f"  📁 {archivo}/")
            else:
                print(f"  📄 {archivo}")
        else:
            print(f"  ❌ Faltante: {archivo}")
    
    print("\n🚀 ¡Proyecto listo para desplegar en Render!")
    print("\n📝 Pasos para el despliegue:")
    print("1. git add .")
    print("2. git commit -m 'Preparado para despliegue en Render'")
    print("3. git push origin main")
    print("4. Conectar repositorio en Render")
    print("5. Configurar variables de entorno (opcional)")

if __name__ == "__main__":
    limpiar_archivos_desarrollo() 