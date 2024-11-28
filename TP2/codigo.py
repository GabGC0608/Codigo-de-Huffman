import os
from collections import Counter

# Módulo: Contador
def contar_palavras(texto):
    """
    Conta a frequência de cada palavra em um texto.
    """
    palavras = texto.split()
    return Counter(palavras)

# Módulo: Construção da Árvore
def construir_arvore(frequencias):
    """
    Constrói a árvore de Huffman no formato de lista ligada:
    [frequência ou palavra, subárvore esquerda, subárvore direita].
    """
    lista_nodos = [[freq, [palavra, None, None]] for palavra, freq in sorted(frequencias.items(), key=lambda x: x[1])]

    while len(lista_nodos) > 1:
        nodo1 = lista_nodos.pop(0)
        nodo2 = lista_nodos.pop(0)

        nova_frequencia = nodo1[0] + nodo2[0]
        nova_subarvore = [nova_frequencia, nodo1[1], nodo2[1]]

        lista_nodos.append([nova_frequencia, nova_subarvore])
        lista_nodos.sort(key=lambda x: x[0])

    return lista_nodos[0][1]

def gerar_codigos(arvore, prefixo="", mapa_codigos=None):
    """
    Gera os códigos de Huffman para cada palavra.
    """
    if mapa_codigos is None:
        mapa_codigos = {}

    if arvore[1] is None and arvore[2] is None:
        mapa_codigos[arvore[0]] = prefixo
    else:
        gerar_codigos(arvore[1], prefixo + "0", mapa_codigos)
        gerar_codigos(arvore[2], prefixo + "1", mapa_codigos)

    return mapa_codigos

# Módulo: Tradução
def codificar_texto(texto, mapa_codigos):
    """
    Codifica um texto com base no mapa de códigos de Huffman.
    """
    palavras = texto.split()
    return ''.join(mapa_codigos[palavra] for palavra in palavras)

def decodificar_texto(codigo_binario, arvore):
    """
    Decodifica um código binário com base na árvore de Huffman.
    """
    resultado = []
    nodo_atual = arvore

    for bit in codigo_binario:
        if bit == "0":
            nodo_atual = nodo_atual[1]
        else:
            nodo_atual = nodo_atual[2]

        if nodo_atual[1] is None and nodo_atual[2] is None:
            resultado.append(nodo_atual[0])
            nodo_atual = arvore

    return ' '.join(resultado)

# Funções auxiliares para lidar com arquivos
def compactar(entrada, saida):
    """
    Compacta o arquivo de entrada para o arquivo de saída.
    """
    try:
        with open(entrada, "r", encoding="utf-8-sig") as arquivo:
            texto = arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo '{entrada}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao abrir o arquivo '{entrada}': {e}")
        return

    frequencias = contar_palavras(texto)
    arvore = construir_arvore(frequencias)
    mapa_codigos = gerar_codigos(arvore)
    codigo_binario = codificar_texto(texto, mapa_codigos)

    # Salvando no arquivo de saída
    with open(saida, "w", encoding="utf-8") as arquivo_saida:
        arquivo_saida.write(f"{frequencias}\n")
        arquivo_saida.write(codigo_binario)
    print(f"Arquivo compactado salvo em: {saida}")

def descompactar(entrada, saida):
    """
    Descompacta o arquivo de entrada para o arquivo de saída.
    """
    try:
        with open(entrada, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
            frequencias = eval(linhas[0].strip())
            codigo_binario = linhas[1].strip()
    except FileNotFoundError:
        print(f"Arquivo '{entrada}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao abrir o arquivo '{entrada}': {e}")
        return

    arvore = construir_arvore(frequencias)
    texto_decodificado = decodificar_texto(codigo_binario, arvore)

    with open(saida, "w", encoding="utf-8") as arquivo_saida:
        arquivo_saida.write(texto_decodificado)
    print(f"Arquivo descompactado salvo em: {saida}")

# Módulo: Main
def main():
    print("Selecione a operação:")
    print("1. Compactar")
    print("2. Descompactar")
    opcao = input("Digite o número da operação desejada: ").strip()

    entrada = "entrada.txt"
    if opcao == "1":
        saida = "saida.huf"
        compactar(entrada, saida)
    elif opcao == "2":
        entrada = "saida.huf"
        saida = "saida.txt"
        descompactar(entrada, saida)
    else:
        print("Opção inválida. Por favor, selecione 1 ou 2.")

if __name__ == "__main__":
    main()
