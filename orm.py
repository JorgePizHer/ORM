import tkinter as tk
import random
import math
import json
import sqlite3

#Declaración de variables globales
personas = []
numeropersonas = 500

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
    
##    #Guardo archivo json
##    cadena = json.dumps([vars(persona) for persona in personas])
##    print(cadena)
##    archivo = open("jugadores2.json",'w')
##    archivo.write(cadena)
    
    #Guardo los personajes en SQL
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()
    cursor.execute('''
            TRUNCATE jugadores
            ''')
    cursor.commit()

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
                "'''+str(persona.entidad)+'''"
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

#Cargar personas desde el disco duro
##try:
##    carga = open("jugadores2.json",'r')
##    cargado = carga.read()
##    cargadolista = json.loads(cargado)
##    for elemento in cargadolista:
##        persona = Persona() #Creación de un nuevo objeto persona
##        persona.__dict__.update(elemento) #Se vuelca la información del elemento en la persona creada
##        personas.append(persona) #Se añade la persona al array de personas
##except:
##    print("Error")

#Al ser un bucle, se repite esto para cada uno de los elementos en cargadolista

#Cargar personas desde SQL

try:
    conexion = sqlite3.connect("jugadores.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''
            SELECT *
            FROM jugadores
            WHERE posx < 216
            AND
            posy < 216
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
        personas.append(persona)

##        For each row fetched from the database, a new Persona object is created.
##        The attributes of the Persona object (posx, posy, radio, direccion, color, entidad)
##        are then populated with the values from the corresponding columns in the database row.
##        The persona object is then added to a list named personas
    
    conexion.close()
except:
    print("Error al leer base de datos")


print(len(personas))   
# En la colección introduzco instancias de personas en el caso de que no existan
##if len(personas) == 0:
##    numeropersonas = 500
##    for i in range(0,numeropersonas):
##        personas.append(Persona())
    
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
