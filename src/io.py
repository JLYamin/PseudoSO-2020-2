# trata a alocação do braço do disco para realização de escrita/leitura nos blocos do disco para os processos.
import copy


class IO:

    cyl_num = 0             # Número total de cilindros
    initial_cyl = 0         # Cilindro inicial
    cyl_sequence = []       # Sequência de cilindros

    def __init__(self, file_data):
        try:
            self.pre_process(file_data)
        except:
            print(
                "Arquivo em formato inválido. Verifique se há linhas em branco adicionais.")
            return

        self.fcfs()
        self.sstf()
        self.scan()

    def pre_process(self, file_data):   # Prepara a entrada do arquivo e atribui às variáveis
        self.cyl_num = copy.deepcopy(int(file_data[0]))
        self.initial_cyl = copy.deepcopy(int(file_data[1]))
        self.cyl_sequence = list(
            map(lambda x: int(x), copy.deepcopy(file_data[2:])))

    def fcfs(self):
        print("FCFS", end=" ")

        total_cyl = 0
        last_pos = self.initial_cyl

        for pos in self.cyl_sequence:           # Varre a sequência de cilindros
            # Pela ordem, calcula o deslocamento pela diferença
            total_cyl += abs(last_pos - pos)
            last_pos = pos                      # Atualiza a posição

        print(total_cyl)

    def sstf(self):
        print("SSTF", end=" ")

        total_cyl = 0
        ordened_sequence = copy.deepcopy(           # Ordena a sequência de cilindros pela distância do inicial
            sorted(self.cyl_sequence, key=lambda x: abs(x - self.initial_cyl)))
        next_pos = 0
        last_pos = self.initial_cyl

        for _ in self.cyl_sequence:                 # Loop em cima do tamanho da sequência
            # O primeiro cilindro da sequência é o mais próximo
            next_pos = ordened_sequence.pop(0)
            # Incrementa a distância deslocada
            total_cyl += abs(last_pos - next_pos)
            last_pos = next_pos                     # Atualiza a posição
            ordened_sequence = sorted(              # Ordena pela distância, sem os cilindros já visitados
                ordened_sequence, key=lambda x: abs(x - next_pos))

        print(total_cyl)

    def scan(self):
        print("SCAN", end=" ")

        total_cyl = 0
        ordened_sequence = copy.deepcopy(               # Ordena todos os cilindros
            sorted(self.cyl_sequence, key=lambda x: x))
        closest_pos = copy.deepcopy(                    # Pega o cilindro mais próximo
            sorted(self.cyl_sequence, key=lambda x: abs(x - self.initial_cyl)))[0]
        direction = closest_pos - self.initial_cyl      # Define a distância

        # Define o cilindro mais à esquerda
        first_pos = ordened_sequence[0]
        # Define o cilindro mais à direita
        last_pos = ordened_sequence[-1]

        if (direction > 0):                             # Se positivo, movimenta para a direita
            total_cyl = last_pos - self.initial_cyl     # Calcula deslocamento da ida
            total_cyl += last_pos - first_pos           # Calcula deslocamento da volta
        else:                                           # Se negativo, movimenta para a esquerda
            total_cyl = self.initial_cyl - first_pos    # Calcula deslocamento da ida
            total_cyl += last_pos - first_pos           # Calcula deslocamento da volta

        print(total_cyl)
