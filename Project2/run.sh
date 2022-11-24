echo "Train data---Pre-Process"
python naive-bayes.py -pps train.json train.preprocessed.json
echo ""
echo "Test data---Pre-Process"
python naive-bayes.py -pps test.json test.preprocessed.json
echo ""
echo "Generate the word count file"
python naive-bayes.py -cw train.preprocessed.json word_count.txt
echo ""
echo "Generate the word dict file"
python naive-bayes.py -fs word_count.txt 10000 word_dict.txt
echo ""
echo "Calculate the probability of each word and class"
python naive-bayes.py -cp word_count.txt word_dict.txt word_probability.txt
echo ""
echo "Prediction"
python naive-bayes.py -cl word_probability.txt test.preprocessed.json classification_result.txt
echo ""
echo "Evaluation"
python naive-bayes.py -f1 test.json classification_result.txt