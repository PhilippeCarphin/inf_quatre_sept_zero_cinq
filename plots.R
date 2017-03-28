#!/usr/local/bin/Rscript
library(gridExtra)
write_csv <- function(algo, data=avg, cas=boner)
{
	# Select rows where algo == algo
	table <- data[
					  data["algo"] == algo, # Select rows
					  c("n_nodes", "n_edges",  "time") # select columns
				  ]

	# File will be saved in Data/ directory and named with what case it is
	filename = paste(c("Data/",algo,"_",cas), collapse="")

	# Write table to csv file
	csv_filename = paste(c(filename,".csv"), collapse="")
	write.table(table, csv_filename, row.names=FALSE,sep=",")

	# Save pdf of the table
	pdf_filename = paste(c(filename,".pdf"), collapse="")
	pdf(pdf_filename)
	grid.table(table)
	dev.off()
}

plot_algos <- function(filename, data, x="n_edges", y="time", log="")
{
	pdf(filename, width=8.5, height=11)
	par(mfrow=c(3,3))
	# Do each graph except for (Algo=counting, Series=2)
	cas = c("cas moyen","pire cas", "meilleur cas")
	i = 1
	for(d in data){
		for(algo in c("backtrack","dynamic","entropy")){
			title <- paste(c("Algorithme ", algo, " en ", cas[i]), collapse="")
			to_plot <- d[d["algo"]==algo,][,c(x,y)]
			plot(to_plot,log=log, main=title)
		}
		i = i+1
	}
	dev.off()
}



# Read the raw data
df <- read.table("Data/master_data.csv", header = TRUE, sep = ",")

# Aggregate the data with averages for same (series, algorithm)
avgs <- aggregate( df[c("time","number")], by=df[c("algo","n_nodes","n_edges","series")], mean)
avgs <- avgs[order( avgs[,"n_nodes"], avgs[,"n_edges"]),]
avgs$ratio_edge <- avgs$time / avgs$n_edges
avgs$ratio_edge_squared <- (avgs$time) / ( avgs$n_edges ** 2)
avgs$edge_squared <- (avgs$n_edges ** 2)
avgs$ratio_node <- avgs$time / avgs$n_nodes
avgs$node_squared <- avgs$n_nodes ** 2
avgs$ratio_node_squared <- (avgs$time) / (avgs$n_nodes ** 2)
avgs$node_squared_edge <- ((avgs$n_nodes ** 2)*(avgs$n_edges))
avgs$ratio_node_squared_edge <- (avgs$time) / ((avgs$n_nodes ** 2)*(avgs$n_edges))

max <- aggregate( df[c("time")], by=df[c("algo","n_nodes","n_edges","series")], max)
max <- max[order( max[,"n_nodes"], max[,"n_edges"]),]
max$ratio_edge <- max$time / ( max$n_edges ** 2)
max$ratio_edge_squared <- max$time / ( max$n_edges ** 2)
max$edge_squared <- (max$n_edges ** 2)
max$ratio_node <- max$time / max$n_nodes
max$node_squared <- max$n_nodes ** 2
max$ratio_node_squared <- (max$time) / (max$n_nodes ** 2)
max$node_squared_edge <- ((max$n_nodes ** 2)*(max$n_edges))
max$ratio_node_squared_edge <- (max$time) / ((max$n_nodes ** 2)*(max$n_edges))

min <- aggregate( df[c("time")], by=df[c("algo","n_nodes","n_edges","series")], min)
min <- min[order( min[,"n_nodes"], min[,"n_edges"]),]
min$ratio_edge <- min$time / min$n_edges
min$ratio_edge_squared <- (min$time) / ( min$n_edges ** 2)
min$edge_squared <- (min$n_edges ** 2)
min$ratio_node <- min$time / min$n_nodes
min$node_squared <- min$n_nodes ** 2
min$ratio_node_squared <- (min$time) / (min$n_nodes ** 2)
min$node_squared_edge <- ((min$n_nodes ** 2)*(min$n_edges))
min$ratio_node_squared_edge <- (min$time) / ((min$n_nodes ** 2)*(min$n_edges))

data_list = list(avgs,max,min)

plot_algos(filename="Graphs/test_log_log_edge.pdf", data=data_list, x="n_edges",y="time", log="xy")
plot_algos(filename="Graphs/test_log_log_nodes.pdf", data=data_list, x="n_nodes", y="time", log="xy")

plot_algos(filename="Graphs/test_ratio_edge.pdf", data=data_list, x="n_edges", y="ratio_edge")
plot_algos(filename="Graphs/test_ratio_node.pdf", data=data_list, x="n_nodes", y="ratio_node")
plot_algos(filename="Graphs/test_ratio_edge_squared.pdf", data=data_list, x="n_edges", y="ratio_edge_squared")
plot_algos(filename="Graphs/test_ratio_node_squared.pdf", data=data_list, x="n_nodes", y="ratio_node_squared")

plot_algos(filename="Graphs/test_const_edge_squared.pdf", data=data_list, x="edge_squared", y="time")
plot_algos(filename="Graphs/test_const_node_squared.pdf", data=data_list, x="node_squared", y="time")
plot_algos(filename="Graphs/test_const_node_squared_edge.pdf", data=data_list, x="node_squared_edge", y="time")

avgs_2 <- aggregate( df[c("time")], by=df[c("algo","n_nodes")], mean)
max_2 <- aggregate( df[c("time")], by=df[c("algo","n_nodes")], max)
min_2 <- aggregate( df[c("time")], by=df[c("algo","n_nodes")], min)
data_list_2 = list(avgs_2,max_2,min_2)

plot_algos(filename="Graphs/log_log_time_vs_nb_noeuds.pdf", data=data_list_2, x="n_nodes", y="time", log="xy")
plot_algos(filename="Graphs/not_log_time_vs_nb_noeuds.pdf", data=data_list_2, x="n_nodes", y="time", log="")

# Write the csv's and the
cas = c("cas moyen","pire cas", "meilleur cas")
i = 1
for(data in data_list){
	for(algo in c("entropy", "backtrack", "dynamic")){
		write_csv(algo=algo, data=data,cas=cas[i])
	}
	i = i+1

}
# avgs[ avgs["algo"] == "dynamic", ]
# max[ max["algo"] == "dynamic", ]
# min[ min["algo"] == "dynamic", ]
