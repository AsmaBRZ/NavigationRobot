#!/usr/bin/env python

from radarGuidance import *
from wallFollower import *

import random #used for the random choice of a y
import sys
import numpy as np
import math
import itertools 
import threading
#--------------------------------------
# Position of the goal:
goalx = 300
goaly = 450
# Initial position of the robot:
initx = 300
inity = 35
# strategy choice related stuff:
choice = -1
choice_tm1 = -1
tLastChoice = 0
rew = 0
trial=0
i2name=['wallFollower','radarGuidance']

# Parameters of State building:
# threshold for wall consideration
th_neglectedWall = 35
# threshold to consider that we are too close to a wall
# and a punishment should be delivered
th_obstacleTooClose = 13
# angular limits used to define states
angleLMin = 0
angleLMax = 55

angleFMin=56
angleFMax=143

angleRMin=144
angleRMax=199



# Q-learning related stuff:
# definition of states at time t and t+1



def buildQ():
    all_list = [['0','1'],['0','1'],['0','1'],['0','1','2','3','4','5','6','7'],['0','1','2'] ]
    permutations= list(itertools.product(*all_list)) 
    new_list = []
    for l in permutations:
        new_list.append(''.join(l))
    Q=dict()
    for s in new_list:
        Q[s]={0:0,1:0}
    return Q

S_t = ''
S_tm1 = ''
Q=buildQ()
initLearning=True
posT=[]
pos=0


#save the robot's position every second
def savePos(robot):
    threading.Timer(1.0, savePos).start
    posT[trial].append(robot.get_pos())

#--------------------------------------
# the function that selects which controller (radarGuidance or wallFollower) to use
# sets the global variable "choice" to 0 (wallFollower) or 1 (radarGuidance)
# * arbitrationMethod: how to select? 'random','randPersist','qlearning'
def strategyGating(arbitrationMethod,verbose=True):
  global choice
  global choice_tm1
  global tLastChoice
  global rew
  global init
  global Q
    
  choice_tm1 = choice
  # The chosen gating strategy is to be coded here:
  #------------------------------------------------
  if arbitrationMethod=='random':
    choice = random.randrange(2)
  #------------------------------------------------
  
  elif arbitrationMethod=='randomPersist':
    if init:
        choice = random.randint(0,1)
        init=False
        tLastChoice=time.time()
    else:
        if time.time()-tLastChoice <2 :
            return 
        else :
            tLastChoice=time.time()
            choice = random.randint(0,1)
            print('Persistent Random selection : to be implemented')
  #------------------------------------------------
  elif arbitrationMethod=='qlearning':
        choice=qlearning()
        

  #------------------------------------------------
  else:
    print(arbitrationMethod+' unknown.')
    exit()

  if verbose:
    print("strategyGating: Active Module: "+i2name[choice])




def qlearning(alpha=0.4, beta=4, gamma=0.95):
  global S_t
  global S_tm1
  global Q
  global rew
  global choice
  global changed
  global choice_tm1
  global tLastChoice
  if rew != 0 or S_tm1 != S_t or choice != choice_tm1:
      #print("train")
      #print('rew %f' % rew)
      #print('gamma',gamma)
      #print('st',S_t)
      Q_st=np.fromiter(Q[S_t].values(), dtype=float)
      #print(Q_st)
    
      Q_stm1=np.fromiter(Q[S_tm1].values(), dtype=float)
      #print(Q_stm1)
      delta = rew + gamma  * np.max(Q_st) - Q_stm1[choice_tm1]
      #print('delta %f' % delta)
      Q[S_tm1][choice_tm1]  = Q[S_tm1][choice_tm1] + alpha * delta

      print("{} : {}".format(S_tm1, Q[S_tm1][choice_tm1]))
      rew = 0
      
  t = time.time()
 
  if t - tLastChoice >= 2 or S_tm1 != S_t or rew != 0:
        action = discreteProb(softmax(Q, S_tm1, beta))
        #print("action %d" % action)
        tLastChoice = t
        return action
   

  return choice


    
#--------------------------------------
def buildStateFromSensors(laserRanges,radar,dist2goal):
  S   = ''
  # determine if obstacle on the left:
  wall='0'
  if min(laserRanges[angleLMin:angleLMax]) < th_neglectedWall:
    wall ='1'
  S += wall
  # determine if obstacle in front:
  wall='0'
  if min(laserRanges[angleFMin:angleFMax]) < th_neglectedWall:
    wall ='1'
    #print("Mur Devant")
  S += wall
  # determine if obstacle on the right:
  wall='0'
  if min(laserRanges[angleRMin:angleRMax]) < th_neglectedWall:
    wall ='1'
  S += wall

  S += str(radar)

  if dist2goal < 125:
    S+='0'
  elif dist2goal < 250:
    S+='1'
  else:
    S+='2'
  #print('buildStateFromSensors: State: '+S)

  return S

