# classes e estruturas de dados relativas ao processo. Basicamente, mantém informações específicas do processo.
# Input: <LINHA = PROCESSO> <$1 = TEMPO DE CHEGADA> <$2 = TEMPO DE DURAÇÃO>

class Process:

    output = []

    def __init__(self, file_data):
        self.pre_process(file_data)
        self.output.append(self.fifo())
        self.output.append(self.sjf())
        self.output.append(self.rr())

        self.save_output()

    def pre_process(self, file_data):
        self.input = [{"id": idx, "arrival": int(data.split()[0]), "duration":int(
            data.split()[1])} for idx, data in enumerate(file_data)]

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

        input_fifo = sorted(self.input, key=lambda x: x['arrival'])
        output_fifo = []

        for data in input_fifo:

            idx = data['id']
            # Caso tempo e chegada menor que tempo total
            if data['arrival'] < tempo_total:
                start = tempo_total                         # tempo de inicio é o tempo total atual
                # incrementando com o tempo de duração
                tempo_total += data['duration']
                end = tempo_total                           # tempo final é o total atual
            else:
                # tempo de inicio é o tempo de chegada
                start = data['arrival']
                # tempo final é o tempo de chegada mais a duração
                end = data['arrival'] + data['duration']
                # tempo total é atualizado com o tempo final
                tempo_total = end

            output_fifo.append(
                "Rodar processo [" + str(idx) + "] de [" + str(start) + "] até [" + str(end) + "]")

        return output_fifo

    def sjf(self):
        output_sjf = []

        # ordena pela chegada e subordena pela duração
        input_sjf = sorted(self.input, key=lambda x: (
            x['arrival'], x['duration']))
        tempo_total = input_sjf[0]['arrival']
        aux_sjf = input_sjf

        while (len(input_sjf) != 0):
            output_sjf.append("Rodar processo [" + str(aux_sjf[0]['id']) + "] de [" + str(tempo_total) + "] até [" + str(aux_sjf[0]['duration'] +
                                                                                                                         tempo_total) + "]")                                                            # salvando a primeira linha após a ordenação

            # atribui a duration da linha atual ao tempo_total
            tempo_total = tempo_total + aux_sjf[0]['duration']

            # remove do input_sjf a linha equivalente (== id) à primeira linha do aux
            input_sjf = list(
                filter(lambda x: x['id'] != aux_sjf[0]['id'], input_sjf))
            # fazer um filtro do input_sjf de todos os tempos de chegada que são <= que o tempo_total e armazenar no aux (quais já chegaram enquanto executava a primeira?)
            aux_sjf = list(
                filter(lambda x: x['arrival'] <= tempo_total, input_sjf))

            # se não tiver nenhuma entrada em input_sjf que seja <= que o tempo_total, o aux vai estar vazio, ordena o input_sjf e o menor tempo de chegada se torna o novo tempo_total. e atribui o aux ao input_sjf
            if (len(aux_sjf) == 0 and len(input_sjf) != 0):

                input_sjf = sorted(input_sjf, key=lambda x: (
                    x['arrival'], x['duration']))    # ordenar o aux por duração
                tempo_total = input_sjf[0]['arrival']
                aux_sjf = input_sjf

            aux_sjf = sorted(aux_sjf, key=lambda x: x['duration'])

        return output_sjf

    def rr(self, quantum=2):
        output_rr = []

        # ordena pela chegada
        input_rr = sorted(self.input, key=lambda x: x['arrival'])
        tempo_total = 0

        while (len(input_rr) != 0):

            print(input_rr)

            if (input_rr[0]['arrival'] <= tempo_total):
                # verifica se a duração > quantum
                if (input_rr[0]['duration'] > quantum):
                    # duração - quantum
                    input_rr[0]['duration'] -= quantum
                    output_rr.append("Rodar processo [" + str(input_rr[0]['id']) + "] de [" + str(
                        tempo_total) + "] até [" + str(tempo_total + quantum) + "]")
                    tempo_total += quantum
                    input_rr.append(input_rr.pop(0))                      #
                else:
                    output_rr.append("Rodar processo [" + str(input_rr[0]['id']) + "] de [" + str(
                        tempo_total) + "] até [" + str(tempo_total + input_rr[0]['duration']) + "]")
                    tempo_total += input_rr[0]['duration']
                    # remove elemento do array
                    input_rr = list(
                        filter(lambda x: x['id'] != input_rr[0]['id'], input_rr))
            else:
                input_rr.append(input_rr.pop(0))

        return output_rr
