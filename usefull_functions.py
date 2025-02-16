import time
import dill
import traceback
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
import sqlite3
import pymongo
from zipfile import ZipFile as zip
import random
import re


dict_temp={}


def calcular_diferencia_horaria(HoraHost):
    #Esta función devuelve la hora de Perú en el momento de la hora del host
    
    
    
    #tiempo de diferencia entre el host - la de perú
    


    if not isinstance(HoraHost, float):
        HoraHost = time.mktime(HoraHost)
        
    
    tiempo_diferencia=int(time.time() - (time.mktime(time.gmtime()) - 18000))
    
    
    #ahora calculo el tiempo total en segundos sumándole o restandole la diferencia horaria entre el host y perú. En caso de que el host tenga la hora más atrasada que la de perú, se le sumará y en caso de que el host tenga la hora adelantada, se le restará
    if str(tiempo_diferencia).startswith("-"):
        #En caso de que el host tenga una hora menor...
        return HoraHost + tiempo_diferencia
        
        
        
    else:
        #En caso de que el host tenga una hora mayor
        return HoraHost - tiempo_diferencia
        
        
        
        

def enviar_mensajes(bot, call, texto, markup=False , msg=False, delete=False):
    """
    msg = objeto Message para editar\n
    delete = Si es True se eliminará el mensaje anterior y se enviará el actual, en lugar de editar el mensaje anterior especificado , es necesario ingresar el msg
    """
    
    

    if "CallbackQuery" in str(type(call)):
        
        try:
            if markup == False:
                
                
                if msg != False or delete == True:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto)
                    
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, call.message.chat.id, msg.message_id)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                            
                            mensaje = bot.send_message(call.message.chat.id , texto)
                else:
                    
                    try:
                        mensaje = bot.edit_message_text(texto, call.message.chat.id, call.message.message_id)
                    except Exception as e:
                        
                        if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                            
                            return
                        
                        mensaje = bot.send_message(call.message.chat.id, texto)
        
        
            
            else:
                
                
                if msg != False:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto, reply_markup=markup)
                        
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, call.message.chat.id, msg.message_id , reply_markup=markup)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                                                
                            mensaje = bot.send_message(call.message.chat.id , texto , reply_markup=markup)
                else:
                
                    try:
                        mensaje = bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup)
                        
                    except Exception as e:
                        
                        if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                            
                            return
                        
                        mensaje = bot.send_message(call.message.chat.id, texto, reply_markup=markup)
                        
        except Exception as error:
            mensaje = bot.send_message(call.message.chat.id, f"¡Ha ocurrido un error intentando enviar el mensaje!\n\nDescripción del error:\n{error}")
                    
    else:
        
        try:
            #si no es un callback y por el contrario es un mensaje....
            message = call
            
            #si no hay markup
            if markup == False:
                
                #si hay msg de ID
                if msg != False or delete == True:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto)
                        
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, message.chat.id, msg.message_id)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                                                
                            mensaje = bot.send_message(message.chat.id , texto)
                
                #si NO hay msg de ID
                else:
                    mensaje = bot.send_message(message.chat.id, texto)
            
            #si hay markup
            else:
                
                if msg != False:
                    
                    if delete == True:
                        bot.delete_message(call.message.chat.id, msg.message_id)
                        
                        mensaje = bot.send_message(call.message.chat.id, texto, reply_markup=markup)
                        
                    else:
                    
                        try:
                            mensaje = bot.edit_message_text(texto, message.chat.id, msg.message_id , reply_markup=markup)
                            
                        except Exception as e:
                            
                            if "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message" in str(e.args):
                                
                                return
                                                
                            mensaje = bot.send_message(message.chat.id , texto , reply_markup=markup)
                        
                else:
                    
                    mensaje = bot.send_message(message.chat.id, texto, reply_markup=markup)
                    
        except Exception as error:
            mensaje = bot.send_message(call.message.chat.id, f"¡Ha ocurrido un error intentando enviar el mensaje!\n\nDescripción del error:\n{error}")
           
        
            
    return mensaje
        


def cargar_conexion():
    if not os.path.isfile("BD_Canales.db"):
        conexion=sqlite3.connect("BD_Canales.db", check_same_thread=False)
        cursor=conexion.cursor()
        cursor.execute("CREATE TABLE CANALES (ID INTEGER, NOMBRE VARCHAR)")
    
    else:
        conexion=sqlite3.connect("BD_Canales.db", check_same_thread=False)
        cursor=conexion.cursor()
        
        try:
            cursor.execute("SELECT ID FROM CANALES")
            
        except:
            cursor.execute("CREATE TABLE CANALES (ID INTEGER, NOMBRE VARCHAR)")
            
        
    conexion.commit()        
        
    return conexion, cursor


def cargar_variables():
    
    with open("publicaciones.dill", "rb") as archivo:
        lote_publicaciones=dill.load(archivo)
        globals()["lote_publicaciones"] = lote_publicaciones

        
    
    return lote_publicaciones
    
    

def guardar_variables(lote_publicaciones , guardar="all"):
    
    if guardar=="publicaciones" or guardar=="all":
        with open("publicaciones.dill", "wb") as archivo:
            dill.dump(lote_publicaciones, archivo)
    
    
    
    
    
    
    
    
    # lote_variables = cargar_variables("variables")
    
    
    
    # if guardar=="publicaciones" or guardar=="all":
    #     with open("publicaciones.dill", "wb") as archivo:
    #         dill.dump(lote_publicaciones, archivo)
    
    # if guardar=="variables" or guardar=="all":
        
    #     dict_variables = {}
        
    #     for key, item in lote_variables.item():
    #         dict_variables[str(key)] = item
        
        
        
    #     with open("variables.dill", "wb") as archivo:
    #         dill.dump(dict_variables, archivo)
        
    return




