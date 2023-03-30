import tkinter as tk
from tkinter import ttk

# Crear ventana principal
root = tk.Tk()

# Crear Treeview
num_pairs = 15  # número de pares de columnas "inc" y "repro"
cols = ["No.", "Matricula", "Nombre"]
for i in range(num_pairs):
    cols.append(f"Inc{i+1}")
    cols.append(f"Repro{i+1}")
tree = ttk.Treeview(root, columns=cols)

# Crear encabezados de columna
tree.heading("#0", text="ID")
tree.heading("No.", text="No.")
tree.heading("Matricula", text="Matricula")
tree.heading("Nombre", text="Nombre")
for i in range(num_pairs):
    tree.heading(f"Inc{i+1}", text=f"Inc{i+1}")
    tree.heading(f"Repro{i+1}", text=f"Repro{i+1}")

# Agregar datos a la tabla
tree.insert("", "end", text="1", values=["1", "123456", "Juan Perez"] + ["2", "1"]*num_pairs)
tree.insert("", "end", text="2", values=["2", "789012", "Maria Hernandez"] + ["1", "0"]*num_pairs)
tree.insert("", "end", text="3", values=["3", "345678", "Pedro Rodriguez"] + ["0", "3"]*num_pairs)

# Agregar scrollbar vertical
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")

# Agregar scrollbar horizontal
hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(side="bottom", fill="x")

# Organizar el Treeview
tree.pack(fill="both", expand=True)

# Mostrar la ventana principal
root.mainloop()
