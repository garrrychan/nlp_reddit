import pandas as pd
import numpy as np
from flask import request, Flask, render_template
# for new predictions
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def post_to_words(raw_post):
    '''Returns a list of words ready for classification, by tokenizing,
    removing punctuation, setting to lower case and removing stop words.'''
    tokenizer = RegexpTokenizer(r'[a-z]+')
    words = tokenizer.tokenize(raw_post.lower())
    meaningful_words = [w for w in words if not w in set(stopwords.words('english'))]
    return(" ".join(meaningful_words))

def predict(input):
    input_ready = re.sub(r"[uU]*[lL][pP][tT]\s*:*", '', post_to_words(input))
    cvect = pickle.load(open("./cvect.pkl","rb"))
    # pre-learned 5104 vocabulary
    new_data = cvect.transform([input_ready])
    logmodel = pickle.load(open("./logmodel.pkl","rb"))
    prediction = logmodel.predict(new_data)
    proba_lpt = logmodel.predict_proba(new_data)
    # prob of life pro tip "0"
    print(input)
    return prediction, proba_lpt[:,0][0]

### run app ###

app = Flask(__name__)

final = pd.read_csv("./data/final.csv", encoding='utf-8')

sample_list = []
# home page
@app.route('/', methods=['GET'])
def form():
    sample = final.title.sample()
    sample_show = sample.values[0].strip()
    sample_list.append([sample_show,sample.index[0]]) # save the index
    return render_template("form.html", sample = sample_show)

# Return prediction
@app.route('/', methods=['POST'])
def form_post():
    # if button is pressed
    try:
        guess = request.form['guess']
        sample = sample_list[-1][0] # get the latest sample
        index = sample_list[-1][1] # get the index
        prediction = final.iloc[index].prediction
        # ensure probability matches prediction
        if final.iloc[index].proba_lpt >= 0.5:
            probability = final.iloc[index].proba_lpt
        else:
            probability = 1-final.iloc[index].proba_lpt
        label = final.iloc[index].label

        return render_template("result.html", sample=sample, guess = guess, pred = prediction, prob = round(probability*100,1), label = label)
    except:
        # text field is completed
        input = request.form["text"]
        if predict(input)[0][0] == 0:
            prediction = "Life Pro Tip"
            probability = predict(input)[1]
        else:
            prediction = "Unethical Life Pro Tip"
            probability = 1-predict(input)[1]

        return render_template("result_new.html", sample=input, pred = prediction, prob = round(probability*100,1))

if __name__ == '__main__':
    app.run(debug=True)
