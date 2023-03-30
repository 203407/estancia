import os
import shutil
import tkinter as tk
from tkinter import END, Scrollbar, ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import customtkinter as ctk 
from PIL import Image
from tkintertable import TableCanvas
import psycopg2
import json
import urllib.request
from urllib.request import urlretrieve
import re

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILEPATH = ""

class Window(ctk.CTk):
    def __init__(self,select_file, get_data):
        super().__init__()
        self.title("Proyecto indicadores CACEI")
        self.geometry("1400x750")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue") 

        #Funciones
        self.select_file = select_file
        self.get_data = get_data

        #Datos
        self.asignaturas = []
        self.alumnos = []
        datas = []
        self.tabla_trayectoria= None
        self.trayectoria = []
        
        hanbi = False
        
        #Paginas/vistas
        self.top_frame = ctk.CTkFrame(master=self, width=1400, height=180, corner_radius=0, fg_color="#E5E5E5") 
        self.bottom_frame = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame2 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame3 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame4 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame5 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame6 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame7 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame8 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")

        #Barra de navegación superior
        self.top_frame.grid(padx=0, pady=0, row=0, column=0)
        
        #Logo y titulo (Barra de navegación superior)
        logo = ctk.CTkImage(light_image=Image.open('img/logo.png'), dark_image=Image.open('img/logo.png'), size=(105,105))
        logo_label = ctk.CTkLabel(master=self.top_frame, corner_radius=0, image=logo, text="")
        logo_label.place(relx=0.340, rely=0.5, anchor=tk.CENTER)
        title_label = ctk.CTkLabel(master=self.top_frame, corner_radius=0, text="Programa indicadores CACEI", font=("Helvetica",  28, 'bold'))
        title_label.place(relx=0.540, rely=0.375, anchor=tk.CENTER)

        #Botones de navegación de páginas
        self.nav_btn_1 = ctk.CTkButton(master=self.top_frame, text="Inicio", width=35 , command = self.view1, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_1.place(relx=0.415, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_2 = ctk.CTkButton(master=self.top_frame, text="Índice reprobados", width=65 , command=self.view2, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_2.place(relx=0.474, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_3 = ctk.CTkButton(master=self.top_frame, text="Expediente", width=40 , command=self.view3, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_3.place(relx=0.543, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_4 = ctk.CTkButton(master=self.top_frame, text="Trayectoria", width=40 , command=self.view4, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_4.place(relx=0.600, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_5 = ctk.CTkButton(master=self.top_frame, text="Reprobados", width=40 , command=self.view5, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_5.place(relx=0.657, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_6 = ctk.CTkButton(master=self.top_frame, text="Cerrar", width=40 ,command=self.logout, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_6.place(relx=0.710, rely=0.625, anchor=tk.CENTER)        

        # self.view1()
        self.viewL()
        
    def chanteStatus(self):
        self.nav_btn_1.configure(state="normal")
        self.nav_btn_2.configure(state="normal")
        self.nav_btn_3.configure(state="normal")
        self.nav_btn_4.configure(state="normal")
        self.nav_btn_5.configure(state="normal")
        self.nav_btn_6.configure(state="normal")        

    def changedagain(self):
        self.nav_btn_1.configure(state="disabled")
        self.nav_btn_2.configure(state="disabled")
        self.nav_btn_3.configure(state="disabled")
        self.nav_btn_4.configure(state="disabled")
        self.nav_btn_5.configure(state="disabled")
        self.nav_btn_6.configure(state="disabled")        

    def logout(self):
        self.navigate()
        self.changedagain()
        self.viewL()

    def navigate(self):
        self.bottom_frame.grid_remove()
        self.bottom_frame2.grid_remove()
        self.bottom_frame3.grid_remove()
        self.bottom_frame4.grid_remove()
        self.bottom_frame5.grid_remove()  
        self.bottom_frame6.grid_remove()  
        self.bottom_frame7.grid_remove()  
        self.bottom_frame8.grid_remove() 

    def show_message(self, title, msj):
        messagebox.showinfo(message=msj, title=title)
    
    def viewL(self):
        self.navigate()
        self.bottom_frame7.grid(padx=0, pady=0, row=1, column=0)
        
        user_l = ctk.CTkLabel(master=self.bottom_frame7, corner_radius=0, text='Usuario:', font=("Helvetica",  24, 'bold'))
        user_l.place(relx=0.35, rely=0.22, anchor=tk.CENTER)      

        users = tk.Entry(self.bottom_frame7, bg="white", font=("Arial", 12))
        users.place(relx=0.55, rely=0.22, anchor=tk.CENTER,width=300,height=60)


        pass_l = ctk.CTkLabel(master=self.bottom_frame7, corner_radius=0, text='Contraseña:', font=("Helvetica",  24, 'bold'))
        pass_l.place(relx=0.35, rely=0.30, anchor=tk.CENTER)  

        passwf = tk.Entry(self.bottom_frame7, bg="white", font=("Arial", 12))
        passwf.place(relx=0.55, rely=0.33, anchor=tk.CENTER,width=300,height=60)

        def checkLogin():
            usuario = users.get()
            contrasena = passwf.get()

            usuarios = self.getUsuers()

            conte = 0
            for x in usuarios:                
                if usuario == x[2] and contrasena == x[3]:
                    print(x[2],"  ",x[3])
                    self.show_message("Mensaje", "Bienvenido")                    
                    self.navigate()
                    self.chanteStatus()
                    self.view1()

                else:                    
                    conte += 1

            print(len(usuarios))
            print(conte)
            if conte == len(usuarios):
                self.show_message("Mensaje", "Verifique las credenciales por favor")                    


        self.btnLo = ctk.CTkButton(master=self.bottom_frame7, text="Log in", width= 170, height= 50, command=checkLogin, corner_radius=3, fg_color="#404CBB", text_color="white", hover_color="#4554DD", font=("Helvetica",  17, 'bold'))
        self.btnLo.place(relx= 0.5, rely=0.52, anchor=tk.CENTER)
        
        def changeview():
            self.navigate()
            self.viewRe()


        self.btnkm = ctk.CTkButton(master=self.bottom_frame7, text="Registrarse", width= 140, height= 35, command=changeview, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnkm.place(relx= 0.58, rely=0.43, anchor=tk.CENTER)

    def viewRe(self):
        
        self.navigate()
        self.bottom_frame8.grid(padx=0, pady=0, row=1, column=0)

        roles = ['Tutor','Secretari','Jefe de carrera','Encargado CACEI']

        
        name_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Nombre completo:', font=("Helvetica",  24, 'bold'))
        name_label.place(relx=0.35, rely=0.12, anchor=tk.CENTER)      
        
        name = tk.Entry(self.bottom_frame8, bg="white", font=("Arial", 12))
        name.place(relx=0.55, rely=0.12, anchor=tk.CENTER,width=300,height=60)
        
        user_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Usuario:', font=("Helvetica",  24, 'bold'))
        user_label.place(relx=0.35, rely=0.22, anchor=tk.CENTER)      

        user = tk.Entry(self.bottom_frame8, bg="white", font=("Arial", 12))
        user.place(relx=0.55, rely=0.22, anchor=tk.CENTER,width=300,height=60)


        pass_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Contraseña:', font=("Helvetica",  24, 'bold'))
        pass_label.place(relx=0.35, rely=0.30, anchor=tk.CENTER)      

        passw = tk.Entry(self.bottom_frame8, bg="white", font=("Arial", 12))
        passw.place(relx=0.55, rely=0.33, anchor=tk.CENTER,width=300,height=60)

        
        rol_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Rol de usuario:', font=("Helvetica",  24, 'bold'))
        rol_label.place(relx=0.35, rely=0.40, anchor=tk.CENTER)      

        opcion_seleccionada = tk.StringVar()
        lista_desplegable = tk.OptionMenu(self.bottom_frame8, opcion_seleccionada, * roles)    
        lista_desplegable.place(relx=0.55, rely=0.40, anchor=tk.CENTER)
        
        
        def register():
            userd = user.get()
            nombre = name.get()
            pasw = passw.get()            

            print(nombre)
            print(userd)
            print(pasw)
            print(opcion_seleccionada.get())

            self.intertUser(nombre,opcion_seleccionada.get(),userd,pasw)
            
            self.show_message("Mensaje", "Se agrego correctamente el usuario")
            
            name.delete(0, 'end')
            user.delete(0, 'end')
            passw.delete(0, 'end')
            opcion_seleccionada.set("")
            
            def changes():
                self.navigate()
                self.viewL()


            changes()

        self.btnR = ctk.CTkButton(master=self.bottom_frame8, text="Guardar", width= 170, height= 50, command=register, corner_radius=3, fg_color="#404CBB", text_color="white", hover_color="#4554DD", font=("Helvetica",  17, 'bold'))
        self.btnR.place(relx= 0.5, rely=0.52, anchor=tk.CENTER)
           
    def view1(self):
        #inicio
        self.navigate()
        self.bottom_frame.grid(padx=0, pady=0, row=1, column=0)

        info_label = ctk.CTkLabel(master=self.bottom_frame, corner_radius=0, text="Elige un archivo", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.5, rely=0.275, anchor=tk.CENTER)
        self.btn1 = ctk.CTkButton(master=self.bottom_frame, text="Explorar archivos", width= 140, height= 35, command=self.select_file, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btn1.place(relx= 0.5, rely=0.4, anchor=tk.CENTER)
        self.btn2 = ctk.CTkButton(master=self.bottom_frame, text="Guardar", width= 170, height= 50, command=self.get_data, corner_radius=3, fg_color="#404CBB", text_color="white", hover_color="#4554DD", font=("Helvetica",  17, 'bold'))
        self.btn2.place(relx= 0.5, rely=0.525, anchor=tk.CENTER)

    def view2(self):
        #indice reprobados
        self.navigate()
        self.alumnos = []
        self.asignaturas = []
        self.selectData()
        self.selectDataA()
        self.bottom_frame2.grid(padx=0, pady=0, row=1, column=0)
        self.bottom_frame2.grid_propagate(False)

        #Frame Izquierdo (lista de asignaturas)
        frame_left = ctk.CTkFrame(master=self.bottom_frame2, width= 380, height= 500,corner_radius=0, fg_color="transparent")
        frame_left.grid(padx= 36, pady= 35, row=0, column = 0)
        frame_left.grid_propagate(False)

        info_label = ctk.CTkLabel(master=frame_left, corner_radius=0, text="Materia", font=("Helvetica",  20, 'bold'), width= 120)
        info_label.grid(pady = 15, row=0, column = 0)

        frame_leftB = ctk.CTkFrame(master=frame_left, width= 350, height= 420,corner_radius=0, fg_color="transparent")
        frame_leftB.grid(padx= 25, pady= 15, row=1, column = 0)
        frame_leftB.grid_propagate(False)

        button_area = tk.Canvas(frame_leftB, height=500)
        scrollbar = ttk.Scrollbar(frame_leftB, orient="vertical", command=button_area.yview)
        button_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right", padx=0)
        button_area.bind('<Configure>', lambda e: button_area.configure(scrollregion= button_area.bbox('all')))

        frame_right = ctk.CTkFrame(master=self.bottom_frame2, width= 900, height= 500,corner_radius=0, fg_color="transparent")
        frame_right.grid(padx= 36, pady= 35, row=0, column = 1)
        frame_right.grid_propagate(False)

        self.get_asignaturas(frame_leftB, button_area, frame_right, 2)              
    
    def view3(self):
        #expediente
        self.navigate()
        self.alumnos = []
        self.asignaturas = []
        self.selectData()
        self.selectDataA()
        self.bottom_frame3.grid(padx=0, pady=0, row=1, column=0)

        info_label = ctk.CTkLabel(master=self.bottom_frame3, corner_radius=0, text="Expediente", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)

        frame_table = ctk.CTkFrame(master=self.bottom_frame3, width= 1100, height= 385,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
#///////////////////////////////////////////////////////////////////

        num_pairs = 15  # número de pares de columnas "inc" y "repro"
        cols = ["Matricula", "Nombre"]
        self.datas = []
        for i in range(num_pairs):
            cols.append(f"Inc{i+1}")
            self.datas.append(f"Inc{i+1}")
            cols.append(f"Repro{i+1}")
        # tree = ttk.Treeview(frame_table, columns=cols)


        tree = ttk.Treeview(frame_table,height=3,columns=cols) # definir cuantas columnas tendra la tabla
        tree.place(x=10,y=20, width=1500,height=400) # le


        tree.heading("#0", text="ID",anchor="w")        
        tree.heading("Matricula", text="Matricula",anchor="w")
        tree.heading("Nombre", text="Nombre",anchor="w")

        for i in range(num_pairs):
            tree.heading(f"Inc{i+1}", text=f"Inc{i+1}",anchor="w")
            tree.heading(f"Repro{i+1}", text=f"Repro{i+1}",anchor="w")


        style = ttk.Style()
        style.configure("Custom.Treeview", borderwidth=10)

        # aplicar estilo personalizado al Treeview
        tree.configure(style="Custom.Treeview")


        def on_cell_click(event):
            # hacer algo cuando se hace clic en la celda
            row_id = event.widget.focus()
            col_id = event.widget.identify_column(event.x)
            col_title = event.widget.heading(col_id)['text']
            
            
            cell_value = event.widget.item(row_id)['values'][0]

            # valor_celda = treeview.item(3, "values")[1] # "values" se refiere a las columnas de datos
            
            if col_title in self.datas:
                # messagebox.showinfo(title="Celda clickeada", message=f"Clickeaste en la fila {row_id} y columna {col_id} ")
                print(f"Cell clicked: row={row_id}, col={col_id}, heading={col_title}")
                #print(cell_value)
                self.navigate()
                self.view6(cell_value,col_title)

        tree.bind('<ButtonRelease-1>', on_cell_click)


        # para definir la scrollbar vertical
        scroll_databaseV = Scrollbar(frame_table, orient="vertical", command=tree.yview)
        scroll_databaseV.place(x=10, y=20, height=400)
        tree.configure(yscrollcommand=scroll_databaseV.set)

        #para definir la scrollbar hortizontal
        scroll_databaseH = Scrollbar(frame_table, orient="horizontal", command=tree.xview)
        scroll_databaseH.place(x=10, y=350, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)
        k = 1
        for x in self.alumnos:
            tree.insert("", "end", text=k, values=[x[2], x[1]] + [" ", " "]*num_pairs)
            k+=1
                

        style = ttk.Style()
        style.configure("Custom.Treeview", borderwidth=10)

        # aplicar estilo personalizado al Treeview
        tree.configure(style="Custom.Treeview")

    def reco(self):
        #print(self.asignaturas)
        self.selectData()
        
    def editar_celda(event, tabla):
        columna = tabla.identify_column(event.x)
        fila = tabla.identify_row(event.y)
        if columna and fila:
            tabla.edit(fila, columna)

    def view4(self):
        #trayectoria
        self.navigate()
        self.alumnos = []
        self.asignaturas = []
        self.selectData()
        self.selectDataA()

        self.trayectoria = []
        self.selectDataTra()
        
        self.bottom_frame4.grid(padx=0, pady=0, row=1, column=0)

        info_label = ctk.CTkLabel(master=self.bottom_frame4, corner_radius=0, text="Trayectoria", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)

        frame_table = ctk.CTkFrame(master=self.bottom_frame4, width= 1100, height= 405,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        cols = ["Matricula", "Nombre",'gradoestar',"materiasqllevar","materiasaprobadas","materiasrepeticion","nommateriasrepe","cuatrimfalta","materiaqfalta","materiarezagada","nombremateriareza","nommatedeberia","nombrellevaactual"]

    
        tree = ttk.Treeview(frame_table,height=3,columns=cols) # definir cuantas columnas tendra la tabla
        tree.place(x=10,y=20, width=1500,height=400) # le


        tree.heading("#0", text="ID",anchor="w")        
        tree.heading("Matricula", text="Matricula",anchor="w")
        tree.heading("Nombre", text="Nombre",anchor="w")



        
        tree.heading("gradoestar", text="gradoestar",anchor="w")
        tree.heading("materiasqllevar", text="materiasqllevar",anchor="w")
        tree.heading("materiasaprobadas", text="materiasaprobadas",anchor="w")

        tree.heading("materiasrepeticion", text="materiasrepeticion",anchor="w")
        tree.heading("nommateriasrepe", text="nommateriasrepe",anchor="w")
        tree.heading("cuatrimfalta", text="cuatrimfalta",anchor="w")
        # tree.heading("MateriaRz", text="MateriaRz",anchor="w")
        tree.heading("materiaqfalta", text="materiaqfalta",anchor="w")
        tree.heading("materiarezagada", text="materiarezagada",anchor="w")
        tree.heading("nombremateriareza", text="nombremateriareza",anchor="w")
        tree.heading("nommatedeberia", text="nommatedeberia",anchor="w")
        tree.heading("nombrellevaactual", text="nombrellevaactual",anchor="w")


        # tree.heading("gradoestar", text="GradoA",anchor="w")
        # tree.heading("materiasqllevar", text="MateriasLLevar",anchor="w")
        # tree.heading("materiasaprobadas", text="MateriasAprobadas",anchor="w")

        # tree.heading("materiasrepeticion", text="MateriasRepeticion",anchor="w")
        # tree.heading("nommateriasrepe", text="NombreMateriasRepe",anchor="w")
        # tree.heading("cuatrimfalta", text="CuatriFaltante",anchor="w")
        # # tree.heading("MateriaRz", text="MateriaRz",anchor="w")
        # tree.heading("materiaqfalta", text="MateriasFaltanes",anchor="w")
        # tree.heading("materiarezagada", text="MateriaRezagada",anchor="w")
        # tree.heading("nombremateriareza", text="NombreMateriaRezagada",anchor="w")
        # tree.heading("nommatedeberia", text="MateriasDeberia",anchor="w")
        # tree.heading("nombrellevaactual", text="MateriasLleva",anchor="w")

        # tree.heading("MateriasCuatri", text="MateriasCuatri",anchor="w")
                               
        # para definir la scrollbar vertical
        scroll_databaseV = Scrollbar(frame_table, orient="vertical", command=tree.yview)
        scroll_databaseV.place(x=10, y=20, height=400)
        tree.configure(yscrollcommand=scroll_databaseV.set)

        #para definir la scrollbar hortizontal
        scroll_databaseH = Scrollbar(frame_table, orient="horizontal", command=tree.xview)
        scroll_databaseH.place(x=10, y=350, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)

       
        def on_cell_click(event):
            # hacer algo cuando se hace clic en la celda
            
            
            row_id = event.widget.focus()
            col_id = event.widget.identify_column(event.x)
            col_title = event.widget.heading(col_id)['text']
            matricula = event.widget.item(row_id)['values'][0]

            # print(column_id)
            cell_value = event.widget.item(row_id)['values'][int(col_id[1:])-1]
                     
            # print(matricula)
            # messagebox.showinfo(title="Celda clickeada", message=f"Clickeaste en la fila {row_id} y columna {col_id} ")                        
            # print(cell_value)              
            a = ""
            # print(col_title)
            newca = ""
            if isinstance(cell_value, int) == False:
                # for x in cell_value: 
                #     if x == ',':
                #         print(a)
                #         newca =+ " " + str(a) + " "
                #         a = ""                   
                #     if x != "'" and x != "[" and x != "]"and x != " ":
                #         print(a)
                #         a += x               
                palabras = re.findall(r"'(\w+)'", cell_value)
                

                # print(palabras)
                if col_title != 'Nombre' and col_title != 'Matricula':
                    new_value = simpledialog.askstring("Editar celda", f"Ingrese un nuevo valor para la celda:", initialvalue=palabras)                           
                    
                    if col_title != "nombremateriareza":
                        a = new_value.split(" ")         
                        print(a)        
                      
                        print(matricula)
                        print(col_title)

                        self.updateTrayectoria(col_title,a,matricula)
                    else:
                        self.updateTrayectoria(col_title,new_value,matricula)

                    self.navigate()
                    self.view4()
                else:
                    self.show_message("Mensaje", "Celda no editable") 
            else:

                if col_title != 'Nombre' and col_title != 'Matricula':
                    new_value = simpledialog.askstring("Editar celda", f"Ingrese un nuevo valor para la celda:", initialvalue=cell_value)
                    
                    print(new_value)
                    print(matricula)
                    print(col_title)

                    self.updateTrayectoria(col_title,int (new_value),matricula)
                    self.navigate()
                    self.view4()
                else:
                    self.show_message("Mensaje", "Celda no editable") 
                

        tree.bind('<ButtonRelease-1>', on_cell_click)
                             

        l = 1
        for x in self.alumnos:
                    
            for d in self.trayectoria:
                if d[-1] == x[2]:                                        
                    tree.insert("", "end", text=l, values=[x[2], x[1], d[0], d[1], d[2], d[3], str(d[4]), d[5], d[6], d[7], d[8], d[9], d[10]])                    
            l+=1
        
        tree.bind('<ButtonRelease-1>', on_cell_click)        
            
    def view5(self):
        #reprobados
        self.alumnos = []
        self.asignaturas = []
        self.selectData()
        self.selectDataA()
        self.navigate()

        

        self.bottom_frame5.grid(padx=0, pady=0, row=1, column=0)

        frame_left = ctk.CTkFrame(master=self.bottom_frame5, width= 350, height= 500,corner_radius=0, fg_color="transparent")
        frame_left.grid(padx= 36, pady= 35, row=0, column = 0)
        frame_left.grid_propagate(False)


        info_label = ctk.CTkLabel(master=frame_left, corner_radius=0, text="Reprobados", font=("Helvetica",  20, 'bold'))
        info_label.grid(padx = 15, pady = 10, row=0, column = 0)

        frame_leftB = ctk.CTkFrame(master=frame_left, width= 350, height= 450,corner_radius=0, fg_color="white")
        frame_leftB.grid(padx= 25, pady= 15, row=1, column = 0)
        frame_leftB.grid_propagate(False)

        button_area = tk.Canvas(frame_leftB, height=500)
        scrollbar = ttk.Scrollbar(frame_leftB, orient="vertical", command=button_area.yview)
        button_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right", padx=0)
        button_area.bind('<Configure>', lambda e: button_area.configure(scrollregion= button_area.bbox('all')))


        frame_right = ctk.CTkFrame(master=self.bottom_frame5, width= 900, height= 500,corner_radius=0, fg_color="transparent")
        frame_right.grid(padx= 36, pady= 35, row=0, column = 1)
        

        self.get_asignaturas(frame_leftB, button_area, frame_right, 5)

    def veri(self):
        
        for x in self.asignaturas:
            print(x)

    def view6(self,matricula,titulo):
        self.bottom_frame6.grid(padx=0, pady=0, row=1, column=0)

        cont = 0
        for x in self.datas:
            if x == titulo:
                cont += 1;
                break;
            else:
                cont += 1;
        incidencias = []
        print(cont)
        alumno = self.getByMatricula(matricula)
        print(alumno)       
        incidencias = self.getIncidencias(matricula,cont)
        print(incidencias)
        frame_table1 = ctk.CTkFrame(master=self.bottom_frame6, width= 1100, height= 385,corner_radius=0)        
        frame_table2 = ctk.CTkFrame(master=self.bottom_frame6, width= 1100, height= 385,corner_radius=0)
        
        
        def navigate2():
            frame_table1.grid_remove()
            frame_table2.grid_remove()          
        
        def viewE():
            navigate2()
            
            frame_table1.grid(padx=0.2, pady=0.1, row=1, column=0)
            info_label = ctk.CTkLabel(master=frame_table1, corner_radius=0, text='Agregar', font=("Helvetica",  24, 'bold'))
            info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)      
            
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
                b.delete(0, 'end')                           
                if incidencias == []:
                    incidencias.append(str(src_file))
                    self.createInci(matricula,cont,incidencias)
                else:
                    a = []
                    for x in incidencias[0]:
                        a.append(x)                                   
                        
                    a.append(str(src_file)+"")                    
                    print(src_file)
                    self.updateInci(matricula,cont,a)                

            # Crear etiquetas y cuadros de texto
            a = tk.Label(frame_table1, text="Archivo:")
            file_path = tk.StringVar()
            b = tk.Entry(frame_table1, textvariable=file_path)
            c = tk.Button(frame_table1, text="Seleccionar archivo", command=browse_file)
            d = tk.Button(frame_table1, text="Subir archivo", command=upload_file)            
            uploaded_file_name_var = tk.StringVar()
            uploaded_file_path_var = tk.StringVar() #path 
                        
            a.place(relx=0.35, rely=0.42, anchor=tk.CENTER,width=130,height=60)
            b.place(relx=0.54, rely=0.42, anchor=tk.CENTER,width=300,height=60)
            c.place(relx=0.45, rely=0.60, anchor=tk.CENTER,width=130,height=60)
            d.place(relx=0.60, rely=0.60, anchor=tk.CENTER,width=130,height=60)                                                        

        def viewR():
            navigate2()
            incidencias = self.getIncidencias(matricula,cont)
            frame_table2.grid(padx=0.2, pady=0.1, row=1, column=0)
            info_label = ctk.CTkLabel(master=frame_table2, corner_radius=0, text='Revisar', font=("Helvetica",  24, 'bold'))
            info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)
            nfo_label = ctk.CTkLabel(master=frame_table2, corner_radius=0, text='No existen incidencias', font=("Helvetica",  24, 'bold'))
            
            if incidencias != []:                                              
                x = 0.30
                i = 0.10
                for x in incidencias[0]:

                    def descargar_archivo(ruta):
                        # Obtener la ruta de destino del usuario
                        destino = filedialog.asksaveasfilename(defaultextension='.pdf')
                        if destino:
                            # Copiar el archivo en la ruta de destino
                            try:
                                shutil.copyfile(ruta, destino)
                                print(f"Archivo guardado en: {destino}")
                            except Exception as e:
                                print(f"Ha ocurrido un error al guardar el archivo: {e}")
                        else:
                            print("La selección de destino ha sido cancelada por el usuario.")

                    
                    boton = tk.Button(frame_table2, text=x.split('/')[-1], command=lambda ruta=x: descargar_archivo(ruta))
                    boton.place(relx=i, rely=0.50, anchor=tk.CENTER)  
                    i+=0.10


        self.btnk1 = ctk.CTkButton(master=self.bottom_frame6, text="Revisar", width= 140, height= 35, command=viewR, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnk1.place(relx= 0.4, rely=0.1, anchor=tk.CENTER)

        self.btnk2 = ctk.CTkButton(master=self.bottom_frame6, text="Agregar", width= 140, height= 35, command=viewE, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnk2.place(relx= 0.6, rely=0.1, anchor=tk.CENTER)
                   
    def getByMatricula(self,matricula):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()        
        # Ejecuta una consulta SQL
        cursor.execute(f"SELECT * FROM alumnos WHERE matricula={matricula}" )

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        # print(results)
        
        cursor.close()
        conn.close()

        return results
    
    def createInci(self,matricula,cuatri,datas):
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        sql = "INSERT INTO incidencias (matriculaalumno, uplo,cuatri) VALUES (%s, %s, %s)"

        valores = (matricula, datas,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()
    
    def updateInci(self,matricula,cuatri,datas):
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        
        sql = "UPDATE incidencias SET uplo = %s WHERE matriculaalumno = %s and cuatri = %s;"

        valores = (datas,matricula,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

    def getIncidencias(self,matricula,cuatri):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()        
        cursor.execute(f"SELECT uplo FROM incidencias WHERE matriculaalumno={matricula} and cuatri={cuatri}" )

        a = []
        results = cursor.fetchall()
        if results != []:
                # print(results[0][0])
                a.append(results[0][0])
                # for x in a :
                #       print(x)
        else:
              print('sin insidencias')    
    
        cursor.close()
        conn.close()
        return a
    
    def get_asignaturas(self, frame_leftB, button_area, frame_right, view):  
        if self.asignaturas:
            button_area.pack(side=tk.LEFT, fill="both", expand="yes", padx=0)
            myframe = tk.Frame(button_area, height=450)
            button_area.create_window((0,0), window=myframe, anchor="nw")

            if view == 2:
                for m in self.asignaturas:
                    b = ctk.CTkButton(master=myframe, text=f"{m}", width= 260, height= 35, command = lambda m=m: self.get_grafica(m, frame_right), corner_radius=2, fg_color="#E5E5E5", text_color="black", hover_color="#DDDEDF", font=("Helvetica",  14))
                    b.pack(padx=10, pady=10, fill=tk.X)
            elif view == 5:
                for m in self.asignaturas:
                    b = ctk.CTkButton(master=myframe, text=f"{m}", width= 260, height= 35, command = lambda m=m : self.update_reprobados(m, frame_right), corner_radius=2, fg_color="#E5E5E5", text_color="black", hover_color="#DDDEDF", font=("Helvetica",  14))
                    b.pack(padx=10, pady=10, fill=tk.X)
                         
        else:
            label_data = ctk.CTkLabel(master=frame_leftB, corner_radius=0, text="No se han guardado asignaturas", font=("Helvetica",  16), width= 300, height=30, bg_color="transparent")
            label_data.pack(side=tk.TOP, pady= 50)

            label_data2 = ctk.CTkLabel(master=frame_right, corner_radius=0, text="No se han guardado datos", font=("Helvetica",  18), bg_color="transparent")
            label_data2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def get_grafica(self, asignatura, frame_right):
        print(asignatura)
        periodos = []
        reprobados = []

        for a in self.alumnos:
            if a[3] == asignatura:
                if a[4] not in periodos:
                    periodos.append(a[4])
                    r = 0
                    for b in self.alumnos:
                        if a[4] == b[4] and b[3] == asignatura:
                            r += 1
                    reprobados.append(r)

        self.graficar(periodos, reprobados, frame_right, asignatura)

    def graficar(self, periodos, reprobados, frame_right, asignatura):
        global canvas
        try:
            canvas.get_tk_widget().destroy()
        except:
            pass

        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.plot(periodos, reprobados, 'bo-')
        ax.set_title(asignatura, loc='center')
        canvas = FigureCanvasTkAgg(figure, master=frame_right)
        canvas.get_tk_widget().pack(fill=tk.X, anchor=tk.CENTER)
        canvas.draw()

    def update_reprobados(self, asignatura, frame_right):
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 14), rowheight=25) 
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 18,'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 

        try:
            self.tablaR.destroy()
        except AttributeError:
            pass

        self.tablaR = ttk.Treeview(frame_right, style="mystyle.Treeview", columns=("col1", "col2"))

        self.tablaR.column("#0", width=160)
        self.tablaR.column("col1", width=300, anchor="center")
        self.tablaR.column("col2", width=340, anchor="center")

        self.tablaR.heading("#0", text="Matricula", anchor="center")
        self.tablaR.heading("col1", text="Nombre", anchor="center")
        self.tablaR.heading("col2", text="Periodo Reprobado", anchor="center")
        
        for a in self.alumnos:
            if str (a[3]) == asignatura:
                self.tablaR.insert("", tk.END, text=f"{a[2]}", values=(a[1], a[4]))
                    

        self.tablaR.configure(height=24)
        self.tablaR.pack(fill="both", expand=True, side=tk.TOP, pady=15, padx=5, anchor=tk.CENTER)

    def test_tabla1(self, frame_table):
        tree = ttk.Treeview(frame_table)
        tree["columns"]=("nombre", "edad")
        tree.column("nombre", width=100)
        tree.column("edad", width=50)
        tree.heading("nombre", text="Nombre")
        tree.heading("edad", text="Edad")
        tree.insert("", "end", values=("Juan", "25"))
        tree.place(relx=0.5, rely= 0.5)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
    def selectData(self):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        # Ejecuta una consulta SQL
        cursor.execute("SELECT * FROM alumnos")

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        #print(results)

        for x in results:
            # print(x)
            self.alumnos.append(x)
        #for x in results:
         #   print(x[3])
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()

    def selectDataA(self):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia",
            client_encoding='utf8'

        )
        cursor = conn.cursor()

        # Ejecuta una consulta SQL
        cursor.execute("SELECT * FROM materias")

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        #print(results)
        # for x in results:
        #     print(str(x))
            #self.asignaturas.append(x)

        nombres_columnas = [desc[0] for desc in cursor.description]


        lista_resultados = []
        for resultado in results:
            diccionario_resultado = {}
            for indice, nombre_columna in enumerate(nombres_columnas):
                diccionario_resultado[nombre_columna] = resultado[indice]
                # print(resultado[indice])
                self.asignaturas.append(resultado[indice])
            lista_resultados.append(diccionario_resultado)       


        cursor.close()
        conn.close()

    def conectar(self):

        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        # Ejecuta una consulta SQL
        cursor.execute("SELECT * FROM alumnos")

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        print(results)

        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()

    def getUsuers(self):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        
        results = cursor.fetchall()
        # print(results)
            
        cursor.close()
        conn.close()

        return results
    
    def intertUser(self,nombre,tipo,usuario,passw):
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        sql = "INSERT INTO users (nombre, tipo,usuario,passw) VALUES (%s, %s, %s, %s)"
                
        valores = (nombre,tipo,usuario,passw)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

    def selectDataTra(self):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM trayectoria")
        
        results = cursor.fetchall()

        for x in results:                
            self.trayectoria.append(x)            
            
        cursor.close()
        conn.close()

        return results
           
    def updateTrayectoria(self,campo,dato,matricula):
                conn = psycopg2.connect(
                        user="postgres",
                        password="carrera10",
                        host="localhost",
                        port="5432",   
                        database="estancia"
                    )
                cursor = conn.cursor()                        
                                 
                valores = (dato,matricula)                                
                sql = "UPDATE trayectoria SET {} = %s WHERE matriculaalumno = %s".format(campo)
                cursor.execute(sql, valores)

                conn.commit()

                cursor.close()
                conn.close()
