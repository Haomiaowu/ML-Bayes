# 时间:2020/12/22  20:57
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
Chemoinformatics_model = BayesianModel([("D", "G"), ("I", "G"),("G", "L"),("I", "S")])

amino_cpd = TabularCPD(
            variable="D",
            variable_card=2,
            values=[[0.6], [0.4]]
)
benzene_cpd = TabularCPD(
            variable="I",
            variable_card=2,
            values=[[0.7], [0.3]]
)
active_cpd = TabularCPD(
    variable="G", # 节点名称
    variable_card=3, # 节点取值个数
    values=[[0.3, 0.05, 0.9, 0.5], # 该节点的概率表
    [0.4, 0.25, 0.08, 0.3],
    [0.3, 0.7, 0.02, 0.2]],
    evidence=["I", "D"], # 该节点的依赖节点
    evidence_card=[2, 2] # 依赖节点的取值个数
)
drug_cpd = TabularCPD(
            variable="L",
            variable_card=2,
            values=[[0.1, 0.4, 0.99],
            [0.9, 0.6, 0.01]],
            evidence=["G"],
            evidence_card=[3]
)
toxicity_cpd = TabularCPD(
            variable="S",
            variable_card=2,
            values=[[0.95, 0.2],
            [0.05, 0.8]],
            evidence=["I"],
            evidence_card=[2]
)

Chemoinformatics_model.add_cpds(
    active_cpd,
    amino_cpd,
    benzene_cpd,
    drug_cpd,
    toxicity_cpd
)

Chemoinformatics_model.get_cpds()

Chemoinformatics_infer = VariableElimination(Chemoinformatics_model)
prob = Chemoinformatics_infer.query(
            variables=["L"],
            evidence={"D": 1,"I":1,"G":0})
print(prob)