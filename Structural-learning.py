# 时间:2020/12/21  15:38
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
from pgmpy.models import BayesianModel
from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import BicScore

data=pd.read_csv(r'C:\Users\haomiaowu\Desktop\BN-Cheminformatics\Train-clear.csv')
bic = BicScore(data)

hs = HillClimbSearch(data, scoring_method=BicScore(data))
best_model = hs.estimate()
print(best_model.edges())

nx.draw(best_model,
        with_labels=True,
        node_size=1000,
        font_weight='bold',
        node_color='y',
        )

plt.show()


