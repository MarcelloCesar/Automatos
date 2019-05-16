# Definicao das excessoes
class EstadoNaoExiste(Exception):
    def __init__(self):
        self.mensagem = 'Utilizacao de estado que não existe no conjunto de'\
            ' estados'


def listToSet(list):
    Set = set()
    for i in list:
        Set.add(i)

    return Set


def listToSet2(list):
    Set = set()
    for i in list:
        SubS = set()
        for k in i:
            SubS.add(k)
        Set.add(SubS)

    return Set


def setToList(set):
    List = list()
    for i in set:
        List.append(i)

    return List


def subConjunto(conjunto):
    if conjunto == []:
        return [conjunto]
    subConjuntos = [conjunto]
    for i in range(0, len(conjunto)):
        sub = subConjunto(conjunto[:i] + conjunto[i+1:])
        for j in sub:
            if j not in subConjuntos:
                subConjuntos.append(j)
    return subConjuntos


def printaFuncPrograma(alfa, funcao, justificado=15, texto = "Funcao gerada: ", tipo = 1, novosNomes = dict()):
    print(texto, end="")
    for i in range(0,90):
        print("-", end="")
    print()
    print(str().ljust(int(justificado)), end="")
    for i in sorted(alfa):
        print((str("| ") + str(i)).ljust(int(justificado)), end="")
    print()
    if tipo == 3:
        for i in funcao:
            if i == "":
                continue
            print(str(novosNomes[i]).ljust(int(justificado)), end="")
            for j in sorted(alfa):
                print(("| " + (str(novosNomes["".join(funcao[i][j])]) if len(funcao[i][j]) > 0 else " - " )).ljust(int(justificado)), end ="")
            print()

    else:
        for i in sorted(funcao):
            print(str(i).ljust(int(justificado)), end="")
            for j in sorted(alfa):
                if tipo == 1:
                    print(("| " + str(("{" + ", ".join(funcao[i][j]) + "}") if len(funcao[i][j]) > 0 else " - " )).ljust(int(justificado)), end ="")
                elif tipo == 2:
                    print(("| " + str(("<" + "".join(funcao[i][j]) + ">") if len(funcao[i][j]) > 0 else " - " )).ljust(int(justificado)), end ="")
            print()



if __name__ == '__main__':
    # Receber dados do usuario
     try:
        # Receber o alfabeto
        entrada = input(
            "Insira o alfabeto separando simbolos por vírgula: "
        )
        alfabetoTemp = list(entrada.split(','))
        alfabeto = list()
        for i in alfabetoTemp:
            if i not in alfabeto:
                alfabeto.append(i)
        print(alfabeto)

        # Receber conjunto de estados
        entrada = input(
            "Insira os estados separando-os por vírgula: "
        )
        estadosTemp = list(entrada.split(','))
        estados = list()
        for i in estadosTemp:
            if i not in estados:
                estados.append(i)
        print(estados)

        # Receber regras de transicao, estados incial e final
        try:
            # Receber regras de transicao
            regraDeTransicao = dict()
            print("Insira agora as transicoes de estados separados por vírgula: ")
            for i in estados:
                regraDeTransicao[i] = dict()
                for j in alfabeto:
                    dic = list()
                    entrada = list(input(str(i) + ": " + str(j) + "-> ").split(","))
                    for k in entrada:
                        if k != '':
                            if k not in estados:
                                raise EstadoNaoExiste()
                            elif k not in dic:
                                dic.append(k)

                    regraDeTransicao[i][j] = dic

            # Receber estado inicial
            estadoInicial = input("Digite o estado inicial: ")
            if estadoInicial not in estados:
                raise EstadoNaoExiste()

            # Receber estados finais
            estadosFinais = input(
                "Digite os estados finais separados por virgula: ")
            estadosFinais = estadosFinais.split(',')
            # verificar se nao foram digitados estados invalidos
            for i in estadosFinais:
                if i not in estados:
                    raise EstadoNaoExiste()
        except EstadoNaoExiste as e:
                raise Exception(e.mensagem)

        # Printar a funcao programa gerada
        printaFuncPrograma(alfabeto, regraDeTransicao,  3*len(estados), "AFN Gerado: ", 1)

        print("\nA conversao pode levar algum tempo, aguarde ...\n")
        # Iniciar a conversao e gerar todas as transiçoes
        estadosLinha = subConjunto(estados)
        print("pass")
        print("Mapeamento concluido")
        regraDeTransicaoLinha = dict()
        estadosFinaisLinha = list()
        for i in estadosLinha:
            regraDeTransicaoLinha["".join(i)] = {}
            for simbolo in alfabeto:
                novaTransicao = list()
                for q in i:
                    for h in regraDeTransicao[q][simbolo]:
                        if h not in novaTransicao:
                            novaTransicao.append(h)

                regraDeTransicaoLinha["".join(i)][simbolo] = sorted(novaTransicao)

        printaFuncPrograma(alfabeto, regraDeTransicaoLinha,  3*len(estados), "\nAFD intermediario: ", 2)

        # Gerar AFD com as transições necessarias
        estadosUtilizados = list()
        estadosRestantes = list()
        estadosRestantes.append(estadoInicial)

        while len(estadosRestantes) > 0:
            for estadoRestante in estadosRestantes:
                if estadoRestante not in estadosUtilizados:
                    estadosUtilizados.append(estadoRestante)
                    estadosRestantes.remove(estadoRestante)
                for simbolo in alfabeto:
                    transicao = list()
                    for t in regraDeTransicaoLinha["".join(estadoRestante)][simbolo]:
                        if t not in transicao:
                            transicao.append(t)
                    if transicao not in estadosRestantes and \
                       transicao not in estadosUtilizados:
                        estadosRestantes.append(transicao)

                    for n in estadosFinais:
                        if n in transicao:
                            if transicao not in estadosFinaisLinha:
                                estadosFinaisLinha.append(transicao)
        regraDeTransicaoLinhaFinal = dict()
        for key in regraDeTransicaoLinha:
            for estadoUtilizado in estadosUtilizados:
                if key == "".join(estadoUtilizado):
                    regraDeTransicaoLinhaFinal[key] = regraDeTransicaoLinha[key]

        printaFuncPrograma(alfabeto, regraDeTransicaoLinhaFinal, 3*len(estados), "\nAFD gerado: ", 2)
        print("\nEstadosFinais: ", end="")
        for i in estadosFinaisLinha:
            print("<"+"".join(i), end="> ")

        # Iniciar a traducao dos nomes dos estados
        cont = 0
        novosNomes = dict()
        for i in regraDeTransicaoLinhaFinal:
            if i != "":
                novosNomes[str(i)] = "P" + str(cont)
                cont += 1

        printaFuncPrograma(alfabeto, regraDeTransicaoLinhaFinal,  3*len(estados), "\nAFD Final: ", 3, novosNomes)
        # Printar dados do automato
        print("\n\nAlfabeto: " + str(alfabeto))
        print("Estado inicial: ", end="")
        print("<" + novosNomes[estadoInicial] + ">")
        print("Estados Finais: ", end="")
        for i in estadosFinaisLinha:
            print("<"+novosNomes["".join(i)], end="> ")

        # printar traducao
        print("\n\nTraducao gerada: ")
        for i in regraDeTransicaoLinhaFinal:
            if i != "":
                print((novosNomes[str(i)]).ljust(3) +  " - " + i)
        input()

     except KeyError:
        print("Abortando programa devido a erros: Tentativa de acesso a transicao nao existente")
     except Exception as e:
        print("Abortando programa devido a erros: %s" % str(e))
        input()
