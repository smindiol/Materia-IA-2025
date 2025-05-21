from pomegranate import Node, BayesianNetwork, DiscreteDistribution, ConditionalProbabilityTable

# Nodo Lluvia
lluvia = Node(DiscreteDistribution({
    "ninguna": 0.7,
    "suave": 0.2,
    "fuerte": 0.1
}), name="lluvia")

# Nodo Mantenimiento
mantenimiento = Node(ConditionalProbabilityTable([
    ["ninguna", "si", 0.4],
    ["ninguna", "no", 0.6],
    ["suave", "si", 0.2],
    ["suave", "no", 0.8],
    ["fuerte", "si", 0.1],
    ["fuerte", "no", 0.9],
], [lluvia.distribution]), name="mantenimiento")

# Nodo Bus
bus = Node(ConditionalProbabilityTable([
    ["ninguna", "si", "a tiempo", 0.8],
    ["ninguna", "si", "retrasada", 0.2],
    ["ninguna", "no", "a tiempo", 0.9],
    ["ninguna", "no", "retrasada", 0.1],
    ["suave", "si", "a tiempo", 0.6],
    ["suave", "si", "retrasada", 0.4],
    ["suave", "no", "a tiempo", 0.7],
    ["suave", "no", "retrasada", 0.3],
    ["fuerte", "si", "a tiempo", 0.4],
    ["fuerte", "si", "retrasada", 0.6],
    ["fuerte", "no", "a tiempo", 0.5],
    ["fuerte", "no", "retrasada", 0.5],
], [lluvia.distribution, mantenimiento.distribution]), name="bus")

# Nodo Cita
cita = Node(ConditionalProbabilityTable([
    ["a tiempo", "atendida", 0.9],
    ["a tiempo", "no atendida", 0.1],
    ["retrasada", "atendida", 0.6],
    ["retrasada", "no atendida", 0.4],
], [bus.distribution]), name="cita")

# Crear modelo
modelo = BayesianNetwork("Red de la Cita")
modelo.add_states(lluvia, mantenimiento, bus, cita)
modelo.add_edge(lluvia, mantenimiento)
modelo.add_edge(lluvia, bus)
modelo.add_edge(mantenimiento, bus)
modelo.add_edge(bus, cita)
modelo.bake()
