data_dir=./tp2-donnees
max_time=180
echo "algo,series,letter,n_nodes,n_edges,time,number"
for ex in $(ls $data_dir); do
	for algo in dynamic backtrack entropy; do
		path=$data_dir/$ex
		letter=${ex: -1}
		series=$( echo $ex | sed 's/poset\([0-9]*-[0-9]*\)[a-j]/\1/')
		n_nodes=$(echo $ex | sed 's/poset\([0-9]*\)-[0-9]*[a-j]/\1/')
		n_edges=$(echo $ex | sed 's/poset[0-9]*-\([0-9]*\)[a-j]/\1/')
		if [[ $(uname) == Darwin ]]; then
			ret=$(gtimeout $max_time ./tp.sh --algo $algo --ex_path $path)
		else
			ret=$(timeout $max_time ./tp.sh --algo $algo --ex_path $path)
		fi
		if [[ $ret == "" ]]; then
			echo "Algo $algo failed for ex $ex by timeout" >& 2
		else
			echo "$algo,$series,$letter,$n_nodes,$n_edges,$ret"
		fi
	done
done



