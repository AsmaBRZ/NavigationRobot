import numpy as np

tab=[]
filepath = 'log/1570788762.1964147-TrialDurations-randomPersist.txt'
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
print(q1,q2,q3)