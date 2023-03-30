import tkinter as tk
from tkinter import filedialog
import shutil
import os

# Crear ventana principal
root = tk.Tk()

# Crear función para seleccionar archivo
def browse_file():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Seleccionar archivo", filetypes = (("Archivos", "*.*"), ("Todos los archivos", "*.*")))
    # Mostrar nombre de archivo seleccionado en cuadro de texto
    file_path.set(filename)

# Crear función para subir archivo
def upload_file():
    src_file = file_path.get()
    dest_folder = os.path.join(os.getcwd(), "uploads")
    shutil.copy(src_file, dest_folder)
    # Obtener nombre de archivo subido
    filename = os.path.basename(src_file)
    # Construir ruta completa del archivo subido
    uploaded_file_path = os.path.join(dest_folder, filename)
    # Guardar ruta completa del archivo subido en una variable de tkinter
    uploaded_file_path_var.set(uploaded_file_path)
    # Guardar nombre del archivo subido en una variable de tkinter
    uploaded_file_name_var.set(filename)
    # Mostrar mensaje de confirmación
    tk.messagebox.showinfo("Subir archivo", "Archivo subido con éxito.")

# Crear función para descargar archivo
def download_file():
    filename = uploaded_file_path_var.get()
    root.filename = filedialog.asksaveasfilename(initialdir = "/", title = "Guardar archivo como", initialfile = filename, defaultextension = os.path.splitext(filename)[1])
    if root.filename:
        shutil.copy(filename, root.filename)
        tk.messagebox.showinfo("Descargar archivo", "Archivo descargado con éxito.")

# Crear etiquetas y cuadros de texto
tk.Label(root, text="Archivo:").grid(row=0, column=0)
file_path = tk.StringVar()
tk.Entry(root, textvariable=file_path).grid(row=0, column=1)
tk.Button(root, text="Seleccionar archivo", command=browse_file).grid(row=1, column=0)
tk.Button(root, text="Subir archivo", command=upload_file).grid(row=1, column=1)
tk.Label(root, text="Archivo subido en:").grid(row=2, column=0)
uploaded_file_name_var = tk.StringVar()
uploaded_file_path_var = tk.StringVar()
tk.Button(root, textvariable=uploaded_file_name_var, command=download_file).grid(row=2, column=1, sticky="W")
tk.Entry(root, textvariable=uploaded_file_path_var).grid(row=3, column=1, sticky="W")

# Iniciar bucle principal
root.mainloop()
