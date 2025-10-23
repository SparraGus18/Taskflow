import sqlite3
from .modelos import Proyecto, Tarea
import os

DATABASE_NAME = "tareas.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = get_connection()
    cursor = conn.cursor()

    #tabla de proyectos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio TEXT,
                estado TEXT
        )""")

    #Tabla de tareas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEXT,
            fecha_limite TEXT,
            prioridad TEXT,
            estado TEXT,
            proyecto_id INTEGER NOT NULL,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
        )
    """)

    try:
        cursor.execute(f"INSERT INTO proyectos (id, nombre, descripcion, estado) VALUES (0, 'Tareas Generales', 'Tareas sin clasificar', 'Activo')")
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()
    


class DBManager:

    def __init__(self):
        crear_tabla()

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tarea._titulo, tarea._descripcion, tarea._fecha_creacion, tarea._fecha_limite, tarea._prioridad, tarea._estado, tarea._proyecto_id))



        tarea.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea

    def obtener_proyectos(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos")
        filas = cursor.fetchall()
        conn.close()

        proyectos = [
            Proyecto(nombre=fila['nombre'], descripcion=fila['descripcion'], id=fila['id'], estado=fila['estado']) 
            for fila in filas
        ]
        return proyectos

    def obtener_tareas(self, estado=None):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM tareas"
        params = []

        if estado:
            sql += " WHERE estado = ?"
            params.append(estado)
        
        sql += " ORDER BY fecha_limite ASC"

        cursor.execute(sql, params)
        filas = cursor.fetchall()
        conn.close()

        tareas = []
        for fila in filas:
            t = Tarea(
                titulo=fila['titulo'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                estado=fila['estado'],
                proyecto_id=fila['proyecto_id'],
                id=fila['id'],
                descripcion=fila['descripcion']
            )
            tareas.append(t)
        return tareas