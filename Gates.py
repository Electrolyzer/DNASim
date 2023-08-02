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


class NotGate(Gate):
    def __init__(self, name, inp, output, delay) -> None:
        self.name = name
        self.inp = inp
        self.output = output

        self.enabler = DnaBucket(name + "_enabler", Amounts.EMPTY)
        self.subtractOutput = DnaBucket(name + "_subtractOutput", Amounts.N)
        self.enableOutput = DnaBucket(name + "_enableOutput", Amounts.EMPTY)

        self.delay_gate = DelayGate(name + "_delay_gate", self.enabler, delay)
        self.subtractionGate = SubtractionGate(name + "_subtractionGate", self.inp, self.subtractOutput)
        self.enableGate = GateEnable(name + "_GateEnable", self.enabler, self.subtractOutput, self.enableOutput)
        self.threshold = ThresholdingSeesaw(name + "_threshold", self.enableOutput, .5*Amounts.N, output)

        self.gates_list = [self.enableGate, self.delay_gate, self.subtractionGate, self.threshold]
        self.bucket_list = [self.inp, self.output, self.enabler, self.subtractOutput, self.enableOutput]

    def get_seesaws_as_list(self) -> list:
        return self.gates_list

    def get_buckets_as_list(self) -> list:
        return self.bucket_list

    def calculate_transfer_amounts(self, ks, kf) -> None:
        for g in self.gates_list:
            g.calculate_transfer_amounts(ks, kf)

    def update_amounts(self) -> None:
        for g in self.gates_list:
            g.update_amounts()
