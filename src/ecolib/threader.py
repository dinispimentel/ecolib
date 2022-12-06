from typing import Callable

from .logger import lg as logging
import time


class Threader:

    def __init__(self, getThreadPool, instances, delay_config=None):
        if delay_config is None:
            self.delay_config = {"delay": 0, "instances_before_delay": 0}
        else:
            self.delay_config = delay_config
        self.getThreadPool = getThreadPool  # medo de pegar uma cópia e não um apontador do objeto original
        self.instances = instances
        self.done = 0
        self.suspendAll = False
        self.suspendTimer = 0

    def __startAndJoin(self, ptr_idx, instances=None, midFunc: Callable = None,
                       endFunc = None):
        instances = instances or self.instances
        delaying = False
        for s in range(0, instances):

            if self.delay_config != {"delay": 0, "instances_before_delay": 0} and \
                    self.done >= self.delay_config["instances_before_delay"]:  # Deve vir primeiro porque se não inicia
                #  outra e esta outra pega um estado em que diz para esperar denovo...
                print(f'Já se passaram {self.done} instancias, pausando por: {self.delay_config["delay"]} secs')
                self.done = 0

                time.sleep(self.delay_config["delay"])
                delaying = True
            if self.suspendAll and not delaying:
                time.sleep(self.suspendTimer)
                self.suspendTimer = 0
                self.suspendAll = False
            self.getThreadPool()[s + ptr_idx].start()
            if midFunc:
                midFunc(s=ptr_idx + 1, e=ptr_idx + instances)
            self.done += 1


        for j in range(0, instances):
            self.getThreadPool()[j + ptr_idx].join()




        if endFunc:
            # print("Aqui")
            endFunc(s=ptr_idx+1, e=ptr_idx+instances)  # +1 pra contar do elemento 1 até ao elemento + num de instâncias



    def dispatch(self, midFunc=None, endFunc: Callable[[int, int], None] =None):



        jobs = len(self.getThreadPool())  # numero de serviços

        # noinspection GrazieInspection
        def start(ptr_idx=0):

            if jobs - 1 == 0 and ptr_idx == 0:  # Edge case de só ter 1 thread
                self.__startAndJoin(ptr_idx, instances=1, midFunc=midFunc, endFunc=endFunc)
                return

            elif ptr_idx >= jobs:  # Esperemos que nunca seja maior, porque se for, aiai
                logging.info(
                    "[THREADER]: Finalizou #[" + str(ptr_idx+1) + ">=" + str(jobs) + "]"
                    )
                return

            elif ptr_idx + self.instances <= jobs:
                # Se o pointer pode percorrer uma sequenciação de instances nos jobs
                logging.info("[THREADER]: Instanciando Full #[" + str(ptr_idx) + "->" + str(ptr_idx+self.instances) +
                             "]")

                self.__startAndJoin(ptr_idx, midFunc=midFunc, endFunc=endFunc)
                ptr_idx += self.instances
                start(ptr_idx)
            elif ptr_idx + self.instances > jobs:
                # Caso o pointer ja aponte para um sequenciação de instancias fora do range dos jobs

                remaining_instances = (jobs - ptr_idx)
                # Numero de instancias que faltam percorrer \n
                # como o range do startAndJoin começa em 0, então não deve ser enviado a simples diferença porque:
                # 1º: o 1o indice enviado não foi processado
                # 2º: os outros indices devem ser processados, e como o range (a,b) vai até b-1 então temos de enviar \n
                # mesmo o número de elementos a serem processados já que seria b+1 porque 0-based (4, 5) #(0,1)

                self.__startAndJoin(ptr_idx, instances=remaining_instances, midFunc=midFunc,
                                    endFunc=endFunc)
                logging.info("[THREADER]: tentando finalizar [" + str(ptr_idx+1) + "->" +  # +1 pra contar a partir do 1
                             str(ptr_idx + remaining_instances) + "]")
                ptr_idx += remaining_instances  # para não ser o número de elementos a mais (ver explicação acima)

                start(ptr_idx)

        start()

    def suspendAllForXTime(self, x):
        self.suspendAll = True
        self.suspendTimer = x or 1



