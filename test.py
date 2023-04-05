import json
import psycopg2

# def createUser():
#         conn = psycopg2.connect(
#                 user="postgres",
#                 password="carrera10",
#                 host="localhost",
#                 port="5432",   
#                 database="estancia"
#             )
#         cursor = conn.cursor()      

#         a = ['']
#         b = ['']
#         c = ['']
#         d = ['']        

#         sql = "INSERT INTO trayectoria (gradoestar,materiasqllevar,materiasaprobadas,materiasrepeticion,nommateriasrepe,cuatrimfalta,materiaqfalta,materiarezagada,nombremateriareza,nommatedeberia,nombrellevaactual,matriculaalumno) VALUES (1,2,3,4,%s,10,%s,2,'as',%s,%s,203407)"           
        
#         valores = (a,b,c,d)

#         cursor.execute(sql,valores)

#         conn.commit()

#         cursor.close()
#         conn.close()

# # createUser()

# def selectData():
#         conn = psycopg2.connect(
#             user="postgres",
#             password="carrera10",
#             host="localhost",
#             port="5432",   
#             database="estancia"
#         )
#         cursor = conn.cursor()

#         cursor.execute("SELECT * FROM trayectoria")
        
#         results = cursor.fetchall()

#         for x in results:                
#             print(x[-1])
            
#         cursor.close()
#         conn.close()

# # selectData()


def updateusuario():
            conn = psycopg2.connect(
                    user="postgres",
                    password="carrera10",
                    host="localhost",
                    port="5432",   
                    database="estancia"
                )
            cursor = conn.cursor()        
            materia = "a"
            newmateroa = materia+" asdasd"
        
              
            valores = (dato,magticula)
            
            
            sql = "UPDATE trayectoria SET {} = %s WHERE matriculaalumno = %s".format(campo)
            cursor.execute(sql, valores)

            conn.commit()

            cursor.close()
            conn.close()

updateTrayectoria()


def selectData():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT notas FROM incidencias where matriculaalumno =191214")
        
        results = cursor.fetchall()


        print(results[0][0])
        if  results[0][0] == None:
                print('no hay ndad')                
        else:
                print('si hayu')
            
        cursor.close()
        conn.close()

# selectData()


def createInci():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
        )
        
        cursor = conn.cursor()      
        matricula= 2034072
        cuatri= 1        
        notas = ['nota1','nota2','nota3']

        sql = "INSERT INTO incidencias (matriculaalumno,cuatri,notas) VALUES (%s,%s,%s)"

        valores = (matricula,cuatri,notas)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

# createInci()




def updateInciN():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        matricula=183392
        cuatri= 1
        datas= [{'a':'s'}]
        
        sql = "UPDATE incidencias SET notas = %s WHERE matriculaalumno = %s and cuatri = %s;"

        valores = (datas,matricula,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

# updateInciN()

def intertUser():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        
                
        n = {{"a":1,"b":2}}
        
        a = json.dumps(n)
        
        sql = "INSERT INTO tes (testd) VALUES (%s)"
        valores = (a)

        cursor.execute(sql, (valores,))

        conn.commit()

        cursor.close()
        conn.close()



def intertUser2():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        
                
       # Definimos los dos JSON
        json_string1 = '{"as":"bs", "dsds":"c"}'
        json_string2 = '{"nombre":"a", "data":"dasd"}'

        # Convertimos los dos JSON en objetos Python
        json_obj1 = json.loads(json_string1)
        json_obj2 = json.loads(json_string2)

        # Combinamos los dos objetos Python en uno solo
        new_json_obj = {**json_obj1, **json_obj2}

        # Convertimos el objeto Python resultante en un nuevo JSON
        new_json_string = json.dumps(new_json_obj)
        
        sql = "INSERT INTO tes (testd) VALUES (%s)"
        valores = (new_json_string)

        cursor.execute(sql, (valores,))

        conn.commit()

        cursor.close()
        conn.close()
        
# intertUser2()

def selectdatas():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tes")
        
        results = cursor.fetchall()

        for x in results:
                print(x[0])
                print(x[0])
        # print(results[0][0])

        # if  results[0][0] == None:
        #         print('no hay ndad')                
        # else:
        #         print('si hayu')
            
        cursor.close()
        conn.close()

# intertUser()
# selectdatas()

# a = {"nombre":"jose","edad":1,"nombre":"jose","edad":1}
# for x in a:
#         print(x)