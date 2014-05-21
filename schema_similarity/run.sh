OUT="./similarity" #Directory that stores similarity scores
mkdir $OUT

cat city_list.txt | while read LINE #
do
  arr=(${LINE//;/ })
  JSON_PATH=${arr[1]} #Path to the directory that contains JSON files
  CITY=${arr[0]} #City name
  python schema_similarity.py $CITY $JSON_PATH $OUT
  break
done
