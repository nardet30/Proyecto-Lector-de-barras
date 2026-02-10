# Proyecto Lector de Barras 1D

**Autor:** Bernardo Moscardo
**GitHub:** [nardet30](https://github.com/nardet30)

## Descripción
Este es un proyecto de Python diseñado para leer códigos de barras 1D de forma interactiva utilizando la cámara web del dispositivo. Cuenta con una interfaz visual intuitiva que permite al usuario gestionar los escaneos manualmente mediante un botón, manteniendo un historial en tiempo real de los códigos capturados.

### Características
- Interfaz interactiva con OpenCV.
- Botón de escaneo manual ("ESCANEAR").
- Historial dinámico en pantalla.
- Feedback sonoro (beep) al detectar un código.
- Optimización para lectura cada 0.5 segundos.

---

## Proceso de Instalación

Sigue estos pasos para configurar el proyecto en tu máquina local (Windows):

### 1. Clonar el repositorio
Si tienes Git instalado, puedes clonar el proyecto directamente:
```bash
git clone https://github.com/nardet30/Proyecto-Lector-de-barras.git
cd Proyecto-Lector-de-barras
```

### 2. Instalar Python
Asegúrate de tener Python 3.7 o superior instalado. Puedes descargarlo desde [python.org](https://www.python.org/).

### 3. Instalar librerías necesarias
Ejecuta el siguiente comando en tu terminal para instalar las dependencias:
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
Para iniciar el lector de barras, ejecuta el script principal:
```bash
python lector_barras.py
```

---

## Instrucciones de Uso (Interfaz)
1. Coloca el código de barras frente a la cámara.
2. Haz clic en el botón naranja que dice **"ESCANEAR"**.
3. El sistema buscará el código, emitirá un sonido al encontrarlo y guardará el resultado en el historial.
4. Para salir, presiona la tecla **'q'**.
