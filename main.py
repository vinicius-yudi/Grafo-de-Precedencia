import multiprocessing as mp
import time

def process(name: str, n: int, t: float, start_semaphore: mp.Semaphore, end_semaphores: list = None) -> None:
    print(f'Processo {name} aguardando')
    start_semaphore.acquire()
    print(f'Processo {name} iniciado')
    for i in range(1, n + 1):
        print(f'{name} - {i}')
        time.sleep(t)
    print(f'Processo {name} finalizado')
    
    if end_semaphores:
        for sem in end_semaphores:
            sem.release()

def main() -> None:
    range_count = int(input('Digite um valor para contagem: '))
    time_count = float(input('Digite um valor para a contagem: '))

    start_A = mp.Semaphore(1)   # A inicia automaticamente
    start_B = mp.Semaphore(0)    # B espera por A
    start_C = mp.Semaphore(0)    # C também espera por A
    start_D = mp.Semaphore(0)    # D espera por B e C

    # Processos
    process_A = mp.Process(target=process, args=('A', range_count, time_count, start_A, [start_B, start_C]))
    process_B = mp.Process(target=process, args=('B', range_count, time_count, start_B, [start_D]))
    process_C = mp.Process(target=process, args=('C', range_count, time_count, start_C, [start_D]))
    process_D = mp.Process(target=process, args=('D', range_count, time_count, start_D))

    # Iniciar processos
    process_A.start()
    process_B.start()
    process_C.start()
    process_D.start()

    # Aguardar processos terminarem
    process_A.join()
    process_B.join()
    process_C.join()
    process_D.join()

if __name__ == '__main__':
    main()
