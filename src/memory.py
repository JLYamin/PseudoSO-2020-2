# provê uma interface de abstração de memória RAM.
import copy


class Memory:

    pages_num = 0
    ref_sequence = []

    def __init__(self, file_data):
        try:
            self.pre_process(file_data)
        except:
            print(
                "Arquivo em formato inválido. Verifique se há linhas em branco adicionais.")
            return

        self.fifo()
        self.second_chance()
        self.lru()

    def pre_process(self, file_data):
        self.pages_num = copy.deepcopy(int(file_data[0]))
        self.ref_sequence = list(
            map(lambda x: int(x), copy.deepcopy(file_data[1:])))

    def fifo(self):
        print("FIFO", end=" ")

        idx = 0                                     # índice que representa a página mais antiga
        page_fault = 0                              # total de page faults
        # representa as páginas do array
        pages_array = [None for i in range(self.pages_num)]

        for ref in self.ref_sequence:
            try:
                # se não encontrar a página no array, lança uma exceção
                pages_array.index(ref)
            except:
                # caso não exista a página, ela é adicionada
                pages_array[idx] = ref
                page_fault += 1                     # incrementa contador de page faults
                idx = (idx + 1) % (self.pages_num)  # itera o índice

        print(page_fault)

    def second_chance(self):
        print("SC", end=" ")

        oldest_page = 0
        page_fault = 0
        pages_array = [{'page': None, 'r': 0, 'ref_count': 0}
                       for i in range(self.pages_num)]

        for ref in self.ref_sequence:                       # roda entre todas as referencias
            for page in pages_array:                        # for pages_array
                if (page['ref_count'] != 0):
                    # se o ref_count !== 0, ref_count -= 1
                    page['ref_count'] -= 1
                else:
                    page['r'] = 0                           # else, r = 0

            found_page = list(
                filter(lambda x: x['page'] == ref, pages_array))
            if (len(found_page) != 0):
                # se já existir, ref_count = 3 e r = 1
                found_page[0]['ref_count'] = 3
                found_page[0]['r'] = 1
            else:
                while (True):                               # se não existir, faz um while (true)
                    if (pages_array[oldest_page]['r'] == 0):
                        pages_array[oldest_page] = {
                            'page': ref, 'r': 1, 'ref_count': 3}
                        page_fault += 1
                        break
                    else:                                   # se não, segue pra próxima página
                        oldest_page = (oldest_page + 1) % (self.pages_num)
                        for page in pages_array:            # decrementa os ref_count
                            if (page['ref_count'] != 0):
                                page['ref_count'] -= 1
                            else:
                                page['r'] = 0

                # incrementa oldest_page
                oldest_page = (oldest_page + 1) % (self.pages_num)

        print(page_fault)

    def lru(self):
        print("LRU", end=" ")

        page_fault = 0
        # Inicializa ref_count com o maior número de iterações possível para ser o primeiro a ser removido
        pages_array = [{'page': None, 'ref_count': self.pages_num + 1}
                       for i in range(self.pages_num)]

        for ref in self.ref_sequence:
            found_page = list(
                filter(lambda x: x['page'] == ref, pages_array))

            if (len(found_page) != 0):      # if (pagina ja existe no array)
                found_page[0]['ref_count'] = 0  # se sim, zera o ref_count dele
            else:
                # se não, ordena o page_array pelo maior ref_count e substitui ele pela nova página
                pages_array.sort(key=lambda x: (x['ref_count']))
                pages_array[-1]['page'] = ref
                pages_array[-1]['ref_count'] = 0
                page_fault += 1

            # incrementa em 1 todos os ref_counts
            for page in pages_array:
                page['ref_count'] += 1

        print(page_fault)
