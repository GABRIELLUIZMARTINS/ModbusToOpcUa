from opcua import Client,ua 
from pyModbusTCP.server import ModbusServer, DataBank
from random import randrange
from time import sleep
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Constantes import *
import subprocess

class Ping:
    def __init__(self, host = 'localhost'):
        self.host = host
        self.ping()
    def ping(self):
        try:
            output = subprocess.check_output(['ping', '-n', '1', self.host])  # Executa o comando ping
            return True
        except subprocess.CalledProcessError:
            return False
    
a=Ping()
a.ping()