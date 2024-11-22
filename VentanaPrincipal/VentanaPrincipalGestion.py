from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

def conectar_bd():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sistema_gestion"
        )
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

class VentanaPrincipalGestionInventario:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema de Gestión")
        self.root.geometry("800x800")

        # Cargar y mostrar fondo
        ruta_fondo = os.path.join(os.path.dirname(__file__), "VENTAS_AL_POR_MENOR.png")
        try:
            imagen_fondo = Image.open(ruta_fondo)
            fondo_redimensionado = imagen_fondo.resize((800, 800))
            self.fondo = ImageTk.PhotoImage(fondo_redimensionado)
            fondo_label = Label(self.root, image=self.fondo)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el fondo: {e}")

        # Cargar imagen del botón
        ruta_boton = os.path.join(os.path.dirname(__file__), "GestionClientes.png")
        try:
            imagen_boton = Image.open(ruta_boton)
            boton_redimensionado = imagen_boton.resize((150, 150))
            self.imagenBoton1 = ImageTk.PhotoImage(boton_redimensionado)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del botón: {e}")
            self.imagenBoton1 = None

        # Botón
        Button(
            self.root,
            image=self.imagenBoton1,
            command=self.gestionar_clientes,
            bg="#5271ff",
            relief="flat"
        ).place(x=95, y=170, width=235, height=190)

    def gestionar_clientes(self):
        def cargar_clientes():
            for row in tree.get_children():
                tree.delete(row)
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM clientes")
                for cliente in cursor.fetchall():
                    tree.insert("", "end", values=cliente)
                conexion.close()

        def agregar_cliente():
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            email = entry_email.get()
            if nombre and telefono and email:
                conexion = conectar_bd()
                if conexion:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)",
                        (nombre, telefono, email)
                    )
                    conexion.commit()
                    conexion.close()
                    cargar_clientes()
                    entry_nombre.delete(0, END)
                    entry_telefono.delete(0, END)
                    entry_email.delete(0, END)
                    messagebox.showinfo("Éxito", "Cliente añadido correctamente.")
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

        def eliminar_cliente():
            selected_item = tree.focus()
            if selected_item:
                cliente_id = tree.item(selected_item)["values"][0]
                conexion = conectar_bd()
                if conexion:
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
                    conexion.commit()
                    conexion.close()
                    cargar_clientes()
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "Selecciona un cliente para eliminar.")

        def modificar_cliente():
            # Obtener el cliente seleccionado
            selected_item = tree.focus()  # Obtener ID del cliente seleccionado en la tabla
            if selected_item:
                cliente = tree.item(selected_item)["values"]
                if cliente:
                    # Rellenar los campos con la información del cliente seleccionado
                    entry_nombre.delete(0, END)
                    entry_telefono.delete(0, END)
                    entry_email.delete(0, END)

                    entry_nombre.insert(0, cliente[1])  # Nombre
                    entry_telefono.insert(0, cliente[2])  # Teléfono
                    entry_email.insert(0, cliente[3])  # Email

                    # Confirmar la modificación
                    def guardar_cambios():
                        nuevo_nombre = entry_nombre.get()
                        nuevo_telefono = entry_telefono.get()
                        nuevo_email = entry_email.get()

                        if nuevo_nombre and nuevo_telefono and nuevo_email:
                            try:
                                conexion = conectar_bd()
                                if conexion:
                                    cursor = conexion.cursor()
                                    cursor.execute(
                                        """
                                        UPDATE clientes
                                        SET nombre = %s, telefono = %s, email = %s
                                        WHERE id = %s
                                        """,
                                        (nuevo_nombre, nuevo_telefono, nuevo_email, cliente[0])  # Cliente[0] es el ID
                                    )
                                    conexion.commit()  # Confirmar los cambios
                                    conexion.close()
                                    cargar_clientes()
                                    messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
                                    # Limpiar los campos después de guardar
                                    entry_nombre.delete(0, END)
                                    entry_telefono.delete(0, END)
                                    entry_email.delete(0, END)
                            except Exception as e:
                                messagebox.showerror("Error", f"Error al modificar cliente: {e}")
                        else:
                            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

                    # Crear botón para guardar cambios
                    Button(frame_form, font= "roboto", text="Guardar Cambios", command=guardar_cambios, relief="flat", bg= "#004aad", fg="white").grid(row=4, column=1, pady=10)
            else:
                messagebox.showwarning("Advertencia", "Selecciona un cliente para modificar.")


        # Configuración de la ventana
        ventana = Toplevel(self.root)
        ventana.title("Gestión de Clientes")
        ventana.geometry("800x600")
        # Imagen de fondo
        ruta_fondo_clientes = os.path.join(os.path.dirname(__file__), "GestionClientesFondo.png")
        try:
            imagen_fondo_clientes = Image.open(ruta_fondo_clientes)
            fondo_redimensionado_clientes = imagen_fondo_clientes.resize((800, 600))
            self.fondo_clientes = ImageTk.PhotoImage(fondo_redimensionado_clientes)
            fondo_label = Label(ventana, image=self.fondo_clientes)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")

        # Formulario
        frame_form = Frame(ventana)
        frame_form.pack(pady=80)
        Label(frame_form, text="").grid(row=0, column=0, padx=5, pady=5)
        Label(frame_form, font= "roboto",text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        entry_nombre = Entry(frame_form)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        Label(frame_form, font= "roboto",text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
        entry_telefono = Entry(frame_form)
        entry_telefono.grid(row=1, column=1, padx=5, pady=5)
        Label(frame_form, font= "roboto",text="Email:").grid(row=2, column=0, padx=5, pady=5)
        entry_email = Entry(frame_form)
        entry_email.grid(row=2, column=1, padx=5, pady=5)

        Button(frame_form, font= "roboto",text="Agregar Cliente", command=agregar_cliente, relief="flat", bg= "#004aad", fg="white").grid(row=3, column=0, pady=20, padx=5)
        Button(frame_form, font= "roboto", text="Modificar Cliente", command=modificar_cliente,relief="flat", bg= "#004aad", fg="white").grid(row=3, column=1, pady=20, padx=5)
        Button(frame_form, font= "roboto", text="Eliminar Cliente", command=eliminar_cliente, relief="flat", bg= "#004aad", fg="white").grid(row=3, column=2, pady=20, padx=5)

        # Tabla
        frame_tabla = Frame(ventana)
        frame_tabla.pack(pady=10, padx=20)
        tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Teléfono", "Email"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Email", text="Email")
        tree.pack()

        # Cargar datos
        cargar_clientes()

    def iniciar(self):
        self.root.mainloop()


# Crear una instancia de la clase y ejecutar
app = VentanaPrincipalGestionInventario()
app.iniciar()
