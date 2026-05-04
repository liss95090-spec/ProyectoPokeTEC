
import tkinter as tk
from tkinter import *
from os import path
from tkinter import PhotoImage
from tkinter import messagebox
import random
import json
from os import path


puntos_jugador = 0
nombre_usuario_final = ""

ventana = tk.Tk()
ventana.title("PokeTEC")
ventana.minsize(1300,664)
ventana.resizable(width=NO, height=NO)
fuente_general = ('Times New Roman', 15)


#_-_-_-_-_-_Lista de los pokemones y Avatares-_-_-__-----
lista_pokemones={
    "Pikachu":"pikachu.png",
    "Charizard":"charizard.png",
    "Mewtow":"mewtwo.png",
    "Rayquaza":"Rayquaza.png",
    "Infernape":"infernape.png",
    "Milotic": "milotic.png",
    "Dragapult":"dragapult.png",
    "Froslass":"froslass.png",
    "Zoroark":"zoroark.png",
    "Garganacl":"garganacl.png"
    }

#  Estadisticas
# [Vida Máxima, Ataque, Defensa]
stats_base = {
    "Pikachu":   {"hp_max": 125, "atq": 170, "def": 10},
    "Charizard": {"hp_max": 180, "atq": 110, "def": 50},
    "Mewtow":    {"hp_max": 180, "atq": 110, "def": 60},
    "Rayquaza":  {"hp_max": 200, "atq": 110, "def": 60},
    "Infernape": {"hp_max": 180, "atq": 130, "def": 40},
    "Milotic":   {"hp_max": 420, "atq": 60, "def": 100},
    "Dragapult": {"hp_max": 180, "atq": 130, "def": 40},
    "Froslass":  {"hp_max": 170, "atq": 160, "def": 20},
    "Zoroark":   {"hp_max": 180, "atq": 140, "def": 40},
    "Garganacl": {"hp_max": 480, "atq": 40, "def": 100}
}

#  Diccionario para rastrear la VIDA ACTUAL durante la pelea
# Empezamos con la vida llena
hp_actual = {nombre: stats_base[nombre]["hp_max"] for nombre in stats_base}


lista_avatares={
    "Chico A":"chicoA.png",
    "Chica A":"chicaA.png",
    "Chico B":"chicoB.png",
    "Chica B":"chicaB.png",
    "Chica C":"chicaC.png",


    "rival":"rival.png"
}

# Variable global para guardar el orden 
orden_seleccion = []


#_______-_-_-_---_-_--FONDO-__---------____---

def cargar_img(nombre):
    ruta  = path.join ('C:/Users/lisa1/OneDrive/Documents/Poketec', nombre)
    img=PhotoImage(file=ruta)
    return img

C_principal = Canvas(ventana, width=1300, height=664, bg='red')
C_principal.place(x=0,y=0) 



C_principal.fondo = cargar_img('fondo.png')
Fondo1 = C_principal.create_image(0,0,anchor=NW, image=C_principal.fondo)

#______________________________________________________________________________________

# ---  FUNCIÓN PARA EL RANKING ---
def gestionar_ranking(nombre_usuario, puntos):
    carpeta_destino = "C:/Users/lisa1/OneDrive/Documents/Poketec"
    archivo = "ranking.json"
    
    if not nombre_usuario: 
        nombre_usuario = "Entrenador"
        
    nuevo_registro = {"nombre": nombre_usuario, "puntos": puntos}
    datos_ranking = []

    if path.exists(archivo):
        with open(archivo, "r") as f:
            try:
                datos_ranking = json.load(f)
            except:
                datos_ranking = []

    datos_ranking.append(nuevo_registro)
    datos_ranking = sorted(datos_ranking, key=lambda x: x['puntos'], reverse=True)

    with open(archivo, "w") as f:
        json.dump(datos_ranking, f, indent=4)

#-------------FUNCION DONDE SE SELECCIONA EL ORDEN DEL POKEMON.....

def registrar_clic_manual():
    #  Ver cuantos hay marcados en la lista
    seleccionados = lista_pokes.curselection()
    
        # Buscamos cuál fue el último clic comparando con nuestro orden guardado
    if len(seleccionados) > 3:
        for i in seleccionados:
            nombre = lista_pokes.get(i)
            if nombre not in orden_seleccion:
                lista_pokes.selection_clear(i)
        return

    #Actualizar nuestro orden interno
    marcados_nombres = [lista_pokes.get(i) for i in seleccionados]
    
    for p in orden_seleccion[:]:
        if p not in marcados_nombres:
            orden_seleccion.remove(p)
            
    for p in marcados_nombres:
        if p not in orden_seleccion:
            orden_seleccion.append(p)
#-------------------------------------------------------------------

#----------Funciones del Combate-----------


