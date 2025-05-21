from modelo import model
from pomegranate import *

# Inferencia: Jorge y María llaman
evidencia = {'Jorge': 'Jorge llama', 'Maria': 'Maria llama'}
resultado = model.predict_proba(evidencia)

nombres_nodos = [state.name for state in model.states]
for nombre, distribucion in zip(nombres_nodos, resultado):
    if isinstance(distribucion, DiscreteDistribution):
        print(f"\n{nombre}:")
        for valor, prob in distribucion.items():
            print(f"  {valor}: {prob:.4f}")
    else:
        print(f"\n{nombre}: {distribucion}")
 