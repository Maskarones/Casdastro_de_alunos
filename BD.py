import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

def inserir(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def consultar(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def alterar(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def excluir(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
