from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos os modelos aqui para garantir que sejam registrados
from .instrutor import Instrutor
from .prova import Prova
from .pontuacao import Pontuacao

