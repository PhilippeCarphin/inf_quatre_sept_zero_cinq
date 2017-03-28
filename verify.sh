
data_dir=./tp2-donnees
calculated_data=./Data/master_data.csv
answers_file=./Data/answers.csv
# for ex in $(ls $data_dir)
echo "ex,calculated_value,true_value" > comparison.csv
echo "ex,calculated_value,true_value" > correct_values.csv
echo "ex,calculated_value,true_value" > wrong.csv
algo=dynamic
for ex in $(ls $data_dir); do
	letter=${ex: -1}
	series=$( echo $ex | sed 's/poset\([0-9]*-[0-9]*\)[a-j]/\1/')
	n_nodes=$(echo $ex | sed 's/poset\([0-9]*\)-[0-9]*[a-j]/\1/')
	n_edges=$(echo $ex | sed 's/poset[0-9]*-\([0-9]*\)[a-j]/\1/')
	calculated_line=$(grep "$algo,$n_nodes-$n_edges,$letter.*" $calculated_data)
	calculated_value=$(echo $calculated_line | sed 's/.*,\([0-9]*\)/\1/')

	answer_line=$(grep $ex $answers_file)
	answer_value=$(echo $answer_line | sed 's/.*;\([0-9]*\)/\1/')
	# echo $answer_line
	# echo $answer_value
	# echo $calculated_line
	# echo $calculated_value
	if [[ "$answer_value" == "$calculated_value" ]]; then
		good_count=$(($good_count+1))
		echo "
$ex,
calculated : $calculated_value,
      true : $answer_value" >> correct_values.csv
	elif [[ "$calculated_value" != "" ]]; then
		bad_count=$(($bad_count+1))
		echo "
$ex,
calculated : $calculated_value,
      true : $answer_value" >> wrong_values.csv
	fi

	if [[ "$calculated_value" != "" ]]; then
		echo $ex,$calculated_value,$answer_value >> comparison.csv
	fi
done

echo "good_values : $good_count, bad_values : $bad_count"


