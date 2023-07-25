import sys

from Simulator import *
from DualRailGates import *


def simulate_delay():
    s = System()
    s.t_max = 1500  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
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

    input = DnaBucket("input", Amounts.N)
    output = DnaBucket("output", Amounts.N)
    fluor = DnaBucket("fluor", Amounts.EMPTY)

    subtractionGate = SubtractionGate("subtractionGate", input, output)
    #reporter = ReporterSeesaw("reporter", w_1, fluor)

    s.gates_list.append(subtractionGate)
    #s.gates_list.append(reporter)

    s.simulate()

    plot_graphs(s.csv_fname, ["input", "output"])

def simulate_enable():
    s = System()
    s.t_max = 15000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    w_1 = DnaBucket("w_1", Amounts.N)
    w_2 = DnaBucket("w_2", Amounts.N)
    w_3 = DnaBucket("w_3", Amounts.EMPTY)
    fluor = DnaBucket("fluor", Amounts.EMPTY)

    Enable = GateEnable("GateEnable", w_1, w_2, w_3)
    reporter = ReporterSeesaw("reporter", w_3, fluor)

    s.gates_list.append(Enable)
    s.gates_list.append(reporter)

    s.simulate()

    plot_graphs(s.csv_fname, ["w_1", "w_2", "w_3", "fluor"])

def testNotGate():
    s = System()
    s.t_max = 80000  # [sec]
    s.K_fast = 0.000315  # fast toehold binding rate constant [nM/s]
    s.K_slow = 0.000015 * 0.95  # slow toehold binding rate constant [nM/s]
    s.print_steps = False

    input = DnaBucket("input", Amounts.EMPTY)
    enabler = DnaBucket("enabler", Amounts.EMPTY)
    subtractOutput = DnaBucket("subtractOutput", Amounts.N)
    enableOutput = DnaBucket("enableOutput", Amounts.EMPTY)
    fluor = DnaBucket("fluor", Amounts.EMPTY)




    delay_gate = DelayGate("delay_gate", 4, enabler)
    subtractionGate = SubtractionGate("subtractionGate", input, subtractOutput)
    enableGate = GateEnable("GateEnable", enabler, subtractOutput, enableOutput)
    reporter = ReporterSeesaw("reporter", enableOutput, fluor)

    s.gates_list.append(enableGate)
    s.gates_list.append(delay_gate)
    s.gates_list.append(subtractionGate)
    s.gates_list.append(reporter)

    s.simulate()

    plot_graphs(s.csv_fname, ["input", "subtractOutput", "enableOutput", "fluor"])

def main() -> int:
    testNotGate()
    return 0


if __name__ == '__main__':
    sys.exit(main())
