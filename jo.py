import array
import psycopg2

def selecty():
    conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
    cursor = conn.cursor()

            # Ejecuta una consulta SQL
    cursor.execute("SELECT * FROM incidencias")

            # Obtén los resultados de la consulta
    results = cursor.fetchall()
    print(results)

            # Cierra el cursor y la conexión
    cursor.close()

# selecty()
def insertt():
    conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
    cursor = conn.cursor()
    data = [['1'],['12']]
    sql = "INSERT INTO incidencias (idalumno, uplo,cuatri) VALUES (%s, %s, %s)"

    valores = ('dddds', data,1)

    cursor.execute(sql, valores)

    conn.commit()

    cursor.close()
    conn.close()

def choise():     
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()
        matricula = 183392
        # Ejecuta una consulta SQL
        cursor.execute(f"SELECT * FROM alumnos WHERE matricula={matricula}" )

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        print(results)

    
        cursor.close()
        conn.close()


# insertt()
choise()