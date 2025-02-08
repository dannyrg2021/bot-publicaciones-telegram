import dill
import os

if not os.path.isfile("publicaciones.dill"):
    print("No existe el archivo")

else:
    def mirar():
        os.system("cls")
        lote_publicaciones=""


        with open("publicaciones.dill", "rb") as archivo:
            lote_publicaciones=dill.load(archivo)



        for publicacion in lote_publicaciones:

            print("\nobjeto: " + publicacion + "\n")

            for key, item in vars(lote_publicaciones[publicacion]).items():

                print("Atributo: " + str(key) + "\nvalor: " + str(item) + "\n")

        valor=input()

        if not valor==".":
            mirar()

        else:
            return

        
    mirar()





