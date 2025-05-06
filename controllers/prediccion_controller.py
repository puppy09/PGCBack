from flask import Flask, request, jsonify, Blueprint, current_app
from flask_mail import Message
from app import db
from app import mail
from models.usuario_model import Usuarios
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from middlewares.menu import token_requerido

prediccionBP = Blueprint('prediccion',__name__)
