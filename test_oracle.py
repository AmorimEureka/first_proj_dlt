import oracledb
import os

# Usa modo thick para conectar com o Instant Client
oracledb.init_oracle_client(lib_dir="/.oracle/instantclient_19_23")

try:
    connection = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
    )
    print("✅ Conectado com sucesso ao Oracle!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT SYSDATE FROM DUAL")
        result = cursor.fetchone()
        print(f"🕒 Data e hora atual no Oracle: {result[0]}")

    connection.close()
except Exception as e:
    print(f"❌ Erro ao conectar ou executar query: {e}")
