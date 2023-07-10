from Gates import *
from DualRailGates import *


class BlackBox(Gate):
    def __init__(self, name, inputs, outputs) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.gates_list = []
        self.buckets_list = []
        self.seesaws_list = []

    def get_buckets_as_list(self) -> list:
        return self.buckets_list

    def get_seesaws_as_list(self) -> list:
        return self.seesaws_list

    def calculate_transfer_amounts(self, ks, kf) -> None:
        for g in self.gates_list:
            g.calculate_transfer_amounts(ks, kf)

    def update_amounts(self) -> None:
        for g in self.gates_list:
            g.update_amounts()


class BlackAndOr(BlackBox):
    def __init__(self, name, inputs, outputs) -> None:
        super(BlackAndOr, self).__init__(name, inputs, outputs)

        for bucket in inputs:
            self.buckets_list.append(bucket)
        for bucket in outputs:
            self.buckets_list.append(bucket)
        mid = DnaBucket("mid", Amounts.EMPTY)
        self.buckets_list.append(mid)

        self.gates_list.append(And2Gate("and_1", [inputs[0], inputs[1]], mid))
        self.gates_list.append(Or2Gate("or_1", [mid, inputs[2]], outputs[0]))


class DoubleBlack(BlackBox):
    def __init__(self, name, inputs, outputs) -> None:
        super(DoubleBlack, self).__init__(name, inputs, outputs)

        for bucket in inputs:
            self.buckets_list.append(bucket)
        for bucket in outputs:
            self.buckets_list.append(bucket)
        middles0 = DnaBucket("middles0", 0)
        self.buckets_list.append(middles0)
        middles1 = DnaBucket("middles1", 0)
        self.buckets_list.append(middles1)
        self.gates_list.append(BlackAndOr("andor", [middles0, inputs[3], inputs[4]], [middles1]))
        self.gates_list.append(BlackOrAnd("orand", [inputs[0], inputs[1], inputs[2]], [middles0]))
        self.gates_list.append(ReporterSeesaw("reporter", middles1, outputs[0]))


class testnand(BlackBox):
    def __init__(self, name, inputs, outputs) -> None:
        super(testnand, self).__init__(name, inputs, outputs)

        for bucket in inputs:
            self.buckets_list.append(bucket)
        for bucket in outputs:
            self.buckets_list.append(bucket)
        middles0 = DualBucket("middles0", 0)
        self.buckets_list.append(middles0)
        self.gates_list.append(Nand2DRGate("nand", [inputs[0], inputs[1]], [middles0]))
        self.gates_list.append(Or2DRGate("or2DR", [inputs[2], middles0], [outputs[0]]))


class BlackOrAnd(BlackBox):
    def __init__(self, name, inputs, outputs) -> None:
        super(BlackOrAnd, self).__init__(name, inputs, outputs)
        
        for bucket in inputs:
            self.buckets_list.append(bucket)
        for bucket in outputs:
            self.buckets_list.append(bucket)
        mid = DnaBucket("mid", 0)
        self.buckets_list.append(mid)
        self.gates_list.append(And2Gate("and_gate", [inputs[2], mid], outputs[0]))
        self.gates_list.append(Or2Gate("or_gate", [inputs[0], inputs[1]], mid))
