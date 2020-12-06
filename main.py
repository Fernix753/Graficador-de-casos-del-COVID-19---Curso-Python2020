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

documentos = {"full_data.csv": 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'}

for doc, enlace in documentos.items():                                                      #Recorro todos los documentos necesarios, definidos en mi diccionario "documentos"
    if not os.path.exists( doc ):                                                           #De no exisitr el documento en mi carpeta actual:
        wget( enlace )                                                                      #   -> Lo descargo utilizando la función wget.

df_datos = pandas.read_csv("full_data.csv")                                                 #Lectura del documento principal, y lo asignamos a un dataframe
df_datos.fillna(0, inplace=True)                                                            #Relleno los valores NaN, con valor 0 para evitar errores en el codigo
paises = set ( df_datos["location"]  )                                                      #Creo un set con todas las locaciones para usarla en una verifiación posteriormente

#/***********************************\
#              Funciones            
#\***********************************/
def igualar_2_listas(lista1, lista2):
    for i in lista1:                                                                       #Recorro mi lista de 1
        if i not in lista2:                                                                #   ->Si el valor no está la lista 2:
            lista1.remove(i)                                                               #       ->Las remuevo. Con el fin de evitar errores en el gráfico
    for i in lista2:                                                                       #Idem atenrior
        if i not in lista1:
            lista2.remove(i)
    k = lista1 if len(lista1) <= len(lista2) else lista2
    return k

def cruce(i, YPrimerPais, YSegundoPais):
    if i > 0:
        yp1_pto1, yp1_pto2 = YPrimerPais[i-1], YPrimerPais[i]
        yp2_pto1, yp2_pto2 = YSegundoPais[i-1], YSegundoPais[i]
        dif1 = yp1_pto1 - yp1_pto2
        dif2 = yp2_pto1 - yp2_pto2
        dif3 = dif1 - dif2
        if dif3 != 0:
            xf = ((yp2_pto1-yp1_pto1))/((dif1/(-1))-(dif2/(-1)))
            if xf > 0 and xf < 1:
                yf = ((dif1)/(-1)*xf)+yp1_pto1
                xf = xf+i-1
                return (xf, yf)
            else: return False
        else: return False
    else: return False

def covid_1(PAIS, save_name=None):                                                          #Gráfico los nuevos casos y muertes de 1 pais
    df_filtrado = df_datos[ df_datos["location"] == PAIS ]                                  #Hago un nuevo dataframe, filtrando por locación
    datosy_cases = []                                                                       #   ->Creo una lista para los valores de "cases", los casos para ese dia
    datosy_deaths = []                                                                      #   ->Creo otra lista para los valores de "death", las muertes para dia
    datosx = list (df_filtrado["date"])                                                     #   ->Creo otra lista, con los valores para el eje X, en este caso las fechas.
    for i in range(len(datosx)):                                                            #Recorro mi lista de fechas
        aux_fecha = datosx[i]                                                               #   Variable Auxiliar de las fechas
        aux_var = int(df_filtrado[ df_filtrado["date"] == aux_fecha]["total_cases"])        #   Variable auxiliar del total de casos para ese día
        aux_var = np.log10(aux_var) if aux_var > 0 else aux_var                             #   ->Si la variable es mayor a 0, la paso por la función log, de lo contrario la colocomo como está
        aux_var1 = int(df_filtrado[ df_filtrado["date"] == aux_fecha]["total_deaths"])      #   Idem anterior
        aux_var1 = np.log10(aux_var1) if aux_var1 > 0 else aux_var1                         #   -
        datosy_cases.append( aux_var )                                                      #   Agrego a mi lista de casos la variable auxiliar
        datosy_deaths.append( aux_var1 )                                                    #   Agrego a mi lista de muertes la variable auxiliar

    plt.figure(figsize=(12,4))                                                              #Configuro mi gráfico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    plt.title("Gráfico de contagios contagios")                                             #Asigno titulo al gráfico
    plt.ylabel('Casos (Miles)')                                                             #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X
    plt.plot(datosx, datosy_cases, "b", label=f"{PAIS}, casos")                             #Ploteo linea casos.
    plt.plot(datosx, datosy_deaths, "r", label=f"{PAIS}, muertes")                          #Ploteo linea muertes.
    plt.legend()                                                                            #Habilito que se ploteen las leyendas
    plt.xticks(datosx[ : :14], rotation=45)                                                 #Muestro 1 fecha de cada 2 semanas (o 14 valores de mi lista)
    plt.tight_layout()                                                                      #Ajusta el gráfico automaticamente
    if (save_name!=None):                                                                   #De haber iingresado un nombre para guardar el gráfico
        plt.savefig(str(save_name))                                                         #   ->Se guarda el gráfico con el nombre deseado
    return plt.show()                                                                       #Por ultimo, muestro el gráfico en el retorno de la función

def covid_compare_2(PAIS1, PAIS2, save_name=None):                                          #Gráfico los casos y muertes de 2 paises, y sus intersecciones
    df_pais1 = df_datos[ df_datos["location"] == PAIS1 ]                                    #Hago un nuevo dataframe, filtrando por locación 1
    df_pais2 = df_datos[ df_datos["location"] == PAIS2 ]                                    #Hago un nuevo dataframe, filtrando por locación 2
    y_p1_n_cases, y_p1_n_deaths, y_p2_n_cases, y_p2_n_deaths = [], [], [], []               #Creo variables de casos y muertes para cada pais, donde alojaré las cordenadas Y (cantidad de casos)
    datosx1, datosx2 = list (df_pais1["date"]), list (df_pais2["date"])                     #Creo listas con las fechas de registradas para cada pais
    datosx = igualar_2_listas(datosx1, datosx2)                                             #Defino mi lista de fechas definitiva

    crucescasos, fechascrucescasos = [], []                                                 #Creo una lista para los cruces de los casos, donde almacenaré los valores de X e Y
    crucesmuertes, fechascrucesmuertes = [], []                                             #Creo una lista para los cruces de las muertes, donde almacenaré los valores de X e Y

    for i in range(len(datosx)):
        aux_fecha = datosx[i]                                                               #Recorro mi lista de fechas
        p1casos = int(df_pais1[ df_pais1["date"] == aux_fecha]["total_cases"])              #Uso variables auxiliares para definir si pasar por log10 los valores o no
        p1casos = np.log10(p1casos) if p1casos > 0 else p1casos
        p2casos = int(df_pais2[ df_pais2["date"] == aux_fecha]["total_cases"])
        p2casos = np.log10(p2casos) if p2casos > 0 else p2casos
        p1muert = int(df_pais1[ df_pais1["date"] == aux_fecha]["total_deaths"])
        p1muert = np.log10(p1muert) if p1muert > 0 else p1muert
        p2muert = int(df_pais2[ df_pais2["date"] == aux_fecha]["total_deaths"])
        p2muert = np.log10(p2muert) if p2muert > 0 else p2muert
        y_p1_n_cases.append(p1casos)                                                        #   ->Agrego a mi lista de casos para el pais 1, el valor actual para esta fecha
        y_p2_n_cases.append(p2casos)                                                        #   ->Agrego a mi lista de casos para el pais 2, el valor actual para esta fecha
        y_p1_n_deaths.append(p1muert)                                                       #   ->Agrego a mi lista de muertes para el pais 1, el valor actual para esta fecha
        y_p2_n_deaths.append(p2muert)                                                       #   ->Agrego a mi lista de muertes para el pais 2, el valor actual para esta fecha
    
    for i in range(len(datosx)):                                                            #Recorro mi lista de datos x
        if bool(cruce(i, y_p1_n_cases, y_p2_n_cases)):                                      #De haber un cruce
            xf, yf = cruce(i, y_p1_n_cases, y_p2_n_cases)                                   #   ->Lo agrego en mis variables
            fechascrucescasos.append(xf)                                                    #   ->Y agrego mis variables a mis listas correspondientes
            crucescasos.append(yf)
        if bool(cruce(i, y_p1_n_deaths, y_p2_n_deaths)):                                    #Idem casos para muertes
            xf, yf = cruce(i, y_p1_n_deaths, y_p2_n_deaths)
            fechascrucesmuertes.append(xf)
            crucesmuertes.append(yf)
        
    plt.figure(figsize=(12,4))                                                              #Configuro mi gráfico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    #Ploteo casos para ambos paises
    plt.subplot(1, 2, 1)                                                                    #Configuracion para usar 2 gráficos en 1 fila
    plt.title("Gráfico de contagios")                                                       #Asigno titulo al gráfico
    plt.ylabel('Contagios (miles)')                                                         #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X
    plt.plot(datosx, y_p1_n_cases,color = '#FF7777',label=f"{PAIS1}, casos")                #Ploteo linea casos pais 1.
    plt.plot(datosx, y_p2_n_cases,color = '#7777FF',label=f"{PAIS2}, casos")                #Ploteo linea casos pais 2.
    plt.plot(fechascrucescasos, crucescasos,'g+',label="Intersecciones")                    #Gráfico las intersecciones
    plt.xticks(datosx1[ : :14], rotation=45)                                                #Muestro 1 fecha de cada 2 semanas
    plt.legend()                                                                            #Habilito que se ploteen las leyendas
    #Ploteo nuevas muertes para ambos paises
    plt.subplot(1, 2, 2)                                                                    #Idem anterior
    plt.title("Gráfico de muertes")
    plt.ylabel('Muertes (miles)')
    plt.xlabel('Fechas')
    plt.plot(datosx, y_p1_n_deaths,color = '#FF0000',label=f"{PAIS1}, muertes")
    plt.plot(datosx, y_p2_n_deaths,color = '#0000FF',label=f"{PAIS2}, muertes")
    plt.plot(fechascrucesmuertes, crucesmuertes,'g+',label="Intersecciones")
    plt.xticks(datosx1[ : :14], rotation=45)
    plt.legend()
    plt.tight_layout()                                                                      #Ajusta el gráfico automaticamente
    if (save_name!=None):                                                                   #De haber iingresado un nombre para guardar el gráfico
        plt.savefig(str(save_name))                                                         #   ->Se guarda el gráfico con el nombre deseado
    return plt.show()                                                                       #Por ultimo, muestro el gráfico en el retorno de la función

def covid_compare_x(l_paises, lapso=None,  save_name=None):                                 #Gráfico los nuevos casos de varios X paises
    plt.figure(figsize=(12,4))                                                              #Configuro mi gráfico de manera rectangular, haciendolo 3 veces mas ancho que alto.
    plt.title("Gráfico de contagios contagios")                                             #Asigno titulo al gráfico
    plt.ylabel('Contagios (miles)')                                                         #Asigno titulo de valores eje Y
    plt.xlabel('Fechas')                                                                    #Asigno titulo de valores eje X

    fechas = None   #Variable para contener todas las fechas, sin repeticiones
    datosx = []     #Variable para contener todas las fechas, ordenadas en una lista
    #           ROJO        PURPURA     AZUL        VERDE       Negro oscuro     
    colores = ["#FF0000",   "#8000FF",  "#0000FF",  "#00FF00",  "#c2c2c2",                  #Creo una lista con los colores para las lineas, esta lista limita
    #   CLST-VRDE   AMARILLO2   GRIS OSCURO ROSA                                            #la cantidad de paises que puedo comparar, alargarla aumentará las posibilidades de la función.
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
                pais_casos = int(df_pais[ df_pais["date"] == fecha ]["total_cases"])                       #    ->Variable auxiliar
                pais_casos = np.log10(pais_casos) if pais_casos > 0 else pais_casos
                datosy_newcases.append( pais_casos )                                                       #    ->Agrego el valor a mi lista de valores en Y
                if (fecha not in datosx):                                                                  #    ->Y si la fecha, NO existe en mi lista de valores X
                    datosx.append(fecha)                                                                   #        ->La agrego a la misma
        plt.plot(datosx, datosy_newcases, color = colores[contador], label=f"{i}, casos")                  #    ->Ploteo mis datos del pais, colocando el color por orden de mi lista de colores
        contador += 1                                                                                      #    ->Sumo a mi contador para la proxima iteración
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
                    print( f"\nLa fecha o lapso introducido, {lapso[1]} ,está", end="")                    #                ->Considero que el rango es invalido.
                    return print(" fuera de del rango de fechas, o bien tiene un formato invalido.\n")     #
                if (len(datosx) - datosx.index(lapso[0])) >= int( lapso[1] ):                              #            ->Si la cantidad de dias deseados, es posible
                    plt.xticks(datosx[ : :1], rotation=45)                                                 #                ->Configuro para mostrar todos los dias, y no 1 cada 2 semanas
                    if (int( lapso[1] ) > 60):                                                             #                ->Si los dias deseados superan los 60, 
                        plt.xticks(datosx[ : :7], rotation=45)                                             #                    ->Configuro para mostrar 1 dia de cada semana
                    plt.xlim(left=datosx.index(lapso[0]),                                                  #                ->Se limitan los bordes del gráfico a los valores deseados
                    right= datosx.index(datosx[datosx.index(lapso[0]) + lapso[1]]))
                else:
                    print( f"\nLa fecha introducida, {lapso[1]} dias despues del {lapso[0]}", end="")
                    return print(" ,está fuera del rango de fechas para estos paises.\n")
        else:
            print( f"\nLa fecha introducida, {lapso[0]} ,está fuera del rango de fechas", end="" )
            return print(" para estos paises, o bien tiene un formato invalido..\n")
    plt.tight_layout()                                                                                     #Ajusta el gráfico automaticamente
    if (save_name!=None):                                                                                  #De haber ingresado un nombre para guardar el gráfico
        plt.savefig(str(save_name))                                                                        #   ->Se guarda el gráfico con el nombre deseado
    return plt.show()                                                                                      #Retorno el ploteo

#/***********************************\
#              Main            
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
            try_pais = try_pais.capitalize()
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
            else:
                try_pais = input(f"No se encuentra {try_pais} en la lista de paises, pruebe ingresando otra vez el pais:\n")
        elif opcion == "2":                                                                                                                                                 #->Si la opción es la 2
            print("Elegiste la opción 2, esto graficará los casos y muertes de DOS pais, se graficarán las intersecciones de los mismos, a continuación ingresa un pais:")  #   ->Mensaje de explicación
            try_pais1 = input("Ingrese el pais 1:\n")                                                                                                                       #   ->Input del primer pais
            try_pais2 = input("Ingrese el pais 2:\n")                                                                                                                       #   ->Input del segundo pais
            try_pais1 = try_pais1.capitalize()
            try_pais2 = try_pais2.capitalize()
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
                try_pais = try_pais.capitalize()
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
        opcion = input("Opción deseada:\n")                                                                                                                                 #   ->Solicito un nuevo input21