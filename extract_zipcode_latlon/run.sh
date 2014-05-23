OUTPUT="data"
mkdir $OUTPUT

cat city_list.txt | while read LINE #
do
  arr=(${LINE//;/ })
  JSON_PATH=${arr[1]} #Path to the directory that contains JSON files
  CITY=${arr[0]} #City name
  echo  $CITY $JSON_PATH $OUTPUT
  python collect_data.py $CITY $JSON_PATH $OUTPUT
  break
done
