import psycopg2
import os
from dotenv import load_dotenv

def add_gain(dados):

    try:
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")
        # db_port = os.getenv("DB_PORT")
        conexao = psycopg2.connect(
            host=db_host, database=db_database, user=db_user, password=db_password
        )

        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO financeiro.gain (category, value, description, date) VALUES (%s,%s,%s, now())",
            (dados["category"], dados["value"], dados["description"]),
        )
        conexao.commit()
        return True

    except Exception as e:
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()


def add_spent(dados):
    try:
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")
        # db_port = os.getenv("DB_PORT")
        conexao = psycopg2.connect(
            host=db_host, database=db_database, user=db_user, password=db_password
        )

        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO financeiro.spent (category, payment_method, value, description, date) VALUES (%s,%s,%s,%s, now())",
            (
                dados["category"],
                dados["payment_method"],
                dados["value"],
                dados["description"],
            ),
        )
        conexao.commit()
        return True

    except Exception as e:
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()


def get_last():
    pass


def delete(dados):
    try:
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")
        # db_port = os.getenv("DB_PORT")
        conexao = psycopg2.connect(
            host=db_host, database=db_database, user=db_user, password=db_password
        )

        cursor = conexao.cursor()
        cursor.execute(
            f"DELETE FROM financeiro.{dados['local']} WHERE id = (SELECT max(id) FROM financeiro.{dados['local']})"
        )
        conexao.commit()
        return True

    except Exception as e:
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()