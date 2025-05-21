from modelo import model  # Asegúrate de importar el modelo correctamente

# Lista de observaciones completas
observaciones = [
    ["Robo", "No Temblor", "Alarma", "Jorge llama", "Maria no llama"],
    ["No Robo", "Temblor", "Alarma", "Jorge no llama", "Maria llama"],
    ["No Robo", "No Temblor", "No Alarma", "Jorge no llama", "Maria no llama"]
]

# Mostrar probabilidades
for obs in observaciones:
    prob = model.probability([obs])
    print(f"Probabilidad para la observación {obs}: {prob:.12f}")
 