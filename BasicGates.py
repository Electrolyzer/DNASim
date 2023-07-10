from SeesawGates import *


class Gate:
    def calculate_transfer_amounts(self, ks, kf) -> None:
        for s in self.get_seesaws_as_list():
            s.calculate_transfer_amounts(ks, kf)

    def update_amounts(self) -> None:
        for s in self.get_seesaws_as_list():
            s.update_amounts()

    def print_gate(self) -> None:
        print(self.name)
        for s in self.get_seesaws_as_list():
            s.print_gate()

    def tostring(self) -> str:
        string = self.__class__.__name__
        string += "(\"" + self.name + "\", ["
        first = True
        for inp in self.inputs:
            if first:
                first = False
            else:
                string += ", "
            string += inp.name
        string += "], "
        if hasattr(self.outputs, '__iter__'):
            first = True
            string += "["
            for out in self.outputs:
                if first:
                    first = False
                else:
                    string += ", "
                string += out.name
            string += "])"
        else:
            string += self.outputs.name + ")"
        return string


class PrimeGate(Gate):
    def __init__(self, name, inputs, output, weight, threshold_amount) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = output
        self.__mid = DnaBucket(name + "_mid", Amounts.EMPTY)
        self.__integrating_seesaw = IntegratingSeesaw(name, inputs, self.__mid, weight)
        self.__thresholdingSeesaw = ThresholdingSeesaw(name, self.__mid, threshold_amount * Amounts.N, output)

    def get_buckets_as_list(self) -> list:
        bl = []
        bl.extend(self.__integrating_seesaw.get_buckets_as_list())
        bl.extend(self.__thresholdingSeesaw.get_buckets_as_list())
        return list(set(bl))

    def get_seesaws_as_list(self) -> list:
        return [self.__integrating_seesaw, self.__thresholdingSeesaw]


class GeneralLinearThresholdGate(Gate):
    def __init__(self, name, inputs_list, weight_list, outputs_list, thresholds_list) -> None:
        self.name = name
        self.__middles = []
        for inp in inputs_list:
            self.__middles.append([DnaBucket(name + "_strand_" + inp.name + "_to_" + output.name, Amounts.EMPTY)
                                   for output in outputs_list])

        self.__multiplying_seesaws = []
        for i, inp in enumerate(inputs_list):
            weight_list_for_seesaw = [weight_list[i] for _ in range(len(outputs_list))]
            m_name = name + "_multiplying_seesaw_for_" + inp.name
            self.__multiplying_seesaws.append(MultiplyingSeesaw(m_name, inp, self.__middles[i], weight_list_for_seesaw))

        weights_sum = sum(weight_list)
        self.__prime_gates = []
        for i, output in enumerate(outputs_list):
            p_name = name + "_prime_gate_for_" + output.name
            inputs_list_for_gate = [row[i] for row in self.__middles]
            self.__prime_gates.append(PrimeGate(p_name, inputs_list_for_gate, output, weights_sum, thresholds_list[i]))

    def get_seesaws_as_list(self) -> list:
        sl = []
        sl.extend(self.__multiplying_seesaws)
        for gate in self.__prime_gates:
            sl.extend(gate.get_seesaws_as_list())
        return list(set(sl))

    def get_buckets_as_list(self) -> list:
        bl = []
        for gate in self.__prime_gates:
            bl.extend(gate.get_buckets_as_list())
        for seesaw in self.__multiplying_seesaws:
            bl.extend(seesaw.get_buckets_as_list())
        return list(set(bl))
