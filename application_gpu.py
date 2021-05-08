from flask import Flask
from flask import render_template
import pandas as pd
from flask import request
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
# def root():
#       return render_template('home.html')

def show_tables():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':

# ici je stock ce qui est tappé dans la textarea de mon html
        choice = request.form.get('user_csv').split('\n')
        print("eheheh :",choice)

    df_gpu = pd.read_csv('gpu.csv', delimiter=";")
    # data.set_index(['Port'])
    # data.set_index(['Name'], inplace=True)
    df_gpu.index.name = None
    #df_gpu = df_gpu.head(10)
    df_gpu = df_gpu.loc[df_gpu.Process==choice[0]]
    return render_template('home.html', tables=[df_gpu.to_html(classes='gpu')],
                           titles=['Cartes graphiques'])


"""
@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        return 'post'

        
        results = []

        user_csv = request.form.get('user_csv').split('\n')
        print user_csv
        reader = csv.DictReader(user_csv)

        for row in reader:
            results.append(dict(row))

       # fieldnames = [key for key in results[0].keys()]

        #return render_template('home.html', results=results, fieldnames=fieldnames, len=len)
        #return render_template("home.html", results=results)
"""
if __name__ == '__main__':
    app.run(debug=True)