def ejecutar_ataque_por_turnos(pj, pr, canvas, txt_j, txt_r, pokes_rival, btn):
    #  Bloqueamos el botón para evitar clics dobles
    btn.config(state=DISABLED, bg="gray")

    # Cálculo del daño 
    dano_al_rival = max(15, stats_base[pj]["atq"] - stats_base[pr]["def"])
    hp_actual[pr] -= dano_al_rival
    
    # Actualizamos la vida en el canvas
    canvas.itemconfig(txt_r, text=f"HP: {max(0, hp_actual[pr])}")

    #  Si el rival murió, el KO y se detiene la función
    if hp_actual[pr] <= 0:
        verificar_ko(pj, pr, pokes_rival, canvas, txt_j, txt_r)
        
        # Si la ventana aún existe (porque quedan más rivales), reactivamos el botón
        if ventana.winfo_exists():
            btn.config(state=NORMAL, bg="red")
        return 

    # Si el rival sigue vivo, esperamos 1 segundo y ataca él
    ventana.after(1000, lambda: turno_rival(pokes_rival, canvas, txt_j, txt_r, btn))

def turno_rival(pokes_rival, canvas, txt_j, txt_r, btn):
    # Usamos las globales para atacar a los pokémon que estén en pantalla en ese momento
    global nombre_poke_elegido, poke_rival_actual
    
    #  ATAQUE DEL RIVAL 
    dano_al_jugador = max(15, stats_base[poke_rival_actual]["atq"] - stats_base[nombre_poke_elegido]["def"])
    hp_actual[nombre_poke_elegido] -= dano_al_jugador
    canvas.itemconfig(txt_j, text=f"HP: {max(0, hp_actual[nombre_poke_elegido])}")

    # Verificar si el pokemon sigue vivo
    if hp_actual[nombre_poke_elegido] <= 0:
        verificar_ko(nombre_poke_elegido, poke_rival_actual, pokes_rival, canvas, txt_j, txt_r)

    #  Reactivamos el botón después del contraataque
    btn.config(state=NORMAL, bg="red")

def verificar_ko(pj, pr, pokes_rival, canvas, id_txt_j, id_txt_r):
    global nombre_poke_elegido, poke_rival_actual, puntos_jugador, orden_seleccion
    global nombre_usuario_final
    

    if hp_actual[pr] <= 0:
        puntos_jugador += 1 
        hp_actual[pr] = stats_base[pr]["hp_max"]
        if pr in pokes_rival: pokes_rival.remove(pr)
        orden_seleccion.append(pr)
        
        if len(pokes_rival) > 0:
            messagebox.showinfo("¡CAPTURADO!", f"¡{pr} ha caído! (+1 punto)")
            poke_rival_actual = pokes_rival[0]
            actualizar_visual_combate(poke_rival_actual, "rival", canvas)
            canvas.itemconfig(id_txt_r, text=f"HP: {hp_actual[poke_rival_actual]}")
        else:
            # VICTORIA 
            gestionar_ranking(nombre_usuario_final, puntos_jugador)
            messagebox.showinfo("FIN DEL JUEGO", f"¡Victoria!\nRanking guardado para: {nombre_usuario_final}")
            ventana.quit()
            ventana.destroy()
            return

    elif hp_actual[pj] <= 0:
        hp_actual[pj] = stats_base[pj]["hp_max"]
        if pj in orden_seleccion: orden_seleccion.remove(pj)
        pokes_rival.append(pj)
        
        if len(orden_seleccion) > 0:
            messagebox.showwarning("¡DERROTA!", f"¡Tu {pj} ha sido capturado!")
            nombre_poke_elegido = orden_seleccion[0]
            actualizar_visual_combate(nombre_poke_elegido, "jugador", canvas)
            canvas.itemconfig(id_txt_j, text=f"HP: {hp_actual[nombre_poke_elegido]}")
        else:
            # DERROTA 
            gestionar_ranking(nombre_usuario_final, puntos_jugador)
            messagebox.showerror("GAME OVER", f"Puntos: {puntos_jugador}")
            ventana.quit()
            ventana.destroy()
            return
            
def actualizar_visual_combate(nombre_poke, tipo, canvas):
    archivo = lista_pokemones[nombre_poke]
    nueva_img = cargar_img(archivo)
    if tipo == "jugador":
        ventana.img_poke_combate = nueva_img
        canvas.itemconfig(ventana.id_img_pj, image=ventana.img_poke_combate)
    else:
        ventana.img_pk_riv = nueva_img
        canvas.itemconfig(ventana.id_img_pr, image=ventana.img_pk_riv)


#_________________________________________________pantalla de combate
def ir_a_combate():
    global nombre_poke_elegido, poke_rival_actual, pokes_rival_lista # Globales para control
    global nombre_usuario_final

    nombre = entrada_nombre.get()
    indice_ava = lista_ava.curselection()
    
    if nombre == "" or len(orden_seleccion) != 3 or not indice_ava:
        messagebox.showwarning("Error", "Revisa tu nombre, elige 3 Pokémon y un Avatar")
        return
    
    nombre_usuario_final = nombre

    #  Definir quiénes pelean
    nombre_poke_elegido = orden_seleccion[0]
    nombre_avatar_elegido = lista_ava.get(indice_ava[0])
    
    avatar_rival_fijo = "rival" 
    todos_los_pokes = list(lista_pokemones.keys())
    # Creamos la lista del rival (excluyendo los que ya tiene el jugador para que no se repitan)
    pokes_disponibles_rival = [p for p in todos_los_pokes if p not in orden_seleccion]
    pokes_rival_lista = random.sample(pokes_disponibles_rival, 3)
    poke_rival_actual = pokes_rival_lista[0]

    #  LIMPIAR PANTALLA
    for widget in ventana.winfo_children():
        widget.destroy()

    #  CREA CANVAS
    canvas_batalla = Canvas(ventana, width=1300, height=664, highlightthickness=0)
    canvas_batalla.pack(fill="both", expand=True)

    #  FONDO EN LA PANTALLA DE COMBATE
    ventana.img_fondo_combate = cargar_img('fondocombate.png') 
    canvas_batalla.create_image(0, 0, anchor=NW, image=ventana.img_fondo_combate)

    #  CARGAR IMÁGENES 
    ventana.img_avatar_combate = cargar_img(lista_avatares[nombre_avatar_elegido])
    ventana.img_poke_combate = cargar_img(lista_pokemones[nombre_poke_elegido])
    ventana.img_av_riv = cargar_img(lista_avatares[avatar_rival_fijo])
    ventana.img_pk_riv = cargar_img(lista_pokemones[poke_rival_actual])

    # DIBUJAR EN CANVAS Y GUARDAR IDS
    # Avatar Jugador
    canvas_batalla.create_image(200, 450, image=ventana.img_avatar_combate, anchor=CENTER)
    # Pokémon Jugador (ID Guardado)
    ventana.id_img_pj = canvas_batalla.create_image(450, 500, image=ventana.img_poke_combate, anchor=CENTER)
    
    # Avatar Rival
    canvas_batalla.create_image(1050, 200, image=ventana.img_av_riv, anchor=CENTER)
    # Pokémon Rival (ID Guardado)
    ventana.id_img_pr = canvas_batalla.create_image(850, 250, image=ventana.img_pk_riv, anchor=CENTER)

    #  TEXTOS DE VIDA
    texto_hp_jugador = canvas_batalla.create_text(440, 350, 
                        text=f"HP: {hp_actual[nombre_poke_elegido]}", 
                        font=(fuente_general, 18, "bold",), fill="red")


    texto_hp_rival = canvas_batalla.create_text(850, 400, 
                        text=f"HP: {hp_actual[poke_rival_actual]}", 
                        font=(fuente_general, 18, "bold"), fill="red")


    # 8. BOTÓN ATACAR
    btn_atacar = Button(ventana, text="¡ATACAR!", bg="red", fg="white", font=(fuente_general, 12, "bold"))

    btn_atacar.config(command=lambda: ejecutar_ataque_por_turnos(
                            nombre_poke_elegido, 
                            poke_rival_actual, 
                            canvas_batalla, 
                            texto_hp_jugador, 
                            texto_hp_rival,
                            pokes_rival_lista,
                            btn_atacar
                        ))
    btn_atacar.place(x=600, y=50, width=150, height=50)

    

# --- PANTALLA DE INICIO ---


#---Lista de Pokemones
lista_pokes=Listbox(ventana, selectmode=MULTIPLE, font=fuente_general,width=9, height=10, exportselection=0,bg="#87CEFA")
lista_pokes.place(x=10, y=10)
for p in lista_pokemones:
    lista_pokes.insert(END, p)

# DETECTA EL CLIC PARA SELECCIONAR EL ORDEN----------------------------------
lista_pokes.bind("<<ListboxSelect>>", lambda e: registrar_clic_manual())

# ---Lista de los avatares
lista_ava=Listbox(ventana, selectmode=SINGLE, font=fuente_general,width= 9, height=5, exportselection=0,bg="#87CEFA")
lista_ava.place(x=210, y=10)
for p in lista_avatares:
    lista_ava.insert(END, p)



#---------------------------------------------------------------------------------------------

entrada_nombre = Entry(ventana,width=30 ,bg="#C0C0C0")

entrada_nombre.place(x=450,y=10)


Btn_empezar = Button(ventana, text='¡EMPEZAR!',command=ir_a_combate,font=(fuente_general,15),bg= "#90EE90", width=10, height=2)
Btn_empezar.place(x=480, y=40)



ventana.mainloop()




