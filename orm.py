import tkinter as tk
import random
import math
import json

personas = []
numeropersonas = 20

class Persona:
    def __init__(self):
        self.posx = random.randint(0,840)
        self.posy = random.randint(0,840)
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
        self.colisiona()
        lienzo.move(self.entidad,
                    math.cos(self.direccion),
                    math.sin(self.direccion))
        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)
        
    def colisiona(self):
        if self.posx < 0 or self.posx > 840 or self.posy < 0 or self.posy > 840:
            self.direccion += 180
            
def guardarPersona():
    print("Guardo a los jugadores")
    cadena = json.dumps([vars(persona) for persona in personas])
    print(cadena)
    
# Creo una ventana
raiz = tk.Tk()

# En la ventana creo un lienzo
lienzo = tk.Canvas (raiz,width=840,height=840)
lienzo.pack()

#Botón de guardar
boton = tk.Button(raiz,text="Guardar",command=guardarPersona)
boton.pack()

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
    raiz.after(10,bucle)

# Ejecuto el bucle
bucle()

raiz.mainloop()
