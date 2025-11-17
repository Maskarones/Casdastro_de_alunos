import sys
sys.stdout.reconfigure(encoding='utf-8')

from BD import conectar, inserir, alterar, excluir, consultar


# FUNÇÃO PARA SALVAR TXT
def salvar_txt(nome_arquivo, dados):
    with open(nome_arquivo + ".txt", "w", encoding="utf-8") as f:

        if nome_arquivo == "alunos":
            f.write("LISTA DE ALUNOS\n\n")
            for a in dados:
                linha = (
                    "Matrícula: " + a[0] +
                    " | Nome: " + a[1] +
                    " | Nascimento: " + a[2] + "\n"
                )
                f.write(linha)

        elif nome_arquivo == "disciplinas":
            f.write("LISTA DE DISCIPLINAS\n\n")
            for d in dados:
                linha = (
                    "ID: " + str(d[0]) +
                    " | Nome: " + d[1] +
                    " | Turno: " + d[2] +
                    " | Sala: " + d[3] +
                    " | Professor: " + d[4] + "\n"
                )
                f.write(linha)

        elif nome_arquivo == "notas":
            f.write("LISTA DE NOTAS\n\n")

            alunos = consultar(conn, "SELECT * FROM ALUNO")
            disciplinas = consultar(conn, "SELECT * FROM DISCIPLINA")

            for n in dados:
                valor = n[1]
                matricula = n[2]
                disc_id = n[3]

                nome_aluno = next((a[1] for a in alunos if a[0] == matricula), "Desconhecido")
                nome_disc = next((d[1] for d in disciplinas if d[0] == disc_id), "Desconhecida")

                linha = (
                    "Nota: " + str(valor) +
                    " | Aluno: " + nome_aluno + " (" + matricula + ")" +
                    " | Disciplina: " + nome_disc + "\n"
                )
                f.write(linha)

        else:
            for item in dados:
                texto = " | ".join(str(x) for x in item)
                f.write(texto + "\n")



# BANCO – CRIAÇÃO DE TABELAS
conn = conectar()

inserir(conn, """
CREATE TABLE IF NOT EXISTS ALUNO (
    MATRICULA TEXT PRIMARY KEY,
    NOME TEXT,
    DT_NASCIMENTO TEXT
);
""")

inserir(conn, """
CREATE TABLE IF NOT EXISTS DISCIPLINA (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME TEXT,
    TURNO TEXT,
    SALA TEXT,
    PROFESSOR TEXT
);
""")

inserir(conn, """
CREATE TABLE IF NOT EXISTS NOTA (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    VALOR REAL,
    MATRICULA TEXT,
    DISCIPLINA_ID INTEGER
);
""")


# CRUD DISCIPLINA
def incluir_disciplina():
    nome = input("Nome da disciplina: ")
    turno = input("Turno: ")
    sala = input("Sala: ")
    professor = input("Professor: ")

    sql = f"INSERT INTO DISCIPLINA (NOME, TURNO, SALA, PROFESSOR) VALUES ('{nome}', '{turno}', '{sala}', '{professor}')"
    inserir(conn, sql)

    print("Disciplina cadastrada!")


def listar_disciplinas():
    dados = consultar(conn, "SELECT * FROM DISCIPLINA")
    print("\n--- LISTA DE DISCIPLINAS ---")
    existe = False
    num = 1

    for d in dados:
        print(f"{num} - ID: {d[0]} | Nome: {d[1]} | Turno: {d[2]} | Sala: {d[3]} | Professor: {d[4]}")
        num += 1
        existe = True

    if not existe:
        print("Nenhuma disciplina cadastrada.")

    salvar_txt("disciplinas", dados)


def alterar_disciplina():
    listar_disciplinas()
    pos = input("Número da disciplina: ")

    dados = consultar(conn, "SELECT * FROM DISCIPLINA")
    num = 1
    alvo = None

    for d in dados:
        if str(num) == pos:
            alvo = d[0]
        num += 1

    if alvo is None:
        print("Número inválido!")
        return

    nome = input("Novo nome: ")
    turno = input("Novo turno: ")
    sala = input("Nova sala: ")
    professor = input("Novo professor: ")

    sql = f"""
    UPDATE DISCIPLINA
    SET NOME='{nome}', TURNO='{turno}', SALA='{sala}', PROFESSOR='{professor}'
    WHERE ID={alvo}
    """

    alterar(conn, sql)
    print("Disciplina alterada!")


def excluir_disciplina():
    listar_disciplinas()
    pos = input("Número da disciplina para excluir: ")

    dados = consultar(conn, "SELECT * FROM DISCIPLINA")
    num = 1
    alvo = None

    for d in dados:
        if str(num) == pos:
            alvo = d[0]
        num += 1

    if alvo is None:
        print("Número inválido!")
        return

    excluir(conn, f"DELETE FROM DISCIPLINA WHERE ID={alvo}")
    print("Disciplina excluída!")


# CRUD ALUNO
def incluir_aluno():
    matricula = input("Matrícula: ")
    nome = input("Nome: ")
    nasc = input("Nascimento: ")

    sql = f"INSERT INTO ALUNO VALUES ('{matricula}', '{nome}', '{nasc}')"
    inserir(conn, sql)
    print("Aluno cadastrado!")


def listar_alunos():
    dados = consultar(conn, "SELECT * FROM ALUNO")
    print("\n--- LISTA DE ALUNOS ---")
    existe = False
    num = 1

    for a in dados:
        print(f"{num} - Matrícula: {a[0]} | Nome: {a[1]} | Data Nasc.: {a[2]}")
        num += 1
        existe = True

    if not existe:
        print("Nenhum aluno cadastrado.")

    salvar_txt("alunos", dados)


def alterar_aluno():
    listar_alunos()
    pos = input("Número do aluno: ")

    dados = consultar(conn, "SELECT * FROM ALUNO")
    num = 1
    alvo = None

    for a in dados:
        if str(num) == pos:
            alvo = a[0]
        num += 1

    if alvo is None:
        print("Número inválido!")
        return

    nome = input("Novo nome: ")
    nasc = input("Nova data de nascimento: ")

    sql = f"UPDATE ALUNO SET NOME='{nome}', DT_NASCIMENTO='{nasc}' WHERE MATRICULA='{alvo}'"
    alterar(conn, sql)
    print("Aluno alterado!")


def excluir_aluno():
    listar_alunos()
    pos = input("Número do aluno para excluir: ")

    dados = consultar(conn, "SELECT * FROM ALUNO")
    num = 1
    alvo = None

    for a in dados:
        if str(num) == pos:
            alvo = a[0]
        num += 1

    if alvo is None:
        print("Número inválido!")
        return

    excluir(conn, f"DELETE FROM ALUNO WHERE MATRICULA='{alvo}'")
    print("Aluno excluído!")


# CRUD NOTA
def incluir_nota():
    listar_alunos()
    mat = input("Escolha a matrícula: ")

    listar_disciplinas()
    pos = input("Número da disciplina: ")

    dados = consultar(conn, "SELECT * FROM DISCIPLINA")
    num = 1
    disc_id = None

    for d in dados:
        if str(num) == pos:
            disc_id = d[0]
        num += 1

    if disc_id is None:
        print("Disciplina inválida!")
        return

    valor = input("Nota: ")

    sql = f"INSERT INTO NOTA (VALOR, MATRICULA, DISCIPLINA_ID) VALUES ('{valor}', '{mat}', {disc_id})"
    inserir(conn, sql)
    print("Nota cadastrada!")


def listar_notas():
    dados_notas = consultar(conn, "SELECT * FROM NOTA")
    alunos = consultar(conn, "SELECT * FROM ALUNO")
    disciplinas = consultar(conn, "SELECT * FROM DISCIPLINA")

    print("\n--- LISTA DE NOTAS ---")
    existe = False
    num = 1

    for n in dados_notas:
        valor = n[1]
        matricula = n[2]
        disc_id = n[3]

        nome_aluno = next((a[1] for a in alunos if a[0] == matricula), "Desconhecido")
        nome_disc = next((d[1] for d in disciplinas if d[0] == disc_id), "Desconhecida")

        print(f"{num} - Nota: {valor} | Aluno: {nome_aluno} ({matricula}) | Disciplina: {nome_disc}")
        num += 1
        existe = True

    if not existe:
        print("Nenhuma nota cadastrada.")

    salvar_txt("notas", dados_notas)


def alterar_nota():
    listar_notas()
    pos = input("Número da nota: ")

    dados = consultar(conn, "SELECT * FROM NOTA")
    num = 1
    alvo = None

    for n in dados:
        if str(num) == pos:
            alvo = n[0]
        num += 1

    if alvo is None:
        print("Número inválido!")
        return

    novo_valor = input("Novo valor da nota: ")

    sql = f"UPDATE NOTA SET VALOR='{novo_valor}' WHERE ID={alvo}"
    alterar(conn, sql)
    print("Nota alterada!")


def excluir_nota():
    listar_notas()
    pos = input("Número da nota: ")

    dados = consultar(conn, "SELECT * FROM NOTA")
    num = 1
    alvo = None

    for n in dados:
        if str(num) == pos:
            alvo = n[0]
        num += 1

    if alvo is None:
        print("Número inválido!")
        return

    excluir(conn, f"DELETE FROM NOTA WHERE ID={alvo}")
    print("Nota excluída!")


# MENUS
def menu():
    print("\n1 - Disciplinas")
    print("2 - Alunos")
    print("3 - Notas")
    print("4 - Sair")
    return input("Escolha: ")


def menu_simples(nome):
    print("\n---", nome, "---")
    print("1 - Incluir")
    print("2 - Listar")
    print("3 - Alterar")
    print("4 - Excluir")
    print("5 - Voltar")
    return input("Escolha: ")


# LOOP PRINCIPAL
opcao = "0"
while opcao != "4":
    opcao = menu()

    if opcao == "1":
        sub = "0"
        while sub != "5":
            sub = menu_simples("DISCIPLINAS")
            if sub == "1": incluir_disciplina()
            if sub == "2": listar_disciplinas()
            if sub == "3": alterar_disciplina()
            if sub == "4": excluir_disciplina()

    if opcao == "2":
        sub = "0"
        while sub != "5":
            sub = menu_simples("ALUNOS")
            if sub == "1": incluir_aluno()
            if sub == "2": listar_alunos()
            if sub == "3": alterar_aluno()
            if sub == "4": excluir_aluno()

    if opcao == "3":
        sub = "0"
        while sub != "5":
            sub = menu_simples("NOTAS")
            if sub == "1": incluir_nota()
            if sub == "2": listar_notas()
            if sub == "3": alterar_nota()
            if sub == "4": excluir_nota()

print("Saindo...")



