import json
import tkinter as tk
import customtkinter as ctk 
from tkinter import filedialog
from interfaz_test import Window

import PyPDF2, re
import uuid
import psycopg2

from alumno import Alumno


# def get_reprobados(pdf_reader, asignatura, periodo):
#     cont = 0
   
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         text = page.extract_text()
#         lines = text.split('\n')
#         for line in lines:
#             # print(lines)
#             if cont > 5:
#                 match = re.match(r'(\b\w+\b.*?)(\d+\s+\d+)', line)
#                 if match != None:
#                     part1 = match.group(1)
#                     part2 = match.group(2)
#                     calificaciones = part2.split(" ")
#                     # print(calificaciones)
#                     for c in calificaciones:
#                         if int(c) < 70:
#                             id_unico = uuid.uuid4()
#                             x = ''+  str(id_unico) 
#                             a = Alumno(x,part1, asignatura, periodo, calificaciones)   

#                             resultado = getByMatricula(a.m)
#                             mats = {f'{asignatura}':f'{periodo}'}
#                             new_json_string = json.dumps(mats)
#                             nn = json.loads(new_json_string)

#                             if resultado == []:
#                                 insertarData(a.id,a.nombre,a.m,asignatura,periodo,new_json_string)                                                     
#                                 createTrayecotira(a.m)                                
#                             else:
                                
#                                 rs = json.dumps(resultado[0][-1])
#                                 materias = json.loads(rs)
                                                                
#                                 # print(new_json_string)

#                                 if all(item in materias.items() for item in nn.items()):
#                                     print("El contenido de 'a' está presente en 'materias'")
#                                 else:
#                                     print("El contenido de 'a' no está presente en 'materias'")                                
#                                     materias.update(nn)       
#                                     ma = json.dumps(materias)                             
#                                     updateusuario(a.m,ma)
#                                     print("el alumno ya esta en la base de datos pero se actualizo")                            
                                                                                               
#                             break

#             cont += 1



def get_reprobados(pdf_reader, asignatura, periodo):
    cont = 0
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if cont > 5:
                
                line = line.replace("100", "100 ")
                # print(line)
                match = re.search(r'\d+\s\d+(?:\s\d+)*\s[\d\.]+', line)
                if match:
                    cal = match.group()
                    calificaciones = cal.split(" ")
                    datos = line.replace(cal, "")
                    #print(datos)
                    #print(calificaciones)
                    if len(calificaciones) > 3:
                        if float(calificaciones[-1]) < 70.0:
                            #print(calificaciones[-1])
                            # a = Alumno(datos, asignatura, periodo, calificaciones)

                            # win.alumnos.append(a)

                            id_unico = uuid.uuid4()
                            x = ''+  str(id_unico) 
                            # print(asignatura)

                            if periodo == " SEPTIEMBRE-DICIEMBRE 2020":
                                 print("si es igual")
                                 periodo = periodo.lstrip()
                            
                            if asignatura == " Calidad del Software":
                                 asignatura = asignatura.lstrip()

                            a = Alumno(x,datos, asignatura, periodo, calificaciones)   

                            resultado = getByMatricula(a.m)
                            # print(periodo)
                            mats = {f'{asignatura}':f'{periodo}'}
                            new_json_string = json.dumps(mats)
                            nn = json.loads(new_json_string)


                            tresdigitos = str(a.m)[:3]
                            print(tresdigitos)
                            ad = selectGeneraciones(tresdigitos)

                            if ad == 0:
                                 intertGeneracion(tresdigitos)
                        
                            if resultado == []:
                                insertarData(a.id,a.nombre,a.m,asignatura,periodo,new_json_string)                                                     
                                createTrayecotira(a.m)                                
                            else:
                                
                                rs = json.dumps(resultado[0][-1])
                                materias = json.loads(rs)
                                                                
                                # print(new_json_string)

                                if all(item in materias.items() for item in nn.items()):
                                    print("El contenido de 'a' está presente en 'materias'")
                                else:
                                    print("El contenido de 'a' no está presente en 'materias'")                                
                                    materias.update(nn)       
                                    ma = json.dumps(materias)                             
                                    updateusuario(a.m,ma)
                                    print("el alumno ya esta en la base de datos pero se actualizo")   
                            
            cont += 1

def insertarData(id,nombre,matricula,materiaR,periodo,mats):
    conn = psycopg2.connect(
            user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
        )
    cursor = conn.cursor()

    # sql = f"INSERT INTO alumnos (id, nombre, matricula,materiar,periodo,mats) VALUES ('{id}','{nombre}',{matricula},'{materiaR}','{periodo}',{mats})"
    sql = "INSERT INTO alumnos (id, nombre, matricula,materiar,periodo,mats) VALUES (%s,%s,%s,%s,%s,%s)"
    
    valores = (id,nombre,matricula,materiaR,periodo,mats)       

    cursor.execute(sql, valores)    
    

    conn.commit()

    cursor.close()
    conn.close()
    
