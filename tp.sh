#!/bin/bash

#
# Parse the command line arguments
#
algo=backtrack
ex_path='tp2-donnees/poset10-4a'
pretty=
while [[ $# -gt 0 ]]
do
    option="$1"
	optarg="$2"
    case $option in
        -a|--algo)
			algo="$optarg"
			shift
			;;
        -e|--ex_path)
			ex_path="$optarg"
			shift
			;;
		-p|--print)
			pretty=yes
			;;
		-t|--time)
			print_time=yes
			;;
        *)
            echo "unknown option: $option"
            exit
			;;
    esac
shift
done



case $algo in
	vorace|entropy)
		duration=$(python entropy.py $ex_path $pretty)
		;;
	retourArriere|backtrack)
		duration=$(python backtrack.py $ex_path $pretty)
		;;
	dynamique|dynamic)
		duration=$(python dynamic.py $ex_path $pretty)
		;;
	*)
		echo "Unknown algorithm"
		;;
esac

echo "$duration"
