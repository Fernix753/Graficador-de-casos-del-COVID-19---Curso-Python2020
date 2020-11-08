#Documento principal y único, proyecto integrador
#Curso-Python2020 - Dictado por integrantes de "ITBA IEEE"
#Participantes del proyecto:
#Proyecto elegido: "Opción 1: Graficador de casos del COVID-19"

#/***********************************\
# Importación de librerias y modulos
#\***********************************/
import matplotlib.pyplot as plt
import pandas
import numpy as np
import requests
import os

np.seterr(divide = 'ignore')  #Configuro numpy para que ignore los errores de división

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
def covid_1(PAIS):                                                                          #Grafico los nuevos casos y muertes de 1 pais
    df_filtrado = df_datos[ df_datos["location"] == PAIS ]                                  #Hago un nuevo dataframe, filtrando por locación
    datosy_newcases = []                                                                    #   ->Creo una lista para los valores de "newcases", los nuevos casos por dia
    datosy_new_deaths = []                                                                  #   ->Creo otra lista para los valores de "new_death", los valores de nuevas muertes por dia
    datosx = list (df_filtrado["date"])                                                     #   ->Creo otra lista, con los valores para el eje X, en este caso las fechas.
    for i in datosx:                                                                        #Recorro mi lista de fechas
        datosy_newcases.append( df_filtrado[ df_filtrado["date"] == i ]["new_cases"] )      #   ->Agrego a mi lista de nuevos casos, los casos de cada fecha
        datosy_new_deaths.append( df_filtrado[ df_filtrado["date"] == i ]["new_deaths"] )   #   ->Agrego a mi lista de nuevas mmuertes, los casos de cada fecha

    plt.title("Nuevos contagios")                                                           #Asigno titulo al grafico
    plt.ylabel('Contagios')                                                                 #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X
    plt.plot(datosx, datosy_newcases, "b", label=f"{PAIS}, nuevos casos")                   #Hago el ploteo de los casos, con las fechas de mi lista.
    plt.plot(datosx, datosy_new_deaths, "r", label=f"{PAIS}, muertes")                      #Hago el ploteo de las muertes, con las fechas de mi lista.
    plt.legend()                                                                            #Habilito que se ploteen las leyendas
    plt.xticks(datosx[ : :14], rotation=45)                                                 #Muestro 1 fecha de cada 2 semanas
    return plt.show()                                                                       #Por ultimo, muestro el grafico en el retorno de la función

def covid_compare_2(PAIS1, PAIS2):                                                          #Grafico los nuevos casos y muertes de 2 paises, y sus intersecciones
    df_pais1 = df_datos[ df_datos["location"] == PAIS1 ]                                    #Hago un nuevo dataframe, filtrando por locación
    df_pais2 = df_datos[ df_datos["location"] == PAIS2 ]                                    #Hago un nuevo dataframe, filtrando por locación
    y_p1_n_cases, y_p1_new_deaths, y_p2_n_cases, y_p2_new_deaths = [], [], [], []           #Creo variables de nuevos casos y nuevas muertes para cada pais, donde alojaré las cordenadas Y (cantidad de casos)
    datosx1, datosx2 = list (df_pais1["date"]), list (df_pais2["date"])                     #Creo listas con las fechas de registradas para cada pais

    for i in datosx1:                                                                       #Recorro mi lista de fechas 1 (pais 1)
        if i not in datosx2:                                                                #   ->Si encuentro fechas que no están la lista de fechas 2 (pais 2):
            datosx1.remove(i)                                                               #       ->Las remuevo. Con el fin de evitar errores en el grafico
    for i in datosx2:                                                                       #Recorro mi lista de fechas 2 (pais 2)
        if i not in datosx1:                                                                #   ->Si encuentro fechas que no están la lista de fechas 1 (pais 1):
            datosx2.remove(i)                                                               #       ->Las remuevo. Con el fin de evitar errores en el grafico
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
        p1casos = np.log10(int(df_pais1[ df_pais1["date"] == i]["new_cases"]))              #Creo unas variables auxiliares
        p2casos = np.log10(int(df_pais2[ df_pais2["date"] == i]["new_cases"]))
        p1muert = np.log10(int(df_pais1[ df_pais1["date"] == i]["new_deaths"]))
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

    plt.figure(figsize=(12,4))                                                              #Configuro mi grafico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    #Ploteo nuevo casos para ambos paises
    plt.subplot(1, 2, 1)                                                                    #Configuracion para usar 2 graficos en 1 fila
    plt.title("Nuevos contagios")                                                           #Asigno titulo al grafico
    plt.ylabel('Contagios')                                                                 #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X
    plt.plot(datosx, y_p1_n_cases,color = '#FF7777',label=f"{PAIS1}, nuevos casos")         #Ploteo linea nuevos casos pais 1.
    plt.plot(datosx, y_p2_n_cases,color = '#7777FF',label=f"{PAIS2}, nuevos casos")         #Ploteo linea nuevos casos pais 2.
    plt.plot(fechascrucescasos, crucescasos,'g+',label="Intersecciones")                    #Grafico las intersecciones
    plt.xticks(datosx1[ : :14], rotation=45)                                                #Muestro 1 fecha de cada 2 semanas
    plt.legend()                                                                            #Habilito que se ploteen las leyendas

    #Ploteo nuevas muertes para ambos paises
    plt.subplot(1, 2, 2)                                                                    #Idem anterior
    plt.title("Nuevas muertes")
    plt.ylabel('Muertes')
    plt.xlabel('Fechas')
    plt.plot(datosx, y_p1_new_deaths,color = '#FF0000',label=f"{PAIS1}, muertes")
    plt.plot(datosx, y_p2_new_deaths,color = '#0000FF',label=f"{PAIS2}, muertes")
    plt.plot(fechascrucesmuertes, crucesmuertes,'g+',label="Intersecciones")
    plt.xticks(datosx1[ : :14], rotation=45)
    plt.legend()
    return plt.show()                                                                       #Por ultimo, muestro el grafico en el retorno de la función

def covid_compare_x(l_paises, lapso=None):                                                  #Grafico los nuevos casos de varios X paises
    plt.figure(figsize=(12,4))                                                              #Configuro mi grafico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    plt.title("Nuevos contagios")                                                           #Asigno titulo al grafico
    plt.ylabel('Contagios')                                                                 #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X

    fechas = None   #Variable para contener todas las fechas, sin repeticiones
    datosx = []     #Variable para contener todas las fechas, ordenadas en una lista
    #           ROJO        PURPURA     AZUL        VERDE       AMARILLO     
    colores = ["#FF0000",   "#8000FF",  "#0000FF",  "#00FF00",  "#FFFF00",                  #Creo una lista con los colores para las lineas, esta lista limita
    #   CLST-VRDE   AMARILLO2   GRIS OSCURO ROSA                                            #la cantidad de paises que puedo comparar, alargarla aumentará las posibilidades de al función.
        "#00FFC1",  "#F39C12",  "#2C3E50",  "#FF00FF"]

    if len(l_paises) > len(colores):                                                        #Comparo la cantidad de paises, con la cantidad de colores para la grafica que tengo.
        return print( f"Sólo puedes comparar {len(colores)} paises" )                       #   ->Si hay mas paises que colores, retorno un error.

    for i in l_paises:                                                                      #Recorro mi lista de paises
        if fechas == None:                                                                  #   ->Si está vacia la variable "fechas"
            df_filtrado = df_datos[ df_datos["location"] == i ]                             #       ->Creo un filtro con la locación
            fechas = set(df_filtrado["date"])                                               #       ->Y la relleno con el set de las fechas
        else:                                                                               #   ->Sino
            df_filtrado = df_datos[ df_datos["location"] == i ]                             #       ->Creo un filtro con la locación
            fechas = fechas & set(df_filtrado["date"])                                      #       ->Comparo el set guardado con el set actual de fechas, y guardo solo las coincidencias

    contador = 0                                                                            #Creo un contador, que asignará el color a cada pais luego.

    for i in l_paises:                                                                      #Recorro mi lista de paises
        df_pais = df_datos[ df_datos["location"] == i ]                                     #->Creo un filtro con la locación
        datosy_newcases = []                                                                #->Creo una lista vacía de valores de Y
        for fecha in list(df_pais["date"]):                                                 #Recorro mis fechas
            if fecha in fechas:                                                                            #Si la fecha existe en mi set de todas las fechas
                datosy_newcases.append( np.log10(int(df_pais[ df_pais["date"] == fecha ]["new_cases"])) )  #    ->Agrego el valor a mi lista de valores en Y
                if (fecha not in datosx):                                                                  #    ->Y la fecha, de NO existir en mi lista de valores X
                    datosx.append(fecha)                                                                   #        ->La agrego a la misma
        plt.plot(datosx, datosy_newcases, color = colores[contador], label=f"{i}, nuevos casos")           #Ploteo mis datos del pais, colocando el color por orden de mi lista de colores
        contador += 1                                                                                      #Sumo a mi contador para la proxima iteración
    plt.legend()                                                                                           #Habilito que se ploteen las leyendas
    plt.xticks(datosx[ : :14], rotation=45)                                                                #Congiruro para mostrar 1 fecha de cada 2 semanas

    if lapso != None:                                                                                      #De haber ingresado una lista con el lapso deseado
        if (lapso[0] in fechas):                                                                           #    ->Si el primer valor de la lista está en las fechas
            if (lapso[1] in fechas):                                                                       #        ->Y si el segundo valor de la lista está en las fechas
                plt.xlim(left=datosx.index(lapso[0]),right=( datosx.index(lapso[1]) ))                     #            ->Se limitando los bordes del grafico a los valores deseados
            else:                                                                                          #        ->Sino, se entiende que el lapso, es primero la fecha y segundo un valor X de días deseados
                if (len(datosx) - datosx.index(lapso[0])) >= int( lapso[1] ):                              #            ->Si la cantidad de dias deseados, es posible de la resta de dias totales
                    plt.xticks(datosx[ : :1], rotation=45)                                                 #                ->Configuro para mostrar todos los dias, y no 1 cada 2 semanas
                    if (int( lapso[1] ) > 60):                                                             #                ->Si los dias deseados superan los 60, 
                        plt.xticks(datosx[ : :7], rotation=45)                                             #                    ->Configuro para muestrar 1 dia de cada semana
                    plt.xlim(left=datosx.index(lapso[0]),                                                  #                ->Se limitando los bordes del grafico a los valores deseados
                    right= datosx.index(datosx[datosx.index(lapso[0]) + lapso[1]]))                        #
                else:                                                                                      #            ->Sino
                    return print( f"\nLa fecha introducida, {lapso[1]} dias despues del {lapso[0]} ,no está en el rango de fechas.\n" )#Considero que el rango es invalido
        else:                                                                                              #    ->Sino
            return print( f"\nLa fecha introducida, {lapso[0]}, no está en el rango de fechas aceptables para estos paises.\n" )#->Considero que el rango es invalido.
        
    return plt.show()           #Retorno el ploteo

#/***********************************\
#              Main            
#\***********************************/
print("\n\nHerramienta: Visualización por gráficos de Covid-19.             Participantes del codigo: ") #Nombre
print("Curso-Python2020 - Dictado por integrantes de 'ITBA IEEE'")
print("Proyecto elegido: Graficador de casos del COVID-19\n")
print("Bienvenid@, a continuación podrás elegir una opcion para utilizar ésta herramienta.")
print("Opción >>  1 << - Visualización del historico de COVID-19, casos y muertes, para 1 pais.")
print("Opción >>  2 << - Visualización del historico de COVID-19, casos y muertes, para 2 pais, se comparan y marcan las intersecciones.")
print("Opción >>  3 << - Visualización del historico de COVID-19, casos para X paises.")
#covid_1("Chile")
#covid_compare_2("Argentina", "Chile")
#covid_compare_x(["Chile", "Bolivia", "Paraguay", "Brazil","Argentina"])



"""
Gráfico a entregar (requisito): Argentina y todos sus países limítrofes (Chile, Bolivia, Paraguay, Brasil y Uruguay) durante los meses de invierno (21 de junio a 21 de septiembre)

Funcionalidad opcional:
    * El programa debe permitir almacenar en un archivo excel los países ordenados de mayor cantidad de casos totales
    acumulados (al día de hoy) a menor cantidad de casos indicando en las distintas columnas el nombre del país, la
    cantidad de casos y los fallecimientos.
    
    * Almacenar en un archivo excel los países ordenados de mayor cantidad de casos totales acumulados a menor cantidad de
    casos indicando en las distintas columnas el nombre del país, la cantidad de casos y los fallecimientos colocando en
    distintas hojas del archivo excel (distintas pestañas) la evolución de este ranking, es decir armar una hoja distinta para
    cada día transcurrido. Defina los días a utilizar acorde a cuanta información se disponga, podría ser una entrada del usuario.
    
    * Para cada gráfico generado el usuario deberá poder ingresar un nombre de archivo y el programa genera un
    archivo *.PNG* del gráfico con el nombre indicado.
    
    * Crear una aplicación de consola que se ejecute continuamente recibiendo comandos del usuario, el usuario
    debe indicar el modo de operación que desea y el programa le pide los datos requeridos. Luego de finalizar
    la tarea el programa regresa al inicio y le pide al usuario el próximo comando. Incluír un comando de *ayuda*
    para que el programa indique al usuario cómo utilizarlo. Incluír un comando de *salida* que provoca la finalización
    del programa.

"""