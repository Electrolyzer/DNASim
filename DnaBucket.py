
class Amounts:
    N = 100          # 0.1x standard concentration
    OFF = 0.1 * N    # logic OFF value = 0.1
    ON = 0.9 * N     # logic ON value = 0.9
    EMPTY = 0 * N    # logic EMPTY value


class DnaBucket:
    def __init__(self, name, amount) -> None:
        self.name = name
        self.amount = amount  # current amount of DNA
        self.dt = 0  # used to accumulate the changes when iterating over gates list

    def print_bucket(self) -> None:
        print("\t\t" + self.name + ": " + str(self.amount))
