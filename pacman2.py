#pacman2.py
#Carla Perez, Aranza Garcia
#Juego de pacman con fantasmas más inteligentes y rápidos y con diferente tablero.

from random import choice
from turtle import *
from freegames import floor, vector
import math

path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
sp=10 #Para hacer a los fantasmas más rapidos se tiene que tener una variable la cual se pueda sustituir en los vectores para aumentar la velocidad.
ghosts = [
    [vector(-180, 160), vector(sp, 0)],
    [vector(-180, -160), vector(0, sp)],# Se sustutuyeron las posiciones +-5 con la variable sp
    [vector(100, 160), vector(0, -sp)],
    [vector(100, -160), vector(-sp, 0)],
]
#Se modificó el tablero del original para que tuviera diferentes características
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    i = 1

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(sp, 0),
                vector(-sp, 0),
                vector(0, sp),  #De igual manera se sustituye sp aqui ya que son los movimientos de los fantasmas.
                vector(0, -sp),
            ]
            


            #course.x = plan.x
            #course.y = plan.y
            
            #get pacman offset
            poff = offset(pacman) #0-posibles índices de las casillas de la lista
            pcol = poff%20 # Encuentra la columna donde se encuentra Pacman
            pren = math.floor(poff/20) #Encuentra el renglón donde se encuentra Pacman
            
            #get ghost offset
            goff = offset(point)
            gcol = goff%20 # Encuentra la columna donde se encuentra el fantasma
            gren = math.floor(goff/20) #Encuentra el renglón donde se encuentra el fantasma
            if(pcol < gcol and pren < gren):
                #elegir arriba o a la izq
                options = [
                    vector(-sp, 0),
                    vector(0, sp), #De igual manera se sustituye sp porque son los movimientos del fantasma
                ]
            if (pcol > gcol and pren < gren):
                #elegir arriba o a la der
                options = [
                    vector(sp, 0),#De igual manera se sustituye sp porque son los movimientos del fantasma
                    vector(0, sp),
                ] 
            if(pcol < gcol and pren > gren):
                #elegir abajo o a la izq
                options = [
                    vector(-sp, 0), #De igual manera se sustituye sp porque son los movimientos del fantasma
                    vector(0, -sp),
                ]
            if(pcol > gcol and pren > gren):
                #elegir abajo o a la der
                options = [
                    vector(sp, 0), #De igual manera se sustituye sp porque son los movimientos del fantasma
                    vector(0, -sp),
                ]
            #escoger alguna opción
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 50)

def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
