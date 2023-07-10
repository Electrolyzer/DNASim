from BasicGates import *
from DualRailGates import *
from Black_Boxes import *
import Black_Boxes


def build_black_box(name, gates, inputBuckets, middleBuckets, outputBuckets):
    # Inputs/outputs of the black box should be in the form inputs[n]/outputs[n]
    # in the gates,other buckets can have any names. When using created types
    # pass in inputs and outputs as lists/arrays.

    if hasattr(Black_Boxes, name):
        print("An object with this name already exists. Please use a different name.")
        return

    boxes = open("Black_Boxes.py", "a")
    boxes.write("\nclass " + name + "(BlackBox):")
    boxes.write("""
    def __init__(self, name, inputs, outputs) -> None:
        super("""+name+""", self).__init__(name, inputs, outputs)
        
        for bucket in inputs:
            self.buckets_list.append(bucket)
        for bucket in outputs:
            self.buckets_list.append(bucket)\n""")
    for bucket in middleBuckets:
        boxes.write("        " + bucket.name + " = " + bucket.tostring() + "\n")
        boxes.write("        self.buckets_list.append(" + bucket.name + ")\n")

    for gate in gates:
        gate_str = gate.tostring()
        boxes.write("        self.gates_list.append(" + gate_str + ")\n")


if __name__ == '__main__':

    inputs = [DnaBucket('inputs[0]', Amounts.ON),
              DnaBucket('inputs[1]', Amounts.OFF),
              DnaBucket('inputs[2]', Amounts.ON)]

    outputs = [DnaBucket('outputs[0]', Amounts.EMPTY)]

    middles = [DnaBucket('mid', Amounts.EMPTY)]

    or_gate = Or2Gate('or_gate', [inputs[0], inputs[1]], middles[0])
    and_gate = And2Gate('and_gate', [inputs[2], middles[0]], outputs[0])
    build_black_box('BlackOrAnd', [and_gate, or_gate], inputs, middles, outputs)


