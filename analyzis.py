import numpy as np
import csv
import ast
import matplotlib.pyplot as plt


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
           #print(line)
           line = ast.literal_eval(line)
           #print(line)
           tab1=line[:10]
           tab2=line[30:40]
           with open('deb.csv', 'w') as writeFile:
               writer = csv.writer(writeFile)
               writer.writerows(tab1)
               writeFile.close()
           with open('fin.csv', 'w') as writeFile:
               writer = csv.writer(writeFile)
               writer.writerows(tab2)
               writeFile.close()
    return tab1,tab2

    
def getHistoDeb(x,y):
    
    plt.hist2d(x, y)
    plt.show()


    
    
#filepath='Analyzis/1571139560.5373607-TrialDurations-randomPersist.txt'
#filepath= 'log/1571389756.340987_Qlearning_values.npy'
#print(getPercentiles(filepath))
t1,t2=openFile('log/POS0.txt')
#print(t1)

for i in range(len(t1)):
    #print(t1[i])
    xt1=[j[0]  for j in t1[i]]
    yt1=[j[1]  for j in t1[i]]

print(yt1)

for i in range(len(t2)):
    #print(t1[i])
    xt2=[j[0]  for j in t2[i]]
    yt2=[j[1]  for j in t2[i]]

print(yt1)

plt.hist2d(xt2, yt2, bins=[12, 12], normed=True, cmap='plasma')
plt.colorbar()
plt.show()
#xt1=[i[0] for i in t1]
#yt1=[i[1] for i in t1]
#print(xt1)
#xt2=[i[0] for i in t2]
#yt2=[i[1] for i in t2]


