from neo4j.v1 import GraphDatabase, basic_auth
from collections import OrderedDict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import cypher




def calculateDegreeCentrality(session):
	print "degree centrality:"
	degrees = session.run("MATCH (c:Deneme) RETURN c.fullName, size( (c)-[:relation_x]-() ) AS degree ORDER BY degree DESC")
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data
	plt.figure(1)
	drawChart(data,"Degree Centrality")

def calculateBetweennessCentrality(session):
	print "betweenness centrality:"
	degrees = session.run("MATCH p=allShortestPaths((source:Deneme)-[:relation_x*]-(target:Deneme)) UNWIND nodes(p)[1..-1] as n RETURN n.fullName, count(*) as betweenness order by betweenness desc")
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data
	plt.figure(2)
	drawChart(data,"Betweenness Centrality")

def calculateClosenessCentrality(session):
	print "closeness centrality:"
	degrees = session.run("MATCH (a:Deneme), (b:Deneme) WHERE a<>b WITH length(shortestPath((a)-[]-(b))) AS dist, a, b RETURN DISTINCT  a.fullName, sum(1.0/dist) AS close_central ORDER BY close_central DESC ")
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data
	plt.figure(3)
	drawChart(data,"Closeness Centrality")

def calculateEigenvectorCentrality(session):
	print "Eigenvector centrality:"
	results = cypher.run("MATCH p = ()-[]-() RETURN p", conn="http://neo4j:123456@localhost:7474/db/data")
	g = results.get_graph()
	dictionary_centrality = nx.eigenvector_centrality_numpy(g)
	plt.figure(4)
	drawChart(dictionary_centrality, "Eigenvector Centrality")


	
def calculatePageRankCentrality(session):
	print "page rank:"
	session.run("UNWIND range(1,10) AS round MATCH (n:Deneme) WHERE rand() < 0.1  MATCH (n:Deneme)-[:relation_x*..10]->(m:Deneme) SET m.rank = coalesce(m.rank,0) + 1")
	degrees = session.run("MATCH (n:Deneme) WHERE n.rank is not null return n.fullName, n.rank order by n.rank desc ")
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data
	plt.figure(5)
	drawChart(data,"Page Rank")

def drawChart(data, title):
	orderedData = OrderedDict(sorted(data.items(), key=lambda t: t[1]))
	plt.gcf().clear()
	y_pos = np.arange(len(orderedData.keys()))
	x_pos = np.arange(len(orderedData.items()))
	plt.bar(y_pos, x_pos, alpha=0.5)
	plt.xticks(y_pos, orderedData.keys(),rotation='vertical')
	plt.yticks(x_pos, orderedData.values())
	plt.ylabel('values')
	plt.xlabel('users')
	plt.title(title) 

	plt.draw()

def main(session):
	calculateDegreeCentrality(session)
	calculateBetweennessCentrality(session)
	calculateClosenessCentrality(session)
	calculateEigenvectorCentrality(session)
	calculatePageRankCentrality(session)
	plt.show()
	

if __name__ == '__main__':
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "123456"))
	session = driver.session()
	main(session)
	session.close()