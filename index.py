import os
import sqlite3

# limpar tela 
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# BANCO DE DADOS
def conectar():
    conexao = sqlite3.connect("alunos.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            media REAL NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


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

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO alunos (nome, media) VALUES (?, ?)",
            (nome, media)
        )
        conexao.commit()
        conexao.close()

        continuar = input("Adicionar outro aluno? (s/n): ").lower()
        if continuar == "n":
            break


# MOSTRAR
def mostrar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, media FROM alunos")
    alunos = cursor.fetchall()
    conexao.close()

    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    print("\nLista de alunos:")
    print("=" * 30)
    for aluno in alunos:
        print(f"{aluno['nome']} - {aluno['media']:.2f}")


# BUSCAR
def buscar_aluno():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, media FROM alunos")
    alunos = cursor.fetchall()
    conexao.close()

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
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, media FROM alunos")
    alunos = cursor.fetchall()

    if not alunos:
        print("Nenhum aluno cadastrado")
        conexao.close()
        return

    nome_busca = input("Digite o nome: ").lower()

    for aluno in alunos:
        if aluno["nome"].lower() == nome_busca:
            print(f"\n{aluno['nome']} - {aluno['media']:.2f}")

            nota1 = ler_nota("Nova nota 1: ")
            nota2 = ler_nota("Nova nota 2: ")
            nota3 = ler_nota("Nova nota 3: ")

            nova_media = (nota1 + nota2 + nota3) / 3

            cursor.execute(
                "UPDATE alunos SET media = ? WHERE id = ?",
                (nova_media, aluno["id"])
            )
            conexao.commit()
            conexao.close()

            print("Aluno atualizado!")
            return

    conexao.close()
    print("Aluno não encontrado")

# REMOVER
def remover_aluno():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, media FROM alunos")
    alunos = cursor.fetchall()

    if not alunos:
        print("Nenhum aluno cadastrado")
        conexao.close()
        return

    nome = input("Nome para remover: ").lower()

    for aluno in alunos:
        if aluno["nome"].lower() == nome:

            print(f"\n{aluno['nome']} - {aluno['media']:.2f}")

            while True:
                certeza = input("Confirmar remoção? (s/n): ").lower()

                if certeza == "s":
                    cursor.execute(
                        "DELETE FROM alunos WHERE id = ?",
                        (aluno["id"],)
                    )
                    conexao.commit()
                    conexao.close()
                    print("Removido com sucesso")
                    return
                elif certeza == "n":
                    conexao.close()
                    print("Cancelado")
                    return
                else:
                    print("Digite s ou n")

    conexao.close()
    print("Aluno não encontrado")


# STATUS FINAL
def mostrar_status():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, media FROM alunos")
    alunos = cursor.fetchall()
    conexao.close()

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
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, media FROM alunos ORDER BY media DESC, nome ASC")
    alunos = cursor.fetchall()
    conexao.close()

    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    print("\nRanking:")
    print("=" * 40)

    for i, aluno in enumerate(alunos, start=1):
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
criar_tabela()

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
