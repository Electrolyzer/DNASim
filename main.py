import sys

from Simulator import *
from DualRailGates import *


def simulate_and2_gate():
    s = System()
    s.t_max = 36000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    w_1 = DnaBucket("w_1", Amounts.N)
    w_2 = DnaBucket("w_2", Amounts.N)
    w_3 = DnaBucket("w_3", Amounts.EMPTY)
    w_4 = DnaBucket("w_4", Amounts.EMPTY)
    fluor = DnaBucket("fluor", Amounts.EMPTY)

    and_gate = And2Gate(name="and_gate", input1=w_1, input2=w_2, output=w_3)
    and_gate2 = And2Gate(name="and_gate_2", input1=w_1, input2=w_3, output=w_4)
    reporter = ReporterSeesaw("reporter", w_4, fluor)

    s.gates_list.append(and_gate)
    s.gates_list.append(and_gate2)
    s.gates_list.append(reporter)

    s.simulate()

    plot_graphs(s.csv_fname, ["w_1", "w_2", "w_3", "w_4", "fluor"])


def main() -> int:
    simulate_and2_gate()
    return 0


if __name__ == '__main__':
    sys.exit(main())
