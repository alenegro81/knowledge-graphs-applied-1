// Run the following queries on DRKG to know the numbers you need to build the random graph

//Total number of nodes
MATCH (n:DrkgNode) RETURN count(n)

//Result: 97238


//Average out-degree
MATCH (n:DrkgNode)-[]->(t)
WITH n, count(t) as outDegree
RETURN avg(outDegree), min(outDegree), max(outDegree)

//Result: 102.95238178695352	1	23866

//Collect numbers for each class
MATCH (n:DrkgNode)
RETURN labels(n)[1], count(n)


//Move to the random graph database
//Generate the random graph (you need apoc installed)
CALL apoc.generate.ba(97238, 102, 'RandomDrkgNode', 'RANDOM_REL')


