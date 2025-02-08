import usefull_functions
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
import pymongo

dic_temp = {}


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
    

def guardar_variables(lote_publicaciones):
    

    

    with open("publicaciones.dill", "wb") as archivo:
        dill.dump(lote_publicaciones, archivo)
    
    # if guardar=="variables" or guardar=="all":
    #     dict_variables=dict(
    #         hilo_publicar = hilo_publicar,
    #         hilo_publicaciones_activo = hilo_publicaciones_activo,
    #         lote_publicaciones = lote_publicaciones,
    #         lista_canales = lista_canales,
    #         admin = admin,
    #         lista_seleccionada = lista_seleccionada,
    #         dic_temp = dic_temp,
    #         operacion = operacion
    
    #     )
        
        
        
    #     with open("variables.dill", "wb") as archivo:
    #         dill.dump(dict_variables, archivo)
        
    return



def main_handler(bot,call, cursor, admin , conexion, lote_publicaciones, lista_canales, lista_seleccionada, hilo_publicaciones_activo, dic_temp, operacion):
    
    
    try:
        cursor.execute("SELECT ID FROM CANALES")
        dic_temp[call.from_user.id] = cursor.fetchall()
        
    except Exception as e:
        
        if "no such table" in  e.args[0]:
            conexion, cursor = usefull_functions.cargar_conexion()
            
            msg = bot.send_message(call.message.chat.id, "No hay ningún canal en la Base de Datos como para crear una nueva publicacion!\n\nDebes de ingresar un canal en el que publicar primero.\nA continuación de este mensaje ingresa el ID o @username de un canal o grupo en cuestion", reply_markup = telebot.types.ForceReply())
            
            bot.register_next_step_handler(msg ,usefull_functions.channel_register , bot, call, cursor, conexion, lote_publicaciones)
            
        else:
            bot.send_message(call.message.chat.id, f"¡Error!\n\nError al percatarme de que no hay base de datos en Canales_callback\n\nDescripcion del error:\n{e}")
    
    
    
    if call.data=="lista_canales_elegir":

        
        markup=InlineKeyboardMarkup(row_width=1)
        markup.add(
                    InlineKeyboardButton("👁 Mis Canales", callback_data="ver_canal_search:0"),
                    InlineKeyboardButton("➕Añadir Canal", callback_data="anadir_canal"),
                    InlineKeyboardButton("❌Eliminar Canal", callback_data="eliminar_canal")
                )
        
        usefull_functions.enviar_mensajes(bot, call, "👇 Elija una de las opciones disponibles 👇\n\n\n<b>Mis Canales</b> - Ver los canales disponibles\n\n<b>Añadir Canal</b> - Añadir canales por ID o @username\n\n<b>Eliminar Canal</b> - Elimina un canal de los disponibles", markup)
        
        
        
    elif "ver_canal" in call.data:
        cursor.execute("SELECT ID FROM CANALES")
        dic_temp[call.from_user.id] = cursor.fetchall()

        
        if not dic_temp[call.from_user.id]:
            usefull_functions.enviar_mensajes(bot, call, "No hay ningún canal en la Base de Datos, por favor, agregue alguno" , InlineKeyboardMarkup([[InlineKeyboardButton("Agregar Canal Aquí 🎆", callback_data="anadir_canal")]]))
            return
        
        

        
        dic_temp[call.from_user.id]=[i[0] for i in cursor.fetchall()]
        
        # if len(dic_temp[call.from_user.id]) == 0:
        #     bot.send_message(call.from_user.id, "No hay ningún canal en la Base de Datos, por favor, agregue alguno", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Agregar Canal Aquí 🎆", callback_data="anadir_canal")]]))
        #     return
            
        if "ver_canal_search" in call.data:

            if int(re.search(r":.*", call.data).group().replace(":", ""))<0:
                bot.answer_callback_query(call.id, "¡Ya estás en la primera parte de la lista!", True)
                return
            
            elif len(dic_temp[call.from_user.id])<int(re.search(r":.*", call.data).group().replace(":", "")):
                bot.answer_callback_query(call.id, "¡Ya estás en la última parte de la lista!", True)
                return
            
            
            
            else:
                #esta funcion retorna el índice de la próxima publicación
                usefull_functions.ver_canal(call ,bot, call.from_user.id, int(re.search(r":.*", call.data).group().replace(":", "")), cursor)
                
        else:
            bot.answer_callback_query(call.id, f"Nombre del canal: {bot.get_chat(int(re.search(r":.*", call.data).group().replace(":", ""))).title}\nTipo de Chat: {bot.get_chat(int(re.search(r":.*", call.data).group().replace(":", ""))).type}\nSub Totales: {bot.get_chat_member_count(int(re.search(r":.*", call.data).group().replace(":", "")))}\nAdministradores en el chat: {len(bot.get_chat_administrators(int(re.search(r":.*", call.data).group().replace(":", ""))))}", True)
            
            
            bot.get_chat(int(re.search(r":.*", call.data).group().replace(":", ""))).title
        
        return
    
  
    
    
    elif call.data=="anadir_canal":
        
        bot.delete_message(call.message.chat.id , call.message.message_id)
        
        msg = bot.send_message(call.message.chat.id, "Muy bien ahora envíeme en el siguiente mensaje los canales que quiere agregar\nEn caso de que sean varios canales: Envíame la lista de canales con el @username de cada uno (o el ID numérico en caso de ser grupos privados o canales privados), SEPARADOS por una <b>,</b> (coma)\n\n<u>Ejemplo</u>:\n'@LastHopePosting, -1001161864648, @LastHopePost'\n\nEn caso de que sea un canal solamente: Pues simplemente envíame el ID o @username de ese único canal en el mensaje\n\nNota Importante:\nPara poder operar con el canal necesito tener derechos de ADMINISTRADOR y de publicar y borrar publicaciones para así poder gestionar las que comparto.\n\nAsegúrate de que tenga dichos permisos antes de continuar", reply_markup=ReplyKeyboardRemove())
        
        
        
        
    
        bot.register_next_step_handler(msg , usefull_functions.channel_register, bot, call, cursor, conexion, lote_publicaciones)
    
    
    elif "eliminar_canal" in call.data:


        try:
            
        
            if "eliminar_canal_search" in call.data:
                if int(re.search(r":.*", call.data).group().replace(":", ""))<0:
                    bot.answer_callback_query(call.id, "¡Ya estás en la primera lista!", True)
                    return
                
                elif int(re.search(r":.*", call.data).group().replace(":", ""))>=len(lista_fetch)-1:
                    bot.answer_callback_query(call.id, "¡Ya estás en la última lista!", True)
                    return
                
                else:
                    usefull_functions.eliminar_canal(call, call.from_user.id, bot, cursor, int(re.search(r":.*", call.data).group().replace(":", "")) ,lista_seleccionada)
                    
                return
                    
                    
            elif "eliminar_canal_select_bethween" in call.data:
                dic_temp[call.from_user.id]=[int(i) for i in re.search(r":.*", call.data).group().replace(":", "").split("-")]
                cursor.execute("SELECT ID FROM CANALES")
                lista_fetch=cursor.fetchall()
                
                for i in range(dic_temp[call.from_user.id][0], dic_temp[call.from_user.id][1] + 1):
                    
                    if lista_fetch[i][0] in lista_seleccionada:
                        continue
                    else:
                        lista_seleccionada.append(lista_fetch[i][0])
                
                usefull_functions.eliminar_canal(call, call.from_user.id, bot , cursor , dic_temp[call.from_user.id][0], lista_seleccionada)
                return
            
            
            elif "eliminar_canal_deselect_all" in call.data:
                if not lista_seleccionada:
                    bot.answer_callback_query(call.id, "¡No tienes ningún canal seleccionado!")

                else:
                    lista_seleccionada.clear()
                    usefull_functions.eliminar_canal(call, call.from_user.id, bot , cursor ,int(re.search(r":.*", call.data).group().replace(":", "")), lista_seleccionada)
                    
                return
            
                    
            elif "eliminar_canal_select" in call.data:
            #"eliminar_canal_select" para cuando un canal es seleccionado
                cursor.execute("SELECT ID FROM CANALES")
                dic_temp[call.from_user.id]=cursor.fetchall()
                
                if dic_temp[call.from_user.id][int(re.search(r":.*", call.data).group().replace(":", ""))][0] in lista_seleccionada:
                    bot.answer_callback_query(call.id, "¡Ya este chat estaba seleccionado!")
                    return
                
                else:
                    #Cuando un canal es seleccionado se vuelve a mostrar la misma lista de canales sólo que con los nombres actualizados (el nuevo canal seleccionado para la eliminación se le pone un ✅ al lado)
                    lista_seleccionada.append(dic_temp[call.from_user.id][int(re.search(r":.*", call.data).group().replace(":", ""))][0])
                    
                    #llamo a la funcion para volver a mostrar los mismos canales, pero esta vez, actualizados
                    if not int(re.search(r":.*", call.data).group().replace(":", ""))%10 == 0:
                        usefull_functions.eliminar_canal(call, call.from_user.id, bot , cursor , int(re.search(r":.*", call.data).group().replace(":", "")) - (int(re.search(r":.*", call.data).group().replace(":", "")) %10 ), lista_seleccionada)
                    
                    else:
                        usefull_functions.eliminar_canal(call, call.from_user.id, bot , cursor , int(re.search(r":.*", call.data).group().replace(":", "")), lista_seleccionada)
                    
                    return
                
            elif "eliminar_canal_deselect" in call.data:
                cursor.execute("SELECT ID FROM CANALES")
                dic_temp[call.from_user.id]=cursor.fetchall()
                
                if not dic_temp[call.from_user.id][int(re.search(r":.*", call.data).group().replace(":", ""))][0] in lista_seleccionada:
                    bot.answer_callback_query(call.id, "¡Este chat no estaba seleccionado para eliminar!")
                    return
                
                else:
                    lista_seleccionada.remove(dic_temp[call.from_user.id][int(re.search(r":.*", call.data).group().replace(":", ""))][0])
                    
                    if not int(re.search(r":.*", call.data).group().replace(":", "")) %10 == 0:
                        usefull_functions.eliminar_canal(call, call.from_user.id, bot , cursor , int(re.search(r":.*", call.data).group().replace(":", "")) - (int(re.search(r":.*", call.data).group().replace(":", "")) %10) , lista_seleccionada)
                        
                    else:
                        usefull_functions.eliminar_canal(call, call.from_user.id, bot , cursor , int(re.search(r":.*", call.data).group().replace(":", "")) , lista_seleccionada)
                    
                    return
                
                
            elif "eliminar_canal_confirm" in call.data:

                for canal in lista_seleccionada:
                    cursor.execute(f"DELETE FROM CANALES WHERE ID={canal}")
                    for publicacion in lote_publicaciones:
                        if canal in lote_publicaciones[publicacion].canales:
                            lote_publicaciones[publicacion].canales.remove(canal)
                    
                conexion.commit()
                
                
                
                dic_temp[call.from_user.id] = "Se han eliminado los siguientes canales exitosamente: \n\n"
                for e,i in enumerate(lista_seleccionada, start=1):
                    try:
                        dic_temp[call.from_user.id]+=f"{e} - " + f"<a href='{bot.get_chat(i).invite_link}'>{bot.get_chat(i).title}</a>" + "\n"
                    except:
                        dic_temp[call.from_user.id]+=f"{e} - " + {bot.get_chat(i).title} + "\n"
                        
                
                try:
                    usefull_functions.enviar_mensajes(bot, call, dic_temp[call.from_user.id])
                
                except Exception as e:
                    bot.send_message(call.from_user.id, "Ha ocurrido un error intentando enviar el mensaje de los canales eliminados")
                    
                lista_seleccionada=[]
                
                guardar_variables(lote_publicaciones)
                    
                return
                
            
                    
            
            else:
                cursor.execute("SELECT * FROM CANALES")
                if not cursor.fetchall():
                    bot.send_message(call.from_user.id, "¡No tienes canales para eliminar!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Añadir Canal", callback_data="anadir_canal")]]))
                    
                    return
                
                usefull_functions.eliminar_canal(call, call.from_user.id, bot, cursor, 0 ,lista_seleccionada)
            
            
            return
        
        except:
            bot.answer_callback_query(call.id, "No sé a que mensaje te refieres, seguro fué eliminado")
            return