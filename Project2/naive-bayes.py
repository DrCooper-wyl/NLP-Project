import json
import re
import tqdm
import nltk
from nltk.corpus import stopwords
import argparse
def preprocess(inputfile,outputfile):
    #TODO: preprocess the input file, and output the result to the output file: train.preprocessed.json,test.preprocessed.json
    #   Delete the useless symbols
    #   Convert all letters to the lowercase
    #   Use NLTK.word_tokenize() to tokenize the sentence
    #   Use nltk.PorterStemmer to stem the words
    with open(inputfile,encoding='utf-8') as f:
        input_dict=json.load(f)
    stemmer = nltk.stem.porter.PorterStemmer()
    for i in tqdm.tqdm(input_dict):
        i[2] = re.sub(u"([^\u0041-\u005a\u0061-\u007a ])", "", i[2]).lower().split()
        for k in range(len(i[2])):
            i[2][k] = stemmer.stem(i[2][k])
    with open(outputfile,'w+',encoding='utf-8') as f:
        f.write(json.dumps(input_dict))
    return
def count_word(inputfile,outputfile):
    #TODO: count the words from the corpus, and output the result to the output file in the format required.
    #   A dictionary object may help you with this work.
    with open(inputfile,encoding='utf-8') as f:
        input_dict=json.load(f)
    sta = {}
    for i in tqdm.tqdm(input_dict):
        for word in i[2]:
            if word not in sta:
                sta[word] = {}
            if i[1] not in sta[word]:
                sta[word][i[1]] = 1
            else:
                sta[word][i[1]] += 1
    crude_sum = 0
    grain_sum = 0
    money_sum = 0
    acq_sum = 0
    earn_sum = 0
    for i in tqdm.tqdm(input_dict):
        s=1
        j=i[1]
        if j == 'crude':
            crude_sum += s
        if j == 'grain':
            grain_sum += s
        if j == 'money-fx':
            money_sum += s
        if j == 'acq':
            acq_sum += s
        if j == 'earn':
            earn_sum += s
    res = '{} {} {} {} {}\n'.format(crude_sum, grain_sum, money_sum, acq_sum, earn_sum)
    t_data=[]
    for i in tqdm.tqdm(sta):
        l = sta[i]
        t = 'crude'
        if t in l:
            crude = l[t]
        else:
            crude = 0
        t = 'grain'
        if t in l:
            grain = l[t]
        else:
            grain = 0
        t = 'money-fx'
        if t in l:
            money = l[t]
        else:
            money = 0
        t = 'acq'
        if t in l:
            acq = l[t]
        else:
            acq = 0

        t = 'earn'
        if t in l:
            earn = l[t]
        else:
            earn = 0
        t_data.append([i, crude, grain, money, acq, earn])
    t_data=sorted(t_data,key=lambda x:x[0])
    for i in t_data:
        res+=' '.join([str(item) for item in i])
        res+='\n'
        # res += "{} {} {} {} {} {}\n".format(i, crude, grain, money, acq, earn)
    with open(outputfile, 'w+', encoding='utf-8') as f:
        f.write(res[:-1])
    return
def feature_selection(inputfile,threshold,outputfile):
    #TODO: Choose the most frequent 10000 words(defined by threshold) as the feature word
    # Use the frequency obtained in 'word_count.txt' to calculate the total word frequency in each class.
    #   Notice that when calculating the word frequency, only words recognized as features are taken into consideration.
    # Output the result to the output file in the format required
    data=[]
    stop=set(stopwords.words('english'))
    with open(inputfile, encoding='utf-8') as f:
        f.readline()
        line = f.readline()
        while line:
            s=line.split()
            if s[0] not in stop:
                for i in range(1,len(s)):
                    s[i]=int(s[i])
                s.append(s[1]+s[2]+s[3]+s[4]+s[5])
                data.append(s)
            line = f.readline()
    res=sorted(data,key=lambda x:(x[-1]))[::-1]
    res=res[:threshold]
    crude_sum = 0
    grain_sum = 0
    money_sum = 0
    acq_sum = 0
    earn_sum = 0
    for i in res:
        crude_sum+=i[1]
        grain_sum += i[2]
        money_sum += i[3]
        acq_sum += i[4]
        earn_sum += i[5]

    st="{} {} {} {} {}\n".format(crude_sum,grain_sum,money_sum,acq_sum,earn_sum)
    for i in res:
        st+="{} {} {} {} {} {}\n".format(i[0],i[1],i[2],i[3],i[4],i[5])
    with open(outputfile, 'w+', encoding='utf-8') as f:
        f.write(st[:-1])
    return
def calculate_probability(word_count,word_dict,outputfile):
    #TODO: Calculate the posterior probability of each feature word, and the prior probability of the class.
    #   Output the result to the output file in the format required
    #   Use 'word_count.txt' and ‘word_dict.txt’ jointly.
    res=""
    with open(word_count, encoding='utf-8') as f:
        line=f.readline().split()
        for i in range(0, len(line)):
            line[i] = int(line[i])
        sum=line[0]+line[1]+line[2]+line[3]+line[4]
        res+="{} {} {} {} {}\n".format(line[0]/sum,line[1]/sum,line[2]/sum,line[3]/sum,line[4]/sum)
    data=[]
    with open(word_dict, encoding='utf-8') as f:
        line=f.readline().split()
        for i in range(0, len(line)):
            line[i] = int(line[i])
        p = line
        line=f.readline()
        while line:
            s = line.split()
            for i in range(1, len(s)):
                s[i] = int(s[i])
            data.append(s)
            line=f.readline()
    for i in tqdm.tqdm(data):
        res+="{} {} {} {} {} {}\n".format(
            i[0],
            (i[1] + 1) / (len(data)+p[0]),
            (i[2] + 1) / (len(data)+p[1]),
            (i[3] + 1) / (len(data)+p[2]),
            (i[3] + 1) / (len(data)+p[3]),
            (i[5] + 1) / (len(data)+p[4])
        )

    with open(outputfile, 'w+', encoding='utf-8') as f:
        f.write(res[:-1])
    return
def classify(probability,testset,outputfile):
    #TODO: Implement the naïve Bayes classifier to assign class labels to the documents in the test set.
    #   Output the result to the output file in the format required
    data={}
    with open(probability, encoding='utf-8') as f:
        line=f.readline().split()
        for i in range(0, len(line)):
            line[i] = float(line[i])
        p = line
        line = f.readline()
        while line:
            s=line.split()
            data[s[0]]=list(map(float,s[1:]))
            line=f.readline()
    res=""
    with open(testset,encoding='utf-8') as f:
        test_data = json.load(f)
    for d in tqdm.tqdm(test_data,total=len(test_data)):
        t_data=[]
        for i in range(5):
            p1=p[i]
            for k in d[2]:
                if k in data:
                    p1=p1*data[k][i]
            t_data.append(p1)
        m=t_data[0]
        m_i=0
        for i in range(5):
            if t_data[i]>m:
                m=t_data[i]
                m_i=i
        if m_i==0:
            res+="{} {}\n".format(d[0],'crude')
        if m_i==1:
            res+="{} {}\n".format(d[0],'grain')
        if m_i==2:
            res+="{} {}\n".format(d[0],'money-fx')
        if m_i==3:
            res+="{} {}\n".format(d[0],'acq')
        if m_i==4:
            res+="{} {}\n".format(d[0],'earn')
    with open(outputfile, 'w+', encoding='utf-8') as f:
        f.write(res[:-1])
    return
def _f1_score(table,index):
    tp=0
    tn=0
    fn=0
    fp=0
    for i in range(len(table)):
        for j in range(len(table)):
            if i!=index and j!=index:
                tn+=table[i][j]
    for i in range(len(table)):
        if i!=index:
            fn+=table[index][i]
            fp+=table[i][index]
    tp=table[index][index]
    return tp,tn,fn,fp

def f1_score(testset,classification_result):
    #TODO: Use the F_1 score to assess the performance of the implemented classification model
    #   The return value should be a float object.
    res=[[0 for i in range(5)] for i in range(5)]
    with open(testset,encoding='utf-8') as f:
        input_dict = json.load(f)
    t=[]
    for i in input_dict:
        if i[1]=='crude':
            t.append(0)
        if i[1]=='grain':
            t.append(1)
        if i[1]=='money-fx':
            t.append(2)
        if i[1]=='acq':
            t.append(3)
        if i[1]=='earn':
            t.append(4)
    t_test=[]
    with open(classification_result, encoding='utf-8') as f:
        line=f.readline()
        while line:
            line=line.split()
            if line[1] == 'crude':
                t_test.append(0)
            if line[1] == 'grain':
                t_test.append(1)
            if line[1] == 'money-fx':
                t_test.append(2)
            if line[1] == 'acq':
                t_test.append(3)
            if line[1] == 'earn':
                t_test.append(4)
            line=f.readline()
    for i in tqdm.tqdm(range(len(t))):
        res[t_test[i]][t[i]]+=1
    ans=0
    for i in range(5):
        tp, tn, fn, fp=_f1_score(res,i)
        p=tp/(tp+fp) if tp+fp>0 else 'undefined'
        r=tp/(tp+fn) if tp+fn>0 else 'undefined'
        f1=2*(p*r)/(p+r) if p!='undefined' and r!='undefined' else 'undefined'
        output=""
        if i==0:
            output+='crude    '
        if i==1:
            output+='grain    '
        if i==2:
            output+='money-fx '
        if i==3:
            output+='acq      '
        if i==4:
            output+='earn     '
        output+=": Precision {:>15.10}, Recall {:>15.10}, F1 {:>15.10}".format(p,r,f1)
        ans+=f1 if f1!='undefined' else 0
        print(output)
    return ans/5
def main():
    ''' Main Function '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-pps', '--preprocess',type=str,nargs=2,help='preprocess the dataset')
    parser.add_argument('-cw','--count_word',type=str,nargs=2,help='count the words from the corpus')
    parser.add_argument('-fs','--feature_selection',type=str,nargs=3,help='\select the features from the corpus')
    parser.add_argument('-cp','--calculate_probability',type=str,nargs=3,
                        help='calculate the posterior probability of each feature word, and the prior probability of the class')
    parser.add_argument('-cl','--classify',type=str,nargs=3,
                        help='classify the testset documents based on the probability calculated')
    parser.add_argument('-f1','--f1_score', type=str, nargs=2,
                        help='calculate the F-1 score based on the classification result.')
    opt=parser.parse_args()

    if(opt.preprocess):
        input_file = opt.preprocess[0]
        output_file = opt.preprocess[1]
        preprocess(input_file,output_file)
    elif(opt.count_word):
        input_file = opt.count_word[0]
        output_file = opt.count_word[1]
        count_word(input_file,output_file)
    elif(opt.feature_selection):
        input_file = opt.feature_selection[0]
        threshold = int(opt.feature_selection[1])
        outputfile = opt.feature_selection[2]
        feature_selection(input_file,threshold,outputfile)
    elif(opt.calculate_probability):
        word_count = opt.calculate_probability[0]
        word_dict = opt.calculate_probability[1]
        output_file = opt.calculate_probability[2]
        calculate_probability(word_count,word_dict,output_file)
    elif(opt.classify):
        probability = opt.classify[0]
        testset = opt.classify[1]
        outputfile = opt.classify[2]
        classify(probability,testset,outputfile)
    elif(opt.f1_score):
        testset = opt.f1_score[0]
        classification_result = opt.f1_score[1]
        f1 = f1_score(testset,classification_result)
        print('The F1 score of the classification result is: '+str(f1))


if __name__ == '__main__':
    main()