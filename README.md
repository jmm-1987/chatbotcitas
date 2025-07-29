# 🏪 Chatbot Peluquería JM

Sistema de gestión de citas para peluquería con chatbot interactivo y panel de administración.

## 🚀 Características

### 💬 Chatbot Interactivo
- **Reserva de citas** en tiempo real
- **Calendario visual** con disponibilidad
- **Validación de teléfonos** españoles
- **Confirmación de reservas** con animaciones
- **Galería de trabajos** y servicios

### 📊 Panel de Administración
- **Calendario semanal** con vista de citas
- **Vista diaria** para móviles
- **Estadísticas** de ocupación
- **Gestión de citas** (WhatsApp, llamar, borrar)
- **Generación de datos** de prueba

## 🛠️ Tecnologías

- **Backend**: Flask (Python)
- **Base de datos**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Despliegue**: Render

## 📦 Instalación

### Local
```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd chatbotjm

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

### Render
1. Conectar repositorio de GitHub
2. Configurar variables de entorno (opcional)
3. Desplegar automáticamente

## 🔧 Configuración

### Variables de Entorno (Opcional)
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu-email@gmail.com
EMAIL_PASS=tu-contraseña
EMAIL_RECEIVER=destinatario@email.com
```

## 📱 Uso

### Chatbot
- Accede a la web principal
- Interactúa con el chatbot
- Reserva citas fácilmente

### Panel de Administración
- Ve a `/panel`
- Gestiona citas existentes
- Genera datos de prueba
- Visualiza estadísticas

## 🎯 Funcionalidades Principales

### ✅ Reserva de Citas
- Selección de servicios
- Calendario con disponibilidad
- Validación de datos
- Confirmación automática

### ✅ Panel de Control
- Vista semanal/diaria
- Gestión de citas
- Estadísticas en tiempo real
- Herramientas de desarrollo

### ✅ Integración WhatsApp
- Contacto directo con clientes
- Mensajes automáticos
- Gestión de recordatorios

## 📊 Estructura del Proyecto

```
chatbotjm/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── Procfile             # Configuración Render
├── citas.db             # Base de datos
├── static/              # Archivos estáticos
│   ├── logo.png
│   ├── fondo.png
│   └── ...
├── templates/           # Plantillas HTML
│   ├── index.html      # Chatbot principal
│   └── panel.html      # Panel de administración
└── scripts/            # Scripts de utilidad
    ├── test_citas.py
    ├── verificar_citas.py
    └── limpiar_y_generar.py
```

## 🚀 Despliegue

### Render
1. **Conectar GitHub**: Vincula tu repositorio
2. **Configurar build**: `pip install -r requirements.txt`
3. **Configurar start**: `gunicorn app:app`
4. **Variables de entorno**: Configura si es necesario
5. **Desplegar**: ¡Listo!

### Variables de Entorno en Render
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu-email@gmail.com
EMAIL_PASS=tu-contraseña
EMAIL_RECEIVER=destinatario@email.com
```

## 🔧 Desarrollo

### Scripts Útiles
```bash
# Generar citas de prueba
python test_citas.py

# Verificar citas en BD
python verificar_citas.py

# Limpiar y generar nuevas citas
python limpiar_y_generar.py
```

### Debug
- Abre herramientas de desarrollador (F12)
- Mira la consola para logs de debug
- Verifica las fechas consultadas

## 📞 Soporte

Para problemas o mejoras:
1. Revisa los logs de debug
2. Verifica la configuración
3. Contacta al desarrollador

## 📄 Licencia

Proyecto privado para Peluquería JM.

---

**¡Listo para desplegar en Render!** 🚀 