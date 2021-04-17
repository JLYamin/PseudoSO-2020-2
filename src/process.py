# classes e estruturas de dados relativas ao processo. Basicamente, mantém informações específicas do processo.
# Input: <LINHA = PROCESSO> <$1 = TEMPO DE CHEGADA> <$2 = TEMPO DE DURAÇÃO>

class Process:

    def __init__(self, file_data):
        self.pre_process(file_data)
        self.fifo()
    
    def pre_process(self,file_data):
        self.input = [{"id":idx, "arrival":int(data.split()[0]), "duration":int(data.split()[1])} for idx, data in enumerate(file_data)]
         

    def fifo(self):
        tempo_total = 0

        input_fifo = sorted(self.input, key = lambda x: x['arrival'])
        
        for data in input_fifo:
            
            idx = data['id']
                                                            # Caso tempo e chegada menor que tempo total
            if data['arrival'] < tempo_total:
                start = tempo_total                         # tempo de inicio é o tempo total atual
                tempo_total += data['duration']             # incrementando com o tempo de duração
                end = tempo_total                           # tempo final é o total atual
            else:
                start = data['arrival']                     # tempo de inicio é o tempo de chegada
                end = data['arrival'] + data['duration']    # tempo final é o tempo de chegada mais a duração
                tempo_total = end                           # tempo total é atualizado com o tempo final

            print(f"Rodar processo [{ idx }] de [{ start }] até [{ end }]")
            