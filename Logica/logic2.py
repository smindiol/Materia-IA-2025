from abc import ABC, abstractmethod
from itertools import product
class EvaluationException(Exception):
    pass
class Sentence(ABC):
    @abstractmethod
    def evaluate(self, model):
        pass
    @abstractmethod
    def formula(self):
        pass
    @abstractmethod
    def symbols(self):
        pass
    @staticmethod
    def validate(sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("El argumento debe ser una instancia de Sentence")
    @staticmethod
    def parenthesize(s):
        def balanced(s):
            count = 0
            for c in s:
                if c == "(": count += 1
                elif c == ")":
                    if count <= 0: return False
                    count -= 1
            return count == 0
        if not s or s.isalpha() or (s.startswith("(") and s.endswith(")") and balanced(s[1:-1])):
            return s
        return f"({s})"

class Symbol(Sentence):
    def __init__(self, name):
        self.name = name
    def evaluate(self, model):
        if self.name in model:
            return model[self.name]
        raise EvaluationException(f"Variable '{self.name}' no definida en el modelo")
    def formula(self):
        return self.name
    def symbols(self):
        return {self.name}
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

class UnarySentence(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

class Not(UnarySentence):
    def evaluate(self, model):
        return not self.operand.evaluate(model)
    def formula(self):
        return f"¬{Sentence.parenthesize(self.operand.formula())}"
    def symbols(self):
        return self.operand.symbols()

class MultiSentence(Sentence):
    def __init__(self, *operands):
        for operand in operands:
            Sentence.validate(operand)
        self.operands = operands

class And(MultiSentence):
    def evaluate(self, model):
        return all(op.evaluate(model) for op in self.operands)
    def formula(self):
        return " ∧ ".join(Sentence.parenthesize(op.formula()) for op in self.operands)
    def symbols(self):
        return set().union(*(op.symbols() for op in self.operands))
    def add(self, operand):
        Sentence.validate(operand)
        self.operands += (operand,)

class Or(MultiSentence):
    def evaluate(self, model):
        return any(op.evaluate(model) for op in self.operands)
    def formula(self):
        return " ∨ ".join(Sentence.parenthesize(op.formula()) for op in self.operands)
    def symbols(self):
        return set().union(*(op.symbols() for op in self.operands))

class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent
    def evaluate(self, model):
        return not self.antecedent.evaluate(model) or self.consequent.evaluate(model)
    def formula(self):
        return f"{Sentence.parenthesize(self.antecedent.formula())} => {Sentence.parenthesize(self.consequent.formula())}"
    def symbols(self):
        return self.antecedent.symbols().union(self.consequent.symbols())

class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right
    def evaluate(self, model):
        return self.left.evaluate(model) == self.right.evaluate(model)
    def formula(self):
        return f"{Sentence.parenthesize(self.left.formula())} <=> {Sentence.parenthesize(self.right.formula())}"
    def symbols(self):
        return self.left.symbols().union(self.right.symbols())

def model_check(knowledge, query):
    symbols = list(knowledge.symbols() | query.symbols())
    for values in product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        if knowledge.evaluate(model):
            if not query.evaluate(model):
                return False
    return True
