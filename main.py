# -*- coding: utf-8 -*-
from grafo import *

myCSV = "/Volumes/GoogleDrive/My Drive/Universidad/Semestre 6/IA/proyecto_busqueda/Grafoproyecto.csv"
grafo = Grafo(myCSV)
grafo = Grafo(myCSV)

# Profundidad limitada
grafo.BFS('A','G')
print('-------------------------------')
grafo.DFS('A','G')
print('-------------------------------')
grafo.DFSLim('A','I')
print('-------------------------------')
grafo.IDFS("A", "G", 1)
print('-------------------------------')


# Best First
#grafo.bestFirst("A", "G")
