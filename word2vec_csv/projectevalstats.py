# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd 


#this just creates some fake data to test on 
df = pd.DataFrame(np.random.randint(0,3,size=(100, 2)), columns=["label", "predicted"])


def evalstats(df): 
    '''
    Input: A pandas dataframe with two columns, one named "label" with the true labels, and one named "predicted" with the predicted labels 
    Output: Prints out all the statistics 
    '''
    cm=np.array(pd.crosstab(df["predicted"], df["label"]))
    print("++++++++++++++++ Accuracy:", round((cm[0,0]+cm[1,1]+cm[2,2])/cm.sum(),3))
    #return

    print("Confusion Matrix:")
    print(pd.crosstab(df["predicted"], df["label"]))
    
    print("**********Stats for 0 label vs 1/2*********")
    Recall=cm[0,0]/cm[:,0].sum()
    print("Sensitivity (aka Recall): ",round(Recall,3))
    print("Specificity: ",round(cm[1:3,1:3].sum()/cm[0:3,1:3].sum(),3))
    Precision=cm[0,0]/cm[0].sum()
    print("PPV (aka Precision): ",round(Precision,3))
    print("NPV: ",round(cm[1:3,1:3].sum()/cm[1:3,0:3].sum(),3))
    print("F1 Score: ",round(2*Precision*Recall/(Precision+Recall),3))


    print("**********Stats for 0/1 label vs 2*********")
    Recall=cm[0:2,0:2].sum()/cm[:,0:2].sum()
    print("Sensitivity (aka Recall): ",round(Recall,3))
    print("Specificity: ",round(cm[2,2]/cm[:,2].sum(),3))
    Precision=cm[0:2,0:2].sum()/cm[0:2,].sum()
    print("PPV (aka Precision): ",round(Precision,3))
    print("NPV: ",round(cm[2,2]/cm[2].sum(),3))
    print("F1 Score: ",round(2*Precision*Recall/(Precision+Recall),3))

    return 

