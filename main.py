# -*- coding: utf-8 -*-
from grafo import *

myCSV = "/Volumes/GoogleDrive/My Drive/Universidad/Semestre 6/IA/proyecto_busqueda/Grafoproyecto.csv"
grafo = Grafo(myCSV)

# Profundidad limitada
grafo.profundidadLim("A", "G")

# Best First
grafo.bestFirst("A", "G")


