import numpy as np
import pandas as pd
import streamlit as st
from mlxtend.frequent_patterns import fpgrowth
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(page_title="Kelompok 5")

header = st.container()
dataset = st.container()
modelTraining = st.container()
Doctor = st.container()

with header:

    st.title('Prediksi Kesehatan Mental')
    st.title('Hello')
   


with dataset:

    df = pd.read_csv("dataset3.csv")

    x=df.loc[:, 'feeling nervous':'blamming yourself'].replace("yes", pd.Series(True, df.columns))
    x=x.loc[:, 'feeling nervous':'blamming yourself'].replace("no", pd.Series(False, df.columns))

    doyou = ['feel hopeless' ,'feel angry' , 'panic' , 'feel negative' , 'have changes in eating' , 'have suicidal thought' , 'have a close friend',
         'have a social media addiction' , 'over react', 'avoid people or activities', 'have material possessions', 'a popping up stressful memory',
         'have trouble concentrating' ]
    
    areyou = ['sweating' , 'having trouble in concentration' , 'having trouble in sleeping' , 'feeling nervous' , 'having nightmares' , 'an intovert',
            'having trouble with work'  , 'feeling tired' , 'blamming yourself' , 'breathing rapidly']
    
    haveYou = ['gained weight']

    final = fpgrowth(x, min_support=0.6 , use_colnames=True )

    fin = final['itemsets']
    y = list()
    for i in fin:
            y.append(list(i))


    def getInList(word , test1): 

        t = [i for i in test1 if word in i]

        for d in t:
            d.remove(word)
        return t

    def getNotInList(word , temp):
        t = [i for i in temp if word not in i]

        return t

    def getMax(freqList):
        fin = final['itemsets']
        k = list()
        for i in fin:
            k.append(list(i))
        u = dict()
        for i in k[0:17]:
            count = 0
            for j in freqList:
                if i[0] in j:
                    count+=1
            u.update({i[0]:count})

        MaxDictVal = max(u, key=u.get)
            
        return MaxDictVal


with modelTraining:

    tel_col1 = st.table()
    tel5 = st.table()
    col1 , col2 = tel5.columns(2)


    col_1 , col_2 =tel_col1.columns(2)
    fName =  col_1.text_input("Nama Depan : ")
    lName =  col_2.text_input("Nama Belakang : ")
    Age =  col_1.text_input("Umur     : ")

    symptoms = list()
    bel = st.header("Jawab pertanyaan berikut")
    
    rflag = 1
    tempwordlist = y
    maxword = getMax(tempwordlist)  
    sel = st.table()
    answers = dict()
    
    word = sel.selectbox("Question 1 : Do you "+maxword+" all the time" ,("-" , "yes" , "no") , 0, help = "test")

    prog=1  
    progressBar = st.progress(prog)
    
    for i in range(0,3):
        if word == 'yes':
            
            answers.update({maxword : word})
            prog+=25
            progressBar.progress(prog)

            symptoms.append(maxword)
            sel.empty()           
            tempwordlist = getInList(maxword ,tempwordlist)
            maxword = getMax(tempwordlist)
            if maxword in areyou:
                question = " Are you "
            elif maxword in doyou:
                question = " Do you "
            else:
                question = " Have you "
            word = sel.selectbox("Question "+str(i+2) + question +maxword+" all the time" ,("-" , "yes" , "no") , 0 , help = "test")
            
            rflag+=1

        elif word == 'no':
            answers.update({maxword : word})
            prog+=25
            progressBar.progress(prog)
            tempwordlist = getNotInList(maxword ,tempwordlist)
            maxword = getMax(tempwordlist)
            if maxword in areyou:
                question = " Are you "
            elif maxword in doyou:
                question = " Do you "
            else:
                question = " Have you "
            word = sel.selectbox("Question "+str(i+2) +question +maxword+" all the time" ,("-" , "yes" , "no") , 0 , help = "test")
            rflag+=1
    if word == 'yes':
        answers.update({maxword : word})

        prog+=24
        progressBar.progress(prog)
        symptoms.append(maxword)
        tempwordlist = getInList(maxword ,tempwordlist)
    elif word == 'no':
        answers.update({maxword : word})
        prog+=24
        progressBar.progress(prog)
        tempwordlist = getNotInList(maxword ,tempwordlist)


    if rflag == 4 and word == 'yes' or word == "no":            
        progressBar.empty()
        bel.empty()

        for i in answers.items():
                output = i[0] +" "+ i[1]
                col1.text(".   ⚙️"+ output)
        
        temp = sel.button("Submit")
        if temp:
            sel.empty()
            tel_col1.empty()
            tel5.empty()
            st.success("Jawaban Anda telah berhasil disimpan! Terima kasih")
            st.balloons()




    frequentSymptoms = list()
    for i in tempwordlist:
        for j in i:
            if j not in frequentSymptoms:
                frequentSymptoms.append(j)
    
    Demo = st.button("Doctor Demo")
    if Demo:
        sel.empty()
        progressBar.empty()
        tel_col1.empty()
        tel5.empty()

        with Doctor:


            st.subheader("Nama Pasien: " + fName + " "+ lName)
            st.subheader("Umur Pasien: " + Age)

            c1 , c2 = st.columns(2)


            c1.subheader("Jawaban Pasien")
            if len(symptoms) != 0:
                for x in symptoms:
                    c1.text(".  "+"⚙️" + x)
            else:
                c1.error("Tidak ada gejala yang ditampilkan : Pasien telah memilih 0 gejala")
            
            c2.subheader("Gejala lain yang mungkin")

            for i in frequentSymptoms:
                c2.text(".   ⚙️" + i)
            
            le=LabelEncoder()
            for i in df[:]:
                df[i]=le.fit(df[i]).transform(df[i])

            col = list()
            for i in df:
                col.append(i)
            
            X,Y=df[col[:24]], df['Disorder']

            clf_gini = DecisionTreeClassifier(criterion='gini', max_depth=3 ,  random_state=1)
            clf_gini.fit(X, Y)

            final_symptoms = frequentSymptoms + symptoms
            rampage = []
            for i in col[0:24]:
                if i in final_symptoms:
                    rampage.append(1)
                else:
                    rampage.append(0)
            rampage=[rampage]
            ramp = pd.DataFrame(rampage)

            y_pred_gini = clf_gini.predict(ramp)

            if len(symptoms) != 0:
                if y_pred_gini[0] == 0:
                    disorder = "Kecemasan"
                elif y_pred_gini[0] == 1:
                    disorder = "Depresi"
                elif y_pred_gini[0] == 2:
                    disorder = "Kesepian"
                elif y_pred_gini[0] == 3:
                    disorder = "None"
                elif y_pred_gini[0] == 4:
                    disorder = "Stress"
            else:
                disorder = "Gangguan tidak dapat diprediksi karena tidak ada gejala yang ditunjukkan"

            st.error("Gangguan yang diprediksi : " + disorder )
    

    

