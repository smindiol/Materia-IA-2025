from pomegranate import Node, DiscreteDistribution, ConditionalProbabilityTable, BayesianNetwork

# 1. Nodos independientes
robo = Node(DiscreteDistribution({
    'Robo': 0.001,
    'No Robo': 0.999
}), name="Robo")

temblor = Node(DiscreteDistribution({
    'Temblor': 0.001,
    'No Temblor': 0.999
}), name="Temblor")
 
# 2. Nodo Alarma condicionado a Robo y Temblor
alarma = Node(ConditionalProbabilityTable([
    ['Robo', 'Temblor', 'Alarma', 0.95],
    ['Robo', 'Temblor', 'No Alarma', 0.05],
    ['Robo', 'No Temblor', 'Alarma', 0.94],
    ['Robo', 'No Temblor', 'No Alarma', 0.06],
    ['No Robo', 'Temblor', 'Alarma', 0.29], 
    ['No Robo', 'Temblor', 'No Alarma', 0.71],
    ['No Robo', 'No Temblor', 'Alarma', 0.001],
    ['No Robo', 'No Temblor', 'No Alarma', 0.999],
], [robo.distribution, temblor.distribution]), name="Alarma")

# 3. Nodos Jorge y María condicionados a Alarma
jorge = Node(ConditionalProbabilityTable([
    ['Alarma', 'Jorge llama', 0.9],
    ['Alarma', 'Jorge no llama', 0.1],
    ['No Alarma', 'Jorge llama', 0.05],
    ['No Alarma', 'Jorge no llama', 0.95],
], [alarma.distribution]), name="Jorge")

maria = Node(ConditionalProbabilityTable([
    ['Alarma', 'Maria llama', 0.7],
    ['Alarma', 'Maria no llama', 0.3],
    ['No Alarma', 'Maria llama', 0.01],
    ['No Alarma', 'Maria no llama', 0.99],
], [alarma.distribution]), name="Maria")

model = BayesianNetwork("Sistema de alarma de Carlos")
model.add_states(robo, temblor, alarma, jorge, maria)

model.add_edge(robo, alarma)
model.add_edge(temblor, alarma)
model.add_edge(alarma, jorge)
model.add_edge(alarma, maria)

model.bake()

print("El modelo se ha creado y cargado correctamente.")
