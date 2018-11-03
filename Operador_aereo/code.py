#-*- coding: utf-8 -*-

### --- Librerias de Python

import os
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import datetime
from datetime import date
import shutil
import pygame
from pygame.locals import *

### --- Funciones necesarias

def comprice(filter =None): # Genera un gráfico que compara precios según los vuelos
    week_days = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    file = open(os.path.join("private_data","maxmin.txt"),'r')
    data = file.readlines()
    file.close()

    ### En estas listas guardamos los precios según el vuelo
    p1_max =[]
    p2_max = []
    p1_min = []
    p2_min = []
    p1_av = []
    p2_av = []

    if filter == "semana": #Esta es la variación de la gráfica según el día de la semana
        for i in range(7):
            p1_max.append([])
            p1_min.append([])
            p1_av.append([])
            p2_max.append([])
            p2_min.append([])
            p2_av.append([])
    for i in data: #Guardamos la información previamente computada
        if filter == "semana":
            t = date(2018,9,data.index(i)+1)
            ind = t.weekday()
            p1_max[ind].append(float(i.split(",")[0].split(":")[0]))
            p1_min[ind].append(float(i.split(",")[0].split(":")[1]))
            p1_av[ind].append(float(i.split(",")[0].split(":")[2]))
            p2_max[ind].append(float(i.split(",")[1].split(":")[0]))
            p2_min[ind].append(float(i.split(",")[1].split(":")[1]))
            p2_av[ind].append(float(i.split(",")[1].split(":")[2]))
        else:
            p1_max.append(float(i.split(",")[0].split(":")[0]))
            p1_min.append(float(i.split(",")[0].split(":")[1]))
            p1_av.append(float(i.split(",")[0].split(":")[2]))
            p2_max.append(float(i.split(",")[1].split(":")[0]))
            p2_min.append(float(i.split(",")[1].split(":")[1]))
            p2_av.append(float(i.split(",")[1].split(":")[2]))
    if filter == "semana": # Agregamos la informaci de interés para la gráfica
        p1_s_max = []
        p1_s_min = []
        p1_s_av = []
        p2_s_max = []
        p2_s_min = []
        p2_s_av = []
        for i in p1_max:
            p1_s_max.append(max(i))
        for i in p1_min:
            p1_s_min.append(min(i))
        for i in p1_av:
            p1_s_av.append(sum(i)/len(i))
        for i in p2_max:
            p2_s_max.append(max(i))
        for i in p2_min:
            p2_s_min.append(min(i))
        for i in p2_av:
            p2_s_av.append(sum(i)/len(i))
    ### Añadimos los puntos a la grafica(x,y)
        plt.plot(week_days,p1_s_max,label = "Precio maximo 2892")
        plt.plot(week_days,p1_s_av,label = "Precio medio 2892")
        plt.plot(week_days,p1_s_min,"--",label = "Precio minimo 2892")
        plt.plot(week_days,p2_s_max,label = "Precio maximo 3745")
        plt.plot(week_days,p2_s_av,label = "Precio medio 3745")
        plt.plot(week_days,p2_s_min,"--",label = "Precio minimo 3745")

    else:
        plt.plot(range(1,31),p1_max,label = "Precio maximo 2892")
        plt.plot(range(1,31),p1_av,label = "Average price 2892")
        plt.plot(range(1,31),p1_min,"--",label = "Precio minimo 2892")
        plt.plot(range(1,31),p2_max,label = "Precio maximo 3745")
        plt.plot(range(1,31),p2_av,label = "Average price 3745")
        plt.plot(range(1,31),p2_min,"--",label = "Precio minimo 3745")
        if max(p1_max) > max(p2_max):
            plt.axis([1,30,0,max(p1_max)+100])
        else:
            plt.axis([1,30,0,max(p2_max)+100])

    plt.xlabel('Dia')
    plt.ylabel('€')
    plt.title("Comparador precios")
    plt.legend()
    plt.show()
    a = str(input("Presiona la tecla enter para volver al menu"))

def compoc(filter =None): # Genera un gráfico que compara la ocupación según los vuelos
    week_days = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

    files = os.listdir("c-data")
    oc_1 =[]
    oc_2 = []

    for i in range(30): # Construyo la lista con los valores iniciales
        oc_1.append(0.0)
        oc_2.append(0.0)
    # Agregamos la ocupación en porcentaje sabiendo que hai 160 plazas
    for i in files:
        if i.split("_")[1] == "2892":
            oc_1[int(i[6:8])-1]+=(1.0/1.6)
        else:
            oc_2[int(i[6:8])-1]+=(1.0/1.6)
    # En caso de que queramos la tabla en función del dia de la semana se complica un poco porque tenemos que calcular cuantos
    # Como dias de la semana se repiten por mes hay que calcular una media
    if filter == "semana":
        oc_1_s = []
        oc_2_s = []
        oc_1_f = []
        oc_2_f = []
        for i in range(7):
            oc_1_s.append([])
            oc_2_s.append([])
        for i in range(30):
            t = date(2018,9,i+1)
            ind = t.weekday()
            oc_1_s[ind].append(oc_1[i])
            oc_2_s[ind].append(oc_2[i])
        for i in range(7):
            oc_1_f.append(sum(oc_1_s[i])/len(oc_1_s[i]))
            oc_2_f.append(sum(oc_2_s[i])/len(oc_2_s[i]))
    # Agregamos los valores a las columnas
        plt.bar(week_days,oc_2_f,label = "Ocupación vuelo 3745",align = "edge",width = -0.4)
        #Como el alineamiento es lateral, al poner el "width" negativo conseguimos que se alinee al otro lado (ver documentación de matplotlib para mayor información)
        plt.bar(week_days,oc_1_f,label = "Ocupación vuelo 2892",align = "edge",width = 0.4)
    else:
        plt.bar(range(1,31),oc_1,label = "Ocupación vuelo 2892",align = "edge",width = 0.4)
        plt.bar(range(1,31),oc_2,label = "Ocupación vuelo 3745",align = "edge",width = -0.4)

    plt.xlabel('Dia')
    plt.ylabel('%')
    plt.title("Comparador ocupación")
    plt.legend()
    plt.show()

def comped(filter = None): # Genera un gráfico que compara las edades medias según los vuelos
    week_days = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    file = open(os.path.join("manifiestos","Vuelos_Edad_Media.csv"))
    reader = csv.reader(file,delimiter = ":",lineterminator = "\r") ##Leemos los archivos en el formato en el que han sido escritos
    vuelos = []
    n = 0
    for row in reader:
        if n==0:n+=1
        else:
            vuelos.append([row[0][0:4],row[0][4:6],row[0][6:],row[1],row[2]])
    file.close()
    vuelos.sort(key=lambda tup: tup[2])
    ev1 = []
    ev2 = []
    if filter == "semana": # Hacemos medias
        ev1t = []
        ev2t = []
        ev1f = []
        ev2f = []
        for i in range(7):
            ev1t.append(0)
            ev2t.append(0)
            ev1.append(0)
            ev2.append(0)
        for i in vuelos:
            t = date(int(i[0]),int(i[1]),int(i[2]))
            if i[3] == "2892":
                ev1t[t.weekday()]+=1
                ev1[t.weekday()]+=float(i[4])
            elif i[3] == "3475":
                ev2t[t.weekday()]+=1
                ev2[t.weekday()]+=float(i[4])
        for i in range(7):
            ev1f.append(ev1[i]/ev1t[i])
            ev2f.append(ev2[i]/ev2t[i])

        plt.bar(week_days,ev1f,label = "Edad media 2892",align = "edge",width = 0.4)
        plt.bar(week_days,ev2f,label = "Edad media 3745",align = "edge",width = -0.4)
    else:
        for i in vuelos:
            if i[3] == "2892":
                ev1.append(float(i[4]))
            elif i[3] == "3475":
                ev2.append(float(i[4]))
            else:
                print("Data con datos incorrectos")
                input("Presiona enter para salir")
                quit()
        plt.bar(range(1,31),ev1,label = "Edad media 2892",align = "edge",width = 0.4)
        plt.bar(range(1,31),ev2,label = "Edad media 3745",align = "edge",width = -0.4)
    plt.xlabel('Dia')
    plt.ylabel('Edad media')
    plt.title("Comparador edades medias")
    plt.legend()
    plt.show()

def show_err(): # Muestra los archivos con información incorrecta
    #Durante la generación de caché ya se escribe en los archivos los errores que tienen
    fileS = os.listdir("b-data")
    for i in fileS:
        print("Nombre del archivo:",i)
        print()
        file = open(os.path.join("b-data",i),'r')
        data =file.readlines()
        file.close()
        print("Información entregada:")
        for i in data[:4]:
            print(" ",i[:-1])
        print()
        print("Errores:")
        for i in data[5:]:
            print(i[:-1])
        print()
    print()
    input("Presiona enter para volver al menú")

def clear(): #Comprueba la información dentro de la carpeta data y prepara todo para funcionar
    try:
        files = os.listdir('data')
    except FileNotFoundError:
        print("Si no hay carpeta data no hay información con la que trabajar")
        try:os.remove("eula.txt")
        except FileNotFoundError: pass
        a = input("Presione enter para salir")
        quit()
    av_days = []
    abecedario = ['T','R','W','A','G','M','Y','F','P','D','X','B','N','J','Z','S','Q','V','H','L','C','K','E']
    for i in range(30):
        if i < 9: av_days.append(("0"+str(i+1)))
        else: av_days.append(str(i+1))
    carpet_names = ["c-data","b-data","output","private_data","manifiestos","custom_manifests"]
    for i in carpet_names:
        if i in os.listdir(os.getcwd()):
            shutil.rmtree(i)
            print("Directorio",i,"eliminado")
            os.mkdir(i)
        else:
            os.mkdir(i)
            print("Directorio "+i+" creado")
    print("Limpiando la información")
    for i in files:
        err_ls = "\n"
        format_err = False
        if len(i) == 21:
            format_err = True
            d_check = False
            if i[0:4] == "2018" and i[4:6] == "09" and i[6:8] in av_days:d_check = True
            else:err_ls+= "Fecha de billete no válido\n"

        else: err_ls+= "Formato no válido\n"
        file = open('data/'+i,'r')
        data = file.readlines()
        file.close()
        data_err = False
        dn_chk = False
        born_ch = True
        if len(data)==4:
            data_err = True
            dni_num = int(data[0][0:8])
            letter = abecedario[dni_num%23]
            if data[0][8]== letter:dn_chk = True
            else:err_ls += "Dni no válido\n"
            try:t = date(int(data[2][0:4]),int(data[2][4:6]),int(data[2][6:8]))
            except ValueError:
                err_ls+= "Fecha de nacimiento no válida\n"
                born_ch = False
        else:
            err_ls += "Data con información en formato no válido\n"
        if dn_chk and d_check and born_ch and format_err and data_err:shutil.copyfile('data/'+i,'c-data/'+i)
        else:
            print("Archivo "+i+" con datos incorrectos encontrados")
            shutil.copyfile(os.path.join('data/',i),os.path.join('b-data/',i))
            file = open(os.path.join("b-data",i),'a')
            file.write(err_ls)
            file.close()

def optimizar(): #Muestra los mejores clientes en función de su sexo, edad y día de gasto
    file = open(os.path.join("private_data","emm.txt"),'r')
    data =  file.read().split(":")
    max_age = int(data[0])
    min_age = int(data[1])
    week_days = ["lunes","martes","miércoles","jueves","viernes","sábados","domingos"]
    week_days_c = ["Lunes:    ","Martes:   ","Miércoles:","Jueves:   ","Viernes:  ","Sábados:  ","Domingos: "]
    intervalos = []
    values =  [] #Aquí se almacena la información completa de los usuarios
    files = os.listdir("c-data")
    for i in files:
        file = open(os.path.join("c-data",i),'r')
        data = file.readlines()
        file.close()
        genre = data[3][:-1]
        paid = float(data[1])
        born = datetime.date(int(data[2][:4]),int(data[2][4:6]),int(data[2][6:8]))
        act_time = datetime.date(2018,9,int(i[6:8]))
        age = int(float(str(act_time-born).split(" ")[0])//365.25)
        values.append([genre,age,paid,act_time.weekday()])
    genres = ["M","F"]
    max_int = (max_age//10) +1
    min_int = min_age//10
    init_val = []
    for i in range(7):
        init_val.append(0)
    for i in range(max_int-min_int):
        intervalos.append([init_val.copy(),init_val.copy()])
    for i in values: # Aquí se añade el dinero gastado por grupo
        index =int(i[1]//10 -min_int)
        intervalos[index][genres.index(i[0])][i[-1]]+=i[2]

    max_prof = [0,0,0]
    max_prof_g = ["","",""]
    max_prof_age = [0,0,0]
    for i in intervalos:
        for l in i:
            for k in range(3):
                if sum(l) > max_prof[k]:### Tal y como está guardada la información es así de sencillo buscar los mayores gastos
                    max_prof.insert(k,sum(l))
                    max_prof.pop(-1)
                    max_prof_g.insert(k,genres[i.index(l)])
                    max_prof_g.pop(-1)
                    max_prof_age.insert(k,intervalos.index(i))
                    max_prof_age.pop(-1)
                    break
    other_big_prof = [[0,0,0],[0,0,0],[0,0,0]]
    other_big_prof_d = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3): # Escogemos los 3 días que más gastaron para dar información adicional
        for l in range(7):
            for h in range(2):
                if intervalos[max_prof_age[i]][genres.index(max_prof_g[i])][l] > other_big_prof[i][h]:
                    other_big_prof[i].insert(h,intervalos[max_prof_age[i]][genres.index(max_prof_g[i])][l])
                    other_big_prof[i].pop(-1)
                    other_big_prof_d[i].insert(h,l)
                    other_big_prof_d[i].pop(-1)
                    break
    for i in range(3): # Mostramos el resultado
        if max_prof_g[i] == "F":
            print("Las mujeres de entre",(max_prof_age[i]+min_int)*10,"y",(max_prof_age[i]+min_int+1)*10,"años se gastaron",round(max_prof[i],2),"€")
        elif max_prof_g[i] == "M":
            print("Los hombres de entre",(max_prof_age[i]+min_int)*10,"y",(max_prof_age[i]+min_int+1)*10,"años se gastaron",round(max_prof[i],2),"€")
        for l in range(3):
            print("  De este dinero",round(other_big_prof[i][l],2),"€ los gastaron los ",week_days[other_big_prof_d[i][l]])
        print()
    condition = True
    while condition: # Por si quieren ver lo gastado por otros grupos
        print("Quieres ver lo que gastaron otros grupos de personas?(y,n)")
        ans = input(" - >").lower()
        if ans == "y":
            condition = False
        elif ans == "n":
            break
        else:
            print("Operación no programada")
    else:
        condition = True
        while condition: #Tan solo hay que sumar las listas previamente rellenadas
            print("Puedes escoger entre estos intervalos")
            for i in range(max_int-min_int):
                print(i,"- Personas entre",(i+min_int)*10,"y",(i+min_int+1)*10,"años")
            try:
                ans = int(input(" - >"))
                if ans not in range(max_int-min_int):
                    print("Valor numérico entero entre",min_int,"y",min_int+max_int-1)
            except ValueError:
                print("Valor numérico entero por favor")
                continue
            print("\n\n")
            print("Este grupo gastó un total de",round(sum(intervalos[ans][0])+sum(intervalos[ans][1]),2),"€")
            print(" Los hombres gastron:",round(sum(intervalos[ans][0]),2),"€")
            for i in range(7):
                print("  "week_days_c[i],"  ",round(intervalos[ans][0][i],2),"€")
            print(" Las mujeres gastaron:",round(sum(intervalos[ans][1]),2),"€")
            for i in range(7):
                print("  "week_days_c[i],"  ",round(intervalos[ans][1][i],2),"€")
            print("\n\n")
            while True:
                print("Quieres ver lo que gastaron otros grupos de personas?(y,n)")
                ans = input(" - >").lower()
                if ans == "y":
                    break
                elif ans == "n":
                    condition = False
                    break
                else:
                    print("Operación no programada")

def generate_all(): # Genera toda la información previamente para que todo sea instantáneo
    ### --- Informacion bruta que va a ser procesada y almacenada en las siguentes listas
    files =os.listdir("c-data")

    week_days = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    users = [] #Aqui alamcenaremos cada DNI como identificador del usuario
    t_u = [] # Y con el mismo indice las veces que ha cogido un avion
    p_u = [] # Aqui se guarda lo que gasta el usuario
    v = [] #Aqui guardamos los identificadores de los vuelos
    oc_v = [] # Las veces que los cogieron
    p_v = [] # precio del vuelo
    u_y = []# Suma de las edades de los usuarios del vuelo
    p_d = [0.0,0.0,0.0,0.0,0.0,0.0,0.0] #Suma de los precios por dia de la semana
    t_d = [0.0,0.0,0.0,0.0,0.0,0.0,0.0] #Suma de billetes por dia de la semana
    t_s = [0.0,0.0,0.0,0.0,0.0,0.0,0.0] # Suma de vuelos por dia de la semana
    o_d = [0.0,0.0,0.0,0.0,0.0,0.0,0.0] #Ocupacion por dia de la semana
    m = [0,0,0,0,0,0,0] # Hombres por dia de la semana
    fem = [0,0,0,0,0,0,0] # Mujeres por dia de la semana
    pr_d_1 = [] # Precio por dia del vuelo 2892
    for i in range(30):
        pr_d_1.append([])
    pr_d_2 = [] # Precio por dia del vuelo 3745
    for i in range(30):
        pr_d_2.append([])

    ### Valores iniciales exagerados para que el programa se reajuste
    min_age = 100
    max_age = 0

    ### --- Procesado para cada una de las funciones pedidas

    for i in files: # Guardo el nombre del archivo en i para futuros usos

        file = open("c-data/"+i,'r')  # Vamos abriendo cada uno de los archivos
        data = file.readlines() # Informacion del archivo
        file.close() #Cerramos para liberar memoria
        u_d = data[0][0:9] #Este es el DNI que hay en cada archivo
        gender = data[3] # El género
        if u_d in users: # Si ya está en la lista agregamos 1 a las veces que estuvo y el dinero que gastó
            t_u[users.index(u_d)] +=1
            p_u[users.index(u_d)] +=float(data[1])
        else: # Si no, lo añadimos a la lista con la informacion basica para que el algoritmo funcione
            users.append(u_d)
            t_u.append(1)
            p_u.append(float(data[1]))

        f = i.split("_")[0:2] # Identificador de cada vuelo

        t = date(int(data[2][0:4]),int(data[2][4:6]),int(data[2][6:8])) #Edad de la persona
        f1 = i.split("_")[0]
        t2 = date(int(f1[0:4]),int(f1[4:6]),int(f1[6:8])) # Fecha del vuelo
        age = int(float(str(t2-t).split(" ")[0])//365.25) #Para calcular las edades

        # Necesito la edad máxima y mínima para el calculador de precios

        if age < min_age:
            min_age = age
        if age > max_age:
            max_age = age

        price = float(data[1]) # Precio del vuelo
        ind  = t2.weekday() # Aprovechando la libreria datetime
        p_d[ind]+=price
        t_d[ind]+=1.0 # Añadimos el billete al numero de billetes en funcion del dia de la semana

        # Esta informacion se guarda para el comparador de precio
        if f[1] =="2892":
            pr_d_1[int(f1[6:])-1].append(price) # Precio del vuelo 2892 por día
        else:
            pr_d_2[int(f1[6:])-1].append(price) # Precio del vuelo 3475 por día


        if f in v: #Si el vuelo estaba ya agregamos informacion sobre el
            u_y[v.index(f)]+= age # Edad para las edades media
            oc_v[v.index(f)]+=1 # Añadimos 1 por ocupante
            p_v[v.index(f)]+=float(data[1]) # Lo gastado por el ocupante
        else: #En caso contrario creamos su sitio
            v.append(f)
            oc_v.append(1.0)
            p_v.append(float(data[1]))
            u_y.append(age)
        #Contamos la cantidad de hombre  y mujeres para trabajar con ello después
        if gender == "M\n":
            m[ind]+=1
        else:
            fem[ind]+=1

    ### --- Creamos las listas que se introduciran en los .csv

    h_u = [] # En esta lista se guarda una tupla con (DNI, Veces que ha cogido el avion) de los usuarios habituales
    fl_wp = [] # En esta lista se guarda una tupla con(Vuelo, ocupación)
    fl_we = [] # En esta lista se guarda una tupla con (Vuelo, precio medio)
    fl_me = [] # En esta lista se guarda una tupla con (Vuelo, edad media)
    pr_d = [] # Lista de precios medios por dia de la semana (indice)
    oc_d = [] #Lista de ocupacion medai por dia de la semana (indice)
    rb_m = [] #Lista de relacion de hombres por dia de la semana
    rb_f = [] # Lista de relacion de mujeres por dia de la semana
    g_u = [] #Lista de tuplas con (DNI, dinero gastado)
    pm_d_1 = []# Precio maximo y mínimo and average en función del día del vuelo 2892
    pm_d_2 = []# Precio máximo y mínimo and average función del día del vuelo 3875

    ### --- Rellenamos las listas creadas con la informacion procesada

    for i in range(len(users)):
        if t_u[i] > 1:
            h_u.append((users[i],t_u[i]))
        g_u.append((users[i],p_u[i]))

    for i in range(len(v)):
        fl_wp.append((v[i],oc_v[i]/160.0))
        fl_we.append((v[i],p_v[i]/oc_v[i]))
        fl_me.append((v[i],u_y[i]/oc_v[i]))

    for i in fl_wp:
        f = i[0][0]
        t = date(int(f[0:4]),int(f[4:6]),int(f[6:8]))
        ind  = t.weekday()
        o_d[ind]+=i[1]
        t_s[ind]+=1

    for i in range(7):
        pr_d.append(round(p_d[i]/t_d[i],2))
        oc_d.append(round((o_d[i]/t_s[i])*100,2))

        total = m[ind] + fem[ind]
        rb_m.append(round((m[ind]/total) * 100,2))
        rb_f.append(round((fem[ind]/total) * 100,2))


    for i in pr_d_1:
        pm_d_1.append([max(i),min(i),sum(i)/len(i)])
    for i in pr_d_2:
        pm_d_2.append([max(i),min(i),sum(i)/len(i)])

    ### --- Ordenamos las listas de mayor a menor que haga fata

    h_u.sort(key=lambda tup: tup[1], reverse = True)

    fl_wp.sort(key=lambda tup: tup[1], reverse = True)

    fl_we.sort(key=lambda tup: tup[1], reverse = True)

    fl_me.sort(key=lambda tup: tup[1], reverse = True)

    g_u.sort(key=lambda tup: tup[1],reverse = True)

    ### --- Generamos los csv con las nuevas listas

    file_name = "Usuarios_habituales.csv" #
    data_f = [["DNI","Veces que ha volado"]]
    for i in h_u:
        data_f.append([i[0],i[1]])
    generate(data_f,file_name)

    file_name = "Vuelos_Porcentaje_Ocupacion.csv" #
    data_f = [["Fecha","Vuelo","Porcentaje (%)"]]
    for i in fl_wp:
        data_f.append([i[0][0],i[0][1],round(i[1]*100,2)])
    generate(data_f,file_name)

    file_name = "Vuelos_Precio_Medio.csv" #
    data_f = [["Fecha","Vuelo","Precio (euros)"]]
    for i in fl_we:
        data_f.append([i[0][0],i[0][1],round(i[1],2)])
    generate(data_f,file_name)

    file_name = "Vuelos_Edad_Media.csv" #
    data_f = [["Fecha","Vuelo","Edad media"]]
    for i in fl_me:
        data_f.append([i[0][0],i[0][1],round(i[1],2)])
    generate(data_f,file_name)

    file_name = "Precio_Medio_Semana.csv"
    data_f = [week_days,pr_d]
    generate(data_f,file_name)

    file_name = "Ocupacion_Media_Semana.csv"
    rweek_days = week_days.copy()
    rweek_days.insert(0," ")
    oc_d.insert(0,"%")
    data_f = [rweek_days,oc_d]
    generate(data_f,file_name)

    file_name = "Reparto_Generos_Semana.csv"
    rweek_days = week_days.copy()
    rweek_days.insert(0,"%")
    rb_m.insert(0,"Hombres")
    rb_f.insert(0,"Mujeres")
    data_f = [rweek_days,rb_m,rb_f]
    generate(data_f,file_name)

    file_name = "10_mejores_clientes.csv" #
    data_f = [["DNI","Dinero gastado (euros)"]]
    for i in g_u[:10]:
        data_f.append([i[0],round(i[1],2)])
    generate(data_f,file_name)

    ### --- Generamos los datos de máximos y mínimos y medias para que se genere la tabla de precios

    directory = "private_data/"
    file_name = "maxmin.txt"
    txt = ""
    for i in range(30):
        p1_max,p1_min,p1_av = pm_d_1[i]
        p2_max,p2_min,p2_av = pm_d_2[i]
        txt+=str(p1_max)+":"+str(p1_min)+":"+str(p1_av)+","+str(p2_max)+":"+str(p2_min)+":"+str(p2_av)+"\n"
    file = open(os.path.join(directory,file_name),'w')
    file.write(txt)
    file.close()

    ### --- Guardamos la edad máxima y la minima para el optimizador de economia:

    file = open(os.path.join("private_data","emm.txt"),'w')
    file.write(str(max_age)+":"+str(min_age))
    file.close()

    ### --- Generamos las representaciones de los aviones

    print("Generando representaciones de los aviones ;)")
    h_siz = 9*4
    v_siz = 5*4
    h_off = 2*4
    v_off = 2*4
    ht_off = 113*4
    vt_off = 55*4
    pygame.init()
    plantilla = pygame.image.load(os.path.join("prefabs","plantilla.jpg"))
    surfaces = []
    h_ind = "ABCD"
    d_col = {"M":(255,0,0),"F":(0,255,0)}
    for i in range(60):
        surfaces.append(plantilla.copy())
    files = os.listdir("c-data")
    for i in surfaces:
        for l in range(40):
            for h in range(4):
                pygame.draw.rect(i,(150,150,150),((h_siz+h_off)*h+ht_off,(v_siz+v_off)*l+vt_off,h_siz,v_siz))
    for i in files:
        f = i.split("_")
        index = int(f[0][6:])-1
        if f[1] == "2892": #Para los indices de los canvas en los que dibujo añado una diferencia de 30 entre los vuelos
            bias = 0
        else:
            bias = 30
        file = open(os.path.join("c-data",i))
        data = file.readlines()
        file.close()
        genre_c = d_col[data[-1][:-1]]
        pygame.draw.rect(surfaces[index+bias],genre_c,((h_siz+h_off)*h_ind.index(f[2][2])+ht_off,(v_siz+v_off)*(int(f[2][:2])-1)+vt_off,h_siz,v_siz))
        t = date(2018,9,int(i[6:8]))
        t2 = date(int(data[2][0:4]),int(data[2][4:6]),int(data[2][6:8]))
        age = int(float(str(t-t2).split(" ")[0])//365.25) #Para calcular las edades
        if age < 17: ## Dibujamos un indicador azul para los menores
            pygame.draw.rect(surfaces[index+bias],(0,0,255),((h_siz+h_off)*h_ind.index(f[2][2])+ht_off,(v_siz+v_off)*(int(f[2][:2])-1)+vt_off,h_siz/2,v_siz))
    n = 0
    for i in surfaces:
        if n < 30:
            if n+1 < 10:# Hay que tener cuidado con los enteros menores de 10 para el nombre de los archivos
                file_name = "2018090"+str(n+1)+"_2892"
            else:
                file_name = "201809"+str(n+1)+"_2892"
        else:
            if n-29 < 10:
                file_name = "2018090"+str(n-29)+"_3475"
            else:
                file_name = "201809"+str(n-29)+"_3475"
        pygame.image.save(i,os.path.join("output",file_name+".jpg"))
        print("Image "+file_name+".jpg"+" saved")
        n+=1
    pygame.quit()

def generate(data,file_name,folder = "manifiestos/"): # Escribe los .csv
    file = open(folder+file_name,'w')
    writer = csv.writer(file,lineterminator = '\r',delimiter = ":") #Cambiamos el lineterminator para que estén juntas las filas
    for i in data:
        writer.writerow(i) # Como ya estaba previamente ordenado solo hay que añadirlos como columnas
    file.close()
    print("Archivo guardado como",file_name,"en la carpeta "+folder[:-1])

def readit(file_name,folder = "manifiestos/"):# Lee los .csv
    try:
        file = open(folder+file_name,"r")
    except FileNotFoundError: ## Cualquier archivo que no existe implica una mala instalación
        print("Faltan archivos base así que en la proxima ejecución del programa se procederá a una resinstalación")
        files = os.listdir(os.getcwd())
        if "eula.txt" in files:
            os.remove("eula.txt")
        a = input("Presiona enter para salir")
        quit()

    reader = csv.reader(file,delimiter = ":",lineterminator = "\r") ##Leemos los archivos en el formato en el que han sido escritos
    n = 0
    for row in reader:
        if n == 0:
            base = row #Se supone que cuando guarda la información la primera línea es un índice
            n+=1
        else:
            txt = ""
            for i in range(len(base)):
                txt+=str(base[i])+": "+str(row[i])+ "   "
            print(txt)
    print()
    print("Podes atopar o arquivo en",folder+file_name)
    print()
    a = str(input("Presiona la tecla enter para continuar"))

def findit(): # Crea los manifiestos personalizados
    ### --- Pedimos los valores al usuario
    while True:
        try:
            ans = int(input("Dia del vuelo?(1-30)"))
            if ans< 1 or ans >30:
                print("Valor numerico entre 1 y 30 por favor")
            else:
                if ans < 10: #Hacemos esta comrpobación para asignar buen los nombres de los archivos
                    d_date = "2018090"+str(ans)
                else:
                    d_date = "201809"+str(ans)
                dd_date = ans
                break
        except ValueError:
            print("Valor numérico entre 1 y 30 por favor")
    while True:
        print("Escoge un vuelo indicando el numero antes del vuelo:")
        print("1  - 2892")
        print("2  - 3475")
        ans = str(input("-> "))
        if ans == "1":
            flight = "2892"
            break
        elif ans == "2":
            flight = "3475"
            break
        else:
            print("Opcion no programada")

    ### --- Guardamos la información en listas con índices comunes y así simplificamos el proceso
    files = os.listdir("c-data")
    asientos = []
    dni =  []
    dinero_pagado = []
    fecha_de_nacimiento = []
    gender = []
    ages = []
    men_edad = []
    for i in files:
        if i[:13] == d_date+"_"+flight: #Basicamente vamos agregando a las listas la información que va a aperecer en los csv
            asientos.append(i[14:17])
            file = open("c-data/"+i,'r')
            data = file.readlines()
            file.close()
            dni.append(data[0])
            dinero_pagado.append(data[1])
            year = int(data[2][:4])
            month = int(data[2][4:6])
            day = int(data[2][6:8])
            t = date(year,month,day)
            t2 = date(2018,9,int(dd_date)) # Fecha del vuelo
            age = int(float(str(t2-t).split(" ")[0])//365.25) #Para calcular las edades
            if month <10:
                month = "0"+str(month)
            if day >9:
                fecha_de_nacimiento.append(str(year)+"/"+str(month)+"/"+str(day))
            else:
                fecha_de_nacimiento.append(str(year)+"/"+str(month)+"/0"+str(day))
            gender.append(data[3])
            ages.append(age)
            if age <18:
                men_edad.append("Sí")
            else:
                men_edad.append("No")

    ### --- Generamos el .csv en el formato que el manifest_reader lo pueda interpretar

    file_name = d_date+"_"+flight+".csv"
    data_f = [["Asiento","Dni","Dinero pagado","Fecha de nacimiento","Genero","Edad","Menor de edad"]]
    for i in range(len(asientos)):
        data_f.append([asientos[i],dni[i][:-1],dinero_pagado[i][:-1],fecha_de_nacimiento[i],gender[i][:-1],ages[i],men_edad[i]])
    generate(data_f,file_name,"custom_manifests/")
    readit(file_name,"custom_manifests/")

    ### --- Le damos la opción de visualizar una representación simplificada del avión

    while True:
        print("Quieres ver una representacion del avion? y/n")
        ans = str(input().lower())
        if ans == "y":
            try:
                img = mpimg.imread('output/'+d_date+"_"+flight+".jpg") #Imagen generada durante la instalación
            except FileNotFoundError: #Cuando no existe la imágen es que se modificaron archivos y se reinstala el programa en la siguente abertura
                print("Faltan archivos base así que en la proxima ejecución del programa se procederá a una resinstalación")
                files = os.listdir(os.getcwd())
                if "eula.txt" in files:
                    os.remove("eula.txt")
                a = input("Presiona enter para salir")
                quit()
            imgplot = plt.imshow(img)
            plt.show() #Abrimos la imagen con matplotlib así se puede hacer zoom o interactuar un poco con la interfaz
            break

        elif ans == "n":break
        else: print("operacion no programada")

### --- Comprobaciones para la posible instalación o resinstalación

checkeo = False
files = os.listdir(os.getcwd()) # El archivo eula.txt le sirve al programa para saber si está todo preparado
if "eula.txt" in files:
    checkeo = False
else:
    checkeo = True
if checkeo == False:
    print("If u changed 'data', pleas, delete the file 'eula.txt' and open again the program so it can install properly")
    a = input("(Press enter to continue)")
else:
    print("Installing...")
    t = time.perf_counter()
    clear()
    generate_all()
    file = open("eula.txt","w")
    file.close()
    print("Instalation complete!")
    print("Time transcurred: "+str(time.perf_counter()-t)+"s")
    a = input("(Press enter to continue)")

### --- Comienza el menu

while True:
    ### --- Opciones
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('cs','nt','dos'):
        os.system('cls')
    print('Bienvenido...')
    print('Que quiere hacer?:')
    print('a - Mostrar una lista de los usuarios habituales')
    print('b - Mostrar los vuelos ordenados por porcentaje de ocupación')
    print('c - Mostrar los vuelos ordenados por precio medio del billete')
    print('d - Vuelos ordenados por edad media de los pasajeros')
    print('e - Precio medio de los billetes por día de la semana')
    print('f - Mostrar ocupación media de los vuelos por día de la semana ')
    print('g - Mostrar reparto de billetes vendidos entre hombres y mujeres por día de la semana')
    print('h - Mostrar lista de los 10 clientes que más dinero han gastado en septiembre')
    print('i - Generar manifiseto proporcionando los datos - fecha y vuelo y representación básica del avión')
    print('j - Comparar los precios de los vuelos por día del mes')
    print('k - Comparar los precios de los vuelos por día de la semana')
    print('l - Comparar la ocupacion de los vuelos por día del mes')
    print('m - Comparar la ocupacion de los vuelos por día de la semana')
    print('n - Comparar la edad media de los vuelos por día del mes')
    print('o - Comparar la edad media de los vuelos por día de la semana')
    print('p - Mostrar el grupo de personas que más consume y que día lo hace')
    print('q - Mostrar los archivos con errores y el por qué')
    print('s - salir del programa')
    ans = str(input(" - >>")).lower()

    ### --- Funciones para cada respuesta
    if ans in "abcdefghipq": #Limpiamos la pantalla para no sobrecargarla
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('cs','nt','dos'):
            os.system('cls')
    if ans == "a" :  readit("Usuarios_habituales.csv");
    elif ans == "b": readit("Vuelos_Porcentaje_Ocupacion.csv")
    elif ans == "c": readit("Vuelos_Precio_Medio.csv")
    elif ans == "d": readit("Vuelos_Edad_Media.csv")
    elif ans == "e": readit("Precio_Medio_Semana.csv")
    elif ans == "f": readit("Ocupacion_Media_Semana.csv")
    elif ans == "g": readit("Reparto_Generos_Semana.csv")
    elif ans == "h": readit("10_mejores_clientes.csv")
    elif ans == "i": findit()
    elif ans == "j": comprice()
    elif ans == "k": comprice("semana")
    elif ans == "l": compoc()
    elif ans == "m": compoc("semana")
    elif ans == "n": comped()
    elif ans == "o": comped("semana")
    elif ans == "p": optimizar()
    elif ans == "q": show_err()
    elif ans == "s":
        a = input('(Presiona la tecla enter para salir)')
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('cs','nt','dos'):
            os.system('cls')
        break
    else: print("Opción non programada")
