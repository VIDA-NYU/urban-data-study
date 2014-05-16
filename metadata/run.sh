OUTPUT_PATH="data"
mkdir $OUTPUT_PATH
cat urls.txt | while read LINE
do
echo $LINE
python get_metadata.py $LINE $OUTPUT_PATH
done
