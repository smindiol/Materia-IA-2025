Aquí tienes un ejemplo de README en español, con toda la información solicitada:

---

# Ejercicios de Iteración de Políticas y Value Iteration en un Entorno tipo FrozenLake

## Descripción

Este código implementa y compara dos algoritmos clásicos de resolución de problemas de decisión de Markov (MDP): **Policy Iteration** y **Value Iteration**. Se utiliza un entorno personalizado similar a FrozenLake, donde un agente debe navegar por una cuadrícula con diferentes tipos de casillas (normales, resbaladizas, alfombra y meta).

## Definición del Entorno

El entorno principal se define en la clase `VacuumGridEnv`, que hereda de `gym.Env`.  
- El entorno es una cuadrícula donde cada celda puede ser normal, resbaladiza (`S`, `F`), alfombra (`H`) o meta (`G`).
- La matriz de transiciones `P` se construye considerando las probabilidades de moverse o quedarse en el mismo lugar, dependiendo del tipo de casilla.
- El espacio de observación y acción es discreto.
- El método `step` utiliza la matriz `P` para determinar la transición y la recompensa, siguiendo la convención de Gymnasium.

## Algoritmos de Resolución

### Policy Iteration
- Alterna entre dos pasos: **evaluación de la política** (calcula el valor esperado de cada estado bajo la política actual) y **mejoramiento de la política** (elige la mejor acción en cada estado según los valores calculados).
- Repite hasta que la política converge (no cambia más).

### Value Iteration
- Actualiza directamente la función de valor de cada estado usando la ecuación de Bellman óptima.
- Al finalizar, extrae la política óptima eligiendo la mejor acción en cada estado según la función de valor final.

#### Diferencias principales
- **Policy Iteration** mantiene y mejora una política explícita en cada iteración.
- **Value Iteration** solo actualiza valores y extrae la política al final.
- Ambos encuentran la política óptima, pero su enfoque es diferente.

## Resultados y Respuestas a Preguntas

### Policy Iteration

**¿Por qué el agente puede obtener un puntaje de 0.0?**  
RTA:  
Porque existen dos estados terminales: los huecos y el objetivo. Si el agente cae en un hueco antes de llegar a la meta, termina el episodio sin recompensa.

**¿Qué pasa si se inicializa la política con ceros?**  
RTA:  
La política inicial afecta la convergencia y los valores esperados. Si se inicializa con ceros, los valores de los estados pueden ser menores y la política final puede cambiar, especialmente en los estados cercanos a la izquierda, debido a movimientos inválidos o subóptimos al inicio.

**¿Qué ocurre si el entorno no es resbaloso (`is_slippery=False`)?**  
RTA:  
La política óptima cambia, ya que el entorno se vuelve determinista. El agente puede ir directo a la meta sin riesgo de resbalar, por lo que la política es más directa y los valores de los estados aumentan.

### Comparaciones y Observaciones

- **Al aumentar el descuento (`gamma`)**, los valores de los estados aumentan y la política preferida puede variar ligeramente, pero la ruta óptima suele ser la misma.
- **La probabilidad de resbalar** afecta la convergencia: si hay más probabilidad de resbalar, el agente puede tardar más en encontrar la política óptima, ya que puede quedarse más tiempo en los mismos estados.
- **Alfombras con alta probabilidad de resbalar:** El agente intenta evitar esas zonas si es posible, pero si la ruta óptima pasa por ellas, no siempre puede evitarlas completamente.
- **Estrategia de recarga:** El agente prefiere rutas sin alfombras para minimizar penalizaciones.

### Value Iteration

- Para un entorno resbaloso con γ=0.9, los resultados (función de valor y política óptima) son iguales a los obtenidos con Policy Iteration.
- Al bajar γ=0.5, también se obtienen los mismos valores y políticas óptimas.
- En entornos más grandes (por ejemplo, 3x3), los resultados de ambos algoritmos siguen coincidiendo.

---

## Uso

1. Define el entorno con la clase `VacuumGridEnv`.
2. Ejecuta los algoritmos `policy_iteration` y `value_iteration` sobre el entorno.
3. Visualiza los resultados con las funciones `values_print` y `actions_print`.

---


