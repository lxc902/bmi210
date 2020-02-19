import numpy as np
from numpy import genfromtxt
import plotly.express as px
import pandas as pd

accuracies = genfromtxt('accuracies1.csv', delimiter=',')

df = pd.DataFrame(accuracies, columns = ['Start','End','Accuracy'])

fig = px.scatter_3d(df, x='Start', y='End', z='Accuracy',
              color='Accuracy')
fig.show()
