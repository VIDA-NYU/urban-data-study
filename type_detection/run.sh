a1="./sample_result" #Directory to store sampling results (OUTPUT)
a2="./detection_result" #Directory to store detection results (OUTPUT)
a3="./ids" #Directory that stores dataset ids (INPUT)

cat city_list.txt | while read LINE #
do
  arr=(${LINE//;/ })
  JSON_PATH=${arr[1]} #Path to the directory that contains JSON files
  CITY=${arr[0]} #City name
  mkdir $a1
  mkdir $a2
  python sample.py $JSON_PATH $a3"/"$CITY"_ids.txt" $a1 $CITY #Sampling data
  python detect.py $a1 $a3"/"$CITY"_ids.txt" $a2 $CITY #Detect type based on sampled data
#  break
done

#Collect information to generate the barchart
a4="generic.csv" #(Name of output file)
a5="loc.csv" #(Name of output file)
a6="time.csv" #(Name of output file)
JSON_PATH="./" #(Name of output file)
echo $a3 $JSON_PATH $a4 $a5 $a6
python collect.py $a4 $a5 $a6 $a3 $JSON_PATH $a2 
