import sys

sys.path.append('..')
sys.path.append('.')
import nltk
nltk.download('punkt')
from MEM import MEMM
from flask import Flask
from flask import jsonify
app = Flask(__name__)
from flask import request
classifier = MEMM()
from flask_cors import CORS
CORS(app)
try:
     classifier.load_model()
     print("Load Model Successfully")
except FileNotFoundError:
    print("No Model")

def test(text:str):
    text_list= nltk.word_tokenize(text)
    t_lables=["0" for i in range(len(text_list)+1)]
    features = [classifier.features(text_list, t_lables[i], i)
                for i in range(len(text_list))]
    results = [classifier.classifier.classify(n) for n in features]
    res=[]
    for i in range(len(text_list)):
        # print("{} {}".format(text_list[i],results[i]))
        res.append([text_list[i],results[i]])
    return res

@app.route('/',methods=['GET'])
def api():
    if request.method=='GET':
        text=request.args.get('text')
        res=test(text)
        return jsonify(res)




# if __name__ == '__main__':
#     test('Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, '
#          'Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped,'
#          'Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, '
#          'Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, '
#          'Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, '
#          'Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, '
#          'Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, Elisei is one of 200 child victims. Ukraine children: Killed as he escaped, '
#          'Elisei is one of 200 child victims.')