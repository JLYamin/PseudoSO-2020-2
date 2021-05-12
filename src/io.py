# trata a alocação do braço do disco para realização de escrita/leitura nos blocos do disco para os processos.
import copy


class IO:

    cyl_num = 0
    initial_cyl = 0
    cyl_sequence = []

    def __init__(self, file_data):
        self.pre_process(file_data)
        self.fcfs()
        self.sstf()
        self.scan()

    def pre_process(self, file_data):
        self.cyl_num = copy.deepcopy(int(file_data[0]))
        self.initial_cyl = copy.deepcopy(int(file_data[1]))
        self.cyl_sequence = list(
            map(lambda x: int(x), copy.deepcopy(file_data[2:])))

    def fcfs(self):
        print("FCFS", end=" ")

        total_cyl = 0
        last_pos = self.initial_cyl

        for pos in self.cyl_sequence:
            total_cyl += abs(last_pos - pos)
            last_pos = pos

        print(total_cyl)

    def sstf(self):
        print("SSTF", end=" ")

        total_cyl = 0

        print(total_cyl)

    def scan(self):
        print("SCAN", end=" ")

        total_cyl = 0

        print(total_cyl)
