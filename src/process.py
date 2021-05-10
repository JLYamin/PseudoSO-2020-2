# classes e estruturas de dados relativas ao processo. Basicamente, mantém informações específicas do processo.
# Input: <LINHA = PROCESSO> <$1 = TEMPO DE CHEGADA> <$2 = TEMPO DE DURAÇÃO>
import copy


class Process:

    output = []

    def __init__(self, file_data):
        self.pre_process(file_data)

        self.output.append(self.fifo())
        self.output.append(self.sjf())
        self.output.append(self.rr())

        self.save_output()
        self.time_analysis()

    def pre_process(self, file_data):
        self.input = [{"id": idx, "arrival": int(data.split()[0]), "duration":int(
            data.split()[1])} for idx, data in enumerate(file_data)]

    def save_output(self):
        file = open("./output/process.out.txt", "w+")

        labels = ["FIFO", "SJF", "RR"]

        for idx in range(len(labels)):
            file.write(labels[idx] + ":\n")
            for line in self.output[idx]:
                file.write("\tRodar processo [" + str(line[0]) + "] de [" + str(
                    line[1]) + "] até [" + str(line[2]) + "]\n")
            file.write("\n")
        file.close()

    def fifo(self):
        tempo_total = 0

        # Para não alterar o original
        input_fifo = copy.deepcopy(
            sorted(self.input, key=lambda x: x['arrival']))
        output_fifo = []  # lista de triplas: [(a,b,c), (a,b,x)]

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

            output_fifo.append((idx, start, end))

        return output_fifo

    def sjf(self):
        output_sjf = []

        # ordena pela chegada e subordena pela duração
        input_sjf = copy.deepcopy(sorted(self.input, key=lambda x: (
            x['arrival'], x['duration'])))
        tempo_total = input_sjf[0]['arrival']
        aux_sjf = input_sjf

        while (len(input_sjf) != 0):
            # salvando a primeira linha após a ordenação
            output_sjf.append(
                (aux_sjf[0]['id'], tempo_total, (aux_sjf[0]['duration'] + tempo_total)))

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
        input_rr = copy.deepcopy(
            sorted(self.input, key=lambda x: x['arrival']))
        # pega o tempo de chegada do primeiro elemento, para o caso de não iniciar em 0
        tempo_total = input_rr[0]['arrival']
        arrived = list(filter(lambda x: x['arrival'] <= tempo_total, input_rr))

        while (len(input_rr) != 0):
            for elem in input_rr:
                # Adiciona os processos que chegam
                if (elem['arrival'] <= tempo_total) and (len(list(filter(lambda x: x['id'] == elem['id'], arrived))) == 0):
                    arrived.insert(len(arrived) - 1, elem)

            if len(arrived) == 0 and len(input_rr) != 0:
                arrived.append(input_rr[0])
                tempo_total = input_rr[0]['arrival']

            # verifica se a duração > quantum
            if (arrived[0]['duration'] > quantum):
                # duração - quantum
                arrived[0]['duration'] -= quantum
                output_rr.append(
                    (arrived[0]['id'], tempo_total, (tempo_total + quantum)))
                tempo_total += quantum
                arrived.append(arrived.pop(0))
            else:
                output_rr.append(
                    (arrived[0]['id'], tempo_total, (tempo_total + arrived[0]['duration'])))
                tempo_total += arrived[0]['duration']
                # remove elemento do array
                removed_element_id = arrived.pop(0)['id']
                input_rr = list(
                    filter(lambda x: x['id'] != removed_element_id, input_rr))

        return output_rr

    def time_analysis(self):

        labels = ["FIFO", "SJF", "RR"]

        for idx, out in enumerate(self.output):
            print(labels[idx], end=" ")

            # Calcular TEMPO TOTAL DE EXECUÇÃO médio = ultimo valor / total de processos

            avg_exec_time = out[-1][2]/len(self.input)
            print(str(round(avg_exec_time, 1)), end=" ")

            # Calcular o TEMPO MÉDIO DE RESPOSTA = sum(primeira exec - arrival) / total de processos

            total_resp_time = 0
            # estrutura do self.input: [id], [arrival], [duração]
            for process in self.input:
                # buscar a primeira execução do processo
                first_exec = list(
                    filter(lambda x: x[0] == process['id'], out))[0]
                total_resp_time += first_exec[1] - process['arrival']

            avg_response_time = total_resp_time / len(self.input)
            print(str(round(avg_response_time, 1)), end=" ")

            # calcular o TEMPO MÉDIO DE ESPERA = sum(última exec - tempo de chegada - tempo de duração)/total de processos
            total_wait_time = 0
            for process in self.input:
                # buscar a primeira execução do processo
                last_exec = list(
                    filter(lambda x: x[0] == process['id'], out))[-1]
                total_wait_time += last_exec[2] - \
                    process['arrival'] - process['duration']

            avg_wait_time = total_wait_time / len(self.input)
            print(str(round(avg_wait_time, 1)))
