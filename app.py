from flask import Flask, render_template, request, redirect, url_for
from src.database import DBManager
from src.modelos import Tarea, Proyecto


app = Flask(__name__)
db_manager = DBManager()


@app.route('/')
def index():
    tareas_pendientes = db_manager.obtener_tareas(estado="Pendiente")
    proyectos = db_manager.obtener_proyectos()

    return render_template('index.html',
                           tareas=tareas_pendientes,
                           proyectos=proyectos)