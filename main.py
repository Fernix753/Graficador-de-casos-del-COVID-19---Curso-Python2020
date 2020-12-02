#Documento principal y único, proyecto integrador
#Curso-Python2020 - Dictado por integrantes de "ITBA IEEE"
#Participantes del proyecto:
#Proyecto elegido: "Opción 1: Graficador de casos del COVID-19"
#Enlace del proyecto en github: https://github.com/Fernix753/Graficador-de-casos-del-COVID-19-Curso-Python2020 (El unico cambio que habrá será que el entregado en el foro tendrá mi nombre completo)

#/***********************************\
# Importación de librerías y módulos
#\***********************************/
import matplotlib.pyplot as plt
import pandas
import numpy as np
import requests
import os

#/***********************************\
#  Def Wget y descarga de documentos
#\***********************************/
def wget(url):
    r = requests.get(url, allow_redirects=True)
    with open(url[url.rfind('/') + 1::], 'wb') as f:
        f.write(r.content)

documentos = {
    "full_data.csv": 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
}

for doc, enlace in documentos.items():                                                      #Recorro todos los documentos necesarios, definidos en mi diccionario "documentos"
    if not os.path.exists( doc ):                                                           #De no exisitr el documento en mi carpeta actual:
        wget( enlace )                                                                      #   -> Lo descargo utilizando la función wget.

#Lectura del documento principal, y lo asignamos a un dataframe
df_datos = pandas.read_csv("full_data.csv")
df_datos.fillna(0, inplace=True)                                                            #Relleno los valores NaN, con valor 0 para evitar errores en el codigo
paises = set ( df_datos["location"]  )                                                      #Creo un set con todas las locaciones para usarla en una verifiación posteriormente

#/***********************************\
#              Funciones            
#\***********************************/
def covid_1(PAIS, save_name=None):                                                          #Gráfico los nuevos casos y muertes de 1 pais
    df_filtrado = df_datos[ df_datos["location"] == PAIS ]                                  #Hago un nuevo dataframe, filtrando por locación
    datosy_newcases = []                                                                    #   ->Creo una lista para los valores de "newcases", los nuevos casos por dia
    datosy_new_deaths = []                                                                  #   ->Creo otra lista para los valores de "new_death", los valores de nuevas muertes por dia
    datosx = list (df_filtrado["date"])                                                     #   ->Creo otra lista, con los valores para el eje X, en este caso las fechas.
    for i in datosx:                                                                        #Recorro mi lista de fechas
        datosy_newcases.append( df_filtrado[ df_filtrado["date"] == i ]["new_cases"] )      #   ->Agrego a mi lista de nuevos casos, los casos de cada fecha
        datosy_new_deaths.append( df_filtrado[ df_filtrado["date"] == i ]["new_deaths"] )   #   ->Agrego a mi lista de nuevas mmuertes, los casos de cada fecha

    plt.title("Nuevos contagios")                                                           #Asigno titulo al gráfico
    plt.ylabel('Contagios')                                                                 #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X
    plt.plot(datosx, datosy_newcases, "b", label=f"{PAIS}, nuevos casos")                   #Hago el ploteo de los casos, con las fechas de mi lista.
    plt.plot(datosx, datosy_new_deaths, "r", label=f"{PAIS}, muertes")                      #Hago el ploteo de las muertes, con las fechas de mi lista.
    plt.legend()                                                                            #Habilito que se ploteen las leyendas
    plt.xticks(datosx[ : :14], rotation=45)                                                 #Muestro 1 fecha de cada 2 semanas
    plt.tight_layout()                                                                      #Ajusta el gráfico automaticamente
    if (save_name!=None):                                                                   #De haber iingresado un nombre para guardar el gráfico
        plt.savefig(str(save_name))                                                         #   ->Se guarda el gráfico con el nombre deseado
    return plt.show()                                                                       #Por ultimo, muestro el gráfico en el retorno de la función

def covid_compare_2(PAIS1, PAIS2, save_name=None):                                          #Gráfico los nuevos casos y muertes de 2 paises, y sus intersecciones
    df_pais1 = df_datos[ df_datos["location"] == PAIS1 ]                                    #Hago un nuevo dataframe, filtrando por locación
    df_pais2 = df_datos[ df_datos["location"] == PAIS2 ]                                    #Hago un nuevo dataframe, filtrando por locación
    y_p1_n_cases, y_p1_new_deaths, y_p2_n_cases, y_p2_new_deaths = [], [], [], []           #Creo variables de nuevos casos y nuevas muertes para cada pais, donde alojaré las cordenadas Y (cantidad de casos)
    datosx1, datosx2 = list (df_pais1["date"]), list (df_pais2["date"])                     #Creo listas con las fechas de registradas para cada pais

    for i in datosx1:                                                                       #Recorro mi lista de fechas 1 (pais 1)
        if i not in datosx2:                                                                #   ->Si encuentro fechas que no están la lista de fechas 2 (pais 2):
            datosx1.remove(i)                                                               #       ->Las remuevo. Con el fin de evitar errores en el gráfico
    for i in datosx2:                                                                       #Recorro mi lista de fechas 2 (pais 2)
        if i not in datosx1:                                                                #   ->Si encuentro fechas que no están la lista de fechas 1 (pais 1):
            datosx2.remove(i)                                                               #       ->Las remuevo. Con el fin de evitar errores en el gráfico
    datosx = datosx1 if len(datosx1) <= len(datosx2) else datosx2                           #Defino mi lista de fechas (valores del eje X) con la lista mas corta en el caso de no sean de identica longitud

    crucescasos, fechascrucescasos = [], []                                                 #Creo una lista para los cruces de los casos, donde almacenaré los valores de X e Y
    crucesmuertes, fechascrucesmuertes = [], []                                             #Creo una lista para los cruces de las muertes, donde almacenaré los valores de X e Y

    if ((list(df_pais1["new_cases"])[0]) >= (list(df_pais2["new_cases"])[0])):              #Creo una variable que maneje el historial del valor mas alto anterior, para graficar las intersecciones en los casos
        histeresis_casos = "pais1"
    else:
        histeresis_casos = "pais2"

    if ((list(df_pais1["new_deaths"])[0]) >= (list(df_pais2["new_deaths"])[0])):            #Creo una variable que maneje el historial del valor mas alto anterior, para graficar las intersecciones en las muertes
        histeresis_muertes = "pais1"
    else:
        histeresis_muertes = "pais2"

    for i in datosx:                                                                        #Recorro mi lista de fechas
        if int(df_pais1[ df_pais1["date"] == i]["new_cases"]) <= 0:                         #Creo variables auxiliares
            p1casos = 0                                                                     #De ser iguales o menores a 0, no las paso por la función de log10
        else:
            p1casos = np.log10(int(df_pais1[ df_pais1["date"] == i]["new_cases"]))
        if int(df_pais2[ df_pais2["date"] == i]["new_cases"]) <= 0:
            p2casos = 0
        else:
            p2casos = np.log10(int(df_pais2[ df_pais2["date"] == i]["new_cases"]))
        if int(df_pais1[ df_pais1["date"] == i]["new_deaths"]) <= 0:
            p1muert = 0
        else:
            p1muert = np.log10(int(df_pais1[ df_pais1["date"] == i]["new_deaths"]))
        if int(df_pais2[ df_pais2["date"] == i]["new_deaths"]) <= 0:
            p2muert = 0
        else:
            p2muert = np.log10(int(df_pais2[ df_pais2["date"] == i]["new_deaths"]))

        y_p1_n_cases.append(p1casos)                                                        #   ->Agrego a mi lista de nuevos casos para el pais 1, el valor actual para esta fecha
        y_p2_n_cases.append(p2casos)                                                        #   ->Agrego a mi lista de nuevos casos para el pais 2, el valor actual para esta fecha
        y_p1_new_deaths.append(p1muert)                                                     #   ->Agrego a mi lista de nuevas muertes para el pais 1, el valor actual para esta fecha
        y_p2_new_deaths.append(p2muert)                                                     #   ->Agrego a mi lista de nuevas muertesnuevos casos para el pais 2, el valor actual para esta fecha

        if  ((p1casos >= p2casos) and (histeresis_casos != "pais1")):                       #Si los casos del pais 1 son mayores a los del pais 2 en el dia "i", y anteriormente no era el mayor
            histeresis_casos = "pais1"                                                      #   ->Cambio la variable del historial
            crucescasos.append(p1casos)                                                     #   ->Agrego a la lista de cruces, el valor
            fechascrucescasos.append(i)                                                     #   ->Y a la lista de fechas, la fecha del valor en cuestion
        elif((p2casos >= p1casos) and (histeresis_casos != "pais2")):                       #Si los casos del pais 2 son mayores a los del pais 1 en el dia "i", y anteriormente no era el mayor
            histeresis_casos = "pais2"                                                      #   ->Cambio la variable del historial
            crucescasos.append(p2casos)                                                     #   ->Agrego a la lista de cruces, el valor
            fechascrucescasos.append(i)                                                     #   ->Y a la lista de fechas, la fecha del valor en cuestion

        if  ((p1muert >= p2muert) and (histeresis_muertes != "pais1")):                     #Idem anterior, pero en lugar de casos, muertes.
            histeresis_muertes = "pais1"
            crucesmuertes.append(p1muert)
            fechascrucesmuertes.append(i)
        elif((p2muert >= p1muert) and (histeresis_muertes != "pais2")):
            histeresis_muertes = "pais2"
            crucesmuertes.append(p2muert)
            fechascrucesmuertes.append(i)

    plt.figure(figsize=(12,4))                                                              #Configuro mi gráfico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    #Ploteo nuevo casos para ambos paises
    plt.subplot(1, 2, 1)                                                                    #Configuracion para usar 2 gráficos en 1 fila
    plt.title("Nuevos contagios")                                                           #Asigno titulo al gráfico
    plt.ylabel('Contagios (miles)')                                                         #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X
    plt.plot(datosx, y_p1_n_cases,color = '#FF7777',label=f"{PAIS1}, nuevos casos")         #Ploteo linea nuevos casos pais 1.
    plt.plot(datosx, y_p2_n_cases,color = '#7777FF',label=f"{PAIS2}, nuevos casos")         #Ploteo linea nuevos casos pais 2.
    plt.plot(fechascrucescasos, crucescasos,'g+',label="Intersecciones")                    #Gráfico las intersecciones
    plt.xticks(datosx1[ : :14], rotation=45)                                                #Muestro 1 fecha de cada 2 semanas
    plt.legend()                                                                            #Habilito que se ploteen las leyendas
    #Ploteo nuevas muertes para ambos paises
    plt.subplot(1, 2, 2)                                                                    #Idem anterior
    plt.title("Nuevas muertes")
    plt.ylabel('Muertes (miles)')
    plt.xlabel('Fechas')
    plt.plot(datosx, y_p1_new_deaths,color = '#FF0000',label=f"{PAIS1}, muertes")
    plt.plot(datosx, y_p2_new_deaths,color = '#0000FF',label=f"{PAIS2}, muertes")
    plt.plot(fechascrucesmuertes, crucesmuertes,'g+',label="Intersecciones")
    plt.xticks(datosx1[ : :14], rotation=45)
    plt.legend()
    plt.tight_layout()                                                                      #Ajusta el gráfico automaticamente
    if (save_name!=None):                                                                   #De haber iingresado un nombre para guardar el gráfico
        plt.savefig(str(save_name))                                                         #   ->Se guarda el gráfico con el nombre deseado
    return plt.show()                                                                       #Por ultimo, muestro el gráfico en el retorno de la función

def covid_compare_x(l_paises, lapso=None,  save_name=None):                                 #Gráfico los nuevos casos de varios X paises
    plt.figure(figsize=(12,4))                                                              #Configuro mi gráfico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    plt.title("Nuevos contagios")                                                           #Asigno titulo al gráfico
    plt.ylabel('Contagios (miles)')                                                         #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X

    fechas = None   #Variable para contener todas las fechas, sin repeticiones
    datosx = []     #Variable para contener todas las fechas, ordenadas en una lista
    #           ROJO        PURPURA     AZUL        VERDE       Negro oscuro     
    colores = ["#FF0000",   "#8000FF",  "#0000FF",  "#00FF00",  "#c2c2c2",                  #Creo una lista con los colores para las lineas, esta lista limita
    #   CLST-VRDE   AMARILLO2   GRIS OSCURO ROSA                                            #la cantidad de paises que puedo comparar, alargarla aumentará las posibilidades de al función.
        "#00FFC1",  "#F39C12",  "#2C3E50",  "#FF00FF"]

    if len(l_paises) > len(colores):                                                        #Comparo la cantidad de paises, con la cantidad de colores para la grafica que tengo.
        return print( f"Sólo puedes comparar {len(colores)} paises" )                       #   ->Si hay mas paises que colores, retorno un error.

    for i in l_paises:                                                                      #Recorro mi lista de paises
        if fechas == None:                                                                  #   ->Si está vacia la variable "fechas"
            df_filtrado = df_datos[ df_datos["location"] == i ]                             #       ->Creo un filtro con la locación
            fechas = set(df_filtrado["date"])                                               #       ->Y la relleno con el set de las fechas
        else:                                                                               #   ->Si no
            df_filtrado = df_datos[ df_datos["location"] == i ]                             #       ->Creo un filtro con la locación
            fechas = fechas & set(df_filtrado["date"])                                      #       ->Comparo el set guardado con el set actual de fechas, y guardo solo las coincidencias

    contador = 0                                                                            #Creo un contador, que asignará el color a cada pais luego.

    for i in l_paises:                                                                      #Recorro mi lista de paises
        df_pais = df_datos[ df_datos["location"] == i ]                                     #->Creo un filtro con la locación
        datosy_newcases = []                                                                #->Creo una lista vacía de valores de Y
        for fecha in list(df_pais["date"]):                                                 #Recorro mis fechas
            if fecha in fechas:                                                                            #Si la fecha existe en mi set de todas las fechas
                pais_casos = int(df_pais[ df_pais["date"] == fecha ]["new_cases"])                         #    ->Variable auxiliar
                if (pais_casos) <= 0:                                                                      #    ->Si son menos a 0
                    datosy_newcases.append( 0 )                                                            #        ->Agrego un 0 para no usar la función log10
                else:                                                                                      #    -Si no
                    datosy_newcases.append( np.log10(int(pais_casos)) )                                    #        ->Agrego el valor a mi lista de valores en Y
                if (fecha not in datosx):                                                                  #    ->Y si la fecha, NO existe en mi lista de valores X
                    datosx.append(fecha)                                                                   #        ->La agrego a la misma
        plt.plot(datosx, datosy_newcases, color = colores[contador], label=f"{i}, nuevos casos")           #Ploteo mis datos del pais, colocando el color por orden de mi lista de colores
        contador += 1                                                                                      #Sumo a mi contador para la proxima iteración
    plt.legend()                                                                                           #Habilito que se ploteen las leyendas
    plt.xticks(datosx[ : :14], rotation=45)                                                                #Congiruro para mostrar 1 fecha de cada 2 semanas

    if lapso != None:                                                                                      #De haber ingresado una lista con el lapso deseado
        if (lapso[0] in fechas):                                                                           #    ->Si el primer valor de la lista está en las fechas
            if (lapso[1] in fechas):                                                                       #        ->Y si el segundo valor de la lista está en las fechas
                plt.xticks(datosx[ : :1], rotation=45)                                                     #            ->Configuro para mostrar todos los dias, y no 1 cada 2 semanas
                if (( datosx.index(lapso[1]) - datosx.index(lapso[0])  ) > 60):                            #                ->Si los dias deseados superan los 60, 
                    plt.xticks(datosx[ : :7], rotation=45)                                                 #                ->Configuro para muestrar 1 dia de cada semana
                plt.xlim(left=datosx.index(lapso[0]),right=( datosx.index(lapso[1]) ))                     #            ->Se limitando los bordes del gráfico a los valores deseados
            else:                                                                                          #        ->Si no, se entiende que el lapso, es primero la fecha y segundo un valor X de días deseados
                if not (isinstance(lapso[1], int) or isinstance(lapso[1], float)):                         #            ->Si tiene un formato distinto a entero o punto flotante
                    print( f"\nLa fecha o lapso introducido, {lapso[1]} ,está fuera de del rango", end="") #
                    return print(" de fechas, o bien tiene un formato invalido.\n")                        #               ->Considero que el rango es invalido.
                if (len(datosx) - datosx.index(lapso[0])) >= int( lapso[1] ):                              #            ->Si la cantidad de dias deseados, es posible de la resta de dias totales
                    plt.xticks(datosx[ : :1], rotation=45)                                                 #                ->Configuro para mostrar todos los dias, y no 1 cada 2 semanas
                    if (int( lapso[1] ) > 60):                                                             #                ->Si los dias deseados superan los 60, 
                        plt.xticks(datosx[ : :7], rotation=45)                                             #                    ->Configuro para muestrar 1 dia de cada semana
                    plt.xlim(left=datosx.index(lapso[0]),                                                  #                ->Se limitando los bordes del gráfico a los valores deseados
                    right= datosx.index(datosx[datosx.index(lapso[0]) + lapso[1]]))                        #
                else:                                                                                      #            ->Si no
                    print( f"\nLa fecha introducida, {lapso[1]} dias despues del {lapso[0]}", end="")
                    return print(" ,está fuera del rango de fechas para estos paises.\n")                  #                ->Considero que el rango es invalido
        else:                                                                                              #    ->Si no
            print( f"\nLa fecha introducida, {lapso[0]}", end="" )
            return print(" ,está fuera del rango de fechas para estos paises.\n")                          #        ->Considero que el rango es invalido.
    plt.tight_layout()                                                                                     #Ajusta el gráfico automaticamente
    if (save_name!=None):                                                                                  #De haber iingresado un nombre para guardar el gráfico
        plt.savefig(str(save_name))                                                                        #   ->Se guarda el gráfico con el nombre deseado
    return plt.show()                                                                                      #Retorno el ploteo

