import sys
from Simulator import *
from DualRailGates import *
from Black_Boxes import *
from BlackBoxCreator import *


def simulate_BOA_gate():
    s = System()
    s.t_max = 36000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    inputs = [DnaBucket("inputs[0]", Amounts.ON),
              DnaBucket("inputs[1]", Amounts.ON),
              DnaBucket("inputs[2]", Amounts.ON),
              DnaBucket("inputs[3]", Amounts.ON),
              DnaBucket("inputs[4]", Amounts.OFF)]

    middles = [DnaBucket("middles0", Amounts.EMPTY),
               DnaBucket("middles1", Amounts.EMPTY)]

    outputs = [DnaBucket("outputs[0]", Amounts.EMPTY)]

    or_and = BlackOrAnd(name="orand", inputs=[inputs[0], inputs[1], inputs[2]], outputs=[middles[0]])
    and_or = BlackAndOr(name="andor", inputs=[middles[0], inputs[3], inputs[4]], outputs=[middles[1]])
    reporter = ReporterSeesaw("reporter", middles[1], outputs[0])
    s.gates_list.extend([and_or, or_and, reporter])
    s.simulate()

    plot_graphs(s.csv_fname, ["inputs[0]", "inputs[1]", "inputs[2]", "inputs[3]", "inputs[4]", "outputs[0]"])


def simulate_double_black():
    s = System()
    s.t_max = 36000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    inputs = [DnaBucket("inputs[0]", Amounts.OFF),
              DnaBucket("inputs[1]", Amounts.OFF),
              DnaBucket("inputs[2]", Amounts.OFF),
              DnaBucket("inputs[3]", Amounts.OFF),
              DnaBucket("inputs[4]", Amounts.ON)]

    middles0 = DnaBucket("middles0", Amounts.EMPTY)
    middles1 = DnaBucket("middles1", Amounts.EMPTY)

    outputs = [DnaBucket("outputs[0]", Amounts.EMPTY)]

    or_and = BlackOrAnd(name="orand", inputs=[inputs[0], inputs[1], inputs[2]], outputs=[middles0])
    and_or = BlackAndOr(name="andor", inputs=[middles0, inputs[3], inputs[4]], outputs=[middles1])
    reporter = ReporterSeesaw("reporter", middles1, outputs[0])

    build_black_box("DoubleBlack", [and_or, or_and, reporter], [], [middles0, middles1], [])

    s.gates_list.extend([and_or, or_and, reporter])
    s.simulate()

    plot_graphs(s.csv_fname, ["inputs[0]", "inputs[1]", "inputs[2]", "inputs[3]", "inputs[4]", "outputs[0]"])

    s = System()
    s.t_max = 36000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    inputs = [DnaBucket("inputs[0]", Amounts.OFF),
              DnaBucket("inputs[1]", Amounts.OFF),
              DnaBucket("inputs[2]", Amounts.OFF),
              DnaBucket("inputs[3]", Amounts.OFF),
              DnaBucket("inputs[4]", Amounts.ON)]

    outputs = [DnaBucket("outputs[0]", Amounts.EMPTY)]

    double_black = DoubleBlack("double_black", inputs, outputs)

    s.gates_list.append(double_black)
    s.simulate()

    plot_graphs(s.csv_fname, ["inputs[0]", "inputs[1]", "inputs[2]", "inputs[3]", "inputs[4]", "outputs[0]"])


def Simulate_Test_Nand():
    s = System()
    s.t_max = 36000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    inputs = [DualBucket("inputs[0]", Amounts.ON),
              DualBucket("inputs[1]", Amounts.OFF),
              DualBucket("inputs[2]", Amounts.OFF)]
    outputs = [DualBucket("outputs[0]", Amounts.EMPTY)]
    nand = testnand("nand", inputs, outputs)

    s.gates_list.append(nand)
    s.simulate()

    plot_graphs(s.csv_fname, ["inputs[0]", "inputs[1]", "inputs[2]", "outputs[0]"])


def main() -> int:
    simulate_BOA_gate()
    return 0


if __name__ == '__main__':
    sys.exit(main())
