import telebot
from Publicaciones_class import Publicaciones
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
import sqlite3
import dill
import os
from flask import Flask, request
import re
import threading
import time


os.chdir(os.path.dirname(os.path.abspath(__file__)))

#----------------Constantes------------------------

bot=telebot.TeleBot(os.environ["token"], "html", disable_web_page_preview=True)
admin=os.environ["admin"]
lote_publicaciones={}
lista_canales=[]
if os.name=="nt":
    OS="\\"
else:
    OS="/"
    
hilo_publicaciones_activo=False
hilo_publicar=False

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


    
        


#====================Bucle para publicar===============================

def enviar_publicacion(publicacion, user):
    global lote_publicaciones

    if not publicacion.canales:
        bot.send_message(user, f"¡La Publicación <b>{publicacion.ID}</b> no tiene ningún canal al que enviar su contenido!\n\n¡Agrégale alguno!")
        return
    
    if publicacion.lista_message_id_eliminar:
        
        for e,mensaje in enumerate(publicacion.lista_message_id_eliminar, start=0):
            try:
                bot.delete_message(publicacion.canales[e], mensaje.message_id)
            except:
                for canal_error in cursor.fetchall():
                    if canal_error[0]==canal:
                        bot.send_message(user, f"No se pudo eliminar el mensaje al canal: {canal_error[1]}, su ID es: {canal_error[0]}\n\nRevisa que yo posea los permisos administrativos y de publicar, o que el canal/grupo siquiera siga existiendo")
        
        
    lista_message_id_eliminar=[]
    publicacion.proxima_publicacion=time.time()+publicacion.tiempo_publicacion

    if publicacion.tiempo_eliminacion:
        publicacion.proxima_eliminacion=time.time()+publicacion.tiempo_eliminacion
        
   
    for canal in publicacion.canales:
        try:
            diccionario_publicacion, lista_opcional=publicacion.mostrar_publicacion()
            for lista in diccionario_publicacion:
                
                
                if lista=="photo":
                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_photo(canal, archivo , caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg)
                    
                        else:
                            msg=bot.send_photo(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                        
                elif lista=="video":
                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_video(canal, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg.message_id)
                        
                        else:
                            msg=bot.send_video(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                
                elif lista=="audio":
                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_audio(canal, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg)
                        
                        else:
                            msg=bot.send_audio(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                
                elif lista=="document":
                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_document(canal, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg)
                            
                        else:
                            msg=bot.send_document(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                
                elif lista=="text":
                    if len(diccionario_publicacion[lista])==2:
                        msg=bot.send_message(canal, diccionario_publicacion[lista][0], reply_markup=diccionario_publicacion[lista][1])
                        lista_message_id_eliminar.append(msg)
                    
                    else:
                        msg=bot.send_message(canal, diccionario_publicacion[lista][0])
                        lista_message_id_eliminar.append(msg)
                
                
                elif lista=="error":
                    bot.send_message(user, f"Ha ocurrido un error. Notifíquele este mensaje a @mistakedelalaif\n\n<u>Descripción del Error</u>:\n{diccionario_publicacion[lista][0]}")
                    return
                
            
                
        except Exception as e:
            cursor.execute('SELECT * FROM CANALES')
            for canal_error in cursor.fetchall():
                if canal_error[0]==canal:
                    bot.send_message(admin, f"No se pudo enviar el mensaje al canal/grupo: <b>{canal_error[1]}</b>, su ID es: <code>{canal_error[0]}</code>\n\nRevisa que yo posea los permisos administrativos y de publicar, o que el canal/grupo siquiera siga existiendo. Mi recomendación es que borre dicho Canal/Grupo de la Publicación y de la Base de Datos\n\n<u><b>Descripción del error</b></u>:\n{e}", parse_mode="html")
            continue
        
        
    publicacion.lista_message_id_eliminar=lista_message_id_eliminar
    
    guardar_variables()

    return


def eliminar_publicacion(publicacion):
    
    for e,mensaje in enumerate(publicacion.lista_message_id_eliminar, start=0):
        try:
            bot.delete_message(publicacion.canales[e], mensaje.message_id)
        except Exception:
            cursor.execute('SELECT * FROM CANALES')
            
            for e, canal_error in enumerate(cursor.fetchall(), start=0):
                if canal_error[0]==publicacion.canales[e]:
                    bot.send_message(admin, f"No se pudo eliminar el mensaje del canal/grupo: {canal_error[1]}, su ID es: <code>{canal_error[0]}</code>\n\nRevisa que yo posea los permisos administrativos y de publicar, que el canal/grupo siquiera siga existiendo o que no haya alguien borrado la publicación antes que yo\n\n<u><b>Descripición del error</b></u>:")
                        
    publicacion.proxima_eliminacion=False
    publicacion.lista_message_id_eliminar=False
    guardar_variables()

    return



def bucle_publicacion(user):
    
    while hilo_publicaciones_activo==True:

        for publicacion in lote_publicaciones:
            
            if time.time()>=lote_publicaciones[publicacion].proxima_eliminacion and not lote_publicaciones[publicacion].proxima_eliminacion==False: 
                eliminar_publicacion(lote_publicaciones[publicacion])
            
            if time.time()>=lote_publicaciones[publicacion].proxima_publicacion or not lote_publicaciones[publicacion].proxima_publicacion:
                enviar_publicacion(lote_publicaciones[publicacion], user)
                                  
        time.sleep(60)
    bot.send_message(admin, "<u><b>Atención! ‼</b></u>\nEl hilo de publicaciones se ha detenido!")
    
    for publicacion in lote_publicaciones:
        lote_publicaciones[publicacion].proxima_publicacion=False
        lote_publicaciones[publicacion].proxima_eliminacion=False
        if lote_publicaciones[publicacion].lista_message_id_eliminar:
            eliminar_publicacion(lote_publicaciones[publicacion])
    
    return


#===============Fin del Bucle para publicar===========================






if not "Publicaciones_media" in os.listdir():
    os.mkdir("Publicaciones_media")

if not os.path.isfile("BD_Canales.db"):
    conexion=sqlite3.connect("BD_Canales.db", check_same_thread=False)
    cursor=conexion.cursor()
    cursor.execute("CREATE TABLE CANALES (ID INTEGER, NOMBRE VARCHAR)")
    
else:
    conexion=sqlite3.connect("BD_Canales.db", check_same_thread=False)
    cursor=conexion.cursor()
    
    
def cargar_variables():
    global lote_publicaciones
    with open("publicaciones.dill", "rb") as archivo:
        lote_publicaciones=dill.load(archivo)
    
    for publicacion in lote_publicaciones:
        lote_publicaciones[publicacion].proxima_publicacion=False
        lote_publicaciones[publicacion].tiempo_eliminacion=False
        lote_publicaciones[publicacion].proxima_eliminacion=False
        if lote_publicaciones[publicacion].lista_message_id_eliminar:
            eliminar_publicacion(lote_publicaciones[publicacion])
    
    return
    

def guardar_variables():
    
    with open("publicaciones.dill", "wb") as archivo:
        dill.dump(lote_publicaciones, archivo)
        
    return
        
        
    
if os.path.isfile("publicaciones.dill"):
    cargar_variables()
    
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




#----------------------------------------------------Handlers----------------------------------------------------

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
    bot.send_message(message.chat.id, f"Bienvenido {bot.get_chat(admin).first_name} :D\n\nSoy un bot que hace mensajes personalizados y los envía a una serie de canales (Si estoy autorizado a publicar en ellos claro...)\nPuedes definir el tiempo de duración de las publicaciones y los canales a los que serán dirigidos los mensajes, por supuesto\n\nEnvíame /panel para comenzar :)")
    bot.send_message(message.chat.id, "Bot creado por @mistakedelalaif")






@bot.message_handler(commands=["panel"])
def cmd_panel(message):
    
    panel=InlineKeyboardMarkup(row_width=1)
    panel.add(
        InlineKeyboardButton("Ver el ID de las Publicaciones 👀📋", callback_data="ver_publicaciones"),
        InlineKeyboardButton("Ver el Grupos/Canales disponibles 👀💻", callback_data="ver_canales"),
        InlineKeyboardButton("Agregar/Quitar Canal(es) 💻", callback_data="lista_canales"),
        InlineKeyboardButton("Agregar/Quitar publicación 📋🪒", callback_data="publicacion"),
        InlineKeyboardButton("Agregar/Quitar canales a una Publicacion", callback_data="agregar_publicacion"),
        InlineKeyboardButton("Tiempo Eliminación de Publicación 💥", callback_data="eliminar_publicacion"),
        InlineKeyboardButton("Comenzar a Publicar 🚦", callback_data="comenzar_hilo"),
        InlineKeyboardButton("Detener hilo de publicación 🛑", callback_data="detener_hilo")
        # InlineKeyboardButton("Cargar/Enviar Copia de Seguridad ⛽", callback_data="copia_seguridad")
        )
    bot.send_message(message.chat.id, f"Bienvenido {bot.get_chat(message.chat.id).first_name} :) ¿En qué te puedo ayudar?", reply_markup=panel)
    
    
    
    
    

    
@bot.callback_query_handler(func=lambda x: True)
def cmd_callback_handler(call):
    global hilo_publicar
    global hilo_publicaciones_activo
    global lote_publicaciones
    global lista_canales
    global admin
    user=call.from_user.id
    
    
    if call.data=="ver_publicaciones":
        
        if len(lote_publicaciones)==0:
            markup=InlineKeyboardMarkup()
            bot.send_message(call.from_user.id, "¡Aún no hay Publicaciones guardadas!\nHaz tu primera Publicación presionando en el botón '<b>Agregar/Quitar publicación 📋🪒</b>'", reply_markup=markup.add(InlineKeyboardButton("Agregar/Quitar publicación 📋🪒", callback_data="publicacion")))
            return
            
            
        def ver_publicaciones_id(call):
            user=call.from_user.id
            
            markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Presiona en el ID para ver la publicación", row_width=3)
            
            markup.row("Cancelar Operación")
            for publicacion in lote_publicaciones:
                ID=str(lote_publicaciones[publicacion].ID)
                markup.add(ID)
            
            

            
            msg=bot.send_message(user, "A continuación, selecciona el ID numérico de la publicación que quieres ver de las que están en el teclado de botones\n\nSi lo que deseas es salir de este panel presiona en '<b>Cancelar Operación</b>'", reply_markup=markup)
            
            def mostrar_publicacion_id(message):
                global lote_publicaciones
                if message.text=="Cancelar Operación":
                    bot.send_message(message.chat.id, "Muy bien :) Te devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                    return
                if not message.text.isdigit():
                    bot.send_message(message.chat.id, "¡Presiona las teclas del teclado que te proporcioné! ¡No escribas nada por tu cuenta!\n\nTe devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                    return
                else:
                    contador=0
                    for publicacion in lote_publicaciones:
                        if int(lote_publicaciones[publicacion].ID)==int(message.text):
                            diccionario_publicacion, lista_opcional=lote_publicaciones[publicacion].mostrar_publicacion()
                            for lista in diccionario_publicacion:
                                
                                if lista=="photo":
                                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                                        if len(diccionario_publicacion[lista])==3:
                                            bot.send_photo(message.chat.id, archivo , caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                    
                                        else:
                                            bot.send_photo(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                        
                                elif lista=="video":
                                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                                        if len(diccionario_publicacion[lista])==3:
                                            bot.send_video(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                        
                                        else:
                                            bot.send_video(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                
                                elif lista=="audio":
                                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                                        if len(diccionario_publicacion[lista])==3:
                                            bot.send_audio(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                        
                                        else:
                                            bot.send_audio(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                
                                elif lista=="document":
                                    with open(diccionario_publicacion[lista][0].name, "rb") as archivo:
                                        if len(diccionario_publicacion[lista])==3:
                                            bot.send_document(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                        
                                        else:
                                            bot.send_document(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                    
                                
                                elif lista=="text":
                                    if len(diccionario_publicacion[lista])==2:
                                        bot.send_message(message.chat.id, diccionario_publicacion[lista][0], reply_markup=diccionario_publicacion[lista][1])
                                    
                                    else:
                                        bot.send_message(message.chat.id, diccionario_publicacion[lista][0])
                                
                                
                                elif lista=="error":
                                    bot.send_message(message.chat.id, f"Ha ocurrido un error. Notifíquele este mensaje a @mistakedelalaif\n\n<u>Descripción del Error</u>:\n{diccionario_publicacion[lista][0]}")
                                    return
                            
                            
                            texto=""
                            if not lote_publicaciones[publicacion].canales:
                                texto+=f"Actualmente esa Publicación no tiene canales/grupos en los que se publica, agregue alguno"
                                
                            else:
                                for e, canal in enumerate(lote_publicaciones[publicacion].canales, start=1):
                                    try:
                                        if canal==lote_publicaciones[publicacion].canales[-1]:
                                            texto+=f"{e}- {bot.get_chat(canal).title}"
                                        else:
                                            texto+=f"{e}- {bot.get_chat(canal).title}\n"
                                    except:
                                        bot.send_message(message.chat.id, "Al parecer, hay un canal que ya ni siquiera existe, lo eliminaré")
                                        lote_publicaciones[publicacion].canales.remove(canal)
                                        return
                            
                            texto=f"<u><b>Esta publicación se distribuye por los siguientes canales</b></u>:\n\n{texto}"
                            
                            texto=f"<u><b>El ID de esta publicación es</b></u>: <b>{lote_publicaciones[publicacion].ID}</b>\n\n{texto}\n\n"
                            
                            texto+=f"Tiempo de publicaciones: {int(lote_publicaciones[publicacion].tiempo_publicacion/60)} minutos"
                            
                            if lote_publicaciones[publicacion].tiempo_eliminacion:
                                texto+=f"\n\nTiempo de eliminación de publicaciones: {int(lote_publicaciones[publicacion].tiempo_eliminacion/60)} minutos"
                            
                            bot.send_message(message.chat.id, texto, reply_markup=ReplyKeyboardRemove())
                            
                            contador+=1
                            
                            for i in lista_opcional:
                                bot.send_message(message.chat.id, i)
                                
                            
                            
                        
                        
                            
                    if contador==0:
                        bot.send_message(message.chat.id, "¡Presiona las teclas del teclado que te proporcioné! ¡No escribas nada por tu cuenta!\n\nTe devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                        return
                
                
                ver_publicaciones_id(call)
                
            bot.register_next_step_handler(msg, mostrar_publicacion_id)
                
                
                
        
        ver_publicaciones_id(call)
    
    
    elif call.data=="ver_canales":
        cursor.execute("SELECT * FROM CANALES")
        lista_canales_actual=cursor.fetchall()        
        texto="<u><b>Lista de canales y grupos del bot</b></u>:\n\n"
        
        cursor.execute("SELECT * FROM CANALES")
        if cursor.fetchall()==[]:
            bot.send_message(call.from_user.id, "¡La lista de canales está vacía! Ponle algunos canales y vuelve luego aquí para verlos\n\nTe devuelvo atrás")
            return
        
        
        for tupla_canal in lista_canales_actual:
            
            try:
                bot.get_chat(tupla_canal[0]).title
            except:
                bot.send_message(call.from_user.id, f"Ha ocurrido un error con el canal/grupo {tupla_canal[1]}\nSeguramente me expulsó, lo eliminaré de los canales")
                cursor.execute(f"DELETE FROM CANALES WHERE ID={tupla_canal[0]}")
                conexion.commit()
                continue
                
            if bot.get_chat(tupla_canal[0]).username:
                texto+=f"ID del canal/grupo: <code>{tupla_canal[0]}</code>, Nombre del grupo/canal: <b>{tupla_canal[1]}</b>, username: @{bot.get_chat(tupla_canal[0]).username}\n\n"
                
            else:
                texto+=f"ID del canal/grupo: <code>{tupla_canal[0]}</code>, Nombre del grupo/canal: <b>{tupla_canal[1]}</b>, username: Este canal es privado, no tiene\n\n"
        
        divisiones=0
        while True:
            if divisiones>0:
                for i in texto.split("\n\n", divisiones):
                    try:
                        bot.send_message(call.from_user.id, i.strip())
                        break
                    except:
                        divisiones+=1
            else:
                try:
                    bot.send_message(call.from_user.id, texto)
                    break
                except:
                    divisiones+=1
                    continue
    
    elif call.data=="lista_canales":
        
        if hilo_publicaciones_activo==True:
            bot.send_message(call.from_user.id, "❌¡No puedes cambiar las publicaciones mientras el hilo de botoneras está activo!❌\n\nVe al /panel y dale en '<b>Detener hilo de publicación 🛑</b>' y luego vuelve aquí o presiona en el botón de abajo si quieres detenerlo")
            return
        
        markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="¿Qué harás exactamente?", row_width=2).add("Agregar", "Quitar")
        msg=bot.send_message(call.from_user.id, "¿Qué pretendes hacer? ¿Agregar o quitar canales a/de la lista?", reply_markup=markup)
        
        
        
        def remove_channels(message):
            global conexion
            user=message.chat.id

            markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="ELija de uno en uno los canales", row_width=3)
            
            
            cursor.execute("SELECT * FROM CANALES")
            
            markup.row("Cancelar Operación")
            
            for canal in cursor.fetchall():
                markup.add(canal[1])
            
                
            msg=bot.send_message(call.from_user.id, "Elija un canal o presione '<b>Cancelar Operación</b>' para salir", reply_markup=markup)
            
            def process_channel_to_delete(message):
                global conexion
                global cursor
                global lote_publicaciones
                if message.text=="Cancelar Operación":
                    bot.send_message(message.chat.id, "Muy bien, eliminación cancelada :)", reply_markup=ReplyKeyboardRemove())
                    return
                
                contador=0
                publicaciones_vinculadas=""
                cursor.execute("SELECT * FROM CANALES")
                for canal in cursor.fetchall():
                    if canal[1]==message.text:
                        for publicacion in lote_publicaciones:
                            for canal_publicacion in lote_publicaciones[publicacion].canales:
                                if canal_publicacion==canal[0]:
                                    lote_publicaciones[publicacion].canales.remove(canal_publicacion)
                                    publicaciones_vinculadas+=f"{lote_publicaciones[publicacion].ID}, "
                                    # bot.send_message(message.chat.id, f"Se ha eliminado el canal de la Publicación: <b>{lote_publicaciones[publicacion].ID}</b>")
                                    
                        cursor.execute(F"DELETE FROM CANALES WHERE ID={canal[0]}")
                        conexion.commit()
                        contador+=1
                
                if contador==0:
                    bot.send_message(message.chat.id, "Al parecer, el canal que has introducido ha sido incorrecto, por favor, presione alguno de los botones y no esté haciendo de las suyas", reply_markup=ReplyKeyboardRemove())
                    
                else:
                    bot.send_message(message.chat.id, f"En este Canal/Grupo se distribuían las Publicaciones: <b>{publicaciones_vinculadas}</b>")
                    bot.send_message(message.chat.id, f"El canal fué eliminado exitosamente", reply_markup=ReplyKeyboardRemove())
                    
                    
                guardar_variables()
                    
                return
                        
                    
                        
                    
                        
            bot.register_next_step_handler(msg, process_channel_to_delete)
                
            
        
        
        
        
        def cmd_agregar_canales(message):
            msg=bot.send_message(message.chat.id, "Muy bien ahora envíeme en el siguiente mensaje los canales que quiere agregar\nEn caso de que sean varios canales: Envíame la lista de canales con el @username de cada uno SEPARADOS por una <b>,</b> (coma)\nSi el canal en cuestión es un canal privado o un grupo privado, a ese en concreto, envíeme su ID en lugar de su @username\n\n<u>Ejemplo</u>:\n'@LastHopePosting, -1001161864648, @LastHopePost'\n\nEn caso de que sea un canal solamente: Pues simplemente envíame el ID o @username de ese único canal en el mensaje", reply_markup=ReplyKeyboardRemove())
        
        
            def channel_register(message):
                global conexion
                
                cursor.execute("SELECT * FROM CANALES")
                lista_existente=cursor.fetchall()
                
                user=message.chat.id
                #Comprobaré si el usuario pasó una lista de canales
                if re.search(',', message.text): 
                    #Al parecer si lo hizo
                    lista=message.text.split(",")
                    contador=0
                    
                    for canal in lista:
                        canal=canal.strip()
                        
                        if canal.isdigit():
                            canal=int(canal)
                            
                            existe=False
                            if not len(lista_existente)==0:
                                for i in lista_existente:
                                    if i[0]==canal:
                                        bot.send_message(message.chat.id, f"¡El canal / grupo {canal} ya existe en la lista!")
                                        existe=True
                            
                            if existe:
                                continue
                            
                            try:
                                bot.get_chat(canal)
                                cursor.execute("INSERT INTO CANALES VALUES (?,?)", (bot.get_chat(canal).id, bot.get_chat(canal).title))
                                conexion.commit()
                                contador+=1
                            except:
                                bot.send_message(message.chat.id, f"Al parecer ha ocurrido un Error con el canal/grupo {canal}\n\n<b>Asegúrate</b> de que dicho canal/grupo EXISTA Y que yo sea ADMINISTRADOR CON DERECHOS para ENVIAR MENSAJES para poderlo agregar a la lista, mientras tanto, lo omito\n")
                                continue
                        else:
                            if not canal.startswith("@"):
                                canal=f"@{canal}"
                            
                            existe=False
                            if not len(lista_existente)==0:
                                for i in lista_existente:
                                    if i[1]==bot.get_chat(canal).title:
                                        bot.send_message(message.chat.id, f"¡El canal / grupo {canal} ya existe en la lista!")
                                        existe=True
                            
                            if existe:
                                continue
                            
                            try:
                                bot.get_chat(canal)
                                cursor.execute("INSERT INTO CANALES VALUES (?,?)", (bot.get_chat(canal).id, bot.get_chat(canal).title))
                                conexion.commit()
                                contador+=1
                            except:
                                bot.send_message(message.chat.id, f"Al parecer ha ocurrido un Error con el canal/grupo {canal}\n\n<b>Asegúrate</b> de que dicho canal/grupo EXISTA Y que yo sea ADMINISTRADOR CON DERECHOS para ENVIAR MENSAJES para poderlo agregar a la lista, mientras tanto, lo omito\n")
                                continue
                
                else:
                    #El usuario solamente pasó 1 canal
                    contador=0
                    
                    
                    if message.text.isdigit() or message.text.startswith("-"):
                        canal=int(message.text)
                        
                        existe=False
                        if not len(lista_existente)==0:
                            for i in lista_existente:
                                if i[0]==canal:
                                    existe=True
                            
                        if existe:
                            bot.send_message(message.chat.id, f"¡El canal / grupo {canal} ya existe en la lista!\n\nTe devuelvo atrás")
                            return

                    
                        try:
                            bot.get_chat(canal)
                            cursor.execute("INSERT INTO CANALES VALUES (?,?)", (bot.get_chat(canal).id, bot.get_chat(canal).title))
                            conexion.commit()
                            contador+=1

                        except Exception as e:
                            bot.send_message(message.chat.id, f"Al parecer ha ocurrido un Error con el canal/grupo {canal}\n\n<b>Asegúrate</b> de que dicho canal/grupo EXISTA Y que yo sea ADMINISTRADOR CON DERECHOS para ENVIAR MENSAJES para poderlo agregar a la lista, mientras tanto, lo omito\n\n<u>Descripción del error</u>\n{e}\n\nTe regreso atrás")
                            return
                    else:
                        
                        if not message.text.startswith("@"):
                            canal=f"@{message.text}"
                        else:
                            canal=message.text
                        
                        existe=False
                        if not len(lista_existente)==0:
                            for i in lista_existente:
                                if i[1]==bot.get_chat(canal).title:
                                    existe=True
                            
                        if existe:
                            bot.send_message(message.chat.id, f"¡El canal / grupo {canal} ya existe en la lista!\n\nTe devuelvo atrás")
                            return
                    
                        try:
                            bot.get_chat(canal)
                            cursor.execute("INSERT INTO CANALES VALUES (?,?)", (bot.get_chat(canal).id, bot.get_chat(canal).title))
                            conexion.commit()
                            contador+=1

                        except Exception as e:
                            bot.send_message(message.chat.id, f"Al parecer ha ocurrido un Error con el canal/grupo {canal}\n\n<b>Asegúrate</b> de que dicho canal/grupo EXISTA Y que yo sea ADMINISTRADOR CON DERECHOS para ENVIAR MENSAJES para poderlo agregar a la lista, mientras tanto, lo omito\n\n<u>Descripción del error</u>\n{e}\n\nTe regreso atrás")
                            return
                    
                if contador==0:
                    bot.send_message(message.chat.id, "No se ha podido agregar ningún grupo/canal\nRevisa que el formato en el que estés mandando el mensaje sea el adecuado\n\nRecuerda que cada @username o ID del canal/grupo al que tenga acceso esté separado cada uno por una <b>,</b> (coma) y en caso de ser solamente un canal/grupo que esté bien escrito y ")
                    
                else:                                        
                    bot.send_message(message.chat.id, f"Se han agregado {contador} grupo(s) / canale(s) :D")
                    
                guardar_variables()
                
                return
            
        
            bot.register_next_step_handler(msg,channel_register)
        
        def process_the_action(message):
            if not message.text=="Agregar" and not message.text=="Quitar":
                bot.send_message(message.chat.id, "Debiste de presionar una de las opciones. Te envío atrás", reply_markup=ReplyKeyboardRemove())
                return
            elif message.text=="Agregar":
                cmd_agregar_canales(message)
            
            elif message.text=="Quitar":
                cursor.execute("SELECT * FROM CANALES")
                if cursor.fetchall()==[]:
                    bot.send_message(message.chat.id, "La lista de canales está vacía!, \n\nNo se puede eliminar nada si no hay nada!", reply_markup=ReplyKeyboardRemove())
                    return
                bot.send_message(message.chat.id, "A continuación, le proporcionaré la lista de canales disponibles, presione en los que quiera remover de la lista", reply_markup=ReplyKeyboardRemove())
                remove_channels(message)
                
                
                
                
        
        
        bot.register_next_step_handler(msg, process_the_action)
        
    elif call.data=="publicacion":
        markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Elige una opción").add("Agregar", "Quitar")
        markup.row("Cancelar Operación")
        msg=bot.send_message(call.from_user.id, "Quieres <b>Agregar</b> o <b>Quitar</b> una nueva Publicación?", reply_markup=markup)
        
        def add_publish(message):
            global lista_canales
            lista_canales=[]
            cursor.execute("SELECT * FROM CANALES")
            lista=cursor.fetchall()
            
            
            if not lista:
                markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Agregar/Quitar canal(es) 💻", callback_data="lista_canales"))
                bot.send_message(message.chat.id, "<b>¡No hay ningún canal en la lista de canales!</b>\n\nAgrega uno y vuelve aquí", reply_markup=markup)
                return
            
            
            def comprobar_medios(message, texto_publicacion):
                if not "Publicaciones_media" in os.listdir():
                    os.mkdir("Publicaciones_media")
                    
                os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}{OS}Publicaciones_media") #Redirección a la carpeta de medios para guardar el archivo

                if message.content_type=="photo":
                    with open(f"{len(lote_publicaciones)+1}_{os.path.basename(bot.get_file(message.photo[-1].file_id).file_path)}", "wb") as archivo:
                        archivo.write(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
                        archivo_multimedia=[os.path.abspath(archivo.name), "photo"]
                        
                        
                elif message.content_type=="video":
                    with open(f"{len(lote_publicaciones)+1}_{os.path.basename(bot.get_file(message.video.file_id).file_path)}", "wb") as archivo:
                        archivo.write(bot.download_file(bot.get_file(message.video.file_id).file_path))
                        archivo_multimedia=[os.path.abspath(archivo.name), "video"]
                        
                        
                elif message.content_type=="audio":
                    
                    try:
                        extension="." + str(os.path.basename(os.path.basename(bot.get_file(message.audio.file_id).file_path)).split(".")[-1])
                        nombre=f"{message.audio.performer} - {message.audio.title}{extension}"
                    except:
                        contador=0
                        for i in message.audio.file_name:
                            if not i.isdigit():
                                break
                            else:
                                contador+=1
                                
                        nombre={message.audio.file_name[contador:]}
                        
                    with open(f"{len(lote_publicaciones)+1}_{nombre}", "wb") as archivo:
                        archivo.write(bot.download_file(bot.get_file(message.audio.file_id).file_path))
                        archivo_multimedia=[os.path.abspath(archivo.name), "audio"]
                        
                        
                elif message.content_type=="document":
                    with open(f"{len(lote_publicaciones)+1}_{os.path.basename(bot.get_file(message.document.file_id).file_path)}", "wb") as archivo:
                        archivo.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
                        archivo_multimedia=[os.path.abspath(archivo.name), "document"]
                        
        
                        
                
                else:
                    bot.send(message.chat.id, "Al parecer, el archivo adjunto que has enviado no es ni una foto, ni un audio, ni un video, ni un documento.\n\nNo puedo recibirlo, dejaré tu publicación en solamente texto")
                    os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    
                    if message.caption:
                        texto_publicacion[message.chat.id]=[message.caption, False]
                    
                    else:
                        texto_publicacion[message.chat.id]=[False, False]

                    return


                if message.caption:
                    texto_publicacion[message.chat.id]=[message.caption, archivo_multimedia]
                
                else:
                    texto_publicacion[message.chat.id]=[False, archivo_multimedia]
    
    
                os.chdir(os.path.dirname(os.path.abspath(__file__)))
                return 
            
            #texto_publicacion={user_id : [texto, multimedia, markup]}
            

            texto_publicacion={}
            texto_publicacion[message.chat.id]=[]
                        
            
            if message.content_type=="text":
                texto_publicacion[message.chat.id].append(message.text)
                texto_publicacion[message.chat.id].append(False)
                
            
            else:
                comprobar_medios(message, texto_publicacion)
            

            
            try:
                if len(re.findall("{{.}}", texto_publicacion[message.chat.id][0].lower()))%2==1:
                    bot.send_message(message.chat.id, "Al parecer, has abierto alguna secuencia de llaves de {{estilo}} pero no lo haz cerrado\nRecuerda que para abrir un estilo también tienes que cerrarlo con la misma secuencia de llaves\n\n<u>Ejemplo</u>\n{{n}}Texto dentro del estilo{{n}} : <b>Texto dentro del estilo</b>")
                    bot.send_message(message.chat.id, "Te devuelvo atrás :)")
                    return
                
                elif re.findall("{{.}}", texto_publicacion[message.chat.id][0].lower())==[]:
                    texto_publicacion[message.chat.id].append(False)
                    pass
                
    
                
                else: 
                    if re.search("{{b}}", texto_publicacion[message.chat.id][0]):
                        texto_publicacion[message.chat.id].append(InlineKeyboardMarkup())
                    else:
                        texto_publicacion[message.chat.id].append(False)
                        
                        
                    estilos=["{{n}}", "{{s}}", "{{i}}", "{{m}}", "{{b}}"]

                    for estilo in estilos:
                        contador=1
                        for i in re.finditer(estilo, texto_publicacion[message.chat.id][0].lower()):
                            busqueda=re.search(estilo, texto_publicacion[message.chat.id][0])
                            if estilo=="{{n}}":
                                if contador==1:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "<b>", 1)
                                    contador=2
                                elif contador==2:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "</b>", 1)
                                    contador=1
                                    
                            elif estilo=="{{s}}":
                                if contador==1:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "<u>", 1)
                                    contador=2
                                elif contador==2:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "</u>", 1)
                                    contador=1
                                    
                            elif estilo=="{{i}}":
                                if contador==1:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "<i>", 1)
                                    contador=2
                                elif contador==2:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "</i>", 1)
                                    contador=1
                            
                            elif estilo=="{{m}}":
                                if contador==1:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "<code>", 1)
                                    contador=2
                                elif contador==2:
                                    texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][busqueda.span()[0]:busqueda.span()[1]], "</code>", 1)
                                    contador=1
                            
                            elif estilo=="{{b}}":
                                for i in re.finditer("{{b}}", texto_publicacion[message.chat.id][0].lower()):
                                    if contador==1:
                                        comienzo=i.span()[0]
                                        contador=2
                                    elif contador==2:
                                        final=i.span()[1]
                                        copia_texto=texto_publicacion[message.chat.id][0][comienzo:final]
                                        if not re.search(r"%.*%", copia_texto):
                                            bot.send_message(message.chat.id, "¡Haz olvidado poner el texto del botón! No registraré el mensaje hasta que todo esté correcto mirei\n\nTe devuelvo atrás")
                                            return
                                        else:
                                            boton_texto=re.search(r"%.*%", copia_texto).group().replace("%","")
                                            copia_texto.replace(re.search(r"%.*%", copia_texto).group(), "")
                                            
                                            
                                        if not re.search(r"&.*&", copia_texto):
                                            bot.send_message(message.chat.id, "¡Haz olvidado poner el enlace hacia dónde conduce el botón! No registraré el mensaje hasta que todo esté correcto mirei\n\nTe devuelvo atrás")
                                            return

                                        else:
                                            boton_enlace=re.search(r"&.*&", copia_texto).group().replace("&","")
                                            copia_texto.replace(re.search(r"&.*&", copia_texto).group(), "")
                                            
                                            
                                        texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].replace(texto_publicacion[message.chat.id][0][comienzo:final], "" , 1)
                                        texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].strip()
                                        texto_publicacion[message.chat.id][2].add(InlineKeyboardButton(boton_texto, url=boton_enlace))
                                        contador=1
                                        break
                                    
                            else:
                                continue
                                    
                        
            
            except Exception as e:
                if not texto_publicacion[message.chat.id][0]:
                    texto_publicacion[message.chat.id].append(False)
                    pass
                
                else:
                    bot.send_message(message.chat.id, f"Ha ocurrido una excepción\n\nDescripción:\n{e}")
                    return
            
            
            try:
                texto_publicacion[message.chat.id][0]=texto_publicacion[message.chat.id][0].strip()
                if texto_publicacion[message.chat.id][0]=="":
                    bot.send_message(message.chat.id, "El mensaje que ingresaste no tenía texto!!\nPonle algo de texto y vuelve aquí\n\n<u>Posible causa alternativa:</u>Muy posiblemente también ingresaste un botón {{b}} solamente, esto tampoco cuenta como texto, ingrese algo más aparte del botón\n\n\nTe regreso atrás")
                    return
            except Exception as e:
                bot.send_message(message.chat.id, f"Ha ocurrido un error guardando el mensaje\n\n<u>Descripción</u>:\n{e}")
                return
            
            bot.send_message(message.chat.id, "Muy bien, ahora de entre los siguientes canales que hay disponibles, presiona ahora en cuál o en cuáles quieres enviar esta publicación\n\n<u>Importante</u>\nVe seleccionando de uno en uno el canal, SIEMPRE LUEGO de que te despliegue el <b>Mensaje de Confirmación</b> siguiente:")
            
        
                        
            def agregar_canales_publicacion(message, markup_botones_mensaje, archivo_multimedia, texto_publicacion):
                global lista_canales
                global conexion
                
                
                cursor.execute("SELECT * FROM CANALES")
                if len(cursor.fetchall())==0:
                    bot.send_message(message.chat.id, "¡La lista de canales disponible está vacía!\n\n¡Agrega canales en los que hacer publicaciones antes de hacer las publicaciones!", reply_markup=InlineKeyboardMarkup(InlineKeyboardButton("Agregar canal(es) 💻", callback_data="lista_canales")))
                    return
                
                
                canales_markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Selecciona un canal", row_width=3)
                cursor.execute("SELECT * FROM CANALES")
                
                canales_markup.row("Finalizar Operación")
                
                for canal in cursor.fetchall():
                    if canal[0] in lista_canales:
                        continue
                    
                    try:
                        canales_markup.add(bot.get_chat(canal[0]).title)
                    except Exception as e:
                        bot.send_message(message.chat.id, f"Al parecer, me han expulsado del canal {canal[1]} o no existe ya, revisa que aún exista y que yo sea admin para poder enviar los mensajes\n<b>Lo eliminaré de la lista de canales</b>, cuando hayas corregido el error ven nuevamente a mí y agrégalo\n\nDescripción del error:\n{e}")
                        cursor.execute(f"DELETE FROM CANALES WHERE ID={canal[0]}")
                        conexion.commit()
                        continue
                    
                
                
                
                
                msg=bot.send_message(message.chat.id, "<u><b>Mensaje de confirmación</b></u>\nA continación, selecciona un canal de los disponibles para agregarlo a a la publicación :) \n\nSi el canal al que quieres agregar la publicación no se encuentra en la lista, escriba /panel y presiona en el botón que dice 'Agregar/Quitar Canal(es) 💻'", reply_markup=canales_markup)
                
                
                
                
                
                def agregar_canal_a_publicar(message, lista_canales, markup_botones_mensaje, archivo_multimedia, texto_publicacion):
                    if message.text=="Finalizar Operación":
                        
                        if len(lista_canales)==0:
                            bot.send_message(message.chat.id, "¡La lista de canales está vacía! ¡No puedo publicar así!\nAsumiré que realmente quieres cancelar la operación actual así que te devuelvo atrás entonces")
                            return
                        
                        bot.send_message(message.chat.id, "Muy bien, me quedaré con los canales que ingresaste ya :)")
                        
                        msg=bot.send_message(message.chat.id, "<b>Por último</b> a continuación de este mensaje, introduce CUÁNTO tiempo estará el mensaje en esos canales (Escríbelo en minutos)\n\n<u>Ejemplo</u>\n'120' : osea, se publicará cada 2 horas ya q 120 minutos lo son, etcétera")
                        
                        def definir_tiempo(message, markup_botones_mensaje, lista_canales, archivo_multimedia, texto_publicacion):
                            global lote_publicaciones
                            
                            if not message.text.isdigit():
                                msg=bot.send_message(message.chat.id, "NO! El formato debe de ser en minutos!\nIngresa nuevamente el tiempo (EN MINUTOS) en el que se va a publicar el mensaje en dichos canales")
                                bot.register_next_step_handler(msg, definir_tiempo)
                            
                            else:
                                
                                if markup_botones_mensaje:
                                    nombre=f"Objeto_{len(lote_publicaciones)+1}_markup"
                                    
                                    globals()[nombre]=Publicaciones(len(lote_publicaciones)+1,texto_publicacion, lista_canales, int(message.text)*60,archivo_multimedia , markup_botones_mensaje)
                                    lote_publicaciones[nombre]=globals()[nombre]
                                    
                                else:
                                    nombre=f"Objeto_{len(lote_publicaciones)+1}_nonmarkup"
                                    
                                    globals()[nombre]=Publicaciones(len(lote_publicaciones)+1, texto_publicacion, lista_canales, int(message.text)*60, archivo_multimedia)
                                    lote_publicaciones[nombre]=globals()[nombre]
                                    
                            bot.send_message(message.chat.id, "La publicación en cuestión es la siguiente:")
                            
                            diccionario_publicacion, lista_opcional= globals()[nombre].mostrar_publicacion()
                            for lista in diccionario_publicacion:
                                try:
                                    if lista=="photo":
                                        with open(diccionario_publicacion[lista][0], "rb") as archivo:
                                            if len(diccionario_publicacion[lista])==3:
                                                bot.send_photo(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                            
                                            else:
                                                bot.send_photo(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                            
                                    elif lista=="video":
                                        with open(diccionario_publicacion[lista][0], "rb") as archivo:
                                            if len(diccionario_publicacion[lista])==3:
                                                bot.send_video(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                            
                                            else:
                                                bot.send_video(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                    
                                    elif lista=="audio":
                                        with open(diccionario_publicacion[lista][0], "rb") as archivo:
                                            if len(diccionario_publicacion[lista])==3:
                                                bot.send_audio(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                            
                                            else:
                                                bot.send_audio(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                    
                                    elif lista=="document":
                                        with open(diccionario_publicacion[lista][0], "rb") as archivo:
                                            if len(diccionario_publicacion[lista])==3:
                                                bot.send_document(message.chat.id, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                                            
                                            else:
                                                bot.send_document(message.chat.id, archivo, caption=diccionario_publicacion[lista][1])
                                        
                                    
                                    elif lista=="text":
                                        if len(diccionario_publicacion[lista])==2:
                                            bot.send_message(message.chat.id, diccionario_publicacion[lista][0], reply_markup=diccionario_publicacion[lista][1])
                                        
                                        else:
                                            bot.send_message(message.chat.id, diccionario_publicacion[lista][0])
                                    
                                    
                                    elif lista=="error":
                                        bot.send_message(message.chat.id, f"Ha ocurrido un error. Notifíquele este mensaje a @mistakedelalaif\n\n<u>Descripción del Error</u>:\n{diccionario_publicacion[lista][0]}")
                                        return
                                except Exception as e:
                                    bot.send_message(message.chat.id, f"Al parecer ha ocurrido un error\n\nMuy posiblemente este error se deba a que empezaste con una {{etiqueta}} y pusiste el cierre de esa {{etiqueta}} dentro de otra diferente. Por favor no hagas eso.\nSi igualmente cree que esa no es la causa del error notífiquele a @mistakedelalaif, mi creador\n\n<u><b>Descripción del error</b></u>:\n{e}\n\nTe regresaré atrás :(")
                                    
                                    del lote_publicaciones[nombre]
                                    del globals()[nombre]
                                    
                                    return
                            
                            
                            for i in lista_opcional:
                                bot.send_message(message.chat.id, i)
                                
                                
                            bot.send_message(message.chat.id, f"El ID de esta publicación es: <b>{globals()[nombre].ID}</b>\n\nRecuérdalo por si quieres volver a trabajar con esta publicación a futuro")
                            
                            guardar_variables()
                            return
                                                                            
                        
                        bot.register_next_step_handler(msg, definir_tiempo, markup_botones_mensaje, lista_canales, archivo_multimedia, texto_publicacion)
                        
                        
                    else:
                        try:
                            contador=0
                            cursor.execute(f"SELECT * FROM CANALES")
                            lista_canales_actual=cursor.fetchall()
                            for tupla_canal in lista_canales_actual:
                                if tupla_canal[1] == message.text:
                                    lista_canales.append(tupla_canal[0])
                                    contador+=1
                            
                            bot.send_message(message.chat.id, "Canal agregado satisfactoriamente a la publicación :)")
                        
                        except:
                            bot.send_message(message.chat.id, "¡Presiona en alguno de los canales que te proporcioné en el teclado!\n\n¡No escribas nada por tu cuenta!\n\nTe devuelvo atrás")
                            return
                            
                        if contador==0:
                            bot.send_message(message.chat.id, "No se agregó ningún canal/grupo!\n\n¡No ingreses valores por tu cuenta!")
                        
                        agregar_canales_publicacion(message, markup_botones_mensaje, archivo_multimedia, texto_publicacion)
                        
                            
                            
                        
                
                bot.register_next_step_handler(msg, agregar_canal_a_publicar, lista_canales, markup_botones_mensaje, archivo_multimedia, texto_publicacion)
                
            

            #agregar_canales_publicacion(message, markup_botones_mensaje, archivo_multimedia, texto_publicacion)            
            agregar_canales_publicacion(message, texto_publicacion[message.chat.id][2], texto_publicacion[message.chat.id][1], texto_publicacion[message.chat.id][0])
                    
                        
            
            
            
            
            
        
        def delete_publish(message):
            
            
            if len(lote_publicaciones)==0:
                bot.send_message(message.chat.id, "¡No puedes eliminar publicaciones si no hay siquiera ninguna!")
                return
                
            markup_inline=InlineKeyboardMarkup(row_width=1)
            markup_inline.add(InlineKeyboardButton("Ver Publicaciones", callback_data="ver_publicaciones"))
            bot.send_message(message.chat.id, "Si NO sabes el ID de la publicación Presiona en el botón de abajo '<b>Ver Publicaciones</b>'. Una vez que lo conozca entonces vuelva aquí", reply_markup=markup_inline)
            
            
            
            markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Selecciona el ID de la publicación", row_width=3)
            

            for publicacion in lote_publicaciones:
                ID=str(lote_publicaciones[publicacion].ID)
                markup.add(ID)
            
            msg=bot.send_message(message.chat.id, "A continuación presiona en el ID de la publicación que quieres eliminar", reply_markup=markup)
            
            def delete_publish_by_id(message):
                global lote_publicaciones
                

                bot.send_message(message.chat.id, "Muy bien, revisaré si existe", reply_markup=ReplyKeyboardRemove())
                if not message.text.isdigit():
                    bot.send_message(message.chat.id, "Debes de proporcionar un ID numérico no un texto listillo\n\nTe regresaré")
                    return
                
                copia_lote_publicaciones=lote_publicaciones.copy()

                contador=0
                for publicacion in lote_publicaciones:
                    if int(lote_publicaciones[publicacion].ID) == int(message.text):
                        if copia_lote_publicaciones[publicacion].multimedia:
                            
                            try:
                                os.remove(copia_lote_publicaciones[publicacion].multimedia[0])
                            except Exception as e:
                                bot.send_message(message.chat.id, f"Por alguna razón no se ha podido eliminar el fichero adjunto a la publicación\nComúnicale a @mistakedelalaif\n\n<u>Descripción del error</u>:\n{e}")
                            
                        del copia_lote_publicaciones[publicacion]

                        
                        contador+=1
                if contador == 0:
                    bot.send_message(message.chat.id, "No había ninguna publicación con semejante ID\n\nTe regreso atrás")
                
                else:
                    lote_publicaciones.clear()
                    
                    
                    for publicacion in copia_lote_publicaciones:
                        #nombre=f"Objeto_3_nonmarkup"
                        
                        nombre_publicacion=publicacion.replace(re.search("_\d*_", publicacion).group(), f"_{len(lote_publicaciones)+1}_")
                        lote_publicaciones[nombre_publicacion]=copia_lote_publicaciones[publicacion]
                        lote_publicaciones[nombre_publicacion].ID=len(lote_publicaciones)
                        
                        
                        
                        if lote_publicaciones[nombre_publicacion].multimedia:
                            nombre=os.path.basename(lote_publicaciones[nombre_publicacion].multimedia[0])
                            
                            nombre=nombre.replace(re.search("\d*_", nombre).group(), "", 1)
                            
                            nombre_archivo=f"{os.path.dirname(lote_publicaciones[nombre_publicacion].multimedia[0])}{OS}{len(lote_publicaciones)}_{nombre}"
                            
                            os.rename(lote_publicaciones[nombre_publicacion].multimedia[0], nombre_archivo)
                            
                            lote_publicaciones[nombre_publicacion].multimedia=[nombre_archivo, lote_publicaciones[nombre_publicacion].multimedia[1]]
                    
                    guardar_variables()
                    
                msg=bot.send_message(message.chat.id, "Publicación eliminada\n¿Quieres eliminar alguna otra?", reply_markup=ReplyKeyboardMarkup(True,True, input_field_placeholder="Elige una opción").add("Si", "No"))
                
                def remove_confirm(message):
                    if not (message.text=="Si" or message.text=="No"):
                        bot.send_message(message.chat.id, "No has introducido correctamente el parámetro, tenias que presionar los botones.\n\nTe devuelvo atrás")
                        return
                    
                    if message.text=="Si":
                        return delete_publish(message)
                        
                    elif message.text=="No":
                        bot.send_message(message.chat.id, "Muy bien, te devuelo atrás :)")
                        return
                    
                    
                bot.register_next_step_handler(msg, remove_confirm)
                    
            
            bot.register_next_step_handler(msg, delete_publish_by_id)
            
    
            
        def process_publish(message):
            user=message.chat.id
            if message.text=="Cancelar Operación":
                bot.send_message(message.chat.id, "Muy bien :) Cancelaré el proceso anterior", reply_markup=ReplyKeyboardRemove())
                return
        
            elif message.text=="Agregar":
                bot.send_message(message.chat.id, "A continuación, haz la publicación o reenvíala aquí :)", reply_markup=ReplyKeyboardRemove())
                msg=bot.send_message(
                    message.chat.id,
"""<u><b>Ayuda para crear publicaciones en este bot</b></u>
A continuación, pondré los formatos que debes de introducir en la izquierda y en la derecha el resultado en el texto que sale:

<code>{{n}}Texto en Negrita{{n}}</code> : <b>Texto en negrita</b>
<code>{{s}}Texto en Subrayado{{s}}</code> : <u>Texto en subrayado</u>
<code>{{i}}Texto en Itálica{{i}}</code> : <i>Texto en italica</i>
<code>{{m}}Texto en Monoespaciado{{m}}</code> : <code>Texto en Monoespaciado</code>
<code>{{b}}%Texto del botón% &Enlace del botón&{{b}}</code> : (el botón es el que está debajo de este mensaje)

También puedes adjuntar fotos, audios o documentos al mensaje ;D

Ahora envía tu mensaje :D""", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Texto del botón", url="https://google.com")))
                
                bot.register_next_step_handler(msg, add_publish)
                
            
            elif message.text=="Quitar":
                delete_publish(message)
                
            
        
        
        
        bot.register_next_step_handler(msg, process_publish)


    

    elif call.data=="agregar_publicacion":
        user=call.from_user.id
        
        cursor.execute("SELECT * FROM CANALES")
        lista=cursor.fetchall()
        
        if hilo_publicaciones_activo==True:
            bot.send_message(call.from_user, "¡No puedes modificar el archivo de publicaciones mientras está el hilo de publicaciones activo! Detén las Publicaciones para poder modificar su archivo\n\nTe devuelvo atrás")
            return
        
        if lista== []:
            markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Agregar/Quitar canal(es) 💻", callback_data="lista_canales"))
            
            bot.send_message(call.from_user.id, "<b>¡No hay ningún canal en la lista!</b> ¡Agrega alguno antes!", reply_markup=markup)
            return
        
        
        
        if not lote_publicaciones:
            markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Agregar/Quitar publicación 📋🪒", callback_data="publicacion"))
            bot.send_message(call.from_user.id, "<b>¡No hay ninguna Publicación en la lista!</b>\n¡Agrega alguna antes!", reply_markup=markup)
            return
        
        markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Selecciona una opción", row_width=2)
        markup.add("Agregar Canal", "Quitar Canal")
        markup.row("Cancelar Operacion")
        
        msg=bot.send_message(call.from_user.id, "Bien, ahora dime ¿Quieres <b>Agregar</b> Canales a una Publicación o <b>Quitar</b> Canales de una Publicación?", reply_markup=markup)
        
        
        def agregar_publicacion_agregar_canal(message):
            markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Selecciona el ID", row_width=3)
            
            markup.row("Cancelar Operación")
            
            for publicacion in lote_publicaciones:
                ID=str(lote_publicaciones[publicacion].ID)
                markup.add(ID)
                
                
            msg=bot.send_message(message.chat.id, "Selecciona a continuación el ID de la publicación a la que quieres agregarle los canales", reply_markup=markup)
            
            def agregar_publicacion_agregar_canales(message, publicacion):
                if message.text=="Finalizar Operación":
                    bot.send_message(message.chat.id, "Muy bien te devuelvo atrás :)", reply_markup=ReplyKeyboardRemove())
                    return
                
                cursor.execute("SELECT * FROM CANALES")
                lista=cursor.fetchall()
                contador=0
                for tupla_canal in lista:
                    if tupla_canal[1]==message.text:
                        contador+=1
                        publicacion.canales.append(tupla_canal[0])
                        bot.send_message(message.chat.id, "Canal agregado exitosamente a la Publicación",  reply_markup=ReplyKeyboardRemove())
                        guardar_variables()
                        
                        
                if contador==0:
                    bot.send_message(message.chat.id, "¡No has seleccionado ningún canal de la lista!\n\nTe devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                    return

                else:
                    markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Elige una opción").add("Si", "No")
                    msg=bot.send_message(message.chat.id, "¿Quieres seguir agregando canales a las Publicaciones?", reply_markup=markup)
                    
                    def agregar_publicacion_repetir(message):
                        if message.text=="Si":
                            bot.send_message(message.chat.id, "Excelente, te enviaré de vuelta a la elección de Publicación :)", reply_markup=ReplyKeyboardRemove())
                            return agregar_publicacion_agregar_canal(message)
                        
                        elif message.text=="No":
                            bot.send_message(message.chat.id, "Muy bien, te devolveré atrás :)", reply_markup=ReplyKeyboardRemove())
                            return 

                        else:
                            bot.send_message(message.chat.id, "No has presionado ninguna de las opciones disponibles, te devolveré atrás", reply_markup=ReplyKeyboardRemove())
                            return
                    
                    bot.register_next_step_handler(msg, agregar_publicacion_repetir)
                    
            
            
            
            def agregar_publicacion_elegir_canal(message, publicacion):
                markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Elige uno", row_width=3)
                cursor.execute("SELECT * FROM CANALES")
                lista=cursor.fetchall()
                
                markup.row("Finalizar Operación")
                for tupla_canal in lista:
                    if tupla_canal[0] in publicacion.canales:
                        continue
                    
                    markup.add(tupla_canal[1])


                if len(markup.keyboard)==1:
                    bot.send_message(message.chat.id, "Al parecer ya esta Publicación se envía a TODOS los canales <b>disponibles</b>, no hace caso querer agregar a más en su repertorio\n\nTe devuelvo atrás :)")
                    return
                    
                msg=bot.send_message(message.chat.id, "Muy bien, de los siguientes canales, a cuál planeas agregar a esta publicación",reply_markup=markup)
                
                return bot.register_next_step_handler(msg, agregar_publicacion_agregar_canales, publicacion)
            
            
            
            
            def agregar_publicacion_procesar_respuesta(message):
                if message.text=="Cancelar Operación":
                    bot.send_message(message.chat.id, "Muy bien, te devuelvo atrás :)", reply_markup=ReplyKeyboardRemove())
                    return
            
                elif not message.text.isdigit():
                    bot.send_message(message.chat.id, "Tenías que presionar uno de los botones Mastodonte!, te devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                    return
                
                else:
                    contador=0
                    for publicacion in lote_publicaciones:
                        
                        if int(lote_publicaciones[publicacion].ID)==int(message.text):
                            contador+=1
                            bot.send_message(message.chat.id, "Encontré la Publicación :D", reply_markup=ReplyKeyboardRemove())
                            publicacion=lote_publicaciones[publicacion]
                            return agregar_publicacion_elegir_canal(message, publicacion)
                            
                            
                    if contador==0:
                        bot.send_message(message.chat.id, "No había ninguna publicación con ese ID Mastodonte, te devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                        return
            
            bot.register_next_step_handler(msg, agregar_publicacion_procesar_respuesta)
        
        
        def agregar_publicacion_quitar_canal_publicacionID(message):
            markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Selecciona el ID", row_width=3)
            
            markup.row("Cancelar Operación")
            
            for publicacion in lote_publicaciones:
                ID=str(lote_publicaciones[publicacion].ID)
                markup.add(ID)
                
                
            msg=bot.send_message(message.chat.id, "Selecciona a continuación el ID de la publicación a la que quieres quitarle los canales", reply_markup=markup)
            
            def agregar_publicacion_quitar_canales(message):
                if not message.text.isdigit():
                    bot.send_message(message.chat.id, "¡Debes de presionar los botones!\nNo ingreses nada por tu cuenta!\n\nTe devolveré atrás", reply_markup=ReplyKeyboardRemove())
                    return
                
                contador=0
                for publicacion in lote_publicaciones:
                    if int(lote_publicaciones[publicacion].ID) == int(message.text):
                        contador+=1
                        publicacion=lote_publicaciones[publicacion]
                        break
                        
                if contador==0:
                    bot.send_message(message.chat.id, "¡Debes de presionar los botones!\nNo ingreses nada por tu cuenta!\n\nTe devolveré atrás", reply_markup=ReplyKeyboardRemove())
                    return
                
                else:
                    bot.send_message(message.chat.id, "Publicación encontrada :D", reply_markup=ReplyKeyboardRemove())
                    markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Elige un Canal para Eliminar de la Publicación")
                    
                    for canal in publicacion.canales:
                        try:
                            markup.add(bot.get_chat(canal).title)
                        except Exception as e:
                            cursor.execute("SELECT * FROM CANALES")
                            lista=cursor.fetchall()
                            for tupla_canal in lista:
                                if tupla_canal[0]==canal:
                                    bot.send_message(message.chat.id, f"Al parecer ha ocurrido un error con <b>{tupla_canal[1]}</b>\n\nMuy posiblemente este canal/grupo me bloqueó o no existe ya, recomiendo deshacerse de él o agregarme nuevamente como administrador con todos los derechos que necesito para publicar y eliminar\n\n<u><b>Descripción del error</b></u>\n{e}")
                                    
                                    markup.add(tupla_canal[1])
                                    break
                                
                    msg=bot.send_message(message.chat.id, "Muy bien, ahora selecciona el Canal/Grupo que quieres que sea eliminado de la Publicación", reply_markup=markup)
                    
                    
                    def agregar_publicacion_quitar_canales_procesar(message, publicacion):
                        global lote_publicaciones
                        contador=0
                        cursor.execute("SELECT * FROM CANALES")
                        lista=cursor.fetchall()
                        for tupla_canal in lista:
                            if tupla_canal[1]==message.text:
                                contador+=1
                                publicacion.canales.remove(tupla_canal[0])
                                guardar_variables()
                                
                        if contador==0:
                            bot.send_message(message.chat.id, "¡Debiste de haber seleccionado uno de los canales que te ofrecí en los botones!\n\nTe devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                            return
                        else:
                            bot.send_message(message.chat.id, "Canal eliminado de la Publicación exitosamente :)", reply_markup=ReplyKeyboardRemove())
                            markup=ReplyKeyboardMarkup(True, True, input_field_placeholder="Elige una opción")
                            markup.add("Si", "No")
                            bot.send_message(message.chat.id, "¿Quieres ELIMINAR algún otro canal de una Publicación?", reply_markup=markup)
                            
                            
                            def agregar_publicacion_quitar_canales_repetir(message):
                                if message.text=="Si":
                                    bot.send_message(message.chat.id, "Muy bien, regresaré para quitar otro canal de alguna Publicación", reply_markup=ReplyKeyboardRemove())
                                    agregar_publicacion_quitar_canal_publicacionID(message)
                                    
                                elif message.text=="No":
                                    bot.send_message(message.chat.id, "Muy bien, terminaré el proceso\n\nTe devuelvo atrás :)", reply_markup=ReplyKeyboardRemove())
                                    return
                                
                                else:
                                    bot.send_message(message.chat.id, "¡Tenías que escoger una de las opciones!\n\nTe devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                                    return
                            
                            bot.register_next_step_handler(msg, agregar_publicacion_quitar_canales_repetir)
                    
                    bot.register_next_step_handler(msg, agregar_publicacion_quitar_canales_procesar, publicacion)
                        
                
                
            
            bot.register_next_step_handler(msg, agregar_publicacion_quitar_canales)
            
            
            
        
        def agregar_publicacion_process_answer(message):
            
            if message.text=="Cancelar Operacion":
                bot.send_message(message.chat.id, "Operación Cancelada, te devuelvo atrás", reply_markup=ReplyKeyboardRemove())
                return

            elif message.text=="Agregar Canal":
                bot.send_message(message.chat.id, "Muy bien, agregaré canales a la Publicación", reply_markup=ReplyKeyboardRemove())
                agregar_publicacion_agregar_canal(message)
            
            elif message.text=="Quitar Canal":
                bot.send_message(message.chat.id, "Muy bien, quitaré canales de una Publicación", reply_markup=ReplyKeyboardRemove())
                agregar_publicacion_quitar_canal_publicacionID(message)
        
        bot.register_next_step_handler(msg, agregar_publicacion_process_answer)
        





    elif call.data=="eliminar_publicacion":
        #Esto es para establecer un tiempo de eliminación de una publicación
        user=call.from_user.id
        
        cursor.execute("SELECT * FROM CANALES")
        lista=cursor.fetchall()
        
        
        
        if not lote_publicaciones:
            markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Agregar/Quitar publicación 📋🪒", callback_data="publicacion"))
            bot.send_message(call.from_user.id, "<b>¡No hay ninguna Publicación en la lista!</b> ¡Agrega alguna antes!", reply_markup=markup)
            return
        
        markup = ReplyKeyboardMarkup(True, True, input_field_placeholder="Selecciona el ID de la publicación", row_width=3)
        for publicacion in lote_publicaciones:
            markup.add(str(lote_publicaciones[publicacion].ID))
        
        
        msg=bot.send_message(call.from_user.id, "Ahora, seleccione el ID de la publicación a la que le quiere definir el tiempo para que se elimine\n\nNota:\nEsta eliminación se aplica LUEGO de ser publicada en los Canales y OBVIAMENTE tiene que ser MENOR que el tiempo en el que se hace dicha publicación", reply_markup=markup)
        
        
        def eliminar_publicacion_ID_publicacion(message):
            bot.send_message(message.chat.id, "Comprobaré la publicación", reply_markup=ReplyKeyboardRemove())
            contador=0
            for publicacion in lote_publicaciones:
                if int(message.text)==lote_publicaciones[publicacion].ID:
                    contador+=1
                    publicacion_elegida=lote_publicaciones[publicacion]
                    break
                    
            if contador==0:
                bot.send_message(message.chat.id, "¡Presiona uno de los botones!\n\nTe devuelvo atrás")
                return
            

            else:
                if (publicacion_elegida.tiempo_publicacion/60)//60>=1:
                    msg=bot.send_message(message.chat.id, f"Muy bien, ahora INGRESA a continuación de ESTE mensaje, la cantidad de tiempo (en MINUTOS) que querrás que pase para que luego de hecha la publicación esta se elimine\n\n<u>Ejemplo de mensaje</u>:\n'120' : representará 120 minutos lo cual son 2 horas\nEste tiempo OBVIAMENTE tiene que ser MENOR que el tiempo en el que se hace dicha publicación\n\nTiempo actual de esta Publicación en los canales es de: <b>{int(str(int((publicacion_elegida.proxima_publicacion - time.time())/60//60)).replace('-', ''))} hora(s) y {int((publicacion_elegida.tiempo_publicacion/60)%60)} minuto(s)</b>")
                else:
                    msg=bot.send_message(message.chat.id, f"Muy bien, ahora INGRESA a continuación de ESTE mensaje, la cantidad de tiempo (en MINUTOS) que querrás que pase para que luego de hecha la publicación esta se elimine\n\n<u>Ejemplo de mensaje</u>:\n'120' : representará 120 minutos lo cual son 2 horas\nEste tiempo OBVIAMENTE tiene que ser MENOR que el tiempo en el que se hace dicha publicación\n\nTiempo actual de esta Publicación en los canales es de: <b>{(int(publicacion_elegida.tiempo_publicacion/60))} minuto(s)</b>")


                def eliminar_publicacion_tiempo_publicacion(message, publicacion_elegida):
                    global lote_publicaciones
                    
                    if not message.text.isdigit():
                        bot.send_message(message.chat.id, "¡Tenías que ingresar una cantidad de minutos!\n\nTe devuelvo atrás")
                        return
                    elif int(message.text)>=publicacion_elegida.tiempo_publicacion/60:
                        bot.send_message(message.chat.id, "¡El tiempo de eliminación no puede ser mayor al tiempo de la próxima publicación del mensaje! Debes de ingresar un valor menor a este\n\nTe devuelvo atrás")
                        return
                    
                    else:
                        publicacion_elegida.tiempo_eliminacion=int(message.text)*60
                        
                    if (publicacion_elegida.tiempo_publicacion/60)//60>=1:
                        bot.send_message(message.chat.id, f"Muy bien, el tiempo de eliminación de la publicación se ha establecido correctamente a: <b>{int(str(int((publicacion_elegida.proxima_eliminacion - time.time())/60//60)).replace('-', ''))} hora(s) y {int((publicacion_elegida.tiempo_eliminacion/60)%60)} minuto(s)</b>")
                    else:
                        bot.send_message(message.chat.id, f"Muy bien, el tiempo de eliminación de la publicación se ha establecido correctamente a: <b>{(int(publicacion_elegida.tiempo_eliminacion/60))} minuto(s)</b>")
                    
                    
                    guardar_variables()
                    bot.send_message(message.chat.id, "Muy bien, te devuelvo atrás :)")
                    return                        
                
                bot.register_next_step_handler(msg, eliminar_publicacion_tiempo_publicacion, publicacion_elegida)
                
        bot.register_next_step_handler(msg, eliminar_publicacion_ID_publicacion)
    



    
    
    elif call.data=="comenzar_hilo":

        global hilo_publicar
        
        
        
        
                

        
        
        if hilo_publicaciones_activo==True:
            bot.send_message(call.from_user.id, "¡Ya hay un hilo activo tarado! No puedes tener dos a la vez")
            return
        
        else:
            if len(lote_publicaciones)==0:
                markup=InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("Agregar/Quitar publicación 📋🪒", callback_data="publicacion"))
                bot.send_message(call.from_user.id, "¡No hay siquiera publicaciones en la lista!\n\nAgrega alguna publicación para empezar", reply_markup=markup)
                return
            
            hilo_publicaciones_activo=True
            guardar_variables()
            bot.send_message(call.from_user.id, "Muy Bien, Iniciaré el <b>Hilo de Publicaciones</b>")
            hilo_publicar=threading.Thread(name="hilo_publicar", target=bucle_publicacion, args=(call.from_user.id, ))
            hilo_publicar.start()
            return
            
            


    
    elif call.data=="detener_hilo":
        if hilo_publicaciones_activo==False:
            bot.send_message(all.from_user.id, "¡No hay ningun hilo activo!")
            return
        
        hilo_publicaciones_activo=False
        bot.send_message(call.from_user.id, "A continuación pararé el hilo. Te notificaré cuando lo esté\n\nTiempo estimado máximo para detenerlo: 1 minuto")
        guardar_variables()
        return
    
    # elif call.data=="copia_seguridad":
    #     bot.send_message(call.from_user.id,"En este apartado puedes mantener mi información a salvo en caso de pérdida o error por parte del servidor dónde estoy alojado como bot\n<u>Dispones de 2 opciones</u>:\n\n1- Guardar Copias:\nCon esta opción te enviaré mis archivos más importantes EN SU ESTADO ACTUAL ('<b>BD_Canales.db</b>' que almacena los Canales y '<b>publicaciones.dill</b>' que almacena las Publicaciones), si se agregan más canales o publicaciones la copia de seguridad deberá de actualizarse, siendo reemplazada por otra. Deberás guardar esto en tu almacenamiento local o en alguna parte de Internet seguro como una copia de seguridad para si ocurre algún error conmigo\n\n1- Cargar Copias:\nMe enviarás dichos archivos para que yo cargue su contenido y obtenga los datos que tenía anteriormente\n<b>ADVERTENCIA IMPORTANTE!:</b>\nCuando cargue los datos de un archivo, los datos que tenía actualmente serán ELIMINADOS. Debes de estar muy seguro de lo que vas a hacer", reply_markup=ReplyKeyboardRemove())
    #     markup=InlineKeyboardMarkup(row_width=1).add(
    #         InlineKeyboardButton("Guardar Copias", callback_data="guarda_copia"),
    #         InlineKeyboardButton("Cargar Copias", callback_data="cargar_copia"),
    #         InlineKeyboardButton("Cancelar", callback_data="cancelar")
    #         )
    #     bot.send_message(call.from_user.id, "Muy bien, qué planeas hacer?", reply_markup=markup)
        
    # elif call.data=="guarda_copia":
    #     if "BD_Canales.db" in os.listdir():
    #         with open("BD_Canales.db", "rb") as archivo:
    #             bot.send_document(call.from_user.id, archivo, caption="Este es la base de datos de Canales")
            
    #     if "publicaciones.dill" in os.listdir():
    #         with open("publicaciones.dill", "rb") as archivo:
    #             bot.send_document(call.from_user.id, archivo, caption="Este es el lista de Publicaciones")
        
    #     bot.send_message(call.from_user.id, "Guarda adecuadamente esos datos, podrían ser necesarios en el futuro\n\nTe devolveré atrás")
        
    #     return
    
    # elif call.data=="cargar_copia":
    #     bot.send_message(call.from_user.id, "Muy bien, ahora envíame ")
    
    
    

@bot.message_handler(func=lambda message: True)
def cmd_dont_be_shy(message):
    bot.send_message(message.chat.id, "Tienes que escribir algo chacal, sino no sabré qué quieres que haga\n\nEmpieza con /help")
    


        
    
    
    

bot.infinity_polling()
