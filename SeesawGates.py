from DnaBucket import *


class Seesaw:
    def update_amounts(self) -> None:
        for b in self.get_buckets_as_list():
            b.amount += b.dt
            assert b.amount >= 0, b.name + " amount < 0"
            b.dt = 0

    def print_gate(self) -> None:
        print("\t" + self.name)
        for b in self.get_buckets_as_list():
            b.print_bucket()


class ThresholdingSeesaw(Seesaw):
    def __init__(self, name, inp, threshold_amount, output) -> None:
        self.name = name + "_thresholding_seesaw"
        self.__input = inp
        self.__input_gate = DnaBucket(name + "_input_gate", Amounts.EMPTY)
        self.__threshold = DnaBucket(name + "_threshold", threshold_amount)
        self.__fuel = DnaBucket(name + "_fuel", 2*Amounts.N)
        self.__fuel_gate = DnaBucket(name + "_fuel_gate", Amounts.EMPTY)
        self.__output_gate = DnaBucket(name + "_output_gate", 1*Amounts.N)
        self.__output = output

    def get_buckets_as_list(self) -> list:
        return [self.__input, self.__input_gate, self.__threshold,
                self.__fuel, self.__fuel_gate, self.__output_gate, self.__output]

    def calculate_transfer_amounts(self, ks, kf) -> None:
        self.__threshold.dt += - kf * self.__input.amount * self.__threshold.amount

        self.__fuel_gate.dt += ks * self.__input_gate.amount * self.__fuel.amount - \
                               ks * self.__fuel_gate.amount * self.__input.amount

        self.__fuel.dt += ks * self.__fuel_gate.amount * self.__input.amount - \
                          ks * self.__fuel.amount * self.__input_gate.amount

        self.__output_gate.dt += ks * self.__input_gate.amount * self.__output.amount - \
                                 ks * self.__output_gate.amount * self.__input.amount

        self.__output.dt += ks * self.__input.amount * self.__output_gate.amount - \
                            ks * self.__output.amount * self.__input_gate.amount

        self.__input_gate.dt += ks * self.__input.amount * self.__output_gate.amount + \
                                ks * self.__input.amount * self.__fuel_gate.amount - \
                                ks * self.__input_gate.amount * self.__fuel.amount - \
                                ks * self.__input_gate.amount * self.__output.amount

        self.__input.dt += ks * self.__input_gate.amount * self.__fuel.amount - \
                           ks * self.__input.amount * self.__fuel_gate.amount + \
                           ks * self.__input_gate.amount * self.__output.amount - \
                           ks * self.__output_gate.amount * self.__input.amount - \
                           kf * self.__input.amount * self.__threshold.amount


class IntegratingSeesaw(Seesaw):
    def __init__(self, name, inputs_list, output, weight) -> None:
        self.name = name + "_integrating_seesaw"
        self.__inputs_list = inputs_list

        self.__input_gates_list = []
        for i in range(1, len(self.__inputs_list)+1):
            self.__input_gates_list.append(DnaBucket(name + "_input" + str(i) + "_gate", Amounts.EMPTY))

        self.__output_gate = DnaBucket(name + "_output_gate", weight * Amounts.N)
        self.__output = output

    def get_buckets_as_list(self) -> list:
        buckets_list = []
        buckets_list.extend(self.__inputs_list)
        buckets_list.extend(self.__input_gates_list)
        buckets_list.extend([self.__output_gate, self.__output])
        return buckets_list

    def calculate_transfer_amounts(self, ks, kf) -> None:
        for i, inp in enumerate(self.__inputs_list):
            inp.dt += ks * self.__input_gates_list[i].amount * self.__output.amount - \
                      ks * inp.amount * self.__output_gate.amount

            self.__input_gates_list[i].dt += ks * inp.amount * self.__output_gate.amount - \
                                             ks * self.__input_gates_list[i].amount * self.__output.amount

        input_gates_sum = sum(input_gate.amount for input_gate in self.__input_gates_list)
        inputs_sum = sum(inp.amount for inp in self.__inputs_list)

        self.__output_gate.dt += ks * input_gates_sum * self.__output.amount - \
                                 ks * inputs_sum * self.__output_gate.amount

        self.__output.dt += ks * inputs_sum * self.__output_gate.amount - \
                            ks * input_gates_sum * self.__output.amount


class AmplifyingSeesaw(Seesaw):
    def __init__(self, name, inp, outputs_list, weight_list, threshold_amount) -> None:
        self.name = name + "_amplifying_seesaw"
        self.__input = inp
        self.__input_gate = DnaBucket(name + "_input_gate", Amounts.EMPTY)

        self.__outputs_list = outputs_list

        self.__output_gates_list = []
        for i in range(1, len(self.__outputs_list)+1):
            self.__output_gates_list.append(DnaBucket(name + "_output"+str(i)+"_gate", weight_list[i-1] * Amounts.N))

        self.__threshold = DnaBucket(name + "_threshold", threshold_amount * Amounts.N)

        weight_sum = sum(weight_list)
        self.__fuel = DnaBucket(name + "_fuel", 2 * weight_sum * Amounts.N)
        self.__fuel_gate = DnaBucket(name + "_fuel_gate", Amounts.EMPTY)

    def get_buckets_as_list(self) -> list:
        buckets_list = [self.__input, self.__input_gate]
        buckets_list.extend(self.__outputs_list)
        buckets_list.extend(self.__output_gates_list)
        buckets_list.extend([self.__threshold, self.__fuel, self.__fuel_gate])
        return buckets_list

    def calculate_transfer_amounts(self, ks, kf) -> None:
        output_gates_sum = sum(output_gate.amount for output_gate in self.__output_gates_list)
        outputs_sum = sum(output.amount for output in self.__outputs_list)

        self.__input.dt += ks * self.__input_gate.amount * outputs_sum + \
                           ks * self.__input_gate.amount * self.__fuel.amount - \
                           ks * self.__input.amount * output_gates_sum - \
                           ks * self.__fuel_gate.amount * self.__input.amount - \
                           kf * self.__input.amount * self.__threshold.amount

        self.__input_gate.dt += ks * self.__input.amount * output_gates_sum + \
                                ks * self.__input.amount * self.__fuel_gate.amount - \
                                ks * self.__input_gate.amount * outputs_sum - \
                                ks * self.__input_gate.amount * self.__fuel.amount

        for i, output in enumerate(self.__outputs_list):
            output.dt += ks * self.__input.amount * self.__output_gates_list[i].amount - \
                      ks * self.__input_gate.amount * output.amount

            self.__output_gates_list[i].dt += ks * self.__input_gate.amount * output.amount - \
                                           ks * self.__input.amount * self.__output_gates_list[i].amount

        self.__fuel.dt += ks * self.__fuel_gate.amount * self.__input.amount - \
                          ks * self.__fuel.amount * self.__input_gate.amount

        self.__fuel_gate.dt += ks * self.__input_gate.amount * self.__fuel.amount - \
                               ks * self.__fuel_gate.amount * self.__input.amount

        self.__threshold.dt += - kf * self.__input.amount * self.__threshold.amount


class MultiplyingSeesaw(Seesaw):
    def __init__(self, name, inp, outputs_list, weight_list) -> None:
        self.name = name
        self.__amplifying_seesaw = AmplifyingSeesaw(name, inp, outputs_list, weight_list, 0.2)

    def get_buckets_as_list(self) -> list:
        return self.__amplifying_seesaw.get_buckets_as_list()

    def calculate_transfer_amounts(self, ks, kf) -> None:
        self.__amplifying_seesaw.calculate_transfer_amounts(ks, kf)


class ReporterSeesaw(Seesaw):
    def __init__(self, name, inp, fluor) -> None:
        self.name = name
        self.__input = inp
        self.__reporter_gate = DnaBucket(name + "_reporter_gate", 1.5 * Amounts.ON)
        self.__fluor = fluor

    def get_buckets_as_list(self) -> list:
        return [self.__input, self.__reporter_gate, self.__fluor]

    def calculate_transfer_amounts(self, ks, kf) -> None:
        self.__input.dt += - ks * self.__reporter_gate.amount * self.__input.amount

        self.__reporter_gate.dt += - ks * self.__reporter_gate.amount * self.__input.amount

        self.__fluor.dt += ks * self.__reporter_gate.amount * self.__input.amount

    def tostring(self):
        return "ReporterSeesaw(\"" + self.name + "\", " + \
               self.__input.name + ", " + self.__fluor.name + ")"
