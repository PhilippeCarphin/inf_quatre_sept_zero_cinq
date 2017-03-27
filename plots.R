#!/usr/local/bin/Rscript
library(gridExtra)
write_csv <- function(algo, data=avg)
{
	# Select rows where algo == algo
	table <- avgs[
					  avgs["algo"] == algo, # Select rows
					  c("n_nodes", "n_edges",  "time", "number") # select columns
				  ]

	# Print table to console
	# print(paste(c("Algo ", algo), collapse=" "))
	# print(table, row.names=FALSE)

	# Write table to csv file
	filename = paste(c("Data/",algo, ".csv"), collapse="")
	write.table(table, filename, row.names=FALSE)

	# Save pdf of the table
	title <- paste(c("Data/Moyennes_", algo,".pdf"), collapse="")
	pdf(title)
	grid.table(table)
	dev.off()
}

plot_log_log <- function(filename="Graphs/Graph.pdf", data=df)
{
	pdf(filename, width=7.5, height=4)
	par(mfrow=c(2,3))
	# Do each graph except for (Algo=counting, Series=2)
	for(algo in c("backtrack","dynamic","entropy")){
		title <- paste(c("Algorithme ", algo), collapse="")
		to_plot <- data[data["algo"]==algo,][,c("n_nodes","time")]
		plot(to_plot,log="xy",main=title)
	}
	for(algo in c("backtrack","dynamic","entropy")){
		title <- paste(c("Algorithme ", algo), collapse="")
		to_plot <- data[data["algo"]==algo,][,c("n_edges","time")]
		plot(to_plot,log="xy",main=title)
	}
	dev.off()
}

plot_algos <- function(filename, data=avg, cols=c("time","n_edges"), log="")
{
	pdf(filename, width=7.5, height=4)
	par(mfrow=c(2,3))
	# Do each graph except for (Algo=counting, Series=2)
	for(algo in c("backtrack","dynamic","entropy")){
		title <- paste(c("Algorithme ", algo), collapse="")
		to_plot <- data[data["algo"]==algo,][,cols]
		plot(to_plot,log=log, main=title)
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
avgs$ratio_node <- avgs$time / avgs$n_nodes

max <- aggregate( df[c("time")], by=df[c("algo","n_nodes","n_edges","series")], max)
max$ratio_edge <- max$time / ( max$n_edges ** 2)
max$ratio_edge_squared <- max$time / ( max$n_edges ** 2)
max$ratio_node <- max$time / max$n_nodes

min <- aggregate( df[c("time")], by=df[c("algo","n_nodes","n_edges","series")], min)
min$ratio_edge <- min$time / ( min$n_edges ** 2)
min$ratio_edge_squared <- min$time / ( min$n_edges ** 2)
min$ratio_node <- min$time / min$n_nodes

# Make a log-log graph
plot_log_log(filename="Graphs/avg-loglog.pdf", data=avgs)
plot_algos(filename="Graphs/ratio_edge_squared_avg.pdf", data=avgs, cols=c("ratio_edge_squared","n_edges"))
plot_algos(filename="Graphs/ratio_edge_avg.pdf", data=avgs, cols=c("ratio_edge","n_edges"))
plot_algos(filename="Graphs/ratio_node_avg.pdf", data=avgs, cols=c("ratio_node","n_nodes"))

# Write the csv's and the
for(algo in c("entropy", "backtrack", "dynamic")){
	write_csv(algo=algo, data=avgs)
}
# avgs[ avgs["algo"] == "dynamic", ]
# max[ max["algo"] == "dynamic", ]
# min[ min["algo"] == "dynamic", ]
