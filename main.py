import telebot.ext
import usefull_functions 
import root_callbacks.Canales_callback as Canales_callback
import root_callbacks.publicaciones_callback as publicaciones_callback
import root_callbacks.copia_seguridad_callback as copia_seguridad_callback
from Publicaciones_class import Publicaciones
import re
import threading
import time
import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
import dill
from flask import Flask, request
from telebot.ext import M






os.chdir(os.path.dirname(os.path.abspath(__file__)))


# HOST_URL = os.environ["mongodb_url"]
HOST_URL = "mongodb://localhost:27017"


#----------------Variables------------------------
telebot.apihelper.ENABLE_MIDDLEWARE = True
bot=telebot.TeleBot(os.environ["token"], "html", disable_web_page_preview=True)


# admin=1413725506
admin = os.environ["admin"]
lote_publicaciones={}
lista_canales=[]
lista_seleccionada=[]
if os.name=="nt":
    OS="\\"
else:
    OS="/"

hilo_publicaciones_activo=False
hilo_publicar=False
dic_temp = {}
operacion = ""

####################Constantes END##################

try:
    print(f"La dirección del servidor es:{request.host_url}")
except:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Hello World"

    def flask():
        app.run(host="0.0.0.0", port=5000)



try:
    print(f"La dirección del servidor es:{request.host_url}")
except:
    hilo_flask=threading.Thread(name="hilo_flask", target=flask)
    hilo_flask.start()


    
       


# Bucle para Publicar





if not "Publicaciones_media" in os.listdir():
    os.mkdir("Publicaciones_media")
    
#Crear la conexion con la base de datos de los canales
conexion, cursor = usefull_functions.cargar_conexion()

    
    
def cargar_variables():

    
    
    with open("publicaciones.dill", "rb") as archivo:
        lote_publicaciones=dill.load(archivo)
        globals()["lote_publicaciones"] = lote_publicaciones
        

    return lote_publicaciones
        
    # if cargar=="variables" or cargar=="all":
    #     with open("variables.dill", "rb") as archivo:
    #         lote_variables=dill.load(archivo)
    #         for key, item in lote_variables.items():
    #             globals()[str(key)] = item

    #     if cargar == "variables":
    #         return lote_variables
    
    # return lote_publicaciones, lote_variables
    

def guardar_variables(nuevo=False):
    

    
    if nuevo != False:
        with open("publicaciones.dill", "wb") as archivo:
            dill.dump({}, archivo)

    with open("publicaciones.dill", "wb") as archivo:
        dill.dump(lote_publicaciones, archivo)
    
        
    return "OK"
        
        
    
if os.path.isfile("publicaciones.dill"):
    lote_publicaciones=cargar_variables()
    
    for publicacion in lote_publicaciones:
        lote_publicaciones[publicacion].proxima_publicacion=False
        lote_publicaciones[publicacion].tiempo_eliminacion=False
        lote_publicaciones[publicacion].proxima_eliminacion=False
        # if lote_publicaciones[publicacion].lista_message_id_eliminar:
        #     usefull_functions.eliminar_publicacion(lote_publicaciones[publicacion], bot, cursor, admin, lote_publicaciones)
            

else:
    guardar_variables(nuevo=True)
    
    
    
conexion, cursor = usefull_functions.cargar_conexion()

    
bot.send_message(admin, "Estoy online bitch >:D")





def agregar_multimedia(publicacion, message):
    os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Publicaciones_media") #Redirección a la carpeta de medios para guardar el archivo

    if message.content_type=="photo":
        with open(f"{publicacion.ID}_{os.path.basename(bot.get_file(message.photo[-1].file_id).file_path)}", "wb") as archivo:
            archivo.write(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
            publicacion.multimedia=[os.path.abspath(archivo.name), "photo"]
            
            
    elif message.content_type=="video":
        with open(f"{publicacion.ID}_{os.path.basename(bot.get_file(message.video.file_id).file_path)}", "wb") as archivo:
            archivo.write(bot.download_file(bot.get_file(message.video.file_id).file_path))
            publicacion.multimedia=[os.path.abspath(archivo.name), "video"]
            
            
    elif message.content_type=="audio":
        
        try:
            extension="." + str(os.path.basename(bot.get_file(message.audio.file_id).file_path).split(".")[-1])
            nombre=f"{message.audio.performer} - {message.audio.title}{extension}"
        except:
            contador=0
            for i in message.audio.file_name:
                if not i.isdigit():
                    break
                else:
                    contador+=1
                    
            nombre=f"{message.audio.file_name[contador:]}"
            
        with open(f"{publicacion.ID}_{nombre}", "wb") as archivo:
            archivo.write(bot.download_file(bot.get_file(message.audio.file_id).file_path))
            publicacion.multimedia=[os.path.abspath(archivo.name), "audio"]
    


            
    elif message.content_type=="document":
        with open(f"{publicacion.ID}_{os.path.basename(bot.get_file(message.document.file_id).file_path)}", "wb") as archivo:
            archivo.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
            publicacion.multimedia=[os.path.abspath(archivo.name), "document"]
            
    else:
        print("Al parecer, no había ningún documento que pudiera guardar")
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        return False

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return True



bot.set_my_commands([
    BotCommand("/help", "Ayuda con el bot"),
    BotCommand("/panel", "Acceso al panel de control")
])


# telebot.apihelper.ENABLE_MIDDLEWARE = True

#----------------------------------------------------Handlers----------------------------------------------------


@bot.middleware_handler()
def revision(bot, update):
    global cursor
    if update.callback_query:
        print(update.callback_query.data)
        try:
            cursor.execute("SELECT ID FROM CANALES")
        except:
            conexion, cursor = usefull_functions.cargar_conexion()

        
    return




@bot.message_handler(func=lambda message: not int(message.chat.id)==int(admin))
def cmd_being_sure_you_are_admin(message):
    if not message.chat.type == "private":
        del message
        return
    
    
    bot.send_message(message.chat.id,f"Lo siento :( Este bot <b>SOLAMENTE</b> puede ser usado por @{bot.get_chat(admin).username}")
    bot.send_message(message.chat.id, "Bot creado por @mistakedelalaif")
    del message
    return





@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    if not message.chat.type== "private":
        return
    
    bot.send_message(message.chat.id, f"Bienvenido {bot.get_chat(admin).first_name} :D\n\nSoy un bot que hace mensajes personalizados y los envía a una serie de canales (Si estoy autorizado a publicar en ellos claro...)\nPuedes definir el tiempo de duración de las publicaciones y los canales a los que serán dirigidos los mensajes, por supuesto\n\nEnvíame /panel para comenzar :)")
    bot.send_message(message.chat.id, "Bot creado por @mistakedelalaif")








    

    
    
#---------------------------callbacks---------------------------------
    
@bot.callback_query_handler(func=lambda call: "volver_menu" in call.data)
@bot.message_handler(commands=["panel"])
def cmd_panel(message):
    
    global operacion
    if os.path.isfile("BD_Canales_prueba.db"):
        os.remove("BD_Canales_prueba.db")
        
    
    panel=InlineKeyboardMarkup(row_width=1)
    panel.add(
        # InlineKeyboardButton("Ver el ID de las Publicaciones 👀📋", callback_data="ver_publicaciones"),
        # InlineKeyboardButton("Ver el Grupos/Canales disponibles 👀💻", callback_data="ver_canales"),
        # InlineKeyboardButton("Agregar/Quitar Canal(es) 💻", callback_data="lista_canales"),
        # InlineKeyboardButton("Agregar/Quitar publicación 📋🪒", callback_data="publicacion"),
        # InlineKeyboardButton("Agregar/Quitar canales a una Publicacion", callback_data="agregar_publicacion"),
        # InlineKeyboardButton("Tiempo Eliminación de Publicación 💥", callback_data="eliminar_publicacion"),
        # InlineKeyboardButton("Comenzar a Publicar 🚦", callback_data="comenzar_hilo"),
        
        
        InlineKeyboardButton("Canales 💻", callback_data="lista_canales_elegir"),
        InlineKeyboardButton("Crear Post ✨", callback_data="publicacion"),
        InlineKeyboardButton("Ver post creados 👁", callback_data="ver_publicaciones"))
    
    if hilo_publicaciones_activo == True:
        panel.add(
            InlineKeyboardButton("Parar hilo de publicación 🛑", callback_data="admin_hilo"),
            InlineKeyboardButton("Cargar/Enviar Copia de Seguridad ⛽", callback_data="copia_seguridad")
        )
        
    else:
        panel.add(
            InlineKeyboardButton("Inciar hilo de publicación 💡", callback_data="admin_hilo"),
            InlineKeyboardButton("Cargar/Enviar Copia de Seguridad ⛽", callback_data="copia_seguridad")
        ) 
    
    
        
    if "CallbackQuery" in str(type(message)):

        call = message
        
        
        if not call.message.chat.type == "private":
            bot.send_message(message.chat.id, "Tienes que hacer esta petición en mi chat privado")
            return
        
        usefull_functions.enviar_mensajes(bot, call, f"Bienvenido {bot.get_chat(call.message.chat.id).first_name} :) ¿En qué te puedo ayudar?", markup=panel)
        
            
    else:
        
        if not message.chat.type == "private":
            bot.send_message(message.chat.id, "Tienes que hacer esta petición en mi chat privado")
            return
        try:
            if not "N" in call.data:
                usefull_functions.enviar_mensajes(bot, message, f"Bienvenido {bot.get_chat(message.chat.id).first_name} :) ¿En qué te puedo ayudar?", panel, message)
                
            else:
                usefull_functions.enviar_mensajes(bot, message, f"Bienvenido {bot.get_chat(message.chat.id).first_name} :) ¿En qué te puedo ayudar?", panel)
                
        except:
            usefull_functions.enviar_mensajes(bot, message, f"Bienvenido {bot.get_chat(message.chat.id).first_name} :) ¿En qué te puedo ayudar?", panel)
        
    return



@bot.callback_query_handler(func=lambda call: "canal" in call.data)
def callback_lista_canales_elegir(call):
    Canales_callback.main_handler(bot,call, cursor, admin , conexion, lote_publicaciones, lista_canales, lista_seleccionada, hilo_publicaciones_activo, dic_temp, operacion)






@bot.callback_query_handler(func=lambda call: "publicacion" in call.data or "operacion" in call.data)
def callback_publicacion(call):

    operacion = publicaciones_callback.l_operacion
    
    publicaciones_callback.main_handler(bot,call, cursor, admin , conexion, lote_publicaciones, lista_canales, lista_seleccionada, hilo_publicaciones_activo, dic_temp, operacion)






@bot.callback_query_handler(func=lambda call: call.data == "admin_hilo")
def callback_publicacion(call):
    global hilo_publicar, hilo_publicaciones_activo 
        
    if hilo_publicaciones_activo==True:
        hilo_publicaciones_activo=False
        bot.send_message(call.from_user.id, "A continuación pararé el hilo. Te notificaré cuando lo esté\n\nTiempo estimado máximo para detenerlo: 1 minuto")
        
        for publicacion in lote_publicaciones:
            lote_publicaciones[publicacion].proxima_publicacion = False
            
        guardar_variables()
        


    else:
        if len(lote_publicaciones)==0:
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Agregar publicación 📋🪒", callback_data="publicacion"))
            bot.send_message(call.from_user.id, "¡No hay siquiera publicaciones en la lista!\n\nAgrega alguna publicación para empezar", reply_markup=markup)
            return
            
        hilo_publicaciones_activo=True
        
        guardar_variables()
        
        bot.send_message(call.from_user.id, "Muy Bien, Iniciaré el <b>Hilo de Publicaciones</b>")
        
        hilo_publicar=threading.Thread(name="hilo_publicar", target=usefull_functions.bucle_publicacion, args=(call.from_user.id, bot, hilo_publicaciones_activo, admin, lote_publicaciones, cursor))
        
        hilo_publicar.start()
    
    
    return   






@bot.callback_query_handler(func=lambda call:  "copia_seguridad" in call.data or "db" in call.data)
def callback_publicacion(call):
    copia_seguridad_callback.main_handler(bot, call, hilo_publicaciones_activo, HOST_URL, conexion, cursor, lote_publicaciones)
    
    return



    

    
    
#---------------------------callbacksEND---------------------------------

@bot.message_handler(func=lambda message: True)
def cmd_dont_be_shy(message):
    if not message.chat.type== "private":
        return
    
    bot.send_message(message.chat.id, "Tienes que escribir algo chacal, sino no sabré qué quieres que haga\n\nEmpieza con /help")
    


        
    
    
    

bot.infinity_polling()