def get_periodo(pdf_reader):
    search = "PERIODO"
    rule = "\d\s[A-Z]{2}"
    found = False
    periodo = None

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')
        profesor = lines[len(lines)-1]
        profesor = profesor.replace(" SERVICIOS ESCOLARES", "")
        for line in lines:
            if search in line:
                found = True
                match = re.search(rule, line)
                pos = match.start() + 1
                lineFormat = line[:pos]
                periodo = lineFormat.replace("PERIODO:", "")
                break
        if found:
            break
    return periodo, profesor

def get_asignatura(pdf_reader):
    search = "ASIGNATURA"
    rule = '\s[A-Z]{2}'
    found = False
    value = None

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if search in line:
                found = True
                lineFormat = re.split(rule, line)
                value = lineFormat[0].replace("ASIGNATURA:", "")
                if value == " Calidad del Software":
                                 value = value.lstrip()
                win.show_message("Mensaje", "Se actualizaron los datos")
                break
        if found:
            break
    return value

def get_data():
    print(FILEPATH)
    pdf_file = open(FILEPATH, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    page = pdf_reader.pages[0]
    text = page.extract_text()
    lines = text.split('\n')
    
    #LECTURA DE PDF ACTA DE CALIFICACIONES
    if "ACTA DE CALIFICACIONES" in lines[1]:
        asignatura = get_asignatura(pdf_reader)
        periodo, profesor = get_periodo(pdf_reader)
        # print(asignatura +" "+ periodo +" "+ profesor)
        get_reprobados(pdf_reader, asignatura, periodo)

        if asignatura not in win.asignaturas and asignatura != None:
            #win.asignaturas.append(asignatura)
            print(asignatura)
            resultado = selectdatasMaterias()
            aux = 0
            for x in resultado:
                if x[0] == asignatura:
                    aux = 1
                    break;
            if aux == 0:
                insertarDataA(asignatura)
            else:
                print("la materia ya esta en la base de datos")

            print(win.asignaturas)

    pdf_file.close()

def insertarDataA(asignatura):
    conn = psycopg2.connect(
            user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
        )
    cursor = conn.cursor()

    sql = f"INSERT INTO materias (materiass) VALUES ('{asignatura}')"

    cursor.execute(sql);

    conn.commit()

    cursor.close()
    conn.close()

def createTrayecotira(matricula):
        conn = psycopg2.connect(
                 user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
            )
        cursor = conn.cursor()      

        a = ['']
        b = ['']
        c = ['']
        d = ['']        

        sql = "INSERT INTO trayectoria (gradoestar,materiasqllevar,materiasaprobadas,materiasrepeticion,nommateriasrepe,cuatrimfalta,materiaqfalta,materiarezagada,nombremateriareza,nommatedeberia,nombrellevaactual,matriculaalumno) VALUES (0,0,0,0,%s,0,%s,0,'',%s,%s,%s)"           
        
        valores = (a,b,c,d,matricula)

        cursor.execute(sql,valores)

        conn.commit()

        cursor.close()
        conn.close()

def select_file():
    global FILEPATH
    FILEPATH = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    label = ctk.CTkLabel(master=win.bottom_frame, text=FILEPATH)
    label.place(relx= 0.5, rely=0.45, anchor=tk.CENTER)

def getByMatricula(matricula):
        conn = psycopg2.connect(
            user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
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

def updateusuario(matricula,datase):
            conn = psycopg2.connect(
                    user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
                )
            cursor = conn.cursor()                    

            campo = 'mats'
            valores = (datase,matricula)
            
            
            sql = "UPDATE alumnos SET {} = %s WHERE matricula = %s".format(campo)
            cursor.execute(sql, valores)

            conn.commit()

            cursor.close()
            conn.close()
            
def selectdatasMaterias():
        conn = psycopg2.connect(
            user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM materias")
        
        results = cursor.fetchall()

        # for x in results:                
        #         if x[0] == "Calidad del Software":
        #                 print("si esta")
                        
                           
        cursor.close()
        conn.close()

        return results

def intertGeneracion(matricula):
        
        conn = psycopg2.connect(
             user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
        )

        cursor = conn.cursor()        
                                
        
        sql = "INSERT INTO generaciones (matri) VALUES (%s)"
        valores = (matricula,)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

def selectGeneraciones(matricula):
        conn = psycopg2.connect(
           user=win.usuariodb,
            password=win.passdb,
            host="localhost",
            port=win.portdb,   
            database=win.namedb
        )
        cursor = conn.cursor()        

        cursor.execute(f'SELECT * FROM generaciones where matri = {matricula}')
        
        results = cursor.fetchall()
        
        response = 0
        if results != []:
                # print(results)
                response = 1
        else:
                print("no hya nada")
            
        cursor.close()
        conn.close()
        
        return response

if __name__ == "__main__":
    win = Window(select_file, get_data)
    win.mainloop()
    
    