from BasicGates import *


class And2Gate(Gate):
    def __init__(self, name, inputs, outputs) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.__prime_gate = PrimeGate(name, inputs, outputs, 2, 1.33)

    def get_buckets_as_list(self) -> list:
        return self.__prime_gate.get_buckets_as_list()

    def get_seesaws_as_list(self) -> list:
        return self.__prime_gate.get_seesaws_as_list()


class Or2Gate(Gate):
    def __init__(self, name, inputs, outputs) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.__prime_gate = PrimeGate(name, inputs, outputs, 2, 0.66)

    def get_buckets_as_list(self) -> list:
        return self.__prime_gate.get_buckets_as_list()

    def get_seesaws_as_list(self) -> list:
        return self.__prime_gate.get_seesaws_as_list()

