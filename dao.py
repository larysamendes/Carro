from models import Carro, Usuario
import psycopg2.extras

SQL_DELETA_CARRO = 'delete from Carro where id = %s'
SQL_CARRO_POR_ID = 'SELECT id, marca, modelo, cor, combustivel, ano from carro where id = %s '
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_CARRO = 'UPDATE carro SET marca=%S, modelo=%S, cor=%S, combustivel=%S, ano=%s where id = %s'
SQL_BUSCA_CARROS = 'SELECT id, marca, modelo, cor, combustivel, ano from carro'
SQL_CRIA_CARRO = 'INSERT into carro (marca, modelo, cor, combustivel) values (%s %s %s %s %s) RETURNING id'
SQL_CRIA_USUARIO = 'INSERT into usuario (id, nome, senha) values (%s %s %s)'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET id=%s, nome=%s, senha=%s where id = %s'
SQL_AUTENTICAR_USUARIO = 'SELECT id, nome, senha from usuario where id = %s AND senha = %s'

class CarroDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, carro):
        cursor = self.__db.cursor()

        if(carro.id):
            cursor.execute(SQL_ATUALIZA_CARRO, (carro.marca, carro.modelo, carro.cor, carro.combustivel, carro.ano , carro.id))

        else:
            cursor.execute(SQL_CRIA_CARRO, (carro.marca, carro.modelo, carro.cor, carro.combustivel, carro.ano))
            carro.id = cursor.fetchone()[0]
        self.__db.commit()
        cursor.close()
        return carro

    def listar(self):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_BUSCA_CARROS)
        carros = traduz_carros(cursor.fetchall())
        cursor.close()
        return carros

    def busca_por_id(self, id):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        cursor.close()
        return Carro(tupla[1],tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])

    def deletar(self, id):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_DELETA_CARRO, (id,))
        self.__db.commit()
        cursor.close()

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fectchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def autenticar(self, id, senha):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_AUTENTICAR_USUARIO, (id, senha,))
        dados = cursor.fectchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def salvar(self, usuario):
        cursor = self.__db.cursor()

        #if (usuario.id)
            # cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        #else:
        cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        self.__db.commit()
        cursor.close()
        return usuario

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])

def traduz_carros(carros):
    def cria_carro_com_tupla(tupla):
        return Carro(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[0])
