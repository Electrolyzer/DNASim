import matplotlib.pyplot as plt
import csv
import pandas as pd
import itertools


class System:
    def __init__(self) -> None:
        self.t_step = 1              # [sec]
        self.t_max = 25000           # [sec]
        self.K_fast = 0.000315       # fast toehold binding rate constant [nM/s]
        self.K_slow = 0.000015*0.95  # slow toehold binding rate constant [nM/s]
        self.gates_list = []
        self.print_steps = False
        self.csv_fname = "sim_res.csv"

    def simulate(self) -> None:
        print("Simulating [0:" + str(self.t_max) + "], in steps of: " + str(self.t_step) + "[sec]")
        ks = self.K_slow * self.t_step
        kf = self.K_fast * self.t_step

        self.__write_csv_header()
        self.__print_step(0)
        for t in range(1, self.t_max+1, self.t_step):
            for g in self.gates_list:
                g.calculate_transfer_amounts(ks, kf)
            for g in self.gates_list:
                g.update_amounts()
            self.__print_step(t)
            self.__save_time_data_to_csv(t)
        self.__csvfile.close()

    def __print_step(self, time) -> None:
        if self.print_steps:
            print("time = " + str(time))
            for g in self.gates_list:
                g.print_gate()
                print('')

    def __get_buckets_as_list(self):
        bl = []
        for g in self.gates_list:
            bl.extend(g.get_buckets_as_list())

        bl = list(set(bl))
        bl.sort(key=lambda b: b.name)
        return bl

    def __write_csv_header(self):
        self.__csvfile = open(self.csv_fname, 'w', newline='', encoding='utf-8')
        csvwriter = csv.writer(self.__csvfile)
        row = ["time"]
        for b in self.__get_buckets_as_list():
            row.append(b.name)
        csvwriter.writerow(row)
        self.__save_time_data_to_csv(0)

    def __save_time_data_to_csv(self, time):
        #if not time % 25 == 0:
        #     return
        row = [time]
        for b in self.__get_buckets_as_list():
            if hasattr(b, "val_bucket"):
                row.append(b.val_bucket.amount)
            else:
                row.append(b.amount)
        csvwriter = csv.writer(self.__csvfile)
        csvwriter.writerow(row)


def plot_graphs(csv_fname, buckets=None):
    print("Plotting Results")
    df = pd.read_csv(csv_fname)
    if buckets is None:
        buckets = list(df.columns)[1:]
    times = list(df['time'])

    #marker = itertools.cycle((',', '+', '.', 'o', '*'))
    styles = ('-', '--', '-.', ':', \
              (0, (5, 5)), (0, (5, 10)), (0, (1, 10)), (0, (1, 1)), (5, (10, 3)), \
              (0, (5, 1)), (0, (3, 10, 1, 10)), (0, (3, 5, 1, 5)), (0, (3, 1, 1, 1)), \
              (0, (3, 5, 1, 5, 1, 5)), (0, (3, 10, 1, 10, 1, 10)), (0, (3, 1, 1, 1, 1, 1)) )
    linestyle = itertools.cycle((styles))

    fig_name = "All_plots"
    plt.figure(fig_name)
    for b in buckets:
        amounts = df[b]
        #plt.plot(times, amounts, label=b, marker=next(marker))
        plt.plot(times, amounts, label=b, linestyle=next(linestyle))

    plt.title(fig_name)
    plt.xlabel('Time [sec]')
    plt.ylabel('DNA amount [nM]')
    plt.legend()
    plt.grid()
    plt.show()
    