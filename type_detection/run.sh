a1="./sample_result" #Directory to store sampling results
a2="./detection_result" #Directory to store detection results
a3="./ids" #Directory to store ids results
cat city_list.txt | while read LINE
do
  arr=(${LINE//;/ })
  JSON_PATH=${arr[1]}
  CITY=${arr[0]}
  mkdir $a1
  mkdir $a2
  python sample.py $JSON_PATH $a3"/"$CITY"_ids.txt" $a1 $CITY
  python detect.py $a1 $a3"/"$CITY"_ids.txt" $a2 $CITY
  break
done

#Collect information to generate the barchart
a4="generic.csv"
a5="loc.csv"
a6="time.csv"
JSON_PATH="./"
echo $a3 $JSON_PATH $a4 $a5 $a6
python collect.py $a4 $a5 $a6 $a3 $JSON_PATH $a2 
