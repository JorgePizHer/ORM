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
                                
        if random.randint(0,3) == 0:
            self.entidadexito = lienzo.create_polygon(
                self.posx - self.radio/2, self.posy + self.radio/2,
                self.posx + self.radio/2, self.posy + self.radio/2,
                self.posx, self.posy - self.radio/2,
                fill='gold')
            self.exito = True
            
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
            
def guardarPersona():
    print("Guardo a los jugadores")
    
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            DELETE from jugadores
            ''')
    conexion.commit()

    for persona in personas:

        cursor.execute('''
            INSERT INTO jugadores
            VALUES (
                NULL,
                '''+str(persona.posx)+''',
                '''+str(persona.posy)+''',
                '''+str(persona.radio)+''',
                '''+str(persona.direccion)+''',
                "'''+str(persona.color)+'''",
                "'''+str(persona.entidad)+'''",
                '''+str(persona.energia)+''',
                '''+str(persona.descanso)+''',
                "'''+str(persona.entidadenergia)+'''",
                "'''+str(persona.entidaddescanso)+'''",
                "'''+str(persona.exito)+'''",
                "'''+str(persona.entidadexito)+'''"
            )
            ''')
    
    conexion.commit()
    conexion.close()
    
# Creo una ventana
raiz = tk.Tk()

# En la ventana creo un lienzo
lienzo = tk.Canvas (raiz,width=840,height=840)
lienzo.pack()

#Botón de guardar
boton = tk.Button(raiz,text="Guardar",command=guardarPersona)
boton.pack()
   
#En la colección introduzco instancias de personas en el caso de que no existan
if len(personas) == 0:
    numeropersonas = 10
    for i in range(0,numeropersonas):
        personas.append(Persona())
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
