# provê uma interface de abstração de memória RAM.
import copy


class Memory:

    pages_num = 0
    ref_sequence = []

    def __init__(self, file_data):
        self.pre_process(file_data)
        self.fifo()
        self.second_chance()
        self.lru()

    def pre_process(self, file_data):
        self.pages_num = copy.deepcopy(int(file_data[0]))
        self.ref_sequence = list(
            map(lambda x: int(x), copy.deepcopy(file_data[1:])))

    def fifo(self):
        print("FIFO", end=" ")

        idx = 0
        page_fault = 0
        pages_array = [None] * self.pages_num

        for ref in self.ref_sequence:
            try:
                pages_array.index(ref)
            except:
                pages_array[idx] = ref
                page_fault += 1
                idx = (idx + 1) % (self.pages_num)

        print(page_fault)

    def second_chance(self):
        print("SC", end=" ")

        page_fault = 0

        print(page_fault)

    def lru(self):
        print("LRU", end=" ")

        page_fault = 0

        print(page_fault)
