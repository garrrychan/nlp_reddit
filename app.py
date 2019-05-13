import pandas as pd
import numpy as np
from flask import request, Flask, render_template

app = Flask(__name__)

final = pd.read_csv("./data/final.csv", encoding='utf-8')

sample_list = []
# home page
@app.route('/', methods=['GET'])
def form():
    sample = final.title.sample()
    sample_show = sample.values[0].strip().capitalize()
    sample_list.append([sample_show,sample.index[0]])
    return render_template("form.html", sample = sample_show)

# Return prediction
@app.route('/', methods=['POST'])
def form_post():
    if request.method == 'POST':
        guess = request.form['text']
        sample = sample_list[-1][0] # get the latest sample
        index = sample_list[-1][1]
        prediction = final.iloc[index].prediction
        # ensure probability matches prediction
        if final.iloc[index].proba_lpt >= 0.5:
            probability = final.iloc[index].proba_lpt
        else:
            probability = 1-final.iloc[index].proba_lpt
        label = final.iloc[index].label
    return render_template("result.html", guess = guess, pred = prediction, prob = round(probability*100,2), label = label)

if __name__ == '__main__':
    app.run(debug=True)
