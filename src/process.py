# classes e estruturas de dados relativas ao processo. Basicamente, mantém informações específicas do processo.
# Input: <LINHA = PROCESSO> <$1 = TEMPO DE CHEGADA> <$2 = TEMPO DE DURAÇÃO>

class Process:

    output = []

    def __init__(self, file_data):
        self.pre_process(file_data)
        self.output.append(self.fifo())
        self.output.append(self.sjf())
        self.output.append(["1"])

        self.save_output()
    
    def pre_process(self,file_data):
        self.input = [{"id":idx, "arrival":int(data.split()[0]), "duration":int(data.split()[1])} for idx, data in enumerate(file_data)]

    def save_output(self):
        file = open("./output/process.out.txt", "w+")

        labels = ["FIFO", "SJF", "RR"]
        
        for idx in range(len(labels)):            
            file.write(labels[idx] + ":\n")
            for line in self.output[idx]:
                file.write("\t" + line + "\n")
            file.write("\n")
        file.close()

    def fifo(self):
        tempo_total = 0

        input_fifo = sorted(self.input, key = lambda x: x['arrival'])
        output_fifo = []
        
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

            output_fifo.append("Rodar processo [" + str(idx) + "] de [" + str(start) + "] até [" + str(end) + "]")

        return output_fifo

    def sjf(self):
        output_sjf = []
        
        input_sjf = sorted(self.input, key = lambda x: (x['arrival'], x['duration'])) # ordena pela chegada e subordena pela duração
        tempo_total = input_sjf[0]['arrival']
        aux_sjf = input_sjf

        while (len(input_sjf) != 0):
            output_sjf.append("Rodar processo [" + str(aux_sjf[0]['id']) + "] de [" + str(tempo_total) + "] até [" + str(aux_sjf[0]['duration'] +\
                 tempo_total) + "]")                                                            # salvando a primeira linha após a ordenação
            
            tempo_total = tempo_total + aux_sjf[0]['duration']                                  # atribui a duration da linha atual ao tempo_total

            input_sjf = list(filter(lambda x: x['id'] != aux_sjf[0]['id'], input_sjf))          # remove do input_sjf a linha equivalente (== id) à primeira linha do aux
            aux_sjf = list(filter(lambda x: x['arrival'] <= tempo_total, input_sjf))            # fazer um filtro do input_sjf de todos os tempos de chegada que são <= que o tempo_total e armazenar no aux (quais já chegaram enquanto executava a primeira?)
            
            if (len(aux_sjf) == 0 and len(input_sjf) != 0):                                     # se não tiver nenhuma entrada em input_sjf que seja <= que o tempo_total, o aux vai estar vazio, ordena o input_sjf e o menor tempo de chegada se torna o novo tempo_total. e atribui o aux ao input_sjf

                input_sjf = sorted(input_sjf, key = lambda x: (x['arrival'], x['duration']))    # ordenar o aux por duração
                tempo_total = input_sjf[0]['arrival']
                aux_sjf = input_sjf

            aux_sjf = sorted(aux_sjf, key = lambda x: x['duration'])

        return output_sjf