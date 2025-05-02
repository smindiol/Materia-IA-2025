# --------------------------
# Estructuras base
# --------------------------
class Node:
    def __init__(self, distribution, name):
        self.name = name
        self.distribution = distribution
        self.parents = []
        self.children = []
    def set_parents(self, parents):
        self.parents = parents
        for p in parents:
            p.children.append(self)

class DiscreteDistribution:
    def __init__(self, probabilities):
        self.probabilities = probabilities
    def probability(self, value):
        return self.probabilities[value]

class ConditionalProbabilityTable:
    def __init__(self, table, parents):
        self.table = table
        self.parents = parents  # lista de nodos
        self.data = {}
        for row in table:
            *parent_vals, value, prob = row
            key = tuple(parent_vals)
            if key not in self.data:
                self.data[key] = {}
            self.data[key][value] = prob
    def probability(self, value, parent_values):
        key = tuple(parent_values)
        if key not in self.data or value not in self.data[key]:
            raise KeyError(f"Clave no encontrada en CPT: padres={key}, valor={value}")
        return self.data[key][value]
# --------------------------
# Red bayesiana
# --------------------------
from itertools import product
class BayesianNetwork:
    def __init__(self):
        self.nodes = []
        self.name_to_node = {}

    def add_state(self, *nodes):
        for node in nodes:
            self.nodes.append(node)
            self.name_to_node[node.name] = node

    def add_edges(self, *edges):
        for i in range(0, len(edges), 2):
            parent, child = edges[i], edges[i+1]
            self.name_to_node[child.name].set_parents(
                self.name_to_node[child.name].parents + [self.name_to_node[parent.name]]
            )

    def bake(self):
        pass

    def predict_proba(self, evidence):
        domains = {}

        for node in self.nodes:
            if isinstance(node.distribution, DiscreteDistribution):
                domains[node.name] = list(node.distribution.probabilities.keys())
            else:
                sample_key = next(iter(node.distribution.data))
                domains[node.name] = list(node.distribution.data[sample_key].keys())

        results = []
        total = 0
        probs = {}

        for values in product(*[domains[n.name] for n in self.nodes]):
            assignment = dict(zip([n.name for n in self.nodes], values))
            if not all(assignment.get(k) == v for k, v in evidence.items()):
                continue

            p = 1.0
            for node in self.nodes:
                val = assignment[node.name]
                if isinstance(node.distribution, DiscreteDistribution):
                    p *= node.distribution.probability(val)
                else:
                    parent_vals = [assignment[p.name] for p in node.parents]
                    p *= node.distribution.probability(val, parent_vals)
            probs[tuple(assignment[n.name] for n in self.nodes)] = p
            total += p

        for node in self.nodes:
            if node.name in evidence:
                results.append(evidence[node.name])
            else:
                dist = {}
                for k, p in probs.items():
                    val = k[[n.name for n in self.nodes].index(node.name)]
                    dist[val] = dist.get(val, 0) + p
                for val in dist:
                    dist[val] /= total
                results.append(DiscreteDistribution(dist))

        return results

    def probability(self, observation):
        p = 1.0
        for node, value in zip(self.nodes, observation):
            if isinstance(node.distribution, DiscreteDistribution):
                p *= node.distribution.probability(value)
            else:
                parent_vals = [
                    observation[self.nodes.index(p)] for p in node.parents
                ]
                p *= node.distribution.probability(value, parent_vals)
        return p