def softmax(Q,x,beta=4):
    # Returns a soft-max probability distribution over actions
    # Inputs :
    # - Q : a Q-function represented as a nX times nU matrix
    # - x : the state for which we want the soft-max distribution
    # - tau : temperature parameter of the soft-max distribution
    # Output :
    # - p : probability of each action according to the soft-max distribution
    
    p = np.zeros((len(Q[x])))
    sump = 0
    for i in range(len(p)) :
        p[i] = np.exp((Q[x][i] * beta))
        sump += p[i]
    p = p/sump
    return p


def discreteProb(p):
        # Draw a random number using probability table p (column vector)
        # Suppose probabilities p=[p(1) ... p(n)] for the values [1:n] are given, sum(p)=1 
        # and the components p(j) are nonnegative. 
        # To generate a random sample of size m from this distribution,
        #imagine that the interval (0,1) is divided into intervals with the lengths p(1),...,p(n). 
        # Generate a uniform number rand, if this number falls in the jth interval given the discrete distribution,
        # return the value j. Repeat m times.
        r = np.random.random()
        cumprob=np.hstack((np.zeros(1),p.cumsum()))
        sample = -1
        for j in range(p.size):
            if (r>cumprob[j]) & (r<=cumprob[j+1]):
                sample = j
                break
        return sample


#--------------------------------------
def main():
  global S_t
  global S_tm1
  global rew
  global init
  init = True
  global initLearning
  global robot   
  global savePos
  global trial
  settings = Settings('worlds/entonnoir.xml')
  env_map = settings.map()
  robot = settings.robot()
  #savePos(robot)
  d = Display(env_map, robot)

  
  method='qlearning'
  # experiment related stuff
  startT = time.time()
  global trial 
  trial = 0
  nbTrials = 40
  trialDuration = np.zeros((nbTrials))
 
  i = 0
  tL=time.time()
  j=0
  while trial<nbTrials:
    posT.append([])
    j=0
    # update the display
    #-------------------------------------
    d.update()
    # get position data from the simulation
    #-------------------------------------
    pos = robot.get_pos()
    #print("##########\nStep "+str(i)+" robot pos: x = "+str(int(pos.x()))+" y = "+str(int(pos.y()))+" theta = "+str(int(pos.theta()/math.pi*180.)))

    # has the robot found the reward ?
    #------------------------------------
    dist2goal = math.sqrt((pos.x()-goalx)**2+(pos.y()-goaly)**2)
    # if so, teleport it to initial position, store trial duration, set reward to 1:
    if (dist2goal<20): # 30       
      print('***** REWARD REACHED *****')
      pos.set_x(initx)
      pos.set_y(inity)
      robot.set_pos(pos) # format ?
      # and store information about the duration of the finishing trial:
      currT = time.time()
      trialDuration[trial] = currT - startT
      startT = currT
      print("Trial "+str(trial)+" duration:"+str(trialDuration[trial]))
      trial +=1
      rew = 1

    # get the sensor inputs:
    #------------------------------------
    lasers = robot.get_laser_scanners()[0].get_lasers()
    laserRanges = []
    for l in lasers:
      laserRanges.append(l.get_dist())

    radar = robot.get_radars()[0].get_activated_slice()

    bumperL = robot.get_left_bumper()
    bumperR = robot.get_right_bumper()


    # 2) has the robot bumped into a wall ?
    #------------------------------------
    if bumperR or bumperL or min(laserRanges[angleFMin:angleFMax]) < th_obstacleTooClose:
      rew = -1
      #print("***** BING! ***** "+i2name[choice])

    # 3) build the state, that will be used by learning, from the sensory data
    #------------------------------------
    S_tm1 = S_t
    
    
    S_t = buildStateFromSensors(laserRanges,radar, dist2goal)

    #------------------------------------
    if(initLearning):
        strategyGating('randomPersist',verbose=False)
        initLearning=False
    else:
        strategyGating(method,verbose=False)
        
    if choice==0:
      v = wallFollower(laserRanges,verbose=False)
    else:
      v = radarGuidance(laserRanges,bumperL,bumperR,radar,verbose=False)
    if( time.time()-tL <1 ):
      tL=time.time() 
      posT[trial].append([int(pos.x()),int(pos.y())])

    i+=1
    j+=1
    
    robot.move(v[0], v[1], env_map)
    time.sleep(0.01)
   
	

  # When the experiment is over:
  np.savetxt('log/'+str(startT)+'-TrialDurations-'+method+'.txt',trialDuration)
  dictlist=[]
  for key, value in Q.items():
    temp = [key,value]
    dictlist.append(temp)

  	
  #save the Qvalues of the last trial
  #save the Qvalues of the last trial
  f = open('log/'+str(startT) +'_Qlearning_values3.txt',"w")
  f.write( str(dictlist) )
  f.close()
  f = open('log/'+str(startT)+'-TrialDurations-Robotpos3.txt',"w")
  f.write( str(posT) )
  f.close()
  
  

#--------------------------------------

if __name__ == '__main__':
  random.seed()
  main()
