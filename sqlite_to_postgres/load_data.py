import os
import io
import csv
import sqlite3
import psycopg2


def get_headers(cur: sqlite3.Cursor) -> dict:
    """Вернет словарь. Ключ - название таблицы, значение - поля таблицы."""
    query = cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
    table_names = [name[0] for name in query]
    headers = dict.fromkeys(table_names)
    for table in table_names:
        table_info = cur.execute(f'SELECT * FROM {table}')
        headers[table] = tuple(map(lambda x: x[0], table_info.description))
    return headers


def get_data_from_sqlite(cur: sqlite3.Cursor, table: str, size: int) -> list:
    """Вернет данные из таблицы table в виде списка коретежей."""
    query = cur.execute(f'SELECT * FROM {table}')
    data = []
    while True:
        query_result = query.fetchmany(size)
        if not query_result:
            break
        for row in query_result:
            data.append(row)
    return data


def put_data_to_postgres(dsn: dict, data: list, columns: str, table: str) -> None:
    """Вставит в таблицу table данные методом множественной вставки."""
    with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
        fake_csv = io.StringIO()
        fake_writer = csv.writer(fake_csv, delimiter='|')
        fake_writer.writerows(data)
        fake_csv.seek(0)
        try:
            cursor.execute(f'TRUNCATE {table} CASCADE;')
            cursor.copy_from(fake_csv, table, sep='|', null='', columns=columns)
            conn.commit()
            print(f"Success copy data to table: '{table}'")
        except Exception as e:
            print(f"Something went wrong: {e}")
    conn.close()


def main() -> None:
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    dsn = {
        'dbname': 'movies',
        'user': 'postgres',
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': '127.0.0.1',
        'port': 5432,
        'options': os.environ.get('POSTGRES_OPTIONS')
    }
    headers = get_headers(cur)
    size = 50
    
    try:
        for table, columns in headers.items():
            data = get_data_from_sqlite(cur, table, size)
            put_data_to_postgres(dsn, data, columns, table)
    finally:
        con.close()
    
if __name__ == '__main__':
    main()

