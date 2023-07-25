import sys

from Simulator import *
from DualRailGates import *


def simulate_delay():
    s = System()
    s.t_max = 1500  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.K_very_slow = 10**-10
    s.print_steps = False

    w_1 = DnaBucket("w_1", Amounts.EMPTY)
    w_2 = DnaBucket("w_2", Amounts.N)
    w_3 = DnaBucket("w_3", Amounts.EMPTY)
    w_4 = DnaBucket("w_4", Amounts.EMPTY)
    fluor = DnaBucket("fluor", Amounts.EMPTY)

    delay_gate = DelayGate("delay_gate", 5, w_1)
    #reporter = ReporterSeesaw("reporter", w_1, fluor)

    s.gates_list.append(delay_gate)
    #s.gates_list.append(reporter)

    s.simulate()

    plot_graphs(s.csv_fname, ["w_1"])

def simulate_subtraction():
    s = System()
    s.t_max = 15000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    w_1 = DnaBucket("w_1", Amounts.OFF)
    w_2 = DnaBucket("w_2", Amounts.N)
    fluor = DnaBucket("fluor", Amounts.EMPTY)

    subtractionGate = SubtractionGate("subtractionGate", w_1, w_2)
    #reporter = ReporterSeesaw("reporter", w_1, fluor)

    s.gates_list.append(subtractionGate)
    #s.gates_list.append(reporter)

    s.simulate()

    plot_graphs(s.csv_fname, ["w_1", "w_2"])

def main() -> int:
    simulate_subtraction()
    return 0


if __name__ == '__main__':
    sys.exit(main())
