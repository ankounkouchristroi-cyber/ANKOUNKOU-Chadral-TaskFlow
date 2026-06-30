import mysql.connector 
from mysql.connector import Error
CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"",
    "database":"taskflow_db",
    "charset":"utf8mb4"
}
def obtenir_connexion():
    try:
        conn=mysql.connector.connect(**CONFIG)
        if conn:
            return conn
    except Error as e:
        print(f"Erreur de connexion: {e}")
    return None

def fermer_connexion(conn):
    if conn:
        conn.close()
        print("connexion ferme avec succes")
    
def test_connexion():
    conn = obtenir_connexion()
    if conn:
        print(" Connexion reussie !")
        fermer_connexion(conn)
    else:
        print(" La connexion a échoué")


if __name__ == "__main__":
    test_connexion()