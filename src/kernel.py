# contém as chamadas para os demais módulos.
import sys
from src.process import Process
from src.memory import Memory
from src.io import IO

# .\__main__.py 1 process.txt
# .\__main__.py 2 memory.txt
# .\__main__.py 3 io.txt

class Kernel:

    def __init__(self):
        input_mode = sys.argv[1]
        file_name = sys.argv[2]

        file_data = self.read_file(file_name)


        if input_mode == "1":
            process = Process(file_data)
        elif input_mode == "2":
            memory = Memory(file_data)
        elif input_mode == "3":
            io = IO(file_data)


    def read_file(self, file_name):
        with open("./input/" + file_name, "r") as f:
            file_data = f.read().split("\n")
        return file_data
