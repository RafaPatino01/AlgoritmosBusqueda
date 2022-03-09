# -*- coding: utf-8 -*-
from grafo import *

myCSV = "/Volumes/GoogleDrive/My Drive/Universidad/Semestre 6/IA/proyecto_busqueda/Grafoproyecto.csv"
grafo = Grafo(myCSV)


# Profundidad limitada
print('BFS')
#rutaBFS = grafo.BFS('M?xico','Monterrey')
#print('Ruta: ',rutaBFS)
print('-------------------------------')
print('DFS')
#rutaDFS = grafo.DFS('M?xico','Monterrey')
#print('Ruta: ',rutaDFS)
print('-------------------------------')
print('DFS Limited')
#rutaDFSLim = grafo.DFSLim('M?xico','Monterrey')
#print('Ruta: ',rutaDFSLim)
print('-------------------------------')#
print('Iterative DFS')
#rutaIDFS = grafo.IDFS("A", "I", 1)
#print('Ruta: ',rutaIDFS)
print('-------------------------------')
print('A estrella')
rutaEstrella = grafo.aEstrella('M?xico','Monterrey')
print('ruta: ',rutaEstrella)
# Best First
#grafo.bestFirst("A", "G")
