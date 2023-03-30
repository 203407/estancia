import psycopg2

def createUser():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()      

        a = ['']
        b = ['']
        c = ['']
        d = ['']        

        sql = "INSERT INTO trayectoria (gradoestar,materiasqllevar,materiasaprobadas,materiasrepeticion,nommateriasrepe,cuatrimfalta,materiaqfalta,materiarezagada,nombremateriareza,nommatedeberia,nombrellevaactual,matriculaalumno) VALUES (1,2,3,4,%s,10,%s,2,'as',%s,%s,203407)"           
        
        valores = (a,b,c,d)

        cursor.execute(sql,valores)

        conn.commit()

        cursor.close()
        conn.close()

# createUser()

def selectData():
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
            print(x[-1])
            
        cursor.close()
        conn.close()

# selectData()


def updateTrayectoria():
            conn = psycopg2.connect(
                    user="postgres",
                    password="carrera10",
                    host="localhost",
                    port="5432",   
                    database="estancia"
                )
            cursor = conn.cursor()        
            campo='materiaqfalta'
           
            magticula = 183392
            dato = ['ninguna','osi']          
            valores = (dato,magticula)
            
            
            sql = "UPDATE trayectoria SET {} = %s WHERE matriculaalumno = %s".format(campo)
            cursor.execute(sql, valores)

            conn.commit()

            cursor.close()
            conn.close()

updateTrayectoria()