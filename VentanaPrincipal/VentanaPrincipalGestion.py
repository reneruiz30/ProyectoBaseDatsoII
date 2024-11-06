# VentanaPrincipal/VentanaPrincipalGestion.py
import tkinter as tk
from tkinter import messagebox

class VentanaPrincipalGestionInventario:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Inventario")
        self.ventana.geometry("600x400")

        # Configuración de la interfaz principal
        tk.Label(self.ventana, text="Bienvenido a la Gestión de Inventario", font=("Arial", 16)).pack(pady=20)

        # Puedes agregar aquí otros widgets necesarios para la gestión de inventario
        tk.Button(self.ventana, text="Salir", command=self.ventana.destroy, font=("Arial", 12), bg="#ff5757", fg="white").pack(pady=20)

    def iniciar(self):
        self.ventana.mainloop()