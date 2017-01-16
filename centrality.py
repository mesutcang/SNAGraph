from neo4j.v1 import GraphDatabase, basic_auth
from collections import OrderedDict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import cypher


def calculateDegreeCentrality(session):
	"""
		calculated degree centrality using Neo4j connection.
	"""
	print "degree centrality:"
	# find the nodes with connection sizes
	degrees = session.run("MATCH (c:Deneme) RETURN c.fullName, size( (c)-[:relation_x]-() ) AS degree ORDER BY degree DESC")

	#prepare data for chart representation
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data

	#give chart a number and draw chart according the data
	plt.figure(1)
	drawChart(data,"Degree Centrality")

def calculateBetweennessCentrality(session):
	"""
		calculates betweenness centrality using Neo4j connection.
	"""
	print "betweenness centrality:"

	#find all the nodes using shortestpaths in network.
	degrees = session.run("MATCH p=allShortestPaths((source:Deneme)-[:relation_x*]-(target:Deneme)) UNWIND nodes(p)[1..-1] as n RETURN n.fullName, count(*) as betweenness order by betweenness desc")

	#prepare data for chart representation.
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data

	#give chart a number and draw chart according the data
	plt.figure(2)
	drawChart(data,"Betweenness Centrality")

def calculateClosenessCentrality(session):
	"""
		calculates closeness centrality using Neo4j connection.
	"""
	print "closeness centrality:"
	# find nodes with closeness values using shortestpaths
	degrees = session.run("MATCH (a:Deneme), (b:Deneme) WHERE a<>b WITH length(shortestPath((a)-[]-(b))) AS dist, a, b RETURN DISTINCT  a.fullName, sum(1.0/dist) AS close_central ORDER BY close_central DESC ")
	
	#prepare data for chart representation.
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data
	
	#give chart a number and draw chart according the data
	plt.figure(3)
	drawChart(data,"Closeness Centrality")

def calculateEigenvectorCentrality(session):
	"""
		calculates eigenvector centrality using Networkx.
	"""
	print "Eigenvector centrality:"

	# get the data from neo4j
	results = cypher.run("MATCH p = ()-[]-() RETURN p", conn="http://neo4j:123456@localhost:7474/db/data")
	g = results.get_graph()

	# calculate the eigenvector centrality using networkx
	dictionary_centrality = nx.eigenvector_centrality_numpy(g)

	#give chart a number and draw chart according the data
	plt.figure(4)
	drawChart(dictionary_centrality, "Eigenvector Centrality")


	
def calculatePageRankCentrality(session):
	"""
		calculates pagerank using Neo4j session.
	"""
	print "page rank:"

	# calculate the rank values for each nodes in the network
	session.run("UNWIND range(1,10) AS round MATCH (n:Deneme) WHERE rand() < 0.1  MATCH (n:Deneme)-[:relation_x*..10]->(m:Deneme) SET m.rank = coalesce(m.rank,0) + 1")

	# get the ranks of each node 
	degrees = session.run("MATCH (n:Deneme) WHERE n.rank is not null return n.fullName, n.rank order by n.rank desc ")
	
	#prepare data for chart representation.
	data = {}
	for degree in degrees:
		data[degree[0]] = degree[1]
	print data

	#give chart a number and draw chart according the data
	plt.figure(5)
	drawChart(data,"Page Rank")

def drawChart(data, title):
	"""
		draw bar chart according the data and uses given title.
	"""
	# sort given data 
	orderedData = OrderedDict(sorted(data.items(), key=lambda t: t[1]))

	# clear the chart
	plt.gcf().clear()

	#y axis is used for keys in data dictionary
	y_pos = np.arange(len(orderedData.keys()))
	#x axis is used for the values in data dictionary
	x_pos = np.arange(len(orderedData.items()))
	#matplotlib is used to draw bar chart using given axises 
	plt.bar(y_pos, x_pos, alpha=0.5)
	plt.xticks(y_pos, orderedData.keys(),rotation='vertical')
	plt.yticks(x_pos, orderedData.values())
	#set the labels for axises
	plt.ylabel('values')
	plt.xlabel('users')
	plt.title(title) 
	# draw the chart
	plt.draw()

def main(session):
	"""
		Main method to run the centrality metrics one by one.
	"""
	calculateDegreeCentrality(session)
	calculateBetweennessCentrality(session)
	calculateClosenessCentrality(session)
	calculateEigenvectorCentrality(session)
	calculatePageRankCentrality(session)
	#show the charts and wait.
	plt.show()
	

if __name__ == '__main__':
	"""
		This block runs if the application is run directly.
		This application can be used as a python module in other projects.
		If added as module this block is not going to run.
	"""

	#Neo4j connection using bolt
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "123456"))
	#session creation for connection.
	session = driver.session()
	#main app
	main(session)
	#closing connection at the end of execution of application.
	session.close()