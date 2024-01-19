import tkinter as tk
import random
import math
import sqlite3

#Declaración de variables globales
personas = []
numeropersonas = 789

class Persona:
    def __init__(self):
        self.posx = random.randint(0,840)
        self.posy = random.randint(0,840)
        self.radio = 30
        self.direccion = random.randint(0,360)
        self.color = "blue"
        self.entidad = "" #identificador
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
        self.exito = False
        self.entidadexito = None

    def dibuja(self):
        
        self.entidad = lienzo.create_oval(
                           self.posx-self.radio/2,
                           self.posy-self.radio/2,
                           self.posx+self.radio/2,
                           self.posy+self.radio/2,
                           fill=self.color)
        
        self.entidadenergia = lienzo.create_rectangle(
                           self.posx-self.radio/2,
                           self.posy-self.radio/2-10,
                           self.posx+self.radio/2,
                           self.posy-self.radio/2-6,
                           fill="light green")
            
        self.entidaddescanso = lienzo.create_rectangle(
                           self.posx-self.radio/2,
                           self.posy-self.radio/2-16,
                           self.posx+self.radio/2,
                           self.posy-self.radio/2-12,
                           fill="light blue")
                                
        if self.exito:
            self.entidadexito = lienzo.create_polygon(
                self.posx - self.radio/2, self.posy + self.radio/2,
                self.posx + self.radio/2, self.posy + self.radio/2,
                self.posx, self.posy - self.radio/2,
                fill='gold')
            
    def mueve(self):
        if self.energia > 0:
            self.energia -=0.25
        if self.descanso > 0:
            self.descanso -=0.25

        self.colisiona()
        lienzo.move(self.entidad,
                    math.cos(self.direccion),
                    math.sin(self.direccion))
        anchuradescanso = (self.descanso/100)*self.radio
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(self.entidadenergia,
                    self.posx-self.radio/2,
                    self.posy-self.radio/2 -10,
                    self.posx-self.radio/2 + anchuraenergia,
                    self.posy-self.radio/2-6)
        lienzo.coords(self.entidaddescanso,
                    self.posx-self.radio/2,
                    self.posy-self.radio/2 -16,
                    self.posx-self.radio/2 + anchuradescanso,
                    self.posy-self.radio/2-12)

        if self.exito and self.entidadexito:
            coords = [
                self.posx - self.radio / 2 * 0.75, self.posy + self.radio / 2 - 50,
                self.posx + self.radio / 2 * 0.75, self.posy + self.radio / 2 - 50,
                self.posx, self.posy - self.radio / 2 * 0.75 - 50
            ]

            if len(coords) == 6:  #Nos aseguramos de que hay 6 coordenadas antes de actualizar
                lienzo.coords(self.entidadexito,*coords) #Solo acepta 4 por coords por defecto, así que hay que dividirlas en pares
        
        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)
        
    def colisiona(self):
        if self.posx < 0 or self.posx > 840 or self.posy < 0 or self.posy > 840:
            self.direccion += 180
    
# Creo una ventana
raiz = tk.Tk()

# En la ventana creo un lienzo
lienzo = tk.Canvas (raiz,width=840,height=840)
lienzo.pack()

#Cargar personas desde SQL

try:
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''
            SELECT *
            FROM jugadores
            ''')
    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        #print (fila)
        persona = Persona()
        persona.posx = fila[1]
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad = fila[6]
        persona.energia = fila[7]
        persona.descanso = fila[8]
        persona.entidadenergia = fila[9]
        persona.entidaddescanso = fila[10]
        persona.exito = fila[11] == "True"
        persona.entidadexito = fila[12]
        personas.append(persona)

##      Para cada fila de la base de datos se crea una nueva persona
##      Los atributos de la persona(posx, posy, radio, direccion, color, entidad)
##      se rellenan con los valores en las correspondientes columnas de la base de datos.
##      La persona es añadida a la lista de personas
    
    conexion.close()
except:
    print("Error al leer base de datos")

print(len(personas))
    
# Pinto cada una de las personas en la colección
for persona in personas:
    persona.dibuja()
    
# Creo un bucle repetitivo
def bucle():
    # Muevo cada una de las personas en la colección
    for persona in personas:
        persona.mueve()
    raiz.after(20,bucle)

# Ejecuto el bucle
bucle()

raiz.mainloop()
