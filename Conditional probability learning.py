# 时间:2020/12/21  17:05
import csv
import warnings
import pandas as pd
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination

warnings.filterwarnings("ignore")

data=pd.read_csv(r'C:\Users\haomiaowu\Desktop\BN-Cheminformatics\Train-Clear.csv')
model = BayesianModel([('MW', 'Class'), ('HBD', 'MW'), ('HeavyAtomCount', 'Polar'),
                       ('ChiralCenterCount', 'ChiralCenterCountAllPossible'), ('ChiralCenterCount', 'MR'),
                       ('ChiralCenterCountAllPossible', 'HeavyAtomCount'), ('ChiralCenterCountAllPossible', 'Class'),
                       ('ChiralCenterCountAllPossible', 'HBD'), ('MR', 'HBD'), ('Polar', 'MR')])
model.fit(data, estimator=MaximumLikelihoodEstimator)

# 打印条件概率分布
doc=open('out.txt','w+')
for cpd in model.get_cpds():
    print("CPD of {variable}:".format(variable=cpd.variable),file=doc)
    print(cpd,file=doc)
doc.close()

#读取测试集属性数据，并存储class预测结果
a=[]
model_infer = VariableElimination(model)
with open(r'C:\Users\haomiaowu\Desktop\BN-Cheminformatics\test.csv','r',encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    fieldnames = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
    csv_reader = csv.DictReader(f,fieldnames=fieldnames)  # self._fieldnames = fieldnames # list of keys for the dict 以list的形式存放键名
    for row in csv_reader:
        d = {}
        for k, v in row.items():
            d[k] = int(v)
        prob_class = model_infer.map_query(variables=["Class"],evidence=d)
        a.append(list(prob_class.values())[0])

print('预测结果：')
print(a)
print('--------------------------------------------------------------------------------------------------')
print('已预测化合物个数：',len(a))

#导入测试集正确分类结果
d=pd.read_csv(r'C:\Users\haomiaowu\Desktop\BN-Cheminformatics\test-class.csv')
b=d['Class'].values
print('测试集包含化合物个数：',len(b))

#进行正确率比较
c=np.absolute(np.array(a) - np.array(b))
print('预测错误个数：',sum(c))
d=(len(a)-sum(c))/len(a)
print('正确率',d)









