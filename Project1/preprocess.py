import json
import re
import nltk

def read_files(dir,fileList):
    corpus = []
    for item in fileList:
        with open(dir + '/'+item, encoding='utf-8') as f:
            corpus.append([item.strip('.txt'),f.read()])
    return corpus
def preprocess_corpus(corpus):
    for i in range(len(corpus)):
        #strip some symbol from the original text
        stripped_text = text_strip(corpus[i][1])
        # print(stripped_text)
        #use the tokenize function to tokenize the text
        tokenized_text = text_tokenize(stripped_text)
    #     #use the stemmer to stem the tokenized words
        for j in range(len(tokenized_text)):
            tokenized_text[j] = text_stem(tokenized_text[j])
            # print(tokenized_text[j])
        corpus[i][1] = tokenized_text
    return corpus
def text_strip(text):
    #Use the regular expression to:
    #   strip the blank and escape symbol from the original text
    #   strip the '...more' at the end of each original text
    #Convert letters to lowercase
    text=text.lower()
    text=re.sub(r'\.\.\.more$','more',text)
    text = re.sub(r'n\'t', ' not', text)
    text = re.sub(r'\'am', ' am', text)
    text = re.sub(r'\'re', ' are', text)
    text = re.sub(r'\'s', ' is', text)
    # text = re.sub(r'\.', '', text)
    # text = re.sub(r',', '', text)
    # text = re.sub(r'\?', '', text)
    # text = re.sub(r'\'', '', text)
    # text = re.sub(r'"', '', text)
    # text = re.sub(r';', '', text)
    # text = re.sub(r':', '', text)
    return text
def text_tokenize(text):
    #The function should return a list that contains the tokenized words as the elements.
    # text=nltk.wordpunct_tokenize(text)
    text = re.sub(r'\.', ' .', text)
    text = re.sub(r',', ' ,', text)
    text = re.sub(r'\?', ' ?', text)
    text = re.sub(r'\'', ' \'', text)
    text = re.sub(r'"', ' \"', text)
    text = re.sub(r';', ' ;', text)
    text = re.sub(r':', ' :', text)
    text=text.split(' ')
    # print(text)
    return text
def text_stem(word):
    #The function receives a word that needs to be stemmed and returns the stemmed word.
    stemmer=nltk.stem.snowball.SnowballStemmer('english',ignore_stopwords=True)
    word=stemmer.stem(word)
    return word
def output_to_file(corpus,save_dir):
    for item in corpus:
        with open(save_dir+item[0]+'.txt','w',encoding='utf-8') as f:
            f.write(str(item[1]))
            f.close()
def output_to_json(corpus,save_dir):
    with open(save_dir+'corpus.json','w',encoding='utf-8') as f:
        corpus = json.dumps(corpus)
        f.write(corpus)
        # f.close()
def main():
    ''' Main Function '''
    import os
    nltk.download('stopwords')
    fileList = os.listdir('test')
    save_dir = './corpus/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    corpus = read_files('test',fileList)
    # print(corpus)
    preprocessed_corpus = preprocess_corpus(corpus)
    output_to_file(preprocessed_corpus,save_dir)
    output_to_json(preprocessed_corpus,'./')

if __name__ == '__main__':
    main()