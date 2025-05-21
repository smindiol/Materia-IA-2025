from modelo import modelo

# Calculemos la probabilidad para una observacion dada
probabilidad = modelo.probability([["ninguna", "no", "a tiempo", "atendida"]])

print(probabilidad)

# Calcular la probabildiad para 3 diferentes observaciones
observaciones = [
    ["ninguna", "no", "a tiempo", "atendida"],
    ["suave", "si", "retrasada", "no atendida"],
    ["fuerte", "si", "a tiempo", "atendida"]
]

for i in observaciones:
    probabilidad = modelo.probability([i])
    print(f"Probabilidad para la observacion {i}: {probabilidad:.6f}")