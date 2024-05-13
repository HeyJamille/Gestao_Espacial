import sqlite3
import datetime

# Conexão
def connect_db():
  try:
    conn = sqlite3.connect('database.db')
    print("Conexão bem-sucedida")
    return conn
  except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)
    return None

# Cria tabela
def create_table():
  conn = connect_db()

  if conn:
    try:
      conn.execute('''
        CREATE TABLE IF NOT EXISTS missoes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_lancamento DATE NOT NULL,
        destino TEXT NOT NULL,
        estado TEXT NOT NULL,
        tripulacao TEXT NOT NULL,
        carga_util TEXT NOT NULL,
        duracao INTERVAL NOT NULL,
        custo DECIMAL NOT NULL,
        status TEXT NOT NULL
      );
      ''')
      print("Tabela criada com sucesso")

    except Exception as e:
      print("Erro ao criar tabela:", e)

    finally:
      conn.close()

# Seleciona missões dentro de um intervalo de datas
def get_search(data_inicial, data_final):
  items = []
  message = None

  try:
    conn = connect_db()

    if conn:
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()

      # Se necessário, converte as datas para o formato apropriado
      data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
      data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()

      cursor.execute('''
                    SELECT nome, destino, estado  
                    FROM missoes 
                    WHERE data_lancamento BETWEEN ? AND ?
                    ''', (data_inicial, data_final))
      rows = cursor.fetchall()

      for row in rows:
        item = {
          'nome': row['nome'],
          'destino': row['destino'],
          'estado': row['estado']
        }
        items.append(item)

        if not items:
          message = "Nenhuma missão encontrada dentro do intervalo de datas especificado."

  except Exception as e:
    message = f"Erro ao visualizar missões: {e}"

  finally:
    if conn:
      conn.close()

  if message:
    return {'error': message}
  else:
    return items

# Lista todas as missões
def get_all():
  results = []
  conn = connect_db()

  if conn:
    try:
      cursor = conn.cursor()
      cursor.execute('''SELECT nome, destino, estado 
                     FROM missoes
                     ORDER BY data_lancamento DESC
                     ''')
      results = cursor.fetchall()

    except Exception as e:
      print("Erro ao listar todas as missões:", e)

    finally:
      conn.close()

  return results

# Insere uma missão 
def insert(item):
  inserted_item = {}

  try:
    conn = connect_db()
    if conn:
      cursor = conn.cursor()
      cursor.execute(''' 
          INSERT INTO missoes (nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
          ''', (item['nome'], item['data_lancamento'], item['destino'], item['estado'],
                item['tripulacao'], item['carga_util'], item['duracao'], item['custo'], item['status']))
      conn.commit()
      inserted_item = {'id': cursor.lastrowid, **item}

  except Exception as e:
    print("Erro ao inserir missão:", e)
    conn.rollback()

  finally:
    if conn:
      conn.close()

  return inserted_item

# Atualiza uma missão
def update(item):
  update_item = {}

  try:
    conn = connect_db()
    if conn:
      cursor = conn.cursor()
      cursor.execute('''
          UPDATE missoes
          SET nome = ?, data_lancamento = ?, destino = ?, estado = ?, tripulacao = ?, carga_util = ?,
          duracao = ?, custo = ?, status = ?
          WHERE id = ?;
          ''', (item['nome'], item['data_lancamento'], item['destino'], item['estado'],
                item['tripulacao'], item['carga_util'], item['duracao'], item['custo'], item['status'], item['id']))
      conn.commit()
      update_item = get_search(item['id'])
  
  except Exception as e:
    print("Erro ao atualizar missão:", e)
  
  finally:
    if conn:
      conn.close()

  return update_item

# Deleta uma missão
def delete(id):
  message = {}

  try:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
                  DELETE FROM missoes 
                  WHERE id = ?; 
                  ''', (id, ))
    conn.commit()

    # Reinicia o contador de ID quando não houver nenhuma missão no banco
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='missoes';")
    conn.commit()
    print("IDs reiniciados com sucesso.")
    
    message['Estado'] = "Missao deletada com sucesso!"

  except Exception as e:
    message['Estado'] = f"Erro ao deletar a missão: {e}"

  finally:
    if conn:
      conn.close()

  return message