#/***********************************\
#               Main            
#\***********************************/
def print_opciones():       #Defino mis opciones para cada vez que las necesite llamarlas
    print("Opción >>  1  << - Visualización del historico de COVID-19, casos y muertes, para 1 pais.")
    print("Opción >>  2  << - Visualización del historico de COVID-19, casos y muertes, para 2 pais, se comparan y marcan las intersecciones.")
    print("Opción >>  3  << - Visualización del historico de COVID-19, casos para X paises, se acepta un rango de fechas.")
    return print("Opción >>  z  << - Salir del programa.")

def main():                 #Defino mi función main
    print("\nHerramienta: Graficador de casos del COVID-19.\nParticipantes del codigo:")
    print("Curso-Python2020 - Dictado por integrantes de 'ITBA IEEE'\n")
    print("Bienvenid@, a continuación podrás elegir una opcion para utilizar esta herramienta.")
    return print_opciones()
main()                                                                                                                                                                      #Llamo mi función main
opciones = ["1","2","3"]                                                                                                                                                    #Defino mis opciones posibles
opcion = input("Opción deseada:\n")                                                                                                                                         #Solicito un input para luego usarlo en mi bucle

while True:                                                                                                                                                                 #Creo mi bucle infinito
    accion = 0                                                                                                                                                              #Asigno acciones = 0 | Variable auxiliar para la opción 3
    if opcion in opciones:                                                                                                                                                  #Si la opción está en mis opciones:
        if   opcion == "1":                                                                                                                                                 #->Si la opción es la 1
            try_pais = input("Elegiste la opción 1, esto graficará los casos y muertes de un pais, ingresa el pais:\n")                                                     #   ->Solicito un pais
            if try_pais in paises:                                                                                                                                          #   ->Si el pais está en mi lista de paises
                gh_name = input("Deseas guardar el gráfico? Ingresesa el nombre para guardarlo o déjalo en blanco para omitir.\n")                                          #       ->Pregunto si quiere guardar el gráfico
                if not bool(gh_name):                                                                                                                                       #           ->De no haber ingresado nombre para el gráfico
                    covid_1(try_pais)                                                                                                                                       #               ->Realizo el gráfico
                    print(f"Se realizó el gráfico de {try_pais}, y se omitió guardarlo.")                                                                                   #               ->Doy un mensaje de exito y explicación de lo que pasó
                else:                                                                                                                                                       #           ->Si dieron un nombre para el gráfico
                    covid_1(try_pais,gh_name)                                                                                                                               #               ->Realizo el gráfico y lo guardo
                    print(f"Se realizó el gráfico de {try_pais}, y se guardo como {gh_name}.")                                                                              #               ->Doy un mensaje de exito y explicación de lo que pasó
                print("\nCómo quieres continuar? Puedes elegir otra opción o salir con el comando >>  z  <<.")                                                              #           ->Doy por realizada la opción y pregunto qué quiere hacer a continuación
                opcion = input("Opción deseada:\n")                                                                                                                         #           ->Solicito un input para el proximo ciclo del bucle
        elif opcion == "2":                                                                                                                                                 #->Si la opción es la 2
            print("Elegiste la opción 2, esto graficará los casos y muertes de DOS pais, se graficarán las intersecciones de los mismos, a continuación ingresa un pais:")  #   ->Mensaje de explicación
            try_pais1 = input("Ingrese el pais 1:\n")                                                                                                                       #   ->Input del primer pais
            try_pais2 = input("Ingrese el pais 2:\n")                                                                                                                       #   ->Input del segundo pais
            while not try_pais1 in paises:                                                                                                                                  #   ->Si el primer pais no está en mi lista de paises
                try_pais1 = input(f"No se encuentra {try_pais1} en la lista de paises, pruebe ingresando otra vez el pais 1:\n")                                              #       ->Solicito un nuevo valor, y lo repito hasta que sea válido
            while not try_pais2 in paises:                                                                                                                                  #   ->Idem pais 1
                try_pais2 = input(f"No se encuentra {try_pais2} en la lista de paises, pruebe ingresando otra vez el pais 2:\n")
            gh_name = input("Deseas guardar el gráfico? Ingresesa el nombre para guardarlo o déjalo en blanco para omitir.\n")                                              #   ->Idem opción 1 para guardar el gráfico, y ver cómo continua
            if not bool(gh_name):
                covid_compare_2(try_pais1, try_pais2)
                print(f"Se realizó el gráfico de {try_pais1} y {try_pais2}. Se omitió guardarlo.")
            else:
                covid_compare_2(try_pais1, try_pais2, gh_name)
                print(f"Se realizó el gráfico de {try_pais1} y {try_pais2}. Se guardo como {gh_name}.")
            print("\nCómo quieres continuar? Puedes elegir otra opción o salir con el comando >>  z  <<.")
            opcion = input("Opción deseada:\n")
        elif opcion == "3":                                                                                                                                                 #->Si la opción es la 3
            accion = 1                                                                                                                                                      #->Asigno el valor de accion a 1, esta variable es auxiliar
            print("Elegiste la opción 3, esto graficará los casos de X paises, a continuación ingresa un pais:")                                                            #
            to_gh = []                                                                                                                                                      #->Creo una lista, se rellenará con los paises a commprar
            while accion == 1:                                                                                                                                              #->Mientras la accion es igual a 1
                try_pais = input(f"Paises en la lista: {to_gh} \nIngresa un pais o >> 0 << para usar la lista actual.\n")                                                   #   ->Solicito un pais o 0 para continuar con la lista actual
                if ((try_pais == "0") and (len(to_gh)>1)):                                                                                                                  #   ->Si se introdujo un 0, y la lista tiene mas de 1 elemento
                    accion = 2                                                                                                                                              #       ->Cambio la variable accion a 2
                elif (try_pais == "0"):                                                                                                                                     #   -Si no y si se introdujo un 0
                    print("Necesitas almenos 2 paises para realizar este gráfico de comparación.")                                                                          #       ->Doy por hecho que es un error porque no se puede comprar 1 pais con nada
                if try_pais in paises:                                                                                                                                      #   ->Si se introdujo cualquier otra cosa, pruebo si está en mi lista de paises
                    to_gh.append(try_pais)                                                                                                                                  #       ->De estar en la lista de paises totales, lo agrego a mi lista local
                else:                                                                                                                                                       #   ->Si no 
                    if try_pais != "0":                                                                                                                                     #       ->Y si tampoco es un 0
                        print("No se encuentra el pais ingresado")                                                                                                            #       ->Doy un advertencia que el input no fue tomado en cuenta.
            if accion == 2:                                                                                                                                                 #->Si la accion es igual a 2
                inicio = input("Ingrese una fecha de inicio, con el siguiente formato AAAA-MM-DD, dejalo en blanco para omitir:\n")                                         #   ->Solicito una fecha de inicio, o nada para omitir
                if bool(inicio):                                                                                                                                            #   ->Si se introdujo fecha de inicio
                    final  = input("Ingrese una fecha final con el siguiente formato AAAA-MM-DD, o una cantidad de día, dejalos:\n")                                        #       ->Solicito fecha de final o dias a mostrar
                    if final.isnumeric():                                                                                                                                   #       ->Si el input "final" es numerico, lo convierto a entero
                        final = int(final)                                                                                                                                  #
            if (not bool(inicio)):                                                                                                                                          #   ->De no tener fecha de inicio
                l_lapso = None                                                                                                                                              #       ->Configuro mi lapso en None
            else:                                                                                                                                                           #   ->Si no
                l_lapso = [inicio, final]                                                                                                                                   #       ->Lo configuro con el input ingresado
            gh_name = input("Deseas guardar el gráfico? Ingresesa el nombre para guardarlo o déjalo en blanco para omitir.\n")                                              #   ->Idem opción 1 para guardar el gráfico, y ver cómo continua
            graficados = str(to_gh[:(len(to_gh)-2):1]).replace("[", "").replace("]", "").replace("'", "") + " y " + str(to_gh[-1]).replace("[", "").replace("]", "")
            if not bool(gh_name):
                covid_compare_x(to_gh,l_lapso)
                print(f"Se graficaron los casos de {graficados}. Se omitió guardarlo.")
            else:
                covid_compare_x(to_gh,l_lapso, gh_name)
                print(f"Se graficaron los casos de {graficados}. Se guardo como {gh_name}.")
            print("\nCómo quieres continuar? Puedes elegir otra opción o salir con el comando >>  z  <<.")
            opcion = input("Opción deseada:\n")
    elif opcion == "ayuda":                                                                                                                                                 #Si no y si la opción es "Ayuda"
        print("A continuación las opciones para utilizar la herramienta.")                                                                                                  #   ->Doy un mensaje y
        print_opciones()                                                                                                                                                    #   ->Muestro las opciones disponibles
        opcion = input("Opción deseada:\n")                                                                                                                                 #   ->Solicito un nuevo input para el siguiente paso del bucle
    elif opcion == "z":                                                                                                                                                     #Si no y si la opción es "Salir"
        aux_var = input("Elegiste cerrar el programa, muchas gracias por probarlo.")                                                                                        #   ->Doy un mensaje de despedida en un input para darle una pausa
        exit()                                                                                                                                                              #   ->Cierro el programa
    else:                                                                                                                                                                   #Si no
        print("Opción inválida, pruebe eligiendo una del menu principal, o ingresando el comando 'ayuda'.")                                                                 #   ->Considero un error el input, doy el tip de ayuda
        opcion = input("Opción deseada:\n")                                                                                                                                 #   ->Solicito un nuevo input