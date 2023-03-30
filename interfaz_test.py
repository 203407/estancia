import os
import shutil
import tkinter as tk
from tkinter import END, Scrollbar, ttk
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk 
from PIL import Image
from tkintertable import TableCanvas
import psycopg2
import json
import urllib.request
from urllib.request import urlretrieve


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

        #Paginas/vistas
        self.top_frame = ctk.CTkFrame(master=self, width=1400, height=180, corner_radius=0, fg_color="#E5E5E5") 
        self.bottom_frame = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame2 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame3 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame4 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame5 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")
        self.bottom_frame6 = ctk.CTkFrame(master=self, width=1400, height=570, corner_radius=0, fg_color="#F5F5F5")

        #Barra de navegación superior
        self.top_frame.grid(padx=0, pady=0, row=0, column=0)
        
        #Logo y titulo (Barra de navegación superior)
        logo = ctk.CTkImage(light_image=Image.open('img/logo.png'), dark_image=Image.open('img/logo.png'), size=(105,105))
        logo_label = ctk.CTkLabel(master=self.top_frame, corner_radius=0, image=logo, text="")
        logo_label.place(relx=0.340, rely=0.5, anchor=tk.CENTER)
        title_label = ctk.CTkLabel(master=self.top_frame, corner_radius=0, text="Programa indicadores CACEI", font=("Helvetica",  28, 'bold'))
        title_label.place(relx=0.540, rely=0.375, anchor=tk.CENTER)

        #Botones de navegación de páginas
        nav_btn_1 = ctk.CTkButton(master=self.top_frame, text="Inicio", width=35 , command = self.view1, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5")
        nav_btn_1.place(relx=0.415, rely=0.625, anchor=tk.CENTER)
        nav_btn_2 = ctk.CTkButton(master=self.top_frame, text="Índice reprobados", width=65 , command=self.view2, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5")
        nav_btn_2.place(relx=0.474, rely=0.625, anchor=tk.CENTER)
        nav_btn_3 = ctk.CTkButton(master=self.top_frame, text="Expediente", width=40 , command=self.view3, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5")
        nav_btn_3.place(relx=0.543, rely=0.625, anchor=tk.CENTER)
        nav_btn_4 = ctk.CTkButton(master=self.top_frame, text="Trayectoria", width=40 , command=self.view4, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5")
        nav_btn_4.place(relx=0.600, rely=0.625, anchor=tk.CENTER)
        nav_btn_5 = ctk.CTkButton(master=self.top_frame, text="Reprobados", width=40 , command=self.view5, corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5")
        nav_btn_5.place(relx=0.657, rely=0.625, anchor=tk.CENTER)
        nav_btn_6 = ctk.CTkButton(master=self.top_frame, text="incidencias", width=40 , corner_radius=0, fg_color="transparent", text_color="black", hover_color="#E5E5E5")
        nav_btn_6.place(relx=0.757, rely=0.725, anchor=tk.CENTER)


        self.view1()


    def navigate(self):
        self.bottom_frame.grid_remove()
        self.bottom_frame2.grid_remove()
        self.bottom_frame3.grid_remove()
        self.bottom_frame4.grid_remove()
        self.bottom_frame5.grid_remove()  
        self.bottom_frame6.grid_remove()  

    def show_message(self, title, msj):
        messagebox.showinfo(message=msj, title=title)

    

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
        self.bottom_frame4.grid(padx=0, pady=0, row=1, column=0)

        info_label = ctk.CTkLabel(master=self.bottom_frame4, corner_radius=0, text="Trayectoria", font=("Helvetica",  24, 'bold'))
        info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)

        frame_table = ctk.CTkFrame(master=self.bottom_frame4, width= 1100, height= 405,corner_radius=0)
        frame_table.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        table = ttk.Treeview(frame_table)

        # Definir las columnas de la tabla
        table['columns'] = ('name', 'age', 'gender')

        # Definir las cabeceras de las columnas
        table.heading('#0', text='ID')
        table.heading('name', text='Name')
        table.heading('age', text='Age')
        table.heading('gender', text='Gender')

        # Agregar los datos a la tabla
        table.insert(parent='', index='end', iid=0, text='1', values=('John', 30, 'Male'))
        table.insert(parent='', index='end', iid=1, text='2', values=('Jane', 25, 'Female'))

        # Ubicar la tabla en la ventana
        table.pack()
        #self.test_tabla1(frame_table)

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

    # def view6(self,matricula,titulo):

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
                # print(src_file)
                # paths = uploaded_file_path_var
                if incidencias == []:
                    incidencias.append(str(src_file))
                    # print(str(src_file)+"")
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
            # ads = tk.Label(frame_table1, text="Archivo subido en:")
            uploaded_file_name_var = tk.StringVar()
            uploaded_file_path_var = tk.StringVar() #path 
            
            # tk.Button(frame_table1, textvariable=uploaded_file_name_var, command=download_file).grid(row=2, column=1, sticky="W")
            # m = tk.Entry(frame_table1, textvariable=uploaded_file_path_var)
            a.place(relx=0.35, rely=0.42, anchor=tk.CENTER,width=130,height=60)
            b.place(relx=0.54, rely=0.42, anchor=tk.CENTER,width=300,height=60)
            c.place(relx=0.45, rely=0.60, anchor=tk.CENTER,width=130,height=60)
            d.place(relx=0.60, rely=0.60, anchor=tk.CENTER,width=130,height=60)
            # ads.place(relx=0.60, rely=0.62, anchor=tk.CENTER,width=130,height=60) 
            # m.place(relx=0.70, rely=0.72, anchor=tk.CENTER,width=130,height=60)                                 
            

        def viewR():
            navigate2()
            incidencias = self.getIncidencias(matricula,cont)
            frame_table2.grid(padx=0.2, pady=0.1, row=1, column=0)
            info_label = ctk.CTkLabel(master=frame_table2, corner_radius=0, text='Revisar', font=("Helvetica",  24, 'bold'))
            info_label.place(relx=0.15, rely=0.12, anchor=tk.CENTER)
            nfo_label = ctk.CTkLabel(master=frame_table2, corner_radius=0, text='No existen incidencias', font=("Helvetica",  24, 'bold'))
            
            if incidencias != []:    
                # nfo_label.place(relx=0, rely=0, anchor=tk.CENTER)                                 
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

                    # print(x)
                # print(incidencias[0])
                # for ruta in incidencias:     
                #     print(ruta)               
                #     boton = tk.Button(frame_table2, text= str(ruta).split('/')[-1])                                        
                #     boton.place(relx=x, rely=0.50, anchor=tk.CENTER)  
                #     x+= 0.10                                           

            # else:                
                # nfo_label.place(relx=0.50, rely=0.50, anchor=tk.CENTER) 



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






