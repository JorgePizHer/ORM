import tkinter as tk
import random
import math

personas = []
numeropersonas = 20

class Persona:
    def __init__(self):
        self.posx = random.randint(0,1024)
        self.posy = random.randint(0,1024)
        self.radio = 30
        self.direccion = random.randint(0,360)
        self.color = "blue"
        self.entidad = "" #identificador

    def dibuja(self):
        self.entidad = lienzo.create_oval(
                           self.posx-self.radio/2,
                           self.posy-self.radio/2,
                           self.posx+self.radio/2,
                           self.posy+self.radio/2,
                           fill=self.color)
    def mueve(self):
        lienzo.move(self.entidad,
                    math.cos(self.direccion),
                    math.sin(self.direccion))
        
# Creo una ventana
raiz = tk.Tk()

# En la ventana creo un lienzo
lienzo = tk.Canvas (width=1024,height=1024)
lienzo.pack()

# En la colección introduzco instancias de personas
for i in range(0,numeropersonas):
    personas.append(Persona())
    
# Pinto cada una de las personas en la colección
for persona in personas:
    persona.dibuja()
    
# Creo un bucle repetitivo
def bucle():
    # Muevo cada una de las personas en la colección
    for persona in personas:
        persona.mueve()
    raiz.after(100,bucle)

# Ejecuto el bucle
bucle()

raiz.mainloop()
