import cv2
import numpy as np
import screen_brightness_control as sbc
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Variable global para controlar el bucle
ajuste_brillo_habilitado = True

# Función para calcular el brillo promedio de una imagen
def calcular_brillo_promedio(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Calcular el brillo promedio de la imagen
    brillo_promedio = np.mean(imagen_gris)
    
    return brillo_promedio

# Función para ajustar el brillo en Windows
def ajustar_brillo_windows(brillo):
    sbc.set_brightness(brillo)  # Establecer el brillo

# Función principal que captura y ajusta el brillo cada 8 segundos
def ajustar_brillo_periodico():
    global ajuste_brillo_habilitado
    while True:
        if not ajuste_brillo_habilitado:
            break  # Salir del bucle si el ajuste está deshabilitado

        # Capturar la imagen de la cámara
        cap = cv2.VideoCapture(0)  # Usa la cámara por defecto

        # Verificar si la cámara está abierta correctamente
        if not cap.isOpened():
            print("No se pudo acceder a la cámara.")
            exit()

        # Captura de una imagen
        ret, frame = cap.read()

        # Liberar la cámara
        cap.release()

        # Verificar si la captura fue exitosa
        if not ret:
            print("Error al capturar la imagen.")
            exit()

        # Calcular el brillo promedio de la imagen
        brillo_promedio = calcular_brillo_promedio(frame)
        print(f"Brillo promedio de la imagen: {brillo_promedio}")

        # Ajustar el brillo de la pantalla según el brillo promedio
        if brillo_promedio < 35:
            print("El entorno es muy oscuro. Reduciendo el brillo al mínimo.")
            ajustar_brillo_windows(0)  # Establecer brillo al 0%
        elif brillo_promedio < 50:
            print("El entorno es oscuro. Ajustando el brillo.")
            ajustar_brillo_windows(10)  # Establecer brillo al 10%
        elif brillo_promedio < 70:
            print("El entorno es algo oscuro. Ajustando el brillo.")
            ajustar_brillo_windows(20)  # Establecer brillo al 20%
        elif brillo_promedio < 90:
            print("El entorno es ligeramente oscuro. Ajustando el brillo.")
            ajustar_brillo_windows(30)  # Establecer brillo al 30%
        elif brillo_promedio < 160:
            print("El entorno es moderadamente brillante. Ajustando el brillo.")
            ajustar_brillo_windows(40)  # Establecer brillo al 40%
        elif brillo_promedio < 180:
            print("El entorno es algo brillante. Ajustando el brillo.")
            ajustar_brillo_windows(50)  # Establecer brillo al 50%
        elif brillo_promedio < 200:
            print("El entorno es brillante. Ajustando el brillo.")
            ajustar_brillo_windows(60)  # Establecer brillo al 60%
        elif brillo_promedio < 220:
            print("El entorno es muy brillante. Ajustando el brillo.")
            ajustar_brillo_windows(70)  # Establecer brillo al 70%
        elif brillo_promedio < 240:
            print("El entorno es extremadamente brillante. Ajustando el brillo.")
            ajustar_brillo_windows(85)  # Establecer brillo al 85%
        else:
            print("El entorno es muy brillante. Estableciendo el brillo máximo.")
            ajustar_brillo_windows(100)  # Establecer brillo al máximo

        # Esperar 8 segundos antes de capturar nuevamente
        time.sleep(8)

# Función para habilitar o deshabilitar el ajuste automático de brillo
def toggle_ajuste_brillo():
    global ajuste_brillo_habilitado
    if ajuste_brillo_habilitado:
        ajuste_brillo_habilitado = False
        button_toggle.config(text="Habilitar Ajuste de Brillo")
        messagebox.showinfo("Ajuste de brillo", "El ajuste automático de brillo ha sido deshabilitado.")
    else:
        ajuste_brillo_habilitado = True
        button_toggle.config(text="Deshabilitar Ajuste de Brillo")
        messagebox.showinfo("Ajuste de brillo", "El ajuste automático de brillo ha sido habilitado.")
        # Iniciar el hilo para el ajuste de brillo nuevamente
        threading.Thread(target=ajustar_brillo_periodico, daemon=True).start()

# Crear la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Ajuste Automático de Brillo")

# Crear un botón para habilitar/deshabilitar el ajuste de brillo
button_toggle = tk.Button(root, text="Deshabilitar Ajuste de Brillo", command=toggle_ajuste_brillo)
button_toggle.pack(pady=20)

# Iniciar el hilo para el ajuste de brillo al inicio
threading.Thread(target=ajustar_brillo_periodico, daemon=True).start()

# Ejecutar la interfaz gráfica
root.mainloop()
