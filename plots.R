
write_csv <- function(algo, data=avg)
{
	table <- avgs[
					  avgs["algo"] == algo, # Select rows
					  c("n_nodes", "n_edges",  "time") # select columns
				  ]
	print(table, row.names=FALSE)
	write.table(table, paste(c(algo, ".csv"), collapse=""), row.names=FALSE)
}

plot_page <- function(title="Graphs/Graph.pdf", data=df)
{
	pdf(title, width=8.5, height=11)
	par(mfrow=c(5,3))
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

df <- read.table("master_data.csv", header = TRUE, sep = ",")
avgs <- aggregate( df["time"], by=df[c("algo","n_nodes","n_edges","series")], mean)


# plot_page(title="Graphs/avg-loglog.pdf", data=avgs)
write_csv("dynamic", avgs)
# for(algo in c("entropy", "backtrack", "dynamic")){
#	write_csv(algo=algo, data=avgs)
#}
