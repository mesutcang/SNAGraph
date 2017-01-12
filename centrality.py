from neo4j.v1 import GraphDatabase, basic_auth
import csv

def calculateDegreeCentrality(session):
	print "degree centrality:"
	degrees = session.run("MATCH (c:Deneme) RETURN c.fullName, size( (c)-[:relation_x]-() ) AS degree ORDER BY degree DESC")
	for degree in degrees:
		print degree[0],"=", degree[1]

def calculateBetweennessCentrality(session):
	print "betweenness centrality:"
	degrees = session.run("MATCH p=allShortestPaths((source:Deneme)-[:relation_x*]-(target:Deneme)) UNWIND nodes(p)[1..-1] as n RETURN n.fullName, count(*) as betweenness order by betweenness desc")
	for degree in degrees:
		print degree[0],"=", degree[1]

def calculateClosenessCentrality(session):
	print "closeness centrality:"
	degrees = session.run("MATCH (a:Deneme), (b:Deneme) WHERE a<>b WITH length(shortestPath((a)-[]-(b))) AS dist, a, b RETURN DISTINCT  a.fullName, sum(1.0/dist) AS close_central ORDER BY close_central DESC ")
	for degree in degrees:
		print degree[0],"=", degree[1]



def main(session):
	# calculateDegreeCentrality(session)
	# calculateBetweennessCentrality(session)
	calculateClosenessCentrality(session)
	

if __name__ == '__main__':
	driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "123456"))
	session = driver.session()
	main(session)
	session.close()