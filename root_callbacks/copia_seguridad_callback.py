import usefull_functions
from Publicaciones_class import Publicaciones
import re
import time
import os
import sqlite3
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
import dill
from zipfile import ZipFile as zip
import pymongo


#-------------------------Variables Functions--------------------------

dict_temp = {}








def main_handler(bot, call, hilo_publicaciones_activo, host_url, conexion, cursor, lote_publicaciones):


        
           
    
    
    #---------------------Copia de seguridad----------------------------------------
    if call.data=="copia_seguridad":
        

        bot.send_message(call.from_user.id,"<b>Explicación</b>:\nEn este apartado puedes mantener mi información a salvo en caso de pérdida o error por parte del servidor dónde estoy alojado como bot\nDispones de 2 opciones:\n\n1- Guardar Copia:\nCon esta opción guardaré mis datos EN SU ESTADO ACTUAL, si se agregan más canales o publicaciones que deseas conservar y guardar en caso de error es recomendable hacer otra copia. Esta copia de seguridad se guarda en un clúster de MongoDB junto con todas las otras hechas en el pasado\n\n2- Cargar Copias:\nAquí te mostraré todas las copias que he guardado anteriormente y decidirás sobre cuál usar\n<b>ADVERTENCIA IMPORTANTE!:</b>\nCuando cargue los datos de un archivo, los datos que tenía actualmente serán ELIMINADOS. Debes de estar muy seguro de lo que vas a hacer", reply_markup=ReplyKeyboardRemove())
        markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("Guardar Copia 💾", callback_data="db_guardar"),
            InlineKeyboardButton("Cargar Copias 💫", callback_data="db_cargar")
            )
        bot.send_message(call.from_user.id, "Muy bien, qué planeas hacer?", reply_markup=markup)
        
        
        
    elif "db_guardar" in call.data:
        
        with zip("Copia_Seguridad", "w") as archivo_comprimido:
        
            
            if "BD_Canales.db" in os.listdir():
                archivo_comprimido.write("BD_Canales.db")
                
            if "publicaciones.dill" in os.listdir():
                archivo_comprimido.write("publicaciones.dill")
                
        with open("Copia_Seguridad", "rb") as archivo_comprimido:
        
            dict_temp[call.from_user.id]=usefull_functions.operaciones_DB(call, bot, host_url, "guardar", archivo_comprimido)
            
        usefull_functions.enviar_mensajes(bot, call, f"¡Copia de Seguridad guardada exitosamente! :D\n\nID de la Copia: {dict_temp[call.from_user.id]["_id"]}\n\nFecha de guardado:\n {dict_temp[call.from_user.id]["fecha"]}")
        
        
        return
    
    elif "db_cargar" in call.data:
        if os.path.isfile("BD_Canales_prueba.db"):
            os.remove("BD_Canales_prueba.db")
            
        if hilo_publicaciones_activo==True:
            bot.send_message(call.from_user.id, "No puedo cargar los ficheros mientras estoy publicando!, ¡Detén el hilo de publicaciones primero y luego regresa!\n\nTe devuelvo atrás")
            return
        
        
        if ":" in call.data:
            
            conexionDB = pymongo.MongoClient(host_url)
    
            db = conexionDB["BaseDatos"]
            
            collection = db["CopiaSeguridad"]
            
            if collection.count_documents({}) == 0:
                usefull_functions.enviar_mensajes(bot, call, "¡No hay ninguna copia de seguridad guardada en la base de datos!")
        
            dict_temp[call.from_user.id] = collection.find_one({"_id" : int(re.search(r":.*", call.data).group().replace(":", ""))})
        
                
            with open("DB.zip", "wb") as file:
                file.write(dict_temp[call.from_user.id]["archivo"])
                
            
            cursor = cursor.close()
            conexion = conexion.close()
            
            os.remove("BD_Canales.db")
            os.remove("publicaciones.dill")
            
            with zip("DB.zip", "r") as comprimido:
                comprimido.extractall(".")
            
            conexion = sqlite3.connect("BD_Canales.db")
            cursor = conexion.cursor()
            
            lote_publicaciones = usefull_functions.cargar_variables()
            
            bot.send_message(call.message.chat.id, "Copia cargada exitosamente :D\n\n/panel para regresar")
            
            return
                    
                
                
        else:
        
            usefull_functions.operaciones_DB(call, bot, host_url, "ver")
            
    elif "db_eliminar" in call.data: 
        usefull_functions.operaciones_DB(call, bot, host_url, "eliminar", id=int(re.search(r":.*", call.data).group().replace(":", "")))
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            
        except:
            pass
        
        bot.send_message(call.message.chat.id, "Copia Eliminada Satisfactoriamente :D\n\nPresiona /panel para volver")
        return
        
        
        