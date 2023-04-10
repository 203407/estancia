import os
import shutil
import sys
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
from decouple import config 

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

        self.nombre_archivo = "datos.txt"

        # Verificar si el archivo existe
        if os.path.exists(self.nombre_archivo):
            print("El archivo ya existe.")
        else:            
            self.archivo = open(self.nombre_archivo, "w")
            self.archivo.close()
            print("El archivo ha sido creado.")       

        self.fechas = {

            "183": {"SEPTIEMBRE-DICIEMBRE 2018":1,"ENERO-ABRIL 2019":2,"MAYO-AGOSTO 2019":3,"SEPTIEMBRE-DICIEMBRE 2019":4,"ENERO-ABRIL 2020":5,"MAYO-AGOSTO 2020":6,"SEPTIEMBRE-DICIEMBRE 2020":7,"ENERO-ABRIL 2021":8,"MAYO-AGOSTO 2021":9,"SEPTIEMBRE-DICIEMBRE 2021":10,"ENERO-ABRIL 2022":11,"MAYO-AGOSTO 2022":12,"SEPTIEMBRE-DICIEMBRE 2022":13,"ENERO-ABRIL 2023":14,"MAYO-AGOSTO 2023":15},

            "191": {"ENERO-ABRIL 2019":1,"MAYO-AGOSTO 2019":2,"SEPTIEMBRE-DICIEMBRE 2019":3,"ENERO-ABRIL 2020":4,"MAYO-AGOSTO 2020":5,"SEPTIEMBRE-DICIEMBRE 2020":6,"ENERO-ABRIL 2021":7,"MAYO-AGOSTO 2021":8,"SEPTIEMBRE-DICIEMBRE 2021":9,"ENERO-ABRIL 2022":10,"MAYO-AGOSTO 2022":11,"SEPTIEMBRE-DICIEMBRE 2022":12,"ENERO-ABRIL 2023":13,"MAYO-AGOSTO 2023":14,"SEPTIEMBRE-DICIEMBRE 2023":15},

            "193": {"ENERO-ABRIL 2023":11,"MAYO-AGOSTO 2023":12,"SEPTIEMBRE-DICIEMBRE 2023":13,"ENERO-ABRIL 2024":14,"MAYO-AGOSTO 2024":15},

            "201": {"ENERO-ABRIL 2023":10,"MAYO-AGOSTO 2023":11,"SEPTIEMBRE-DICIEMBRE 2023":12,"ENERO-ABRIL 2024":13,"MAYO-AGOSTO 2024":14,"SEPTIEMBRE-DICIEMBRE 2024":15},

            "203": {"ENERO-ABRIL 2023":8,"MAYO-AGOSTO 2023":9,"SEPTIEMBRE-DICIEMBRE 2023":10,"ENERO-ABRIL 2024":11,"MAYO-AGOSTO 2024":12,"SEPTIEMBRE-DICIEMBRE 2024":13,"ENERO-ABRIL 2025":14,"MAYO-AGOSTO 2025":15},

            "211": {"ENERO-ABRIL 2023":7,"MAYO-AGOSTO 2023":8,"SEPTIEMBRE-DICIEMBRE 2023":9,"ENERO-ABRIL 2024":10,"MAYO-AGOSTO 2024":11,"SEPTIEMBRE-DICIEMBRE 2024":12,"ENERO-ABRIL 2025":13,"MAYO-AGOSTO 2025":14,"SEPTIEMBRE-DICIEMBRE 2025":15},

            "213": {"ENERO-ABRIL 2023":5,"MAYO-AGOSTO 2023":6,"SEPTIEMBRE-DICIEMBRE 2023":7,"ENERO-ABRIL 2024":8,"MAYO-AGOSTO 2024":9,"SEPTIEMBRE-DICIEMBRE 2024":10,"ENERO-ABRIL 2025":11,"MAYO-AGOSTO 2025":12,"SEPTIEMBRE-DICIEMBRE 2025":13,"ENERO-ABRIL 2026":14,"MAYO-AGOSTO 2026":15},

            "221": {"ENERO-ABRIL 2023":4,"MAYO-AGOSTO 2023":5,"SEPTIEMBRE-DICIEMBRE 2023":6,"ENERO-ABRIL 2024":7,"MAYO-AGOSTO 2024":8,"SEPTIEMBRE-DICIEMBRE 2024":9,"ENERO-ABRIL 2025":10,"MAYO-AGOSTO 2025":11,"SEPTIEMBRE-DICIEMBRE 2025":12,"ENERO-ABRIL 2026":13,"MAYO-AGOSTO 2026":14,"SEPTIEMBRE-DICIEMBRE 2026":15},

            "223": {"ENERO-ABRIL 2023":2,"MAYO-AGOSTO 2023":3,"SEPTIEMBRE-DICIEMBRE 2023":4,"ENERO-ABRIL 2024":5,"MAYO-AGOSTO 2024":6,"SEPTIEMBRE-DICIEMBRE 2024":7,"ENERO-ABRIL 2025":8,"MAYO-AGOSTO 2025":9,"SEPTIEMBRE-DICIEMBRE 2025":10,"ENERO-ABRIL 2026":11,"MAYO-AGOSTO 2026":12,"SEPTIEMBRE-DICIEMBRE 2026":13,"ENERO-ABRIL 2027":14,"MAYO-AGOSTO 2027":15},

            "231": {"ENERO-ABRIL 2023":1,"MAYO-AGOSTO 2023":2,"SEPTIEMBRE-DICIEMBRE 2023":3,"ENERO-ABRIL 2024":4,"MAYO-AGOSTO 2024":5,"SEPTIEMBRE-DICIEMBRE 2024":6,"ENERO-ABRIL 2025":7,"MAYO-AGOSTO 2025":8,"SEPTIEMBRE-DICIEMBRE 2025":9,"ENERO-ABRIL 2026":10,"MAYO-AGOSTO 2026":11,"SEPTIEMBRE-DICIEMBRE 2026":12,"ENERO-ABRIL 2027":13,"MAYO-AGOSTO 2027":14,"SEPTIEMBRE-DICIEMBRE 2027":15},

        }

        self.periodosAca = {

            "183": ["SEPTIEMBRE-DICIEMBRE 2018","ENERO-ABRIL 2019","MAYO-AGOSTO 2019","SEPTIEMBRE-DICIEMBRE 2019","ENERO-ABRIL 2020","MAYO-AGOSTO 2020","SEPTIEMBRE-DICIEMBRE 2020","ENERO-ABRIL 2021","MAYO-AGOSTO 2021","SEPTIEMBRE-DICIEMBRE 2021","ENERO-ABRIL 2022","MAYO-AGOSTO 2022","SEPTIEMBRE-DICIEMBRE 2022","ENERO-ABRIL 2023","MAYO-AGOSTO 2023"],

            "191": ["ENERO-ABRIL 2019","MAYO-AGOSTO 2019","SEPTIEMBRE-DICIEMBRE 2019","ENERO-ABRIL 2020","MAYO-AGOSTO 2020","SEPTIEMBRE-DICIEMBRE 2020","ENERO-ABRIL 2021","MAYO-AGOSTO 2021","SEPTIEMBRE-DICIEMBRE 2021","ENERO-ABRIL 2022","MAYO-AGOSTO 2022","SEPTIEMBRE-DICIEMBRE 2022","ENERO-ABRIL 2023","MAYO-AGOSTO 2023","SEPTIEMBRE-DICIEMBRE 2023"],        
        
        }
     
        self.inicios = {
            "181":"ENERO-ABRIL 2018",

            "183":"SEPTIEMBRE-DICIEMBRE 2018",

            "191":"ENERO-ABRIL 2019",

            "193":"SEPTIEMBRE-DICIEMBRE 2019",

            "201":"ENERO-ABRIL 2020",

            "203":"SEPTIEMBRE-DICIEMBRE 2020",

            "211":"ENERO-ABRIL 2021",

            "213":"SEPTIEMBRE-DICIEMBRE 2021",

            "221":"ENERO-ABRIL 2022",

            "223":"SEPTIEMBRE-DICIEMBRE 2022",

            "231":"ENERO-ABRIL 2023",

            "233":"SEPTIEMBRE-DICIEMBRE 2023",

            "241":"ENERO-ABRIL 2024",
        }
        
        # print(self.inicios)
        # print("aquiiiiiiiiiiiii")
        # print(self.fechas["183"]["ENERO-ABRIL 2021"])
        # print(fechas["231"])

        hanbi = False
        self.usuariodb = ""
        self.passdb = ""
        self.portdb = ""
        self.namedb = ""

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
        self.bottom_frame9 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame10 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame20 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame21 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame22 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")

        #Barra de navegación superior
        self.top_frame.grid(padx=0, pady=0, row=0, column=0)
        fotico = self.resource_path('logo.png')

        #Logo y titulo (Barra de navegación superior)
        # logo = ctk.CTkImage(light_image=Image.open(fotico), dark_image=Image.open(fotico), size=(105,105))
        # logo_label = ctk.CTkLabel(master=self.top_frame, corner_radius=0, image=logo, text="")
        # logo_label.place(relx=0.340, rely=0.5, anchor=tk.CENTER)
        title_label = ctk.CTkLabel(master=self.top_frame, corner_radius=0, text="Programa indicadores CACEI", font=("Helvetica",  28, 'bold'))
        title_label.place(relx=0.540, rely=0.375, anchor=tk.CENTER)

        #Botones de navegación de páginas
        self.nav_btn_1 = ctk.CTkButton(master=self.top_frame, text="Inicio", width=35 , command = self.view1, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_1.place(relx=0.415, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_2 = ctk.CTkButton(master=self.top_frame, text="Índice reprobados", width=65 , command=self.view2, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_2.place(relx=0.474, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_3 = ctk.CTkButton(master=self.top_frame, text="Expediente", width=40 , command=self.view3, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_3.place(relx=0.543, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_4 = ctk.CTkButton(master=self.top_frame, text="TrayectoriaI", width=40 , command=self.view4, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_4.place(relx=0.600, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_7 = ctk.CTkButton(master=self.top_frame, text="TrayectoriaG", width=40 , command=self.viewTrayeG, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_7.place(relx=0.657, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_5 = ctk.CTkButton(master=self.top_frame, text="Reprobados", width=40 , command=self.view5, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_5.place(relx=0.710, rely=0.625, anchor=tk.CENTER)
        self.nav_btn_6 = ctk.CTkButton(master=self.top_frame, text="Cerrar", width=40 ,command=self.logout, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5",state="disabled")
        self.nav_btn_6.place(relx=0.770, rely=0.625, anchor=tk.CENTER)        

        # self.view1()
        self.viewL()
    
    def resource_path(self,relative_path):
        # """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def chanteStatus(self):
        self.nav_btn_1.configure(state="normal")
        self.nav_btn_2.configure(state="normal")
        self.nav_btn_3.configure(state="normal")
        self.nav_btn_4.configure(state="normal")
        self.nav_btn_5.configure(state="normal")
        self.nav_btn_6.configure(state="normal")        
        self.nav_btn_7.configure(state="normal") 

    def changedagain(self):
        self.nav_btn_1.configure(state="disabled")
        self.nav_btn_2.configure(state="disabled")
        self.nav_btn_3.configure(state="disabled")
        self.nav_btn_4.configure(state="disabled")
        self.nav_btn_5.configure(state="disabled")
        self.nav_btn_6.configure(state="disabled")        
        self.nav_btn_7.configure(state="disabled") 

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
        self.bottom_frame9.grid_remove()         
        self.bottom_frame10.grid_remove()         
        self.bottom_frame20.grid_remove()       
        self.bottom_frame21.grid_remove()  
        self.bottom_frame22.grid_remove()  
        
    def show_message(self, title, msj):
        messagebox.showinfo(message=msj, title=title)
    
    def viewL(self):
        self.navigate()
        self.bottom_frame7.grid(padx=0, pady=0, row=1, column=0)
        
        def actualizarData():
            
            nombre_archivo = "datos.txt"
            tamanio = os.path.getsize(nombre_archivo)
            if tamanio == 0:
                print("El archivo está vacío.")
                self.show_message("Mensaje", "No existe la configuracion")                    
            else:                
                self.archivo = open("datos.txt", "r")            
                lineas = self.archivo.readlines()
                
                self.archivo.close()            
                datos = []                                
                for linea in lineas:                
                    linea = linea.rstrip("\n")                
                    datos.append(linea)
                
                # print(datos[0])
                self.usuariodb= datos[0]
                # print(datos[1])
                self.passdb = datos[1]
                # print(datos[2])
                self.portdb = datos[2]

                self.namedb = datos[3]
                print(self.namedb)

        user_l = ctk.CTkLabel(master=self.bottom_frame7, corner_radius=0, text='Usuario:', font=("Helvetica",  24, 'bold'))
        user_l.place(relx=0.38, rely=0.22, anchor=tk.CENTER)      

        users = ctk.CTkEntry(self.bottom_frame7,  font=("Arial", 12),corner_radius=10,border_width=2)
        users.place(relx=0.55, rely=0.22, anchor=tk.CENTER,width=300,height=60)


        pass_l = ctk.CTkLabel(master=self.bottom_frame7, corner_radius=0, text='Contraseña:', font=("Helvetica",  24, 'bold'))
        pass_l.place(relx=0.38, rely=0.33, anchor=tk.CENTER)  

        passwf = ctk.CTkEntry(self.bottom_frame7,  font=("Arial", 12),corner_radius=10,border_width=2,show='*')
        passwf.place(relx=0.55, rely=0.33, anchor=tk.CENTER,width=300,height=60)
       
        
        def checkLogin():

            actualizarData()
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
        
        self.btnkm = ctk.CTkButton(master=self.bottom_frame7, text="configuracion", width= 140, height= 35, command=self.config, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnkm.place(relx= 0.90, rely=0.05, anchor=tk.CENTER)
    
    def config(self):
        self.navigate()
        self.bottom_frame22.grid(padx=0, pady=0, row=1, column=0)

        def back():            
            self.viewL()
    
        self.btnkm = ctk.CTkButton(master=self.bottom_frame22, text="Regresar", width= 140, height= 35, command=back, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnkm.place(relx= 0.90, rely=0.05, anchor=tk.CENTER)

        def saveData():

            nombre_archivo = "datos.txt"            
            archivo = open(nombre_archivo, "w")            
            archivo.truncate()            
            archivo.close()

            self.archivo = open("datos.txt", "a")
            usuario = userc.get()
            contra = passc.get()
            port = puertoc.get()
            names = namec.get()

            # Escribir datos en el archivo
            self.archivo.write(f'{usuario}\n')
            self.archivo.write(f'{contra}\n')
            self.archivo.write(f'{port}\n')
            self.archivo.write(f'{names}\n')
            self.archivo.close()
            self.show_message("Mensaje", "Actualizado correctamente")     

        userk = ctk.CTkLabel(master=self.bottom_frame22, corner_radius=0, text='Usuario db:', font=("Helvetica",  24, 'bold'))
        userk.place(relx=0.38, rely=0.22, anchor=tk.CENTER)      

        userc = ctk.CTkEntry(self.bottom_frame22,  font=("Arial", 12),corner_radius=10,border_width=2)
        userc.place(relx=0.55, rely=0.22, anchor=tk.CENTER,width=300,height=60)

        passk = ctk.CTkLabel(master=self.bottom_frame22, corner_radius=0, text='Password db:', font=("Helvetica",  24, 'bold'))
        passk.place(relx=0.38, rely=0.35, anchor=tk.CENTER)      

        passc = ctk.CTkEntry(self.bottom_frame22,  font=("Arial", 12),corner_radius=10,border_width=2)
        passc.place(relx=0.55, rely=0.35, anchor=tk.CENTER,width=300,height=60)

        puerto = ctk.CTkLabel(master=self.bottom_frame22, corner_radius=0, text='Puerto db:', font=("Helvetica",  24, 'bold'))
        puerto.place(relx=0.38, rely=0.47, anchor=tk.CENTER)      

        puertoc = ctk.CTkEntry(self.bottom_frame22,  font=("Arial", 12),corner_radius=10,border_width=2)
        puertoc.place(relx=0.55, rely=0.47, anchor=tk.CENTER,width=300,height=60)
        
        name = ctk.CTkLabel(master=self.bottom_frame22, corner_radius=0, text='Nombre db:', font=("Helvetica",  24, 'bold'))
        name.place(relx=0.38, rely=0.59, anchor=tk.CENTER)      

        namec = ctk.CTkEntry(self.bottom_frame22,  font=("Arial", 12),corner_radius=10,border_width=2)
        namec.place(relx=0.55, rely=0.59, anchor=tk.CENTER,width=300,height=60)

        btns = ctk.CTkButton(master=self.bottom_frame22, text="Guardar", width= 170, height= 50, command=saveData, corner_radius=3, fg_color="#404CBB", text_color="white", hover_color="#4554DD", font=("Helvetica",  17, 'bold'))
        btns.place(relx= 0.5, rely=0.78, anchor=tk.CENTER)

    def viewRe(self):
        
        self.navigate()
        self.bottom_frame8.grid(padx=0, pady=0, row=1, column=0)
        self.rol=None
        roles = ['Tutor','Secretari','Jefe de carrera','Encargado CACEI']

        
        name_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=10, text='Nombre completo:', font=("Helvetica",  24, 'bold'))
        name_label.place(relx=0.35, rely=0.12, anchor=tk.CENTER)      
        
        name = ctk.CTkEntry(self.bottom_frame8,corner_radius=10,border_width=2)
        name.place(relx=0.55, rely=0.12, anchor=tk.CENTER,width=300,height=60)
        
        user_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Usuario:', font=("Helvetica",  24, 'bold'))
        user_label.place(relx=0.35, rely=0.22, anchor=tk.CENTER)      

        user = ctk.CTkEntry(self.bottom_frame8,corner_radius=10,border_width=2 )
        user.place(relx=0.55, rely=0.22, anchor=tk.CENTER,width=300,height=60)


        pass_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Contraseña:', font=("Helvetica",  24, 'bold'))
        pass_label.place(relx=0.35, rely=0.30, anchor=tk.CENTER)      

        passw = ctk.CTkEntry(self.bottom_frame8,corner_radius=10,border_width=2)
        passw.place(relx=0.55, rely=0.33, anchor=tk.CENTER,width=300,height=60)

        
        rol_label = ctk.CTkLabel(master=self.bottom_frame8, corner_radius=0, text='Rol de usuario:', font=("Helvetica",  24, 'bold'))
        rol_label.place(relx=0.35, rely=0.45, anchor=tk.CENTER)      

        def back():            
            self.viewL()
    
        self.btnkm = ctk.CTkButton(master=self.bottom_frame8, text="Regresar", width= 140, height= 35, command=back, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnkm.place(relx= 0.90, rely=0.05, anchor=tk.CENTER)

        # opcion_seleccionada = tk.StringVar()
        # lista_desplegable = tk.OptionMenu(self.bottom_frame8, opcion_seleccionada, * roles)    
        # lista_desplegable.place(relx=0.55, rely=0.40, anchor=tk.CENTER)
        

        def optionmenu_callback(choice):
            print("optionmenu dropdown clicked:", choice)
            self.rol=choice

        combobox = ctk.CTkOptionMenu(master=self.bottom_frame8,
                                            values=roles,
                                            command=optionmenu_callback)
        
        combobox.place(relx=0.55, rely=0.45, anchor=tk.CENTER,width=300,height=60)

        
        def register():
            print(self.rol)
            userd = user.get()
            nombre = name.get()
            pasw = passw.get()            

            print(nombre)
            print(userd)
            print(pasw)
            # print(opcion_seleccionada.get())

            self.intertUser(nombre,self.rol,userd,pasw)
            
            self.show_message("Mensaje", "Se agrego correctamente el usuario")
            
            name.delete(0, 'end')
            user.delete(0, 'end')
            passw.delete(0, 'end')            
            # opcion_seleccionada.set("")
            
            def changes():
                self.navigate()
                self.viewL()


            changes()

        self.btnR = ctk.CTkButton(master=self.bottom_frame8, text="Guardar", width= 170, height= 50, command=register, corner_radius=3, fg_color="#404CBB", text_color="white", hover_color="#4554DD", font=("Helvetica",  17, 'bold'))
        self.btnR.place(relx= 0.5, rely=0.62, anchor=tk.CENTER)
           
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

        look = tk.Entry(self.bottom_frame3, bg="white", font=("Arial", 12))
        look.place(relx=0.71, rely=0.12, anchor=tk.CENTER,width=300,height=40)
       

        def getDataForLook():
            matrix = look.get()

            if matrix != "" and matrix != " ":
                if  matrix.isdigit() == True:
                                        
                    self.viewLook(matrix)
                else:
                    self.show_message("Mensaje", "Solo se aceptan numeros")                        
            else:
                self.show_message("Mensaje", "Campo vacio")                    
                        
        # print(self.alumnos[0])

        send = tk.Button(self.bottom_frame3, text="Buscar", command=getDataForLook)            
        send.place(relx=0.85, rely=0.12, anchor=tk.CENTER,width=130,height=40)


        frame_table = ctk.CTkFrame(master=self.bottom_frame3, width= 1200, height= 385,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings        

        num_pairs = 15  # número de pares de columnas "inc" y "repro"
        
        cols = ["Matricula", "Nombre"]
        self.datas = []
        for i in range(num_pairs):
            cols.append(f"Inc{i+1}")
            self.datas.append(f"Inc{i+1}")
            cols.append(f"Repro{i+1}")        

        tree = ttk.Treeview(frame_table,height=3,columns=cols,style="mystyle.Treeview") # definir cuantas columnas tendra la tabla
        tree.place(x=10,y=20, width=1500,height=400) # le


        tree.heading("#0", text="ID",anchor="w")        
        tree.heading("Matricula", text="Matricula",anchor="w")
        tree.heading("Nombre", text="Nombre",anchor="w")

        for i in range(num_pairs):
            tree.heading(f"Inc{i+1}", text=f"Inc{i+1}",anchor="w")
            tree.heading(f"Repro{i+1}", text=f"Repro{i+1}",anchor="w")



        def on_cell_click(event):
            # hacer algo cuando se hace clic en la celda
            row_id = event.widget.focus()
            col_id = event.widget.identify_column(event.x)
            col_title = event.widget.heading(col_id)['text']
            
            
            cell_value = event.widget.item(row_id)['values'][0]
            
            
            if col_title in self.datas:
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
        scroll_databaseH.place(x=10, y=420, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)
        k = 1
        for x in self.alumnos:
            # ,"vacio" if d[4] == [''] else d[4],
            # print(x[-1])
            matsfromdates = self.crearArray(x[-1],x[2])
            # tree.insert("", "end", text=k, values=[x[2], x[1]] + [" ", " "]*num_pairs)
            tree.insert("", "end", text=k, values=[x[2], x[1]," ", matsfromdates[0]," ", matsfromdates[1]," ", matsfromdates[2]," ", matsfromdates[3]," ", matsfromdates[4]," ",matsfromdates[5]," ", matsfromdates[6]," ", matsfromdates[7]," ", matsfromdates[8]," ", matsfromdates[9]," ", matsfromdates[10]," ", matsfromdates[11]," ", matsfromdates[12]," ", matsfromdates[13]," ", matsfromdates[14]] )
            k+=1            
    
    def crearArray(self,dataF,matricula):        
        rs = json.dumps(dataF)
        materias = json.loads(rs)
        
        tresdigitos = str(matricula)[:3]
        
        array = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
        
        # print(materias)        
        # print(matricula)

        # print(tresdigitos)

        # print(self.fechas[tresdigitos])

        # print(self.fechas["183"]["ENERO-ABRIL 2021"])

        for key, value in materias.items():                        
            # print(key, value)
            # print(self.fechas[tresdigitos][value])
            array[self.fechas[tresdigitos][value]-1] += key
        
        # print(array)

        return array

    def viewLook(self,matricula):
        #expediente
        self.navigate()                
        self.bottom_frame9.grid(padx=0, pady=0, row=1, column=0)       
        alumnito = self.getByMatricula(matricula)
        incidencita = self.getByMatriculaIN(matricula)
        def bac():                    
            self.view3()

        self.Back = ctk.CTkButton(master=self.bottom_frame9, text="Regresar", width= 140, height= 35, command=bac, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.Back.place(relx= 0.8, rely=0.1, anchor=tk.CENTER)


        num_pairs = 15  # número de pares de columnas "inc" y "repro"
        cols = ["Matricula", "Nombre"]
        self.datas = []
        for i in range(num_pairs):
            cols.append(f"Inc{i+1}")
            self.datas.append(f"Inc{i+1}")
            cols.append(f"Repro{i+1}")
        # tree = ttk.Treeview(frame_table, columns=cols)


        tree = ttk.Treeview(self.bottom_frame9,height=3,columns=cols) # definir cuantas columnas tendra la tabla
        tree.place(x=85,y=105, width=1500,height=400) # le


        tree.heading("#0", text="ID",anchor="w")        
        tree.heading("Matricula", text="Matricula",anchor="w")
        tree.heading("Nombre", text="Nombre",anchor="w")

        for i in range(num_pairs):
            tree.heading(f"Inc{i+1}", text=f"Inc{i+1}",anchor="w")
            tree.heading(f"Repro{i+1}", text=f"Repro{i+1}",anchor="w")    


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
                # self.navigate()
                self.view6(cell_value,col_title)

        tree.bind('<ButtonRelease-1>', on_cell_click)      

        #para definir la scrollbar hortizontal
        scroll_databaseH = Scrollbar(self.bottom_frame9, orient="horizontal", command=tree.xview)
        scroll_databaseH.place(x=75, y=520, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)
        
        
        matsfromdates = self.crearArray(alumnito[0][-1],alumnito[0][2])
        
        tree.insert("", "end", text=1, values=[alumnito[0][2], alumnito[0][1]," ", matsfromdates[0]," ", matsfromdates[1]," ", matsfromdates[2]," ", matsfromdates[3]," ", matsfromdates[4]," ",matsfromdates[5]," ", matsfromdates[6]," ", matsfromdates[7]," ", matsfromdates[8]," ", matsfromdates[9]," ", matsfromdates[10]," ", matsfromdates[11]," ", matsfromdates[12]," ", matsfromdates[13]," ", matsfromdates[14]] )            
        
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

        info_label = ctk.CTkLabel(master=self.bottom_frame4, corner_radius=0, text="Trayectoria por alumno", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)

        frame_table = ctk.CTkFrame(master=self.bottom_frame4, width= 1200, height= 405,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.55, anchor=tk.CENTER)


        look = tk.Entry(self.bottom_frame4, bg="white", font=("Arial", 12))
        look.place(relx=0.71, rely=0.12, anchor=tk.CENTER,width=300,height=40)
       

        def getDataForLook():
            matrix = look.get()

            if matrix != "" and matrix != " ":
                if  matrix.isdigit() == True:
                                        
                    self.viewLook2(matrix)
                else:
                    self.show_message("Mensaje", "Solo se aceptan numeros")                        
            else:
                self.show_message("Mensaje", "Campo vacio")                    
                        


        send = tk.Button(self.bottom_frame4, text="Buscar", command=getDataForLook)            
        send.place(relx=0.85, rely=0.12, anchor=tk.CENTER,width=130,height=40)


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
                               
        # para definir la scrollbar vertical
        scroll_databaseV = Scrollbar(frame_table, orient="vertical", command=tree.yview)
        scroll_databaseV.place(x=10, y=20, height=400)
        tree.configure(yscrollcommand=scroll_databaseV.set)

        #para definir la scrollbar hortizontal
        scroll_databaseH = Scrollbar(frame_table, orient="horizontal", command=tree.xview)
        scroll_databaseH.place(x=10, y=420, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)

       
        def on_cell_click(event):
            # hacer algo cuando se hace clic en la celda
            
            
            row_id = event.widget.focus()
            col_id = event.widget.identify_column(event.x)
            col_title = event.widget.heading(col_id)['text']
            matricula = event.widget.item(row_id)['values'][0]

            # print(column_id)
            cell_value = event.widget.item(row_id)['values'][int(col_id[1:])-1]
                     
             
            a = ""
            
            newca = ""
            if isinstance(cell_value, int) == False:

                

                # print(palabras)
                if col_title != 'Nombre' and col_title != 'Matricula':
                    new_value = simpledialog.askstring("Editar celda", f"Ingrese un nuevo valor para la celda:", initialvalue=cell_value)                           
                    
                    if col_title != "nombremateriareza":
                        print(new_value)
                        a = new_value.replace(" ", "")

                        a = a.split(",")         

                        print(a)                                
                        print(matricula)
                        print(col_title)
                        print(a)
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
                    tree.insert("", "end", text=l, values=[x[2], x[1], d[0], d[1], d[2] , d[3], "vacio" if d[4] == [''] else d[4], d[5], "vacio" if d[6] == [''] else d[6], d[7], "vacio" if d[8] == ""else d[8],  "vacio" if d[9] == [''] else d[9], "vacio" if d[10] == [''] else d[10]])                    
            l+=1
        
        tree.bind('<ButtonRelease-1>', on_cell_click)        
                 
    def viewLook2(self,matricula):
        self.navigate()               
        alumnito = self.getByMatricula(matricula)

        tray = self.selectDataTraByM(matricula)
        # tray = self.g
         
        self.bottom_frame10.grid(padx=0, pady=0, row=1, column=0)
        
        
        info_label = ctk.CTkLabel(master=self.bottom_frame10, corner_radius=0, text="Trayectoria", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)

        frame_table = ctk.CTkFrame(master=self.bottom_frame10, width= 1100, height= 405,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        def bac():                    
            self.view4()

        self.Back = ctk.CTkButton(master=self.bottom_frame10, text="Regresar", width= 140, height= 35, command=bac, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.Back.place(relx= 0.8, rely=0.1, anchor=tk.CENTER)

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
                               
        # para definir la scrollbar vertical
        scroll_databaseV = Scrollbar(frame_table, orient="vertical", command=tree.yview)
        scroll_databaseV.place(x=10, y=20, height=400)
        tree.configure(yscrollcommand=scroll_databaseV.set)

        #para definir la scrollbar hortizontal
        scroll_databaseH = Scrollbar(frame_table, orient="horizontal", command=tree.xview)
        scroll_databaseH.place(x=10, y=420, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)

       
        def on_cell_click(event):
                                   
            row_id = event.widget.focus()
            col_id = event.widget.identify_column(event.x)
            col_title = event.widget.heading(col_id)['text']
            matricula = event.widget.item(row_id)['values'][0]

            # print(column_id)
            cell_value = event.widget.item(row_id)['values'][int(col_id[1:])-1]
                     
             
            a = ""                        
            if isinstance(cell_value, int) == False:
                
                # print(palabras)
                if col_title != 'Nombre' and col_title != 'Matricula':
                    new_value = simpledialog.askstring("Editar celda", f"Ingrese un nuevo valor para la celda:", initialvalue=cell_value)                           
                    
                    if col_title != "nombremateriareza":
                        print(new_value)
                        a = new_value.replace(" ", "")

                        a = a.split(",")         

                        print(a)                                
                        print(matricula)
                        print(col_title)
                        print(a)
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
                         
        print(alumnito[0][2])                                           
        if tray[-1] == alumnito[0][2]:                                        
            tree.insert("", "end", text=1, values=[alumnito[0][2], alumnito[0][1], tray[0], tray[1], tray[2] , tray[3], "vacio" if tray[4] == [''] else tray[4], tray[5], "vacio" if tray[6] == [''] else tray[6], tray[7], "vacio" if tray[8] == ""else tray[8],  "vacio" if tray[9] == [''] else tray[9], "vacio" if tray[10] == [''] else tray[10]])                                
        
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

    def viewTrayeG(self):
        self.navigate()
        self.bottom_frame20.grid(padx=0, pady=0, row=1, column=0)

        info_label = ctk.CTkLabel(master=self.bottom_frame20, corner_radius=0, text="Trayectoria por generacion", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)

        gen = self.selectGeneraciones()
        
        i= 0.1
        for x in gen:
            print(x[0])                
            btnLod = ctk.CTkButton(master=self.bottom_frame20, text=f'{x[0]}', width= 80, height= 40, command=lambda matricula=x[0]: self.viewTrayeGChoice(matricula), corner_radius=3, fg_color="#404CBB", text_color="white", hover_color="#4554DD", font=("Helvetica",  15, 'bold'))
            btnLod.place(relx= i, rely=0.32, anchor=tk.CENTER)            
            i+=0.1            

    def viewTrayeGChoice(self,matricula):
        self.navigate()
        self.bottom_frame21.grid(padx=0, pady=0, row=1, column=0)

        info_label = ctk.CTkLabel(master=self.bottom_frame21, corner_radius=0, text="Trayectoria por generacion", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.06, anchor=tk.CENTER)
        

        def backs():  
            info_labelI.destroy()
            self.navigate()          
            self.viewTrayeG()                                    

        self.Back = ctk.CTkButton(self.bottom_frame21, text="Regresar", width= 140, height= 35, command=backs, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.Back.place(relx= 0.8, rely=0.1, anchor=tk.CENTER)

        info_labelI = ctk.CTkLabel(self.bottom_frame21, corner_radius=0, text=f'Periodo de ingreso: {self.inicios[str(matricula)]}', font=("Helvetica",  16, 'bold'))
        info_labelI.place(relx=0.15, rely=0.20, anchor=tk.CENTER)
        

        info_labelm = ctk.CTkLabel(self.bottom_frame21, corner_radius=0, text=f'Matricula: {str(matricula)}', font=("Helvetica",  16, 'bold'))
        info_labelm.place(relx=0.05, rely=0.25, anchor=tk.CENTER)

                      
        frame_table = ctk.CTkFrame(self.bottom_frame21, width= 1200, height= 385,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        

        datos = self.selectTrayByGeneraciones(matricula)
       
        if datos == []:
            print("se crea")
            self.intertUser2(matricula)
            datos = self.selectTrayByGeneraciones(matricula)    
       

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings        
        
        
        cols = ["cuatrimestre","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]                

        tree = ttk.Treeview(frame_table,height=3,columns=cols,style="mystyle.Treeview") # definir cuantas columnas tendra la tabla
        tree.place(x=10,y=20, width=1500,height=400) # le


        tree.heading("#0", text="ID",anchor="w")        
        tree.heading("cuatrimestre", text="cuatrimestre",anchor="w")
        tree.heading("1", text="1",anchor="w")
        tree.heading("2", text="2",anchor="w")
        tree.heading("3", text="3",anchor="w")
        tree.heading("4", text="4",anchor="w")
        tree.heading("5", text="5",anchor="w")
        tree.heading("6", text="6",anchor="w")
        tree.heading("7", text="7",anchor="w")
        tree.heading("8", text="8",anchor="w")
        tree.heading("9", text="9",anchor="w")
        tree.heading("10", text="10",anchor="w")
        tree.heading("11", text="11",anchor="w")
        tree.heading("12", text="12",anchor="w")
        tree.heading("13", text="13",anchor="w")
        tree.heading("14", text="14",anchor="w")
        tree.heading("15", text="15",anchor="w")
      
         # para definir la scrollbar vertical
        scroll_databaseV = Scrollbar(frame_table, orient="vertical", command=tree.yview)
        scroll_databaseV.place(x=10, y=20, height=400)
        tree.configure(yscrollcommand=scroll_databaseV.set)

        #para definir la scrollbar hortizontal
        scroll_databaseH = Scrollbar(frame_table, orient="horizontal", command=tree.xview)
        scroll_databaseH.place(x=10, y=420, width=1300)
        tree.configure(xscrollcommand=scroll_databaseH.set)
        
   
        mat = datos[0][0]
        periodo_academico= datos[0][-1]
        cantidad_alumnos = datos[0][1]
        reprobacion= datos[0][2]
        rezago= datos[0][3]
        retencion= datos[0][4]
        abandono_escolar= datos[0][5]
        desercion= datos[0][6]
        terminaron = datos[0][7]
        eficiencia_terminal= datos[0][8]
        titulados= datos[0][9]

        tree.insert("", "end", text=1, values= ["periodo_academico"]+periodo_academico[0:] )
        tree.insert("", "end", text=1, values= ["cantidad_alumnos"]+cantidad_alumnos[0:] )
        tree.insert("", "end", text=1, values= ["reprobacion"]+reprobacion[0:] )
        tree.insert("", "end", text=1, values= ["rezago"]+rezago[0:] )
        tree.insert("", "end", text=1, values= ["retencion"]+retencion[0:] )
        tree.insert("", "end", text=1, values= ["abandono_escolar"]+abandono_escolar[0:] )
        tree.insert("", "end", text=1, values= ["desercion"]+desercion[0:] )
        tree.insert("", "end", text=1, values= ["terminaron"]+terminaron[0:] )
        tree.insert("", "end", text=1, values= ["eficiencia_terminal"]+eficiencia_terminal[0:] )
        tree.insert("", "end", text=1, values= ["titulados"]+titulados[0:] )

        def on_cell_click(event):
            # hacer algo cuando se hace clic en la celda
                        
            row_id = event.widget.focus()
            col_id = event.widget.identify_column(event.x)
            col_title = event.widget.heading(col_id)['text']
            titulito = event.widget.item(row_id)['values'][0]

            # print(column_id)
            cell_value = event.widget.item(row_id)['values'][int(col_id[1:])-1]                                  

            print(cell_value) #valor de la columna
            print(titulito) #titulo para ver a que arreglo se le colocara el nuevo valor
            print(col_title) # el numero de columna que es el numero de cuatrimestre
        # ,campo,dato,matricula
            tipo = ""
            new = []
            if col_title != "cuatrimestre":
                if titulito != "periodo_academico":
                    new_value = simpledialog.askstring("Editar celda", f"Ingrese un nuevo valor para la celda:", initialvalue=cell_value)                                                    

                    if titulito == "cantidad_alumnos":
                        tipo = "cantidad_alumnos"
                        cantidad_alumnos[int(col_title)-1] = int(new_value)
                        new = cantidad_alumnos

                    elif titulito == "reprobacion":
                        tipo = "reprobacion"
                        reprobacion[int(col_title)-1] = int(new_value)
                        new = reprobacion

                    elif titulito == "rezago":
                        tipo = "rezago"
                        rezago[int(col_title)-1] = int(new_value)
                        new = rezago

                    elif titulito == "retencion":
                        tipo = "retencion"
                        retencion[int(col_title)-1] = int(new_value)
                        new = retencion

                    elif titulito == "abandono_escolar":
                        tipo = "abandono_escolar" 
                        abandono_escolar[int(col_title)-1] = int(new_value)
                        new = abandono_escolar

                    elif titulito == "desercion":
                        tipo = "desercion"
                        desercion[int(col_title)-1] = int(new_value)
                        new = desercion

                    elif titulito == "terminaron":
                        tipo = "terminaron"
                        terminaron[int(col_title)-1] = int(new_value)
                        new = terminaron

                    elif titulito == "eficiencia_terminal":
                        tipo = "eficiencia_terminal"
                        eficiencia_terminal[int(col_title)-1] = int(new_value)
                        new = eficiencia_terminal

                    elif titulito == "titulados":
                        tipo = "titulados"
                        titulados[int(col_title)-1] = int(new_value)
                        new = titulados

                    self.updateTrayectoriaByGene(titulito,new,matricula)
                    print("el tipo desues del seleccion: ",str(tipo))     
                    self.navigate()
                    self.viewTrayeGChoice(matricula)   

                else:
                    self.show_message("Mensaje", "Celda no editable")
                
            else:
                self.show_message("Mensaje", "Celda no editable")
           

            
            

        tree.bind('<ButtonRelease-1>', on_cell_click)

    def selectGeneraciones(self):
        conn = psycopg2.connect(
               user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
        )
        cursor = conn.cursor()        

        cursor.execute(f'SELECT * FROM generaciones')
        
        results = cursor.fetchall()               
            
        cursor.close()
        conn.close()
        
        return results
    
    def veri(self):
       
        for x in self.asignaturas:
            print(x)

    def view6(self,matricula,titulo):
        self.navigate()
        
        self.bottom_frame6.grid(padx=0, pady=0, row=1, column=0)        
        cont = 0
        for x in self.datas:
            if x == titulo:
                cont += 1;
                break;
            else:
                cont += 1;       
        frame_table1 = ctk.CTkFrame(master=self.bottom_frame6, width= 1100, height= 455,corner_radius=0)        
        frame_table2 = ctk.CTkFrame(master=self.bottom_frame6, width= 1100, height= 455,corner_radius=0)
        
        
        def navigate2():
            frame_table1.grid_remove()
            frame_table2.grid_remove()          
                

        def viewE(matri):
            navigate2()               
            print(matri)
            
            frame_table1.grid(padx=0.2, pady=0.1, row=1, column=0)
            info_label = ctk.CTkLabel(master=frame_table1, corner_radius=0, text='Agregar', font=("Helvetica",  24, 'bold'))
            info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)      
            
            def browse_file():
                filename = filedialog.askopenfilename(initialdir = "/", title = "Seleccionar archivo", filetypes = (("Archivos", "*.*"), ("Todos los archivos", "*.*")))
                # Mostrar nombre de archivo seleccionado en cuadro de texto
                file_path.set(filename)

            # Crear función para subir archivo
            def upload_file():
                
                incidenciask = []
                incidenciask = self.getIncidencias(matri,cont)
                # print(incidencias)
                notask = []
                notask = self.getIncidenciasN(matri,cont)

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
                print(incidenciask)
                if incidenciask[0] == None and notask[0] == None:
                    new = []
                    new.append(str(src_file))
                    self.createInci(matri,cont,new)
                else:
                    a = []
                    print('aqui')
                    if incidenciask[0] == None:
                        a.append(str(src_file)+"")
                    else:
                        for x in incidenciask[0]:
                            print(x)
                            a.append(x)                                   
                            
                        a.append(str(src_file)+"")                    
                    # print(src_file)
                    self.updateInci(matri,cont,a)                                                                               
                

            info_labelF = ctk.CTkLabel(master=frame_table1, corner_radius=0, text='Archivos', font=("Helvetica",  24, 'bold'))
            info_labelF.place(relx=0.25, rely=0.32, anchor=tk.CENTER)      
            
            # Crear etiquetas y cuadros de texto
            a = tk.Label(frame_table1, text="Archivo:")
            file_path = tk.StringVar()
            b = tk.Entry(frame_table1, textvariable=file_path)
            c = tk.Button(frame_table1, text="Seleccionar archivo", command=browse_file)
            d = tk.Button(frame_table1, text="Subir archivo", command=upload_file)            
            uploaded_file_name_var = tk.StringVar()
            uploaded_file_path_var = tk.StringVar() #path 
                        
            a.place(relx=0.15, rely=0.52, anchor=tk.CENTER,width=130,height=60)
            b.place(relx=0.34, rely=0.52, anchor=tk.CENTER,width=300,height=60)
            c.place(relx=0.25, rely=0.70, anchor=tk.CENTER,width=130,height=60)
            d.place(relx=0.40, rely=0.70, anchor=tk.CENTER,width=130,height=60)                                                        

            def sendNota():
                incidenciask = []
                incidenciask = self.getIncidencias(matri,cont)
                # print(incidencias)
                notask = []
                notask = self.getIncidenciasN(matri,cont)

                texto = g.get("1.0", tk.END)

                print(notask)
                if notask[0] == None and incidenciask[0] == None:                    
                    print('aqui')
                    new = []
                    new.append(str(texto))
                    print(new)
                    self.createInciN(matri,cont,new)
                else:
                    a = []
                    if notask[0] == None:
                         a.append(texto)
                    else:                        
                        for x in notask[0]:
                            print(x)
                            a.append(x)                                   
                            
                        a.append(str(texto))                    
                    print(texto)
                    print(a)
                    tk.messagebox.showinfo("Subir nota", "Nota subida con éxito.")

                    self.updateInciN(matri,cont,a)  

                g.delete('1.0', END)

            info_labelN = ctk.CTkLabel(master=frame_table1, corner_radius=0, text='Notas', font=("Helvetica",  24, 'bold'))
            info_labelN.place(relx=0.65, rely=0.32, anchor=tk.CENTER)                  
            
            g = tk.Text(frame_table1)
            g.place(relx=0.74, rely=0.62, anchor=tk.CENTER,width=350,height=200)
            g2 = tk.Button(frame_table1, text="Enviar nota", command=sendNota)            
            g2.place(relx=0.74, rely=0.92, anchor=tk.CENTER,width=130,height=60)


        def viewR(matri):
            navigate2()

            incidenciasd = []
            # print(cont)
            alumno = self.getByMatricula(matri)
            # print(alumno)       
            incidenciasd = self.getIncidencias(matri,cont)
            # print(incidencias)
            notasd = []
            notasd = self.getIncidenciasN(matri,cont)
            # print(notas)
            

            frame_table2.grid(padx=0.2, pady=0.1, row=1, column=0)
            info_label = ctk.CTkLabel(master=frame_table2, corner_radius=0, text='Revisar', font=("Helvetica",  24, 'bold'))
            info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)            
            
            if incidenciasd[0] != None:                                              
                x = 0.30
                i = 0.1
                for x in incidenciasd[0]:

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
                    boton.place(relx=i, rely=0.40, anchor=tk.CENTER)  
                    i+=0.12

            
            if notasd[0] != None:

                def mostrar_nombre(nombre):
                    widget_texto.delete('1.0', tk.END)  # Limpiamos el widget de texto
                    widget_texto.insert(tk.END, nombre)

                c = 0
                i= 0.1
                for nombre in notasd[0]:
                    print(nombre)
                    if nombre != None:
                        btnkr = tk.Button(master=frame_table2, text=f'nota{c}', command=lambda nombre=nombre: mostrar_nombre(nombre))
                        btnkr.place(relx= i, rely=0.6, anchor=tk.CENTER)
                        c+=1
                        i+=0.05

                widget_texto = tk.Text(master=frame_table2, height=5)
                widget_texto.place(relx= 0.4, rely=0.75, anchor=tk.CENTER)      
                
            else:
                print('sin nada que mostrar chula')
            
            self.btnk1 = ctk.CTkButton(master=frame_table2, text="Notas", width= 140, height= 35, command=None, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
            self.btnk1.place(relx= 0.4, rely=0.1, anchor=tk.CENTER)

        def backs():
            navigate2()
            # self.navigate()            
            self.view3()

        self.btnk1 = ctk.CTkButton(master=self.bottom_frame6, text="Revisar", width= 140, height= 35, command=lambda: viewR(matricula), corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnk1.place(relx= 0.4, rely=0.1, anchor=tk.CENTER)

        self.btnk2 = ctk.CTkButton(master=self.bottom_frame6, text="Agregar", width= 140, height= 35, command=lambda: viewE(matricula), corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.btnk2.place(relx= 0.6, rely=0.1, anchor=tk.CENTER)
        
        self.Back = ctk.CTkButton(master=self.bottom_frame6, text="Regresar", width= 140, height= 35, command=backs, corner_radius=3, fg_color="#E5E5E5", text_color="black", hover_color="#EEEEEE", font=("Helvetica",  15))
        self.Back.place(relx= 0.8, rely=0.1, anchor=tk.CENTER)
                   
    def getByMatricula(self,matricula):
        conn = psycopg2.connect(
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
    
    def getByMatriculaIN(self,matricula):
        conn = psycopg2.connect(
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
        )
        cursor = conn.cursor()        
        # Ejecuta una consulta SQL
        cursor.execute(f"SELECT * FROM incidencias WHERE matriculaalumno={matricula}" )

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        # print(results)
        
        cursor.close()
        conn.close()

        return results
            
    def createInci(self,matricula,cuatri,datas):
        conn = psycopg2.connect(
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
            )
        cursor = conn.cursor()        
        sql = "INSERT INTO incidencias (matriculaalumno, uplo,cuatri) VALUES (%s, %s, %s)"

        valores = (matricula, datas,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()
    
    def createInciN(self,matricula,cuatri,datas):
        conn = psycopg2.connect(
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
            )
        cursor = conn.cursor()        

        sql = "INSERT INTO incidencias (matriculaalumno,cuatri,notas) VALUES (%s,%s,%s)"

        valores = (matricula,cuatri,datas)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

    def updateInci(self,matricula,cuatri,datas):
        conn = psycopg2.connect(
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
            )
        cursor = conn.cursor()        
        
        sql = "UPDATE incidencias SET uplo = %s WHERE matriculaalumno = %s and cuatri = %s;"

        valores = (datas,matricula,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

    def updateInciN(self,matricula,cuatri,datas):
        conn = psycopg2.connect(
            user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
            )
        cursor = conn.cursor()        
        
        sql = "UPDATE incidencias SET notas = %s WHERE matriculaalumno = %s and cuatri = %s;"

        valores = (datas,matricula,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()
        
    def getIncidencias(self,matricula,cuatri):
        conn = psycopg2.connect(
              user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
              a.append(None)
    
        cursor.close()
        conn.close()
        return a
    
    def getIncidenciasN(self,matricula,cuatri):
        conn = psycopg2.connect(
            user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
        )
        cursor = conn.cursor()        
        cursor.execute(f"SELECT notas FROM incidencias WHERE matriculaalumno={matricula} and cuatri={cuatri}" )

        
        a = []
        results = cursor.fetchall()
        # print(results)
        if results != []:
                # print(results[0][0])
                a.append(results[0][0])
                # for x in a :
                #       print(x)
        else:
              print('sin notas')    
              a.append(None)
    
    
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
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
           user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb

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
           user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
              user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
            user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
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
                        user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
                    )
                cursor = conn.cursor()                        
                                 
                valores = (dato,matricula)                                
                sql = "UPDATE trayectoria SET {} = %s WHERE matriculaalumno = %s".format(campo)
                cursor.execute(sql, valores)

                conn.commit()

                cursor.close()
                conn.close()

    def selectDataTraByM(self,matricula):
        conn = psycopg2.connect(
              user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
        )
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM trayectoria Where matriculaalumno = {matricula}')
        
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results[0]
    
    def selectTrayByGeneraciones(self,matricula):
        conn = psycopg2.connect(
             user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
        )
        cursor = conn.cursor()        

        cursor.execute(f'SELECT * FROM trayectoriageneral where mat = {matricula}')
        
        results = cursor.fetchall()
        
        # print(results)
            
        cursor.close()
        conn.close()
        
        return results

    def intertUser2(self,matricula):
        conn = psycopg2.connect(
                  user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
            )
        cursor = conn.cursor()        
                                
        cantidad_alumnos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        reprobacion=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        rezago=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        retencion=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        abandono_escolar=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        desercion=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        terminaron =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        eficiencia_terminal=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        titulados= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]           
        
        tresdigitos = str(matricula)[:3]
        dete = self.fechas[tresdigitos]


        # print(dete)

        alumnitos = self.selectdatasfromUsuarioBy(int(tresdigitos))

        # print(alumnitos)
        cont = 0

        for x in alumnitos:
            # cont += 1
            print(x[-1])
            for key, value in x[-1].items():                        
                print(key, value)
                print(self.fechas[tresdigitos][value])
                reprobacion[self.fechas[tresdigitos][value]-1] += 1
                rezago[self.fechas[tresdigitos][value]-1] += 1

            # print(self.fechas[tresdigitos][value])
            # array[self.fechas[tresdigitos][value]-1] += key
        
        
        sql = "INSERT INTO trayectoriageneral (mat,cantidad_alumnos,reprobacion,rezago,retencion,abandono_escolar,desercion,terminaron,eficiencia_terminal,titulados,periodo_academico) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"        
        
        valores = (matricula,cantidad_alumnos,reprobacion,rezago,retencion,abandono_escolar,desercion,terminaron,eficiencia_terminal,titulados,self.periodosAca[str(matricula)])       

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()


    def createReprobacion(self):
        pass
        
    def updateTrayectoriaByGene(self,campo,dato,matricula):
                conn = psycopg2.connect(
                          user=self.usuariodb,
            password=self.passdb,
            host="localhost",
            port=self.portdb,   
            database=self.namedb
                    )
                cursor = conn.cursor()                        
                                 
                valores = (dato,matricula)                                
                sql = "UPDATE trayectoriageneral SET {} = %s WHERE mat = %s".format(campo)
                cursor.execute(sql, valores)

                conn.commit()

                cursor.close()
                conn.close()


    def selectdatasfromUsuarioBy(self,matricula):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM alumnos WHERE CAST(matricula AS TEXT) LIKE '{matricula}%'")

        resultado = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return resultado