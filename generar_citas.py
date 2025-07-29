import requests
import json

def generar_citas_desde_script():
    """Genera citas de prueba usando el endpoint de la API"""
    try:
        # Hacer la petición POST al endpoint
        response = requests.post('http://localhost:5000/generar_citas_prueba')
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                print(f"✅ {data['mensaje']}")
                print(f"📊 Se generaron {len(data['citas'])} citas:")
                
                # Mostrar algunas citas como ejemplo
                for i, cita in enumerate(data['citas'][:5]):
                    print(f"   {i+1}. {cita['nombre']} - {cita['servicio']} - {cita['fecha']} {cita['hora']}")
                
                if len(data['citas']) > 5:
                    print(f"   ... y {len(data['citas']) - 5} citas más")
            else:
                print(f"❌ Error: {data.get('error', 'Error desconocido')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. Asegúrate de que la aplicación esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error: {e}")

def limpiar_citas_desde_script():
    """Limpia todas las citas usando el endpoint de la API"""
    try:
        response = requests.post('http://localhost:5000/limpiar_citas')
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                print(f"✅ {data['mensaje']}")
            else:
                print(f"❌ Error: {data.get('error', 'Error desconocido')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. Asegúrate de que la aplicación esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎲 Generador de Citas de Prueba")
    print("=" * 40)
    
    # Preguntar qué acción realizar
    print("1. Generar citas de prueba")
    print("2. Limpiar todas las citas")
    print("3. Generar y luego limpiar (para testing)")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion == "1":
        generar_citas_desde_script()
    elif opcion == "2":
        confirmar = input("¿Estás seguro de que quieres eliminar todas las citas? (s/n): ").strip().lower()
        if confirmar == 's':
            limpiar_citas_desde_script()
        else:
            print("Operación cancelada.")
    elif opcion == "3":
        print("\n🎲 Generando citas...")
        generar_citas_desde_script()
        print("\n🗑️ Limpiando citas...")
        limpiar_citas_desde_script()
    else:
        print("Opción no válida.") 