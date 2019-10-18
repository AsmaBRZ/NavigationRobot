import numpy as np
import csv
import ast


def getPercentiles(filepath):
    tab=[]
    with open(filepath) as fp:

       line = fp.readline()
       cnt = 1
       while line:
           line = fp.readline().split("\n")[0]
           if line != '':
               tab.append(float(line))
    tab=np.array(tab)
    #Median
    med=np.median(tab)
    print(med)
    q1=np.percentile(tab, 25) 
    q2=np.percentile(tab, 50) 
    q3=np.percentile(tab, 75) 
    return q1,q2,q3


def openFile(filepath):
    tab=[]
    with open(filepath) as fp:
       line = fp.readline()
       if line != '':
           print(line)
           line = ast.literal_eval(line)
           #print(line)
           tab1=line[0]
           tab2=line[1]
           with open('deb.csv', 'w') as writeFile:
               writer = csv.writer(writeFile)
               writer.writerows(tab1)
               writeFile.close()
           with open('fin.csv', 'w') as writeFile:
               writer = csv.writer(writeFile)
               writer.writerows(tab2)
               writeFile.close()
    return tab1,tab2

    
def getHistoDeb(data):
    
    column_labels = np.arange(0,300,50)
    row_labels = np.arange(0,400,50)
    data = datadeb # quatre lignes de trois colonnes
    fig, axis = plt.subplots() # il me semble que c'est une bonne habitude de faire supbplots
    heatmap = axis.pcolor(data, cmap=plt.cm.Blues) # heatmap contient les valeurs

    
    
#filepath='Analyzis/1571139560.5373607-TrialDurations-randomPersist.txt'
#filepath= 'log/1571389756.340987_Qlearning_values.npy'
#print(getPercentiles(filepath))
t1,t2=openFile('t.txt')

xt1=[i[0] for i in t1]
yt1=[i[1] for i in t1]
xt2=[i[0] for i in t2]
yt2=[i[1] for i in t2]


