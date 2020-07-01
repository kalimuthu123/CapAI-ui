#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from flask import Flask
from flask import Flask, flash, redirect, render_template, request
import os
import speech_recognition as sr
import subprocess
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import capai

from sqlalchemy import create_engine

app = Flask(__name__)

@app.route("/")
def LoadHome():
    return render_template('SpeechToText.html')

@app.route('/Speech', methods=['GET', 'POST'])
def Speech():
    Output = ""#"Text: "
    df = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        Output = Output + r.recognize_google(audio);
    except:
        pass;
    sqlUri="mysql+pymysql://root:mysqlroot@localhost/blk_superset"
    # Create your connection.
    engine2 = create_engine(sqlUri)
    cnx = engine2.connect()
    query=capai.getSql(Output, sqlUri)
    print("--####>",query)
    df1 = pd.read_sql_query(query, cnx) 
    return render_template('SpeechToText.html', Output = Output, OutputQuery = df, tables=[df1.to_html(classes='TableBody')], titles=df1.columns.values)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False,host='0.0.0.0', port=5001)
