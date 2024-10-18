from rdflib import Graph
import sys

g = Graph().parse(sys.argv[1])
if len(g) > 0:
    print("ok")