#====================Bucle para publicar===============================

def enviar_publicacion(publicacion, user, bot, cursor, admin, lote_publicaciones , hilo_publicaciones_activo=None):

    if not publicacion.canales:
        bot.send_message(user, f"¡La Publicación <b>{publicacion.ID}</b> no tiene ningún canal al que enviar su contenido!\n\n¡Agrégale alguno!")
        return
    
    if publicacion.lista_message_id_eliminar:
        
        # eliminar_publicacion(publicacion, bot, cursor, admin, lote_publicaciones)
        
        for i,mensaje in enumerate(publicacion.lista_message_id_eliminar, start=0):
            try:
                bot.delete_message(publicacion.canales[i], mensaje.message_id)
            except Exception as e:
                
                if "message to delete not found" in e.args[0]:
                    pass
                
                else:
                    bot.send_message(user, f"No se pudo eliminar el mensaje al canal: <a href='{bot.get_chat(publicacion.canales[i]).invite_link}'>{bot.get_chat(publicacion.canales[i]).title}</a>, el ID de la publicación es: {publicacion.ID}\n\nRevisa que yo posea los permisos administrativos y de ELIMINAR, o que el canal/grupo siquiera siga existiendo\n\nDescripción del error:\n{e.args[0]}")
                
                # for canal_error in cursor.fetchall():
                #     if canal_error[0]==canal:
                #         bot.send_message(user, f"No se pudo eliminar el mensaje al canal: {canal_error[1]}, su ID es: {canal_error[0]}\n\nRevisa que yo posea los permisos administrativos y de ELIMINAR, o que el canal/grupo siquiera siga existiendo")
        
    
    
    
    lista_message_id_eliminar=[]
    
    
    #Si el hilo no está activo y el usuario presionó en las opciones de Publicación "Enviar Post Ahora" se publicará sin fijar un momento de nueva publicación en el futuro
    if hilo_publicaciones_activo != None and hilo_publicaciones_activo==False:
        pass
        
    else:
        publicacion.proxima_publicacion=time.time() + publicacion.tiempo_publicacion

        if publicacion.tiempo_eliminacion:
            publicacion.proxima_eliminacion=time.time() + publicacion.tiempo_eliminacion
        
        guardar_variables(lote_publicaciones)
        
   
    for canal in publicacion.canales:
        try:
            diccionario_publicacion, lista_opcional=publicacion.mostrar_publicacion()
            for lista in diccionario_publicacion:
                
                
                if lista=="photo":
                    with open(diccionario_publicacion[lista][0], "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_photo(canal, archivo , caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg)
                    
                        else:
                            msg=bot.send_photo(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                        
                elif lista=="video":
                    with open(diccionario_publicacion[lista][0], "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_video(canal, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg.message_id)
                        
                        else:
                            msg=bot.send_video(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                
                elif lista=="audio":
                    with open(diccionario_publicacion[lista][0], "rb") as archivo:
                        if len(diccionario_publicacion[lista])==3:
                            msg=bot.send_audio(canal, archivo, caption=diccionario_publicacion[lista][1], reply_markup=diccionario_publicacion[lista][2])
                            lista_message_id_eliminar.append(msg)
                        
                        else:
                            msg=bot.send_audio(canal, archivo, caption=diccionario_publicacion[lista][1])
                            lista_message_id_eliminar.append(msg)
                
                elif lista=="document":
                    with open(diccionario_publicacion[lista][0], "rb") as archivo:
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
                    bot.send_message(user, f"Ha ocurrido un error intentando enviar la publicacion #{publicacion.ID}. Notifíquele este mensaje a @mistakedelalaif\n\n<u>Descripción del Error</u>:\n{diccionario_publicacion[lista][0]}")
                    return
                
            
                
        except Exception as e:
            
            try:
                bot.send_message(user, f"No se pudo enviar el mensaje al canal: <a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>, el ID de la publicación es: {publicacion.ID}\n\nRevisa que yo posea los permisos administrativos y de ENVIAR, o que el canal/grupo siquiera siga existiendo\n\nDescripción del error:\n{e.args[0]}")
                
                
            except:
                cursor.execute('SELECT * FROM CANALES')
                for canal_error in cursor.fetchall():
                    if canal_error[0]==canal:
                        bot.send_message(admin, f"No se pudo enviar el mensaje al canal/grupo: <b>{canal_error[1]}</b>, su ID es: <code>{canal_error[0]}</code>\n\nRevisa que yo posea los permisos administrativos y de publicar, o que el canal/grupo siquiera siga existiendo. Mi recomendación es que borre dicho Canal/Grupo de la Publicación y de la Base de Datos\n\n<u><b>Descripción del error</b></u>:\n{e}\n<u>Traceback error</u>:\n{traceback.print_exc()}", parse_mode="html")
                        
                        
            continue
        
    publicacion.lista_message_id_eliminar=lista_message_id_eliminar.copy()
            
    guardar_variables(lote_publicaciones)

    
    # if hilo_publicaciones_activo != None and hilo_publicaciones_activo==False:
    #     pass
        
    # else:
    #     publicacion.lista_message_id_eliminar=lista_message_id_eliminar.copy()
            
    #     guardar_variables(lote_publicaciones, publicacion)
    

    return


def eliminar_publicacion(publicacion, bot, cursor, admin, lote_publicaciones):
    
    for e,mensaje in enumerate(publicacion.lista_message_id_eliminar, start=0):
        try:
            bot.delete_message(publicacion.canales[e], mensaje.message_id)
        except Exception as error:
            
            try:
                
                bot.send_message(admin, f"No se pudo eliminar el mensaje del canal/grupo: <a href='{bot.get_chat(publicacion.canales[e]).invite_link}'>{bot.get_chat(publicacion.canales[e]).title}</a>, el ID de la publicación es: {publicacion.ID}\n\nRevisa que yo posea los permisos administrativos y de ELIMINAR, o que el canal/grupo siquiera siga existiendo\n\nDescripción del error:\n{e.args[0]}")
                
            
            except:
                cursor.execute('SELECT * FROM CANALES')
                
                for e, canal_error in enumerate(cursor.fetchall(), start=0):
                    if canal_error[0]==publicacion.canales[e]:
                        bot.send_message(admin, f"No se pudo eliminar el mensaje del canal/grupo: {canal_error[1]}, su ID es: <code>{canal_error[0]}</code>\n\nRevisa que yo posea los permisos administrativos y de publicar, que el canal/grupo siquiera siga existiendo o que no haya alguien borrado la publicación antes que yo\n\n<u><b>Descripición del error</b>{error}</u>:")
                        
    publicacion.proxima_eliminacion=False
    publicacion.lista_message_id_eliminar=False
    guardar_variables(lote_publicaciones)

    return



def bucle_publicacion(user, bot, hilo_publicaciones_activo, admin, lote_publicaciones, cursor):
    
    
    while hilo_publicaciones_activo==True:
        

        lote_publicaciones=cargar_variables()
        
        for publicacion in lote_publicaciones:
            
            print("tiempo actual: " + str(time.localtime(time.time())) + "\n>=\n" + "Tiempo para la proxima publicacion: "  + str(time.localtime(lote_publicaciones[publicacion].proxima_publicacion)) + "\n" + str(time.time()>=lote_publicaciones[publicacion].proxima_publicacion) + "\n\n")
            
            if time.time()>=lote_publicaciones[publicacion].proxima_eliminacion and not lote_publicaciones[publicacion].proxima_eliminacion==False: 
                
                eliminar_publicacion(lote_publicaciones[publicacion], bot, cursor, admin, lote_publicaciones)
                
                guardar_variables(lote_publicaciones)
            
            if time.time()>=lote_publicaciones[publicacion].proxima_publicacion or not lote_publicaciones[publicacion].proxima_publicacion:
                
                enviar_publicacion(lote_publicaciones[publicacion], user, bot, cursor, admin, lote_publicaciones)
                

                guardar_variables(lote_publicaciones)
                                  
        time.sleep(30)
        
    bot.send_message(admin, "<u><b>Atención! ‼</b></u>\nEl hilo de publicaciones se ha detenido!")
    
    for publicacion in lote_publicaciones:
        lote_publicaciones[publicacion].proxima_publicacion=False
        lote_publicaciones[publicacion].proxima_eliminacion=False
        # if lote_publicaciones[publicacion].lista_message_id_eliminar:
        #     eliminar_publicacion(lote_publicaciones[publicacion])
    
    return


#===============Fin del Bucle para publicar===========================

#----------------Administrar Canales----------------------------------

def ver_canal(call, bot, user, indice, cursor):
    lista_id=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    dict_temp[user]={1: [] , 2: [] }
    cursor.execute("SELECT ID FROM CANALES")
    lista_fetch=cursor.fetchall()

    
    indice_inicial=indice
    texto=""
    texto="A continuación la lista de canales disponibles, fíjate en el ID del canal y presiona el botón inferior correspondiente a dicho canal\n\n"
    try:

        for i in range(10):
            
            texto+=str(lista_id[i]) + " =>  " + f"<a href='{bot.get_chat(lista_fetch[indice][0]).invite_link}'>{bot.get_chat(lista_fetch[indice][0]).title}</a>\n\n"
            
            
            if i<4:
                dict_temp[user][1].append(InlineKeyboardButton(lista_id[i], callback_data="ver_canal:"+ str(lista_fetch[i][0])))
            
            else:
                dict_temp[user][2].append(InlineKeyboardButton(lista_id[i], callback_data="ver_canal:"+ str(lista_fetch[i][0])))
            
            indice+=1
            
        
        
    except Exception as e:
        if indice > len(lista_fetch)-1:
            pass
        
        else:
            bot.send_message(user, f"Ha ocurrido un error al intentar mostrar la lista de canales en el archivo usefull_functions.ver_canal()\n\nDescripción:\n{e}")
    
    
    if dict_temp[user][2]:
        markup_canales=InlineKeyboardMarkup([[i for i in dict_temp[user][1]],[i for i in dict_temp[user][2]]])
        
    else:
        markup_canales=InlineKeyboardMarkup([[i for i in dict_temp[user][1]]])
        
        
    
    texto+=f"\n\n\nMostrados {indice} canales/grupos de {len(lista_fetch)}"
    markup_canales.row(InlineKeyboardButton("⬅️", callback_data=f"ver_canal_search:{indice_inicial-10}"), InlineKeyboardButton("➡️", callback_data=f"ver_canal_search:{indice}"))
    markup_canales.row(InlineKeyboardButton("Menú | Volver ♻", callback_data="volver_menu"))
    
    try:
        enviar_mensajes(bot, call, texto, markup_canales)

    except:
        bot.send_message(user, f"Ha ocurrido el siguiente error en userfull_functions.ver_canal: \n\n{e}")
    
    return indice



def eliminar_canal(call, user , bot, cursor, indice, lista_seleccionada: list = []):

    # lista_seleccionada = ID de los canales seleccionados para eliminar
    cursor.execute("SELECT ID FROM CANALES")
    markup_canales=InlineKeyboardMarkup(row_width=1)
    lista_fetch=cursor.fetchall()
    indice_inicial=indice
    
    
    try:

        for i in range(10):

                    
            if lista_seleccionada and lista_fetch[indice][0] in lista_seleccionada:
                markup_canales.add(InlineKeyboardButton(f"✅ {bot.get_chat(lista_fetch[indice][0]).title}", callback_data=f"eliminar_canal_deselect:{indice}"))
            else:   
                markup_canales.add(InlineKeyboardButton(bot.get_chat(lista_fetch[indice][0]).title, callback_data=f"eliminar_canal_select:{indice}"))
            
            indice+=1
            
    except Exception as e:
        if indice > len(lista_fetch)-1:
            pass
        
        else:
            bot.send_message(user, f"Ha ocurrido un error al intentar mostrar la lista de canales en el archivo usefull_functions.eliminar_canal()\n\nDescripción:\n{e}")
    
    markup_canales.row(
        InlineKeyboardButton("⬅️", callback_data=f"eliminar_canal_search:{indice_inicial-10}"),
        InlineKeyboardButton("➡️", callback_data=f"eliminar_canal_search:{indice}"))
    
    markup_canales.row(
        InlineKeyboardButton("🧨Seleccionar Todos (de esta lista)🧨", callback_data=f"eliminar_canal_select_bethween:{indice_inicial}-{indice-1}"))
    markup_canales.row(
        InlineKeyboardButton("🎃Deseleccionar Todos🎃", callback_data=f"eliminar_canal_deselect_all:{indice_inicial}"))
    
    markup_canales.row(InlineKeyboardButton("✅ Listo (Eliminar)", callback_data="eliminar_canal_confirm"))
    markup_canales.row(InlineKeyboardButton("Menú | Volver ♻", callback_data="volver_menu"))

    try:
        enviar_mensajes(bot, call, "Selecciona el/los canal(es) a ELIMINAR", markup_canales)
    
    except:
        bot.send_message(user, f"Ha ocurrido el siguiente error en userfull_functions.eliminar_canal: \n\n{e}")
        
    return indice, lista_seleccionada

#----------------Fin Administrar Canales----------------------------------
    
    
    
def ver_publicaciones(call, bot, user, cursor, indice, lote_publicaciones, operacion="ver_publicaciones"):

    lista_inline=[]
    indice_inicial=indice
    
    
    # operacion = "del_publicaciones" para borrar
    # operacion = "ver_publicaciones" para ver
    
    
    for indicef,publicacion in enumerate(lote_publicaciones, start=0):
        
        
        try:
            #al mandar el callback_data se enviará el nombre del elemento en el diccionario (lote_publicaciones), para obtenerlo es preciso usar re para buscar el nombre en el propio callback (ej: callback_data = "ver_publicaciones_index:objeto_1_markup"), extraer el nombre del elemento (va seguido de ":") y usar el metodo .get() de los diccionarios 
            lista_inline.append(InlineKeyboardButton(f"{lote_publicaciones[publicacion].ID}", callback_data=f"{operacion}_index:{publicacion}")) 
                
            indice+=1
            
            if indicef==29:
                break
            
        except Exception as e:
            
            if indice > len(lote_publicaciones)-1:
                break
            
            else:
                bot.send_message(user, f"Ha ocurrido un error intentando recopilar información para mostrar las publicaciones\n\n{e}")
                return
    
    if len(lista_inline) <=10:
        dict_temp[user]=1
        
    elif len(lista_inline) > 10 and len(lista_inline) <= 20:
        dict_temp[user]=2
        
    elif len(lista_inline) > 20 and len(lista_inline) <=30:
        dict_temp[user]=3
        
    
    
    markup_publicacion=InlineKeyboardMarkup([[i for i in lista_inline]], row_width=dict_temp[user]) 
    

    markup_publicacion.row(
        InlineKeyboardButton("⬅️", callback_data=f"{operacion}_search:{indice_inicial-10}"),
        InlineKeyboardButton("➡️", callback_data=f"{operacion}_search:{indice}"))
        
    # elif tipo=="change":
    #     markup_publicacion.row(
    #         InlineKeyboardButton("⬅️", callback_data=f"ver_publicaciones_config/change_time_search:{indice_inicial-10}"),
    #         InlineKeyboardButton("➡️", callback_data=f"ver_publicaciones_config/change_time_search:{indice}"))
    
    markup_publicacion.row(InlineKeyboardButton("Menú | Volver ♻", callback_data="volver_menu"))
    
    if operacion == "ver_publicaciones":
        msg = enviar_mensajes(bot, call, "👇 Lista de Publicaciones 👇\nPresiona en alguna para <b>VER</b> más información acerca de esta\n\n(#ID de Publicación)", markup_publicacion)
        
    else:
        msg = enviar_mensajes(bot, call, "👇 Lista de Publicaciones 👇\nPresiona en alguna para <b>ELIMINAR</b> esta publicación\n\n(#ID de Publicación)", markup_publicacion)
        

            
            
    # elif tipo=="change":
        
    #     try:
    #         bot.edit_message_text(" 👇 Elige una Publicación para cambiar 👇 ", chat_id=user , message_id=call.message.message_id, reply_markup=markup_publicacion)
            
    #     except:
    #         bot.send_message(user, " 👇 Lista de Publicaciones 👇 ", reply_markup=markup_publicacion)
    
    return
            
                
        
def change_channels(call, user , bot, indice, publicacion, tipo, operacion , lista_seleccionada: list = [], cursor = "", conexion = ""):
    global dict_temp
    indice_inicial=indice
    markup_canales=InlineKeyboardMarkup(row_width=1)
    
    
    
    # lista_seleccionada = ID de los canales seleccionados para eliminar
    
    
    
    if tipo == "eliminar":
        
        operacion = "ver_publicaciones_config/change_channels_eliminar_"
        
        try:
            
            
            for i in range(10):
                
                if lista_seleccionada and publicacion.canales[indice] in lista_seleccionada:
                    markup_canales.add(InlineKeyboardButton(f"✅ {bot.get_chat(publicacion.canales[indice]).title}", callback_data=f"operacion_eliminar/deselect:{indice}&{publicacion.ID}"))
                else:   
                    markup_canales.add(InlineKeyboardButton(bot.get_chat(publicacion.canales[indice]).title, callback_data=f"operacion_eliminar/select:{indice}&{publicacion.ID}"))
                
                indice+=1
                
        except Exception as e:
            if indice > len(publicacion.canales)-1:
                pass
            
            else:
                bot.send_message(user, f"Ha ocurrido un error al intentar mostrar la lista de canales en el archivo usefull_functions.change_channels('eliminar')\n\nDescripción:\n{e}")
        
        if len(publicacion.canales) > 10:
            markup_canales.row(
                InlineKeyboardButton("⬅️", callback_data=f"operacion_eliminar/search:{indice_inicial-10}"),
                InlineKeyboardButton("➡️", callback_data=f"operacion_eliminar/search:{indice}"))
        
        markup_canales.row(
            InlineKeyboardButton("🧨Seleccionar Todos (de esta lista)🧨", callback_data=f"operacion_eliminar/select_bethween:{indice_inicial}-{indice-1}&{publicacion.ID}"))
        markup_canales.row( 
            InlineKeyboardButton("🎃Deseleccionar Todos🎃", callback_data=f"operacion_eliminar/deselect_all:{indice_inicial}&{publicacion.ID}"))
        
        markup_canales.row(InlineKeyboardButton("✅ Listo (Eliminar)", callback_data=f"operacion_eliminar/confirm:{publicacion.ID}"))
        markup_canales.row(InlineKeyboardButton("Menú | Volver ♻", callback_data="volver_menu"))
        
        

        call.data = "Selecciona el/los canal(es) a eliminar de la Publicación\n\nPara deseleccionar presiona en el canal que seleccionaste marcado con ✅"

    
    elif tipo == "anadir" :
        
        
        operacion = "ver_publicaciones_config/change_channels_anadir_"
        
        cursor.execute("SELECT ID FROM CANALES")
        dict_temp[user] = cursor.fetchall()
        
        
        try:
            for i in range(10):
                
                if not dict_temp[user][indice] in lista_seleccionada:
                    markup_canales.add(InlineKeyboardButton(bot.get_chat(dict_temp[user][indice]).tittle, callback_data=f"operacion_anadir/select:{indice}&{publicacion.ID}"))
                    
                else:
                    markup_canales.add(InlineKeyboardButton("✅ "+ bot.get_chat(dict_temp[user][indice]).tittle, callback_data=f"operacion_anadir/deselect:{indice}&{publicacion.ID}"))
                    
                indice +=1
                
                
        except Exception as e:
            if indice > len(publicacion.canales)-1:
                pass
            
            else:
                bot.send_message(user, f"Ha ocurrido un error al intentar mostrar la lista de canales en el archivo usefull_functions.change_channels('eliminar')\n\nDescripción:\n{e}")
                
        
        if len(publicacion.canales) > 10:
            markup_canales.row(
                InlineKeyboardButton("⬅️", callback_data=f"operacion_anadir/search:{indice_inicial-10}&{publicacion.ID}"),
                InlineKeyboardButton("➡️", callback_data=f"operacion_anadir/search:{indice}&{publicacion.ID}"))
        
        markup_canales.row(InlineKeyboardButton("🧨Seleccionar Todos (de esta lista)🧨", callback_data=f"operacion_anadir/select_bethween:{indice_inicial}-{indice-1}&{publicacion.ID}"))
        
        markup_canales.row(InlineKeyboardButton("🎃Deseleccionar Todos🎃", callback_data=f"operacion_anadir/deselect_all:{indice_inicial}&{publicacion.ID}"))
        
        markup_canales.row(InlineKeyboardButton("✅ Listo (Añadir)", callback_data=f"operacion_anadir/confirm:{publicacion.ID}"))
        markup_canales.row(InlineKeyboardButton("Menú | Volver ♻", callback_data="volver_menu"))
        
        call.data = "Selecciona el/los canal(es) para añadir a la Publicación\n\nPara deseleccionar presiona en el canal que seleccionaste, marcado con ✅"
        
        
    try:
        bot.edit_message_text(call.data, chat_id=user , message_id=call.message.message_id, reply_markup=markup_canales)
        
    except Exception as e:
        
        try:
            bot.send_message(user, call.data , reply_markup=markup_canales)
        except:
            bot.send_message(user, f"Ha ocurrido el siguiente error en userfull_functions.change_channels: \n\n{e}")
                
    return indice , lista_seleccionada , operacion




def agregar_canal_publicacion(bot, call, indice, lista_seleccionada, cursor):

        markup_canales=InlineKeyboardMarkup(row_width=1)
        cursor.execute("SELECT ID FROM CANALES")
        
        indice_inicial=indice
        dict_temp[call.from_user.id] = cursor.fetchall()
        
        try:
            
            
            for i in range(10):
                
                
                if lista_seleccionada and dict_temp[call.from_user.id][indice][0] in lista_seleccionada:
                    #deselect
                    markup_canales.add(InlineKeyboardButton(f"✅ {bot.get_chat(dict_temp[call.from_user.id][indice][0]).title}", callback_data=f"publicacion/c/deselect:{indice}"))
                else:   
                    #select
                    markup_canales.add(InlineKeyboardButton(bot.get_chat(dict_temp[call.from_user.id][indice][0]).title, callback_data=f"publicacion/c/select:{indice}"))
                
                indice+=1
                
        except Exception as e:
            if indice > len(dict_temp[call.from_user.id])-1:
                pass
            
            else:
                bot.send_message(call.message.chat.id, f"Ha ocurrido un error al intentar mostrar la lista de canales en el archivo usefull_functions.change_channels('agregar_publicacion')\n\nDescripción:\n{e}")
                
        
        if len(dict_temp[call.from_user.id]) > 10:
            markup_canales.row(
                #search
                InlineKeyboardButton("⬅️", callback_data=f"publicacion/c/s:{indice_inicial-10}"),
                InlineKeyboardButton("➡️", callback_data=f"publicacion/c/s:{indice}"))
        
        markup_canales.row(
            #select_bethween
            InlineKeyboardButton("🧨Seleccionar Todos (de esta lista)🧨", callback_data=f"publicacion/c/_sb:{indice_inicial}-{indice-1}"))
        markup_canales.row( 
            #deselect_all
            InlineKeyboardButton("🎃Deseleccionar Todos🎃", callback_data=f"publicacion/c/da:{indice_inicial}"))
        
        markup_canales.row(InlineKeyboardButton("✅ Listo (Agregar)", callback_data=f"publicacion/c/confirm"))
        markup_canales.row(InlineKeyboardButton("Cancelar Operación ❌", callback_data="publicacion/c/cancel"))
        
        if call.message.text and "Selecciona el/los canal(es) a incluir en la Publicación" in call.message.text:
            enviar_mensajes(bot, call, "Selecciona el/los canal(es) a incluir en la Publicación.\nEstos serán a donde irá la Publicación una vez iniciado el hilo de publicaciones\n\nPara deseleccionar presiona en el canal que seleccionaste marcado con ✅" , markup_canales)
            
        else:
            bot.send_message(call.message.chat.id, "Selecciona el/los canal(es) a incluir en la Publicación.\nEstos serán a donde irá la Publicación una vez iniciado el hilo de publicaciones\n\nPara deseleccionar presiona en el canal que seleccionaste marcado con ✅", reply_markup = markup_canales)
        
        return
    
    
    
    
def operaciones_DB(call, bot, host_url, operacion , archivo=False, id=False):

    

    try:
        conexionDB = pymongo.MongoClient(host_url)
        
        db = conexionDB["BaseDatos"]
        
        collection = db["CopiaSeguridad"]
        
    except Exception as e:
        try:
            print(e)
            bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB\n\nDescripción del error:\n{re.search('error=.*timeout', e.args[0]).group().split('(')[1]}")
        except:
            bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB")
            
        return "Error"
            

    
    
    
    
    if operacion == "guardar":
        
        try:
            
            dict_temp[call.from_user.id] = collection.count_documents({}) + 1 
            
            collection.insert_one(
                {"_id": dict_temp[call.from_user.id],
                "fecha" : time.time(),
                "archivo" : archivo.read()
                }
                )
            
            
            
        except Exception as e:
            try:

                #Se puede producir una excepción si el "_id" asignado arriba ya coincide con el de otro archivo
            
                dict_temp[call.from_user.id] = random.randint(1, 1000)
                
                collection.insert_one(
                    {"_id": dict_temp[call.from_user.id],
                    "fecha" : time.time(),
                    "archivo" : archivo.read()
                    }
                    )
                
            except Exception as e:
                contador= 0
                while contador != "OK":
                    
                    bot.send_message(call.message.chat.id, f"Intento {str(contador+1)} de 5 para conectar con la Base de Datos")
                
                    try:
                        #Se puede producir una excepción si el "_id" asignado arriba ya coincide con el de otro archivo
                        
                        collection.insert_one(
                            {"_id": random.randint(1, 1000),
                            "fecha" : time.time(),
                            "archivo" : archivo.read()
                            }
                            )
                        
                        contador = "OK"
                        
                    except Exception as e:
                        if contador >= 4:
                            try:
                                bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB\n\nDescripción del error:\n{re.search('error=.*timeout', e.args[0]).group().split('(')[1]}")
                            except:
                                bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB")
                                
                            return "Error"
                        
                        else:
                            contador += 1
                            
                        pass
            
            
            
        dict_temp[call.from_user.id] = collection.find_one({"_id": dict_temp[call.from_user.id]})
        
        return {"_id": dict_temp[call.from_user.id]["_id"], "fecha" : time.strftime(f"<b>Hora</b>: %H:%M %p\n<b>Fecha</b>: %d/%m/%Y", time.localtime(calcular_diferencia_horaria(dict_temp[call.from_user.id]["fecha"])))}
    
    
    
    
    
    
    elif operacion == "ver":
        
        # conexionDB._init_kwargs["host"]
        
        try:
            if collection.count_documents({}) == 0:
                bot.send_message(call.message.chat.id, "¡No hay ninguna copia de seguridad guardada en la base de datos!\n\nOperación Cancelada")
                
                return
                
        except Exception as e:
            try:
                bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB\n\nDescripción del error:\n{re.search('error=.*timeout', e.args[0]).group().split('(')[1]}")
            except:
                bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB")
                
            return "Error"
        
        lista = collection.find({}).to_list()
        
        for diccionario in lista:
            

            bot.send_document(call.message.chat.id, diccionario["archivo"], caption=f"ID de archivo: {diccionario["_id"]}\n\n<u>Fecha Creación</u>:\n{time.strftime("<b>Hora</b>: %H:%M %p\n<b>Fecha</b>: %d/%m/%Y", time.localtime(calcular_diferencia_horaria(diccionario["fecha"])))}", reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Cargar Archivo 💫", callback_data=f"db_cargar:{diccionario["_id"]}")], [InlineKeyboardButton("Eliminar Archivo 💥", callback_data=f"db_eliminar:{diccionario["_id"]}")]
                    ]
                ))
            
        return
            
            
            
            
            
            
    elif operacion == "eliminar":
        
        try:
            collection.delete_one({"_id": id})
            
        except Exception as e:
            try:
                bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB\n\nDescripción del error:\n{re.search('error=.*timeout', e.args[0]).group().split('(')[1]}")
            except:
                bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando hacer la operación de: '{operacion}' en la Base de Datos de Mongo DB")
                
            return "Error"
        
        return
    
    


def channel_register(message, bot, call, cursor, conexion, lote_publicaciones):
    
    # bot.delete_message(message.chat.id, message.message_id)
    
    #Esta variable definirá si hay base de datos o no, en caso de que no omitirá las comprobaciones de si el canal ingresado coincide con algun otro en la BD (Base de Datos)


    dict_temp[call.from_user.id]=""
    
    try:
        cursor.execute("SELECT * FROM CANALES")
        lista_existente=cursor.fetchall()
    
    except Exception as e:
        if "no such table" in e.args[0] :
            conexion, cursor = cargar_conexion()
            pass
            
        else:
            bot.send_message(call.message.chat.id, f"Ha ocurrido un error intentando crear el canal\n\nDescripción del error:\n{e}")    
        
    

    #Comprobaré si el usuario pasó una lista de canales
    
    lista=message.text.split(",")
    if len(lista) > 1: 
        #Al parecer si lo hizo
        contador=0
        
        for canal in lista:
            canal=canal.strip()
            
            #llamar a la base de datos en cada iteración para asegurarse de que los canales enviados no se repiten en el mismo mensaje
            try:
                cursor.execute("SELECT * FROM CANALES")
                lista_existente=cursor.fetchall()
            
            except Exception as e:
                if "no such table" in e.args[0] :
                    conexion, cursor = cargar_conexion()
            #---------------------------------------------------
                    
        
            if canal.isdigit() or canal.startswith("-"):
                canal=int(canal)
            
            elif "t.me/" in str(canal):
                canal = "@" + canal.split(r"/")[-1]
            
            elif not canal.startswith("@"):
                canal=f"@{canal}"
                
                
            try:
                bot.get_chat_member(canal, bot.user.id).status
            except Exception as e:
                
                if "member list is inaccessible" in str(e.args):
                    dict_temp[call.from_user.id]+=f"❌¡Ni siquiera soy miembro de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>)!\nHazme admin ahí para poder agregarlo\n\n"
                    continue
                
                else:
                    dict_temp[call.from_user.id]+=f"❌¡Ha ocurrido un error con el chat de: <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>)!\n\n<u>Descripción del error</u>\n{e}\n\n"
                    continue
            
            if not bot.get_chat_member(canal, bot.user.id).status == "administrator":
                dict_temp[call.from_user.id]+=f"❌Ni siquiera soy administrador en el chat de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>), dame los permisos de administrador para poder agregarlo a las publicaciones\n\n"
                
                continue
            
            elif not bot.get_chat_member(canal, bot.user.id).can_delete_messages:
                dict_temp[call.from_user.id]+=f"❌No puedo eliminar mensajes en el chat de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>), dame los permisos correspondientes para poder agregarlo a las publicaciones\n\n"
                
                continue
            
            
            coincide = False
            for i in lista_existente:
                if i[0]==bot.get_chat(canal).id:
                    dict_temp[call.from_user.id]+=f"❌¡El canal / grupo <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>) ya existe en la lista!\n\n"
                    
                    coincide = True
                    break
                
            if coincide == True:
                continue
            
            try:
                cursor.execute("INSERT INTO CANALES VALUES (?,?)", (bot.get_chat(canal).id, bot.get_chat(canal).title))
                conexion.commit()
                
                
                contador+=1
                
                dict_temp[call.from_user.id]+=f"✅¡El canal / grupo <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>) ha sido agregado exitosamente!\n\n"
                
            
                
            except:
                dict_temp[call.from_user.id]+=f"❌Al parecer ha ocurrido un Error con el canal/grupo <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>)\n\n<b>Asegúrate</b> de que dicho canal/grupo EXISTA Y que yo sea ADMINISTRADOR CON DERECHOS para ENVIAR MENSAJES para poderlo agregar a la lista, mientras tanto, lo omito\n"
                
                continue
            
        
                

    
    else:
        #El usuario solamente pasó 1 canal
        print("Pasó 1 canal")
        
        
        contador=0
        if  message.text.startswith("@"):
            canal = message.text
            
        elif r"t.me/" in message.text:
            canal = "@" + message.text.split(r"/")[-1]
        
        elif message.text.isdigit() or message.text.startswith("-"):
            canal=int(canal)
                
        elif not message.text.startswith("@"):
            canal=f"@{message.text}"

        
            
        try:
            bot.get_chat_member(canal, bot.user.id).status
            
        except Exception as e:
                
            if "member list is inaccessible" in str(e.args):
                dict_temp[call.from_user.id]+=f"❌¡Ni siquiera soy miembro de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>)!\nHazme admin ahí para poder agregarlo"

            
            else:
                try:
                    dict_temp[call.from_user.id]+=f"❌¡Ha ocurrido un error con el chat de: <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>)!\n\n<u>Descripción del error</u>\n{e}"
                    
                except:
                    dict_temp[call.from_user.id]+="¡No has ingresado la información correcta!\n\nOperacion Cancelada"

            
            bot.send_message(message.chat.id, dict_temp[call.from_user.id], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Volver | Menú ♻", callback_data="volver_menu")]]))

            
            return
        
        if not bot.get_chat_member(canal, bot.user.id).status == "administrator":
            dict_temp[call.from_user.id]+=f"❌Ni siquiera soy administrador en el chat de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>), dame los permisos de administrador para poder agregarlo a las publicaciones\n\n<b>Operación Cancelada</b>"
            
            bot.send_message(message.chat.id, dict_temp[call.from_user.id], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Volver | Menú ♻", callback_data="volver_menu")]]))
            
            return
        
        elif not bot.get_chat_member(canal, bot.user.id).can_delete_messages:
            dict_temp[call.from_user.id]+=f"❌No puedo eliminar mensajes en el chat de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>), dame los permisos correspondientes para poder agregarlo a las publicaciones\n\n<b>Operación Cancelada</b>"
            
            bot.send_message(message.chat.id, dict_temp[call.from_user.id], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Volver | Menú ♻", callback_data="volver_menu")]]))
            
            
            return
        


        for i in lista_existente:
            if i[0]==bot.get_chat(canal).id:
                dict_temp[call.from_user.id]+=f"❌¡El canal / grupo <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>) ya existe en la lista!\n\n<b>Operación Cancelada</b>"
                
                bot.send_message(message.chat.id, dict_temp[call.from_user.id], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Volver | Menú ♻", callback_data="volver_menu")]]))

                return
            

            

    
        try:
            bot.get_chat(canal)
            cursor.execute("INSERT INTO CANALES VALUES (?,?)", (bot.get_chat(canal).id, bot.get_chat(canal).title))
            conexion.commit()
            contador+=1

        except Exception as e:
            
            bot.send_message(message.chat.id, f"Al parecer ha ocurrido un Error con el canal/grupo de <code>{canal}</code> (<a href='{bot.get_chat(canal).invite_link}'>{bot.get_chat(canal).title}</a>)\n\n<b>Asegúrate</b> de que dicho canal/grupo EXISTA Y que yo sea ADMINISTRADOR CON DERECHOS para ENVIAR MENSAJES para poderlo agregar a la lista, mientras tanto, lo omito\n\n<u>Descripción del error</u>\n{e}\n\n<b>Operación Cancelada</b>") 

            return
        
    
    if contador==0:
        
        
        if dict_temp[call.from_user.id]:
            bot.send_message(message.chat.id, f"{dict_temp[call.from_user.id]}\nNo se ha podido agregar ningún grupo/canal\nRevisa que el formato en el que estés mandando el mensaje sea el adecuado\n\nRecuerda que cada @username o ID del canal/grupo al que tenga acceso esté separado cada uno por una <b>,</b> (coma) y en caso de ser solamente un canal/grupo que esté bien escrita la información. También asegurate que entre el/los canales que envies ninguno esté ya en la lista de canales disponibles\n\n<b>Operación Cancelada</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Volver | Menú ♻", callback_data="volver_menu")]]))
            
        else:
            bot.send_message(message.chat.id, "No se ha podido agregar ningún grupo/canal\nRevisa que el formato en el que estés mandando el mensaje sea el adecuado\n\nRecuerda que cada @username o ID del canal/grupo al que tenga acceso esté separado cada uno por una <b>,</b> (coma) y en caso de ser solamente un canal/grupo que esté bien escrita la información. También asegurate que entre el/los canales que envies ninguno esté ya en la lista de canales disponibles\n\n<b>Operación Cancelada</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Volver | Menú ♻", callback_data="volver_menu")]]))
        
    else:
        if dict_temp[call.from_user.id]:
            enviar_mensajes(bot, call, f"{dict_temp[call.from_user.id]}\nSe han agregado {contador} grupo(s) / canale(s) exitosamente, presiona /panel.", msg=message)
            
        else:                                        
            enviar_mensajes(bot, call, f"Se han agregado {contador} grupo(s) / canale(s) exitosamente, presiona /panel.", msg=message)


        
    guardar_variables(lote_publicaciones)
    
    return
        
    
    