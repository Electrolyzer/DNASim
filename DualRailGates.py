from Gates import *
from DualBucket import *


class TwoInputsAndOrBasedDRGate(Gate):
    def get_buckets_as_list(self) -> list:
        bl = []
        bl.extend(self.and_2_gate.get_buckets_as_list())
        bl.extend(self.or_2_gate.get_buckets_as_list())
        return list(set(bl))

    def get_seesaws_as_list(self) -> list:
        sl = []
        sl.extend(self.and_2_gate.get_seesaws_as_list())
        sl.extend(self.or_2_gate.get_seesaws_as_list())
        return list(set(sl))
        

class Or2DRGate(TwoInputsAndOrBasedDRGate):
    def __init__(self, name, inputs, output) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = output
        self.or_2_gate = Or2Gate(name + "_or", [inp.val_bucket for inp in inputs], [out.val_bucket for out in output])
        self.and_2_gate = And2Gate(name + "_and", [inp.inv_bucket for inp in inputs], [out.inv_bucket for out in output])
        

class And2DRGate(TwoInputsAndOrBasedDRGate):
    def __init__(self, name, inputs, output) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = output
        self.and_2_gate = And2Gate(name + "_and", [inp.val_bucket for inp in inputs], [out.val_bucket for out in output])
        self.or_2_gate = Or2Gate(name + "_or", [inp.inv_bucket for inp in inputs], [out.inv_bucket for out in output])


class Nand2DRGate(TwoInputsAndOrBasedDRGate):
    def __init__(self, name, inputs, output) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = output
        self.and_2_gate = And2Gate(name + "_and", [inp.val_bucket for inp in inputs], [out.inv_bucket for out in output])
        self.or_2_gate = Or2Gate(name + "_or", [inp.inv_bucket for inp in inputs], [out.val_bucket for out in output])


class ThresholdDRGate1Out(Gate):
    def __init__(self, name, inputs_list, weight_list, output, threshold) -> None:
        self.name = name
        inputs_val_list = [bucket.val_bucket for bucket in inputs_list]
        inputs_inv_list = [bucket.inv_bucket for bucket in inputs_list]

        weight_plus_list = []
        weight_minus_list = []
        for weight in weight_list:
            if weight >= 0:
                weight_plus_list.append(weight)
                weight_minus_list.append(0)
            else:
                weight_plus_list.append(0)
                weight_minus_list.append(-weight)
        new_weight_list = []
        new_weight_list.extend(weight_plus_list)
        new_weight_list.extend(weight_minus_list)

        val_gate_inputs = []
        val_gate_inputs.extend(inputs_val_list)
        val_gate_inputs.extend(inputs_inv_list)

        val_threshold = sum(weight_minus_list) + threshold
        self.val_threshold_gate = GeneralLinearThresholdGate(name + "_val", val_gate_inputs, new_weight_list,
                                                             [output.val_bucket], [val_threshold])

        inv_gate_inputs = []
        inv_gate_inputs.extend(inputs_inv_list)
        inv_gate_inputs.extend(inputs_val_list)

        epsilon = 0.3
        inv_threshold = sum(weight_plus_list) - threshold + epsilon
        self.inv_threshold_gate = GeneralLinearThresholdGate(name + "_inv", inv_gate_inputs, new_weight_list,
                                                             [output.inv_bucket], [inv_threshold])

    def get_buckets_as_list(self) -> list:
        bl = []
        bl.extend(self.val_threshold_gate.get_buckets_as_list())
        bl.extend(self.inv_threshold_gate.get_buckets_as_list())
        return list(set(bl))

    def get_seesaws_as_list(self) -> list:
        sl = []
        sl.extend(self.val_threshold_gate.get_seesaws_as_list())
        sl.extend(self.inv_threshold_gate.get_seesaws_as_list())
        return list(set(sl))


class MultiplyingDRSeesaw(Seesaw):
    def __init__(self, name, inp, outputs_list, weight_list) -> None:
        self.name = name
        val_output_buckets = [b.val_bucket for b in outputs_list]
        inv_output_buckets = [b.inv_bucket for b in outputs_list]
        self.__multiplying_val_seesaw = MultiplyingSeesaw(name+"_val", inp.val_bucket, val_output_buckets, weight_list)
        self.__multiplying_inv_seesaw = MultiplyingSeesaw(name+"_inv", inp.inv_bucket, inv_output_buckets, weight_list)

    def get_buckets_as_list(self) -> list:
        lst = []
        lst.extend(self.__multiplying_val_seesaw.get_buckets_as_list())
        lst.extend(self.__multiplying_inv_seesaw.get_buckets_as_list())
        return lst

    def calculate_transfer_amounts(self, ks, kf) -> None:
        self.__multiplying_val_seesaw.calculate_transfer_amounts(ks, kf)
        self.__multiplying_inv_seesaw.calculate_transfer_amounts(ks, kf)
