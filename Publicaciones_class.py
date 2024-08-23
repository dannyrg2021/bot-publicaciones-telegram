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
    def __init__(self, ID, texto, canales:list , tiempo_publicacion, multimedia=False , markup=False):
        self.texto=texto
        self.ID=ID
        self.markup=markup
        self.canales=canales
        self.multimedia=multimedia
        self.tiempo_publicacion=tiempo_publicacion
        self.proxima_publicacion=False
        self.tiempo_eliminacion=False
        self.proxima_eliminacion=False
        self.lista_message_id_eliminar=False
    
    
    
    
    def mostrar_publicacion(self, tipo=False):
        #envia la publicación en cuestión al user_id
        diccionario={}
        if self.multimedia:
            if self.multimedia[1]=="photo":
                if self.markup:
                    diccionario["photo"]=[self.multimedia[0], self.texto, self.markup]
                else:
                    diccionario["photo"]=[self.multimedia[0], self.texto]
                    
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
            tiempo_restante=(self.proxima_publicacion - time.time())/60
            horas=int(str(int(tiempo_restante//60)).replace("-", ""))
            minutos=int(tiempo_restante%60)
            if horas < 1:
                lista_opcional.append(f"Para el próximo envío de la Publicación <b>{self.ID}</b> faltan {minutos} minuto(s)")
            else:
                lista_opcional.append(f"Para el próximo envío de la Publicación <b>{self.ID}</b> faltan {horas} hora(s) y {minutos} minutos(s)")
                
        if not self.proxima_eliminacion==False:
            tiempo_restante=(self.proxima_eliminacion - time.time())/60
            horas=int(str(int(tiempo_restante//60)).replace("-", ""))
            minutos=int(tiempo_restante%60)
            if horas < 1:
                lista_opcional.append(f"Para la próxima eliminación de la Publicación <b>{self.ID}</b> en los canales faltan {minutos} minuto(s)")
            else:
                lista_opcional.append(f"Para la próxima eliminación de la Publicación <b>{self.ID}</b> en los canales faltan {horas} hora(s) y {minutos} minutos(s)")
                
        return diccionario, lista_opcional

    
    
