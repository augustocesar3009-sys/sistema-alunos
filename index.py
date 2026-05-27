import os
import json

# limpar tela 
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

alunos = []


# CARREGAR / SALVAR
def carregar_alunos():
    if os.path.exists("alunos.json"):
        with open("alunos.json", "r") as arquivo:
            dados = json.load(arquivo)
            alunos.clear()
            alunos.extend(dados)

def salvar_alunos():
    with open("alunos.json", "w") as arquivo:
        json.dump(alunos, arquivo, indent=4)


# UTILIDADES
def ler_nota(texto):
    while True:
        try:
            return float(input(texto))
        except:
            print("Digite um número válido!")


# CADASTRAR
def cadastrar_alunos():
    while True:
        nome = input("Nome do aluno: ")

        nota1 = ler_nota("Nota 1: ")
        nota2 = ler_nota("Nota 2: ")
        nota3 = ler_nota("Nota 3: ")

        media = (nota1 + nota2 + nota3) / 3

        print(f"\nNome: {nome}")
        print(f"Média: {media:.2f}")

        while True:
            certeza = input("Confirmar cadastro? (s/n): ").lower()

            if certeza == "s":
                break
            elif certeza == "n":
                print("Cadastro cancelado")
                return
            else:
                print("Digite s ou n")

        aluno = {
            "nome": nome,
            "media": media
        }

        alunos.append(aluno)
        salvar_alunos()

        continuar = input("Adicionar outro aluno? (s/n): ").lower()
        if continuar == "n":
            break


# MOSTRAR
def mostrar_alunos():
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    print("\nLista de alunos:")
    print("=" * 30)
    for aluno in alunos:
        print(f"{aluno['nome']} - {aluno['media']:.2f}")


# BUSCAR
def buscar_aluno():
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    nome_busca = input("Digite o nome: ").lower()
    encontrado = False

    for aluno in alunos:
        if nome_busca in aluno["nome"].lower():
            print(f"{aluno['nome']} - {aluno['media']:.2f}")
            encontrado = True

    if not encontrado:
        print("Aluno não encontrado")


# EDITAR
def editar_aluno():
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    nome_busca = input("Digite o nome: ").lower()

    for aluno in alunos:
        if aluno["nome"].lower() == nome_busca:
            print(f"\n{aluno['nome']} - {aluno['media']:.2f}")

            nota1 = ler_nota("Nova nota 1: ")
            nota2 = ler_nota("Nova nota 2: ")
            nota3 = ler_nota("Nova nota 3: ")

            aluno["media"] = (nota1 + nota2 + nota3) / 3
            salvar_alunos()

            print("Aluno atualizado!")
            return

    print("Aluno não encontrado")

# REMOVER
def remover_aluno():
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    nome = input("Nome para remover: ").lower()

    for aluno in alunos:
        if aluno["nome"].lower() == nome:

            print(f"\n{aluno['nome']} - {aluno['media']:.2f}")

            while True:
                certeza = input("Confirmar remoção? (s/n): ").lower()

                if certeza == "s":
                    alunos.remove(aluno)
                    salvar_alunos()
                    print("Removido com sucesso")
                    return
                elif certeza == "n":
                    print("Cancelado")
                    return
                else:
                    print("Digite s ou n")

    print("Aluno não encontrado")


# STATUS FINAL
def mostrar_status():
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    print("\nStatus dos alunos:")
    print("=" * 40)

    for aluno in alunos:
        status = "Aprovado" if aluno["media"] >= 6 else "Reprovado"
        print(f"{aluno['nome']:<10} | {aluno['media']:.2f} | {status}")


# RANKING
def ranking_alunos():
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    print("\nRanking:")
    print("=" * 40)

    ordenados = sorted(alunos, key=lambda x: (-x["media"], x["nome"]))

    for i, aluno in enumerate(ordenados, start=1):
        print(f"{i:>2}º | {aluno['nome']:<10} | {aluno['media']:.2f}")


# MENU
def mostrar_menu():
    print("=" * 30)
    print("   SISTEMA DE ALUNOS")
    print("=" * 30)
    print("1 - Cadastrar")
    print("2 - Mostrar")
    print("3 - Buscar")
    print("4 - Remover")
    print("5 - Status")
    print("6 - Editar")
    print("7 - Ranking")
    print("8 - Sair")
    print("=" * 30)


# EXECUÇÃO
carregar_alunos()

while True:
    limpar_tela()
    mostrar_menu()

    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_alunos()
    elif opcao == "2":
        mostrar_alunos()
    elif opcao == "3":
        buscar_aluno()
    elif opcao == "4":
        remover_aluno()
    elif opcao == "5":
        mostrar_status()
    elif opcao == "6":
        editar_aluno()
    elif opcao == "7":
        ranking_alunos()
    elif opcao == "8":
        break
    else:
        print("Opção inválida")

    input("\nPressione ENTER para continuar...")