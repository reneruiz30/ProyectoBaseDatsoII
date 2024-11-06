import mysql.connector
import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from VentanaPrincipal.VentanaPrincipalGestion import VentanaPrincipalGestionInventario


# Conexión a la base de datos
conexion1 = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="proyectobd2gestionempresa"
)

# Función de inicio de sesión
def login():
    nombre = usuario.get()
    contraseña = password.get()
    
    cursor1 = conexion1.cursor()
    contraQuery = "SELECT password FROM usuarios WHERE nombre_usuario = %s"
    cursor1.execute(contraQuery, (nombre,))
    result = cursor1.fetchone()
    
    if result and result[0] == contraseña:
        messagebox.showinfo('Bienvenido!', 'Bienvenido al Sistema. Contraseña Correcta')
        ventana.destroy()  # Cerramos la ventana de login
        abrir_ventana_principal()
    else:
        nombre_entry.delete(0, tk.END)
        correo_entry.delete(0, tk.END)
        messagebox.showerror('Advertencia...!', 'Contraseña Incorrecta')
    
    cursor1.close()


# Función para abrir la ventana principal de gestión de inventario
def abrir_ventana_principal():
    ventana_principal = VentanaPrincipalGestionInventario()
    ventana_principal.iniciar()

# Función para abrir la ventana de registro
def abrir_ventana_registro():
    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("400x300")
    
    tk.Label(ventana_registro, text="Nombre de Usuario:", font=("Arial", 12)).pack(pady=10)
    nuevo_usuario = tk.Entry(ventana_registro, font=("Arial", 12))
    nuevo_usuario.pack()

    tk.Label(ventana_registro, text="Contraseña:", font=("Arial", 12)).pack(pady=10)
    nueva_password = tk.Entry(ventana_registro, font=("Arial", 12), show="*")
    nueva_password.pack()

    def guardar_usuario():
        nombre = nuevo_usuario.get()
        contraseña = nueva_password.get()
        
        if nombre and contraseña:
            cursor2 = conexion1.cursor()
            insert_query = "INSERT INTO usuarios (nombre_usuario, password) VALUES (%s, %s)"
            try:
                cursor2.execute(insert_query, (nombre, contraseña))
                conexion1.commit()
                messagebox.showinfo("Registro exitoso", "Usuario agregado correctamente")
                ventana_registro.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al registrar usuario: {err}")
            finally:
                cursor2.close()
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos")

    tk.Button(
        ventana_registro, text="Guardar Usuario", command=guardar_usuario,
        font=("Arial", 12), bg="#4CAF50", fg="white"
    ).pack(pady=20)

# Configuración de la ventana principal
ventana = tk.Tk()
usuario = tk.StringVar()
password = tk.StringVar()

ventana.title("Login")
ventana.geometry("414x896")
ventana.resizable(width=False, height=False)

# Fondo de la ventana
ruta_imagen = "InicioSesion/LoginR.png"
if not os.path.exists(ruta_imagen):
    print(f"Advertencia: No se encontró el archivo {ruta_imagen}")
else:
    fondo = tk.PhotoImage(file=ruta_imagen)
    fondo1 = tk.Label(ventana, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)

# Campos de entrada
nombre_entry = tk.Entry(textvariable=usuario, font=("Arial", 12), fg="White", bg="#474a4a", bd=0, highlightthickness=0)
nombre_entry.place(x=70, y=465, width=280, height=40)

correo_entry = tk.Entry(textvariable=password, font=("Arial", 12), fg="White", bg="#474a4a", bd=0, highlightthickness=0, show="*")
correo_entry.place(x=70, y=550, width=280, height=40)

# Botones
signup_button = tk.Button(
    ventana, text="Sign Up", command=login, font=("Arial", 12), bg="#ff5757", fg="white", bd=0, highlightthickness=0, cursor="hand2"
)
signup_button.place(x=70, y=622, width=260, height=44)

# Botón para abrir la ventana de registro de usuario
registro_button = tk.Button(
    ventana, text="Registrar Nuevo Usuario", command=abrir_ventana_registro,
    font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, highlightthickness=0, cursor="hand2"
)
registro_button.place(x=70, y=720, width=260, height=44)

# Ejecutar la aplicación
ventana.mainloop()
