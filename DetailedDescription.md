
# SOCIAL NETWORK ANALYSIS PROJECT REPORT
## By
## Mesut Can GÜRLE
## Emre KARAGÖZ
## Altay SEYHAN



# Introduction 	

Since graphs are frequently used throughout the Intoduction to Social Network Analysis, the project is assigned centering Neo4j which is a graph database management system which allows the users to understand, query and manipulate the data more efficiently and quickly.

Purpose of the Project

The purpose of the project is to understand the importance of graphs in social networks and how to analyze them.

# Tools and Libraries Used 

Neo4j 3.1 (For Individuals, non-Business usage)
Python 2.7.12
Networkx
Git
Numpy
neo4j.v1 
matplotlib
cypher

# Understanding the Data and the Process

The data are consisted of appreciation mails among a company employees. The appreciation between the employees are shown as TAKDIR_ALDI(received appreciation) and TAKDIR_ETTI(done the appreciation). 
At first, each appreciation was also another node alongside the employees and this created some confusion in the beginning. 
After setting up Neo4j we executing the following snippet of code we managed to visualize all the nodes (both employee and appreciations). 

MATCH (n) RETURN n *
However in this visualization there were some employees and appreciations without being connected to no other node. This looked strange and after some detailed testing with different queries and confirmations done via using python, it’s understood that the node number was limited to 300 and this caused most of the nodes not being displayed. The visualization widget works so slowly and laggy, this is why the limit was set. The limit was set to 800 in order to get the program show all the nodes with the following snippet of code: 

:config initialNodeDisplay: 800
Which appeared in the result tab as : 

{ 
"initialNodeDisplay": 800 
} 

Even though it got slower, now it was clearer to see and the seperate appreciations were visible once again. After making sure they existed once again, the following code was used to find their exact numbers:
 MATCH (a:Employee) WHERE not ((a)-[:TAKDIR_ETTI]->(:Takdir))and not ((a)-[:TAKDIR_ALDI]->(:Takdir)) RETURN a; 

Which showed 17 employees. Same thing done to find the appreciations as well and the result was once again 17. This indicated a serious problem with the veracity of the given data. 
It was realized that many of the employees have been appreciated by the same people multiple times. In order to have a more meaningful and clear graph the number of the appreciations were thought to be grouped and labelled as the weight of the edge between the two nodes. In order to do that the appreciation nodes were to be removed and formed into a single edge. 
With the following code the appreciations between the same people are grouped: 

MATCH ((a:Employee)-[:TAKDIR_ALDI]->(t:Takdir)<-[:TAKDIR_ETTI]-(b:Employee)) RETURN a,b,count(t);
	Instead of this long chain of connections we decided to use one relation and two nodes to show them all simply. To create a relationship between two nodes, we first get the two nodes. Once the nodes are loaded, we simply create a relationship between them.
MATCH (a:Employee),(b: Employee)
WHERE (a:Employee)-[:TAKDIR_ALDI]->(t:Takdir)<-[:TAKDIR_ETTI]-(b:Employee)
CREATE (a)-[r:relation_x]->(b)
RETURN r
	Thus we had created the new relation for ease of use.
“Calculation and reporting of centrality metrics for different types of relations between employees (degree centrality, closeness centrality, betweenness centrality, eigenvector centrality, PageRank)” topic was chosen to be implemented.
For this, the centralities must be remembered:

# Results and Discussion

	By looking at overall results one can easily infer that the node with the most degree centralities are the core and top employees at the firm such as directors and headchiefs of various departments.
	Another important conclusion might be that the seperated nodes from the hull of the concentrated nodes indicate that this comparatively smaller group of employees should be working apart from the other employees and interacting them with little to none degree which proposes these employees to be an outsource equip working in another environment.
Using Snap! software would improve the credibility and reliability of the results and it would ensure the similar if not the same results in case of a bigger data was used in the project.

# References 
[1] https://www.cl.cam.ac.uk/teaching/1314/L109/stna-lecture3.pdf
[2] Analyzing the Social Web by Jennifer Golbeck