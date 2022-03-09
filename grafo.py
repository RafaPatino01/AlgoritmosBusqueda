# -*- coding: utf-8 -*-
from importlib.resources import path
import pandas as pd

class Grafo:
    def __init__(self, pathCSV):

        csvData = pd.read_csv(pathCSV)
        dataList = csvData.values.tolist()
        nombreNodoArray = []

        #Nodos de ida
        for i in csvData.iloc[:,0]:
            if i not in nombreNodoArray:
                nombreNodoArray.append(i)

        #Nodos destino, para obtener los ultimos nodos que no aparecen en ida
        for j in csvData.iloc[:,1]:
            if j not in nombreNodoArray:
                nombreNodoArray.append(j)

        nodos = []
        for i in nombreNodoArray: #recorro cada nodo, [S,A,D,B,E ... G]
            for j in dataList:
                if i == j[0]: #si encuentro el nodo, lo pusheo a una lista [[S,A,3], [S,D,4]...[F,G,3]]
                    nodos.append(j)
                if i == j[1]:
                    aux = [j[1], j[0]]
                    aux += j[2:]
                    nodos.append(aux)

        self.nodosLista = nodos
        #diccionario de conexiones
        #{
            # 'S': [('A', 3), ('D', 4)],
            # 'A': [('B', 4), ('D', 5)],
        # }
        diccionarioConexiones = {}
        for i in nombreNodoArray:
            aux = []
            for j in nodos:
                if j[0] == i: # S == [S,A,3], compara la conexion y pushea al auxiliar 
                    aux.append(j)

            aux2 = []
            for k in aux:#recorro las nuevas conexiones para x nodo -> [['S', 'A', 3], ['S', 'D', 4]]
                aux2.append((k[1], k[2]))#Pusheo en el nuevo arreglo para que sean los valors de la llave
            diccionarioConexiones[i] = aux2 #quedaria i = S : (['S', 'A', 3]), (['S', 'D', 4])
        
        self.listaConexiones = diccionarioConexiones
    
    # ----- Get Conexiones del vértice -----
    def verticesConexion(self, v):
        return self.listaConexiones[v] #regresa la lista de conexioens de "v" nodo 

    #funcion que nos devuelve la heuristica
    def heuristica(self, n):
        #recibe el nodo a utilizar
        dcoord, ncoord = (0, 0), (0, 0)
        #dcoord son las coordenadas del nodo destino
        #ncoord son las coordenadas del nodo en curso
        heu = None
        
        #aqui se sacan los valores para x1 y y1
        #que son los del destino
        for i in self.nodosLista:
            if i[0] == self.nodoDestino:
                dcoord = (i[3], i[4]) 
                break
            
        
        for i in self.nodosLista:
            if i[0] == n:#checar los valores de x2 y y2, de mi nodo actual
                ncoord = (i[3], i[4])
                #formula para la heuristica
                heu = (((ncoord[0] - dcoord[0]) ** (2)) + ((ncoord[1] - dcoord[1]) ** (2))) ** (0.5)
                break

        return heu

    # ----- Algoritmo primero a lo ancho -----
    def BFS(self, nodoInicio, nodoDestino):

        self.nodoDestino = nodoDestino
        
        porExplorar = set([nodoInicio]) #lista de nodos con conexiones SIN explorar
        yaExplorados = set([]) #lista de nodos con conexiones YA explorados
        

        d = {} #es el nivel del arbol
        d[nodoInicio] = 0
        
        #es el diccionario que va a guardar el nodo con su padre
        padreDic = {}
        padreDic[nodoInicio] = nodoInicio
        
        while len(porExplorar) > 0: #recorremos la lista hasta que se vacie
            n = None
            for v in porExplorar:
                if n == None or d[v] < d[n]: #reviso siempre que el nodo sea NONe
                    #o que el nodo tenga un nivel de arbol menor al nodo que explorare
                    #esto porque sigo explorando el mismo nivel, no avanzo
                    n = v;
       
            print('nodo que voy llegando',n)
             #comprobar si llegamos al final
            if n == nodoDestino:
                ruta = []
                while padreDic[n] != n: #buscamos la llave que contenga el valor de N 
                    #o bien el padre encuentra a su hijo,
                    #tipo n vale B, entonces encuentra a su hijo C y asi iterativamente
                    #iteramos siempre que no se haya llegado al nodo inicial - 1
                    ruta.append(n) #pusheamos el nodo a la ruta
                    n = padreDic[n]  # n ahora toma el valor de su padre
                
                ruta.append(nodoInicio) # el iinicio lo insertamos porque no estaba 
                #y revertimos el arreglo de la nueva ruta
                ruta.reverse()
                return ruta

            for nodoConexion, arbolNivel in self.verticesConexion(n): #iteramos en las conexiones del nodo actual
                #nodoConexion es la conexion del nodo n
                #si el nodo no esta en explorados ni por explorar lo agrego
                if nodoConexion not in porExplorar and nodoConexion not in yaExplorados:
                    porExplorar.add(nodoConexion) #se actualiza para explorar
                    padreDic[nodoConexion] = n   #{'S': 'S', 'A': 'S', 'D': 'S'} obtengo padre e hijo
                    d[nodoConexion] = d[n] + 1 # d = {'S': 0, 'A': 1, 'D': 1} asigno el nivel del "arbol", 1
            
            if n == None:
                return None
            
            #n ya fue explorado, se pasa al siguiente nodo y ya no esta para explorarse
            porExplorar.remove(n)
            yaExplorados.add(n)
            
        return ('La ruta no existe pai ')

    # ----- Algoritmo Primero Profundidad -----
    def DFS(self,nodoInicio, nodoDestino):

        self.nodoDestino = nodoDestino
        
        porExplorar = set([nodoInicio]) #lista de nodos con conexiones SIN explorar
        yaExplorados = set([]) #lista de nodos con conexiones YA explorados
        

        d = {} #es el nivel del arbol
        d[nodoInicio] = 0
        
        #es el diccionario que va a guardar el nodo con su padre
        padreDic = {}
        padreDic[nodoInicio] = nodoInicio
        
        while len(porExplorar) > 0: #recorremos la lista hasta que se vacie
            n = None


            for v in porExplorar:
                if n == None or d[v] > d[n]:
                    #exploro siempre y cuando el nodo actual sea menor que el por explorar
                    #esto para que el nivel enn el arbol siga avanzando
                    n = v;
                    
                         
           # print('nodo que voy llegando',n)                
             #comprobar si llegamos al final
            if n == nodoDestino:
                ruta = []
                while padreDic[n] != n: #buscamos la llave que contenga el valor de N 
                    #o bien el padre encuentra a su hijo,
                    #tipo n vale B, entonces encuentra a su hijo C y asi iterativamente
                    #iteramos siempre que no se haya llegado al nodo inicial - 1
                    ruta.append(n) #pusheamos el nodo a la ruta
                    n = padreDic[n]  # n ahora toma el valor de su padre

                ruta.append(nodoInicio) # el iinicio lo insertamos porque no estaba 
                #y revertimos el arreglo de la nueva ruta
                ruta.reverse()
                return ruta
            
            for nodoConexion, arbolNivel in self.verticesConexion(n): #iteramos en las conexiones del nodo actual
                #nodoConexion es la conexion del nodo n
                #dist es la arbolNivel entre estos 2 nodos
                #si el nodo no esta en explorados ni por explorar lo agrego
                if nodoConexion not in porExplorar and nodoConexion not in yaExplorados:
                    porExplorar.add(nodoConexion) #se actualiza para explorar
                    padreDic[nodoConexion] = n   #{'S': 'S', 'A': 'S', 'D': 'S'} obtengo padre e hijo
                    d[nodoConexion] = d[n] + 1 # d = {'S': 0, 'A': 1, 'D': 1} asigno el nivel del "arbol", 1
                    #d[nodoConexion] es el puro nivel                
                else:
                    if d[nodoConexion] > d[n] + 1: #si el nivel de mi conexion es mayor que mi nivel actual + 1
                        d[nodoConexion] = d[n] + 1 #le asigno ese nuevo nivel  que lo hace bajar 1
                        padreDic[nodoConexion] = n #n ahora es parte de los padres
                        if nodoConexion in yaExplorados:
                            yaExplorados.remove(nodoConexion)
                            porExplorar.add(nodoConexion)

                        
            if n == None:
                return None
            
            #n ya fue explorado, se pasa al siguiente nodo y ya no esta para explorarse
            porExplorar.remove(n)
            yaExplorados.add(n)
            
        return ('La ruta no existe pai ')
    
    # ----- Algoritmo profundidad Limitada -----
    def DFSLim(self,nodoInicio, nodoDestino):

        self.nodoDestino = nodoDestino
        
        porExplorar = set([nodoInicio]) #lista de nodos con conexiones SIN explorar
        yaExplorados = set([]) #lista de nodos con conexiones YA explorados
        

        d = {} #es el nivel del arbol
        d[nodoInicio] = 0
        
        #es el diccionario que va a guardar el nodo con su padre
        padreDic = {}
        padreDic[nodoInicio] = nodoInicio

        limite = 2
        
        while len(porExplorar) > 0: #recorremos la lista hasta que se vacie
            n = None
            
            for v in porExplorar:
                if n == None or d[v] > d[n] and d[v] < limite:
                    #mismas reglas de DFS
                    #Pero solo entra si el nivel de arbol actual es menor que el limite
                      n = v
                      if(d[v]==limite): #si llego al limite, entonces es el destino
                        #ya llegue porque llegue a mi limite
                        nodoDestino = n
               
            print('nodo que voy llegando ',n)  
             #comprobar si llegamos al final
            if n == nodoDestino:
                ruta = []
                while padreDic[n] != n: #buscamos la llave que contenga el valor de N 
                    #o bien el padre encuentra a su hijo,
                    #tipo n vale B, entonces encuentra a su hijo C y asi iterativamente
                    #iteramos siempre que no se haya llegado al nodo inicial - 1
                    ruta.append(n) #pusheamos el nodo a la ruta
                    n = padreDic[n]  # n ahora toma el valor de su padre
                    

                ruta.append(nodoInicio) # el iinicio lo insertamos porque no estaba 
                #y revertimos el arreglo de la nueva ruta
                ruta.reverse()
                return ruta

            for nodoConexion, arbolNivel in self.verticesConexion(n): #iteramos en las conexiones del nodo actual
                #nodoConexion es la conexion del nodo n
                #dist es la arbolNivel entre estos 2 nodos
                #si el nodo no esta en explorados ni por explorar lo agrego
                if nodoConexion not in porExplorar and nodoConexion not in yaExplorados:
                    porExplorar.add(nodoConexion) #se actualiza para explorar
                    padreDic[nodoConexion] = n   #{'S': 'S', 'A': 'S', 'D': 'S'} obtengo padre e hijo
                    d[nodoConexion] = d[n] + 1 # d = {'S': 0, 'A': 1, 'D': 1} asigno el nivel del "arbol", 1
                    #d[nodoConexion] es el puro nivel                
                else:

                    if d[nodoConexion] > d[n] + 1: #si el nivel de mi conexion es mayor que mi nivel actual + 1
                        d[nodoConexion] = d[n] + 1 #le asigno ese nuevo nivel  que lo hace bajar 1
                        padreDic[nodoConexion] = n #n ahora es parte de los padres

                        
            if n == None:
                return None
            
            #n ya fue explorado, se pasa al siguiente nodo y ya no esta para explorarse
            porExplorar.remove(n)
            yaExplorados.add(n)
            
        return ('La ruta no existe pai ')
    
    # ----- Algoritmo profundidad iterativa -----
    def IDFS(self,nodoInicio, nodoDestino,limite):

        self.nodoDestino = nodoDestino
        
        porExplorar = set([nodoInicio]) #lista de nodos con conexiones SIN explorar
        yaExplorados = set([]) #lista de nodos con conexiones YA explorados
        

        d = {} #es el nivel del arbol
        d[nodoInicio] = 0
        
        #es el diccionario que va a guardar el nodo con su padre
        padreDic = {}
        padreDic[nodoInicio] = nodoInicio


        while len(porExplorar) > 0: #recorremos la lista hasta que se vacie
            n = None

            for v in porExplorar: #recorremos los que queremos explorar sus conexiones
                if n == None or d[v] > d[n] and d[v] <= limite:
                    #Siempre y cuando el limite sea igual o menor, si llega
                    n = v;

            print('nodo al que llego',n)
            if n == None: # aqui hacemos recursividad para aumentar por 1 el limte
                #en caso que el nodo sea None saliendo de los explorados, le agregamos un nivel a 
                #recorrer en el arbol para buscar 
                limite += 1
                self.IDFS(nodoInicio, nodoDestino,limite)
                return None
                      
             #comprobar si llegamos al final
            if n == nodoDestino:
                ruta = []
                while padreDic[n] != n: #buscamos la llave que contenga el valor de N 
                    #o bien el padre encuentra a su hijo,
                    #tipo n vale B, entonces encuentra a su hijo C y asi iterativamente
                    #iteramos siempre que no se haya llegado al nodo inicial - 1
                    ruta.append(n) #pusheamos el nodo a la ruta
                    n = padreDic[n]  # n ahora toma el valor de su padre
                    

                ruta.append(nodoInicio) # el iinicio lo insertamos porque no estaba 
                #y revertimos el arreglo de la nueva ruta
                ruta.reverse()
                return ruta

            for nodoConexion, arbolNivel in self.verticesConexion(n): #iteramos en las conexiones del nodo actual
                #nodoConexion es la conexion del nodo n
                #dist es la arbolNivel entre estos 2 nodos
                #si el nodo no esta en explorados ni por explorar lo agrego
                if nodoConexion not in porExplorar and nodoConexion not in yaExplorados:
                    porExplorar.add(nodoConexion) #se actualiza para explorar
                    padreDic[nodoConexion] = n   #{'S': 'S', 'A': 'S', 'D': 'S'} obtengo padre e hijo
                    d[nodoConexion] = d[n] + 1 # d = {'S': 0, 'A': 1, 'D': 1} asigno el nivel del "arbol", 1
                    #d[nodoConexion] es el puro nivel                
                else:
                    
                    if d[nodoConexion] > d[n] + 1: #si el nivel de mi conexion es mayor que mi nivel actual + 1
                        d[nodoConexion] = d[n] + 1 #le asigno ese nuevo nivel  que lo hace bajar 1
                        padreDic[nodoConexion] = n #n ahora es parte de los padres
                        
            if n == None:
                return None
            
            #n ya fue explorado, se pasa al siguiente nodo y ya no esta para explorarse
            porExplorar.remove(n)
            yaExplorados.add(n)
            
        return ('La ruta no existe pai ')
            
    
    # ----- Algoritmo hill climbing -----
    def hillClimbing(self, nodoInicio, nodoDestino):

        ruta = [nodoInicio]
        visitados = [nodoInicio] # Visitar el nodo inicial

        # añadir ordenadamente los nodos adyacentes a la agenda
        agenda = sorted(self.verticesConexion(nodoInicio), key=lambda tup: tup[1]) 

        # mientras haya elementos en la agenda
        while agenda:
            actual = agenda[0][0] # Moverse al mejor nodo

            if actual == nodoDestino: # Si es el nodo destino, terminar el while
                ruta.append(actual)
                break

            temp_agenda = []
            for nodo in self.verticesConexion(actual):
                if nodo[0] not in visitados:
                    temp_agenda.append(nodo)

            temp_agenda = sorted(temp_agenda, key=lambda tup: tup[1]) # nodos adyacentes del nodo actual 
            
            visitados.append(actual) # marcar visitado el nodo actual
            ruta.append(actual) # añadirlo a la ruta

            if temp_agenda != []:
                agenda = temp_agenda[0] # Eliminar el resto y seleccionar el mejor
            else:
                print("No fue posible encontrar el nodo deseado")
                break


            

        # Limpiar ruta 
        # Si el último elemento no tiene conexión con el penúltimo entonces lo borra
        for i in range(len(ruta)-1,-1,-1):
            aux = []
            for element in self.verticesConexion(ruta[i-1]):
                aux.append(element[0])

            if (not ruta[i] in aux) and (i != 0):
                del ruta[i-1]
                    
        print("ruta: " + str(ruta))

    # ----- Algoritmo best first -----
    def bestFirst(self, nodoInicio, nodoDestino):

        ruta = [nodoInicio]
        visitados = [nodoInicio] # Visitar el nodo inicial

        # añadir ordenadamente los nodos adyacentes a la agenda
        agenda = sorted(self.verticesConexion(nodoInicio), key=lambda tup: tup[1]) 

        # mientras haya elementos en la agenda
        while agenda:
            actual = agenda[0][0] # Moverse al mejor nodo

            if actual == nodoDestino: # Si es el nodo destino, terminar el while
                ruta.append(actual)
                break

            temp_agenda = []
            for nodo in self.verticesConexion(actual):
                if nodo[0] not in visitados:
                    temp_agenda.append(nodo)

            temp_agenda = sorted(temp_agenda, key=lambda tup: tup[1]) # nodos adyacentes del nodo actual 
            
            del agenda[0] # eliminar el nodo actual de la agenda
            temp_agenda.extend(agenda) # extender la agenda con todos los nodos que siguen
            agenda = temp_agenda

            visitados.append(actual) # marcar visitado el nodo actual
            ruta.append(actual) # añadirlo a la ruta

        # Limpiar ruta 
        # Si el último elemento no tiene conexión con el penúltimo entonces lo borra
        for i in range(len(ruta)-1,-1,-1):
            aux = []
            for element in self.verticesConexion(ruta[i-1]):
                aux.append(element[0])

            if (not ruta[i] in aux) and (i != 0):
                del ruta[i-1]
                    
        print("ruta: " + str(ruta))

    # ----- Algoritmo beam search -----
    def beam(self, nodoInicio, nodoDestino, w):
        print("hola mundo")
        
    def aEstrella(self, nodoInicio, nodoDestino):

        self.nodoDestino = nodoDestino

        porExplorar = set([nodoInicio])
        yaExplorados = set([])

        d = {}
        d[nodoInicio] = 0

        padreDic = {}
        padreDic[nodoInicio] = nodoInicio
        
        while len(porExplorar) > 0:
            n = None
            for v in porExplorar:
                if n == None or d[v] + self.heuristica(v) < d[n] + self.heuristica(n):
                    n = v;


             #comprobar si llegamos al final
            if n == nodoDestino:
                ruta = []
                while padreDic[n] != n: #buscamos la llave que contenga el valor de N 
                    #o bien el padre encuentra a su hijo,
                    #tipo n vale B, entonces encuentra a su hijo C y asi iterativamente
                    #iteramos siempre que no se haya llegado al nodo inicial - 1
                    ruta.append(n) #pusheamos el nodo a la ruta
                    n = padreDic[n]  # n ahora toma el valor de su padre
                    

                ruta.append(nodoInicio) # el iinicio lo insertamos porque no estaba 
                #y revertimos el arreglo de la nueva ruta
                ruta.reverse()
                return ruta

            for (nodoConexion, peso) in self.verticesConexion(n):

                if nodoConexion not in porExplorar and nodoConexion not in yaExplorados:
                    porExplorar.add(nodoConexion)
                    padreDic[nodoConexion] = n
                    d[nodoConexion] = d[n] + peso

                else:
                    if d[nodoConexion] > d[n] + peso:
                        d[nodoConexion] = d[n] + peso
                        padreDic[nodoConexion] = n

                        if nodoConexion in yaExplorados:
                            yaExplorados.remove(nodoConexion)
                            porExplorar.add(nodoConexion)

            porExplorar.remove(n)
            yaExplorados.add(n)
        
        return ('No se encontro un camino')
    
        
