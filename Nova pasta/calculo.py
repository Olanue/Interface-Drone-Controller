import time
import multiprocessing

def contar_sequencias(n):
    quantidade = 0
    for inicio in range(1, n):
        soma = 0
        i = inicio
        while soma < n:
            soma += i
            i += 1
        if soma == n:
            quantidade += 1
    return quantidade

def processa(valor, conn):
    inicio_tempo = time.time()
    max_sequencias = 0
    numero_com_mais_sequencias = 1
    relatorio = []
    sequencias_por_numero = []

    for n in range(1, valor + 1):
        qtd = contar_sequencias(n)
        relatorio.append(f"Número {n}: {qtd} sequência(s)")
        sequencias_por_numero.append(qtd)
        if qtd > max_sequencias:
            max_sequencias = qtd
            numero_com_mais_sequencias = n
        # Envia resultado parcial
        conn.send({
            "parcial": f"Número {n}: {qtd} sequência(s)\n",
            "n": n,
            "total": valor
        })

    fim_tempo = time.time()
    tempo_total_ms = (fim_tempo - inicio_tempo) * 1000
    tempo_total_s = fim_tempo - inicio_tempo

    resultado = {
        "relatorio": "\n".join(relatorio) + "\n\n"
            f"Número com mais sequências possíveis: {numero_com_mais_sequencias} ({max_sequencias} sequência(s))\n"
            f"Tempo de execução: {int(tempo_total_ms)} milissegundos ({tempo_total_s:.3f} segundos)\n",
        "sequencias": sequencias_por_numero,
        "fim": True
    }
    conn.send(resultado)
    conn.close()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    while True:
        entrada = input("Digite um número inteiro (ou 'x' para sair): ").strip()
        if entrada.lower() == 'x':
            break
        try:
            valor = int(entrada)
            parent_conn, child_conn = multiprocessing.Pipe()
            p = multiprocessing.Process(target=processa, args=(valor, child_conn))
            p.start()
            resultado = parent_conn.recv()
            p.join()

            print(resultado["relatorio"])

        except ValueError:
            print("Entrada inválida. Digite um número inteiro ou 'x' para sair.")
