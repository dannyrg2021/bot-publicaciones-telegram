import os
import random
import time


os.chdir(os.path.dirname(os.path.abspath(__file__)))

OS=""
if not os.name=="nt":
    OS="/"
else:
    OS="\\"



class Publicaciones():
    
    #----------Built in Functions---------------
    def __init__(self, ID, texto, canales:list , tiempo_publicacion, nombre , multimedia=False , markup=False):
        """
        Clase que instancializa las clases en el bot
        """
        
        self.ID=ID
        #--------contenido
        self.texto=texto
        self.multimedia=multimedia # self.multimedia = ["D:\\ruta completa del archivo", "tipo de archivo (photo, audio, document, etc)"]
        self.markup=markup
        #--------contenido--------
        self.canales=canales #lista de canales en los que se reparte la publicación
        
        self.nombre = nombre #nombre dentro de el lote de publicaciones
        
        self.tiempo_publicacion=tiempo_publicacion #es la medida en segundos del tiempo para la proxima publicacion
        
        self.proxima_publicacion=False # objeto time.time() de cuando se publicará
        
        self.tiempo_eliminacion=False  #es la medida en segundos del tiempo para la proxima eliminacion
        
        self.proxima_eliminacion=False  # objeto time.time() de cuando se eliminará la publicacion
        
        self.lista_message_id_eliminar=False #lista de los mensajes ID de esta publicación regados por algún lugar, con este listado de ID se pueden localizar los mensajes con esta publicación y borrarlos
    
    
    
    
    def __enter__(self):
        return self
    
    def __exit__(self):
        return self
    
    
    #--------------Personalized Functions-----------------------------
    
    
    def mostrar_publicacion(self, tipo=False):
        #envia la publicación en cuestión al user_id
        diccionario={}
        if self.multimedia:
            
            #self.multimedia = [os.path.abspath(archivo.name), "photo"]
            
            if self.multimedia[1]=="photo":
                if self.markup:
                    diccionario["photo"]=[self.multimedia[0], self.texto, self.markup]
                    
                else:
                    diccionario["photo"]=[self.multimedia[0], self.texto]
                    
            if self.multimedia[1]=="voice":
                if self.markup:
                    diccionario["voice"]=[self.multimedia[0], self.texto, self.markup]
                    
                else:
                    diccionario["voice"]=[self.multimedia[0], self.texto]
                    
            elif self.multimedia[1]=="video": #video
                if self.markup:
                    diccionario["video"]=[self.multimedia[0], self.texto, self.markup]
                else:
                    diccionario["video"]=[self.multimedia[0], self.texto]
                        
            elif self.multimedia[1]=="audio": #audio
                if self.markup:
                    diccionario["audio"]=[self.multimedia[0], self.texto, self.markup]
                else:
                    diccionario["audio"]=[self.multimedia[0], self.texto]
            
            elif self.multimedia[1]=="document":
                if self.markup:
                    diccionario["document"]=[self.multimedia[0], self.texto, self.markup]
                else:
                    diccionario["document"]=[self.multimedia[0], self.texto]
                        
                                                     
        else:
            if self.markup:
                diccionario["text"]=[self.texto, self.markup]
            
            else:
                diccionario["text"]=[self.texto]
        
        lista_opcional=[]
        if self.proxima_publicacion:
            tiempo_restante=(self.proxima_publicacion - time.time())//60
            horas=int(str(int(tiempo_restante//60)).replace("-", ""))
            minutos=int(tiempo_restante%60)
            if horas < 1:
                lista_opcional.append(f"Para el próximo envío de la Publicación <b>{self.ID}</b> faltan {minutos} minuto(s) y {tiempo_restante} segundo(s)")
            else:
                lista_opcional.append(f"Para el próximo envío de la Publicación <b>{self.ID}</b> faltan {horas} hora(s) y {minutos} minutos(s)")
                
        if not self.proxima_eliminacion==False:
            tiempo_restante=(self.proxima_eliminacion - time.time())//60
            horas=int(str(int(tiempo_restante//60)).replace("-", ""))
            minutos=int(tiempo_restante%60)
            if horas < 1:
                lista_opcional.append(f"Para la próxima eliminación de la Publicación <b>{self.ID}</b> en los canales faltan {minutos} minuto(s) y {tiempo_restante} segundo(s)")
            else:
                lista_opcional.append(f"Para la próxima eliminación de la Publicación <b>{self.ID}</b> en los canales faltan {horas} hora(s) y {minutos} minutos(s)")
                
                
        # return {"photo": [os.abspath(file), "texto", telebot.type.InlineKeyboardMarkup]}, ["Para el próximo envío de la Publicación <b>1</b> faltan 30 minuto(s) y 24 segundo(s)", "Para la próxima eliminación de la Publicación <b>1</b> en los canales faltan 2 minuto(s) y 3 segundo(s)"]
        
        return diccionario, lista_opcional

    
    
