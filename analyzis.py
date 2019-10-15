import numpy as np



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
    
    
filepath='Analyzis/1571139560.5373607-TrialDurations-randomPersist.txt'
print(getPercentiles(filepath))