import cv2
import time
import numpy as np
import winsound  # Librería nativa de Windows para sonidos

def beep():
    """Emite un pitido similar al de un escáner de supermercado."""
    frequency = 2500  # Frecuencia en Hercios (agudo)
    duration = 150    # Duración en milisegundos (corto)
    winsound.Beep(frequency, duration)

def main():
    """
    Script optimizado para lectura de códigos de barras 1D cada 0.5 segundos.
    """
    # 1. Inicializar detector
    detector = cv2.barcode.BarcodeDetector()
    
    # 2. Iniciar captura
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo acceder a la webcam.")
        return

    # Configuración de rendimiento
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Variables de control de tiempo e historial
    last_scan_time = 0
    scan_interval = 0.5
    history = []
    MAX_HISTORY = 10
    last_detected_code = ""
    is_scanning = False # Estado del lector
    
    # Definición del botón (posición en el panel)
    # El panel empieza en x=640. El botón estará centrado en el panel.
    btn_x, btn_y, btn_w, btn_h = 20, 400, 260, 60
    
    def on_mouse(event, x, y, flags, param):
        nonlocal is_scanning
        if event == cv2.EVENT_LBUTTONDOWN:
            # Ajustar x a las coordenadas del panel (x - 640)
            panel_x = x - 640
            if btn_x <= panel_x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h:
                is_scanning = True
                print("Botón pulsado: Escaneando...")

    # Crear ventana y asignar evento de ratón
    cv2.namedWindow('Lector de Barras Interactivo')
    cv2.setMouseCallback('Lector de Barras Interactivo', on_mouse)

    print("--- Lector de Barras con Botón Activo ---")
    print("Haz clic en el botón 'ESCANEAR' para leer un código.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 3. Lógica de escaneo (Solo si se pulsó el botón)
        if is_scanning:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_info, decoded_type, points = detector.detectAndDecode(gray)
            
            if decoded_info and any(decoded_info):
                full_code = "".join([str(info).strip() for info in decoded_info if info])
                
                if full_code:
                    timestamp = time.strftime('%H:%M:%S')
                    history.insert(0, f"[{timestamp}] {full_code}")
                    beep()
                    is_scanning = False # Detener escaneo tras éxito
            
            # Si pasa 1 segundo sin detectar nada, detenemos el escaneo para no quedar bloqueados
            if time.time() - last_scan_time > 1.0 and is_scanning:
                # Opcional: podrías dejarlo siempre encendido hasta que detecte, 
                # pero aquí lo limitamos por seguridad de UX.
                pass

        # 4. Panel lateral y Botón
        h, w, _ = frame.shape
        panel_width = 300
        panel = np.zeros((h, panel_width, 3), dtype=np.uint8)
        
        # Título Historial
        cv2.putText(panel, "HISTORIAL", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
        cv2.line(panel, (20, 50), (panel_width-20, 50), (200, 200, 200), 1)

        # Dibujar historial (máximo 8 para dejar espacio al botón)
        for i, text in enumerate(history[:8]):
            y_pos = 80 + (i * 25)
            cv2.putText(panel, text, (15, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 127), 1)

        # DIBUJAR BOTÓN ESCANEAR
        # Cambiar color si está escaneando
        btn_color = (0, 165, 255) if not is_scanning else (0, 255, 0)
        cv2.rectangle(panel, (btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h), btn_color, -1)
        cv2.rectangle(panel, (btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h), (255, 255, 255), 2)
        
        text_btn = "ESCANEAR" if not is_scanning else "BUSCANDO..."
        cv2.putText(panel, text_btn, (btn_x + 50, btn_y + 40), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

        # Instrucción debajo del botón
        cv2.putText(panel, "Haz clic para leer", (btn_x + 45, btn_y + 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

        # 5. Combinar y mostrar
        combined_img = np.hstack((frame, panel))
        cv2.imshow('Lector de Barras Interactivo', combined_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
