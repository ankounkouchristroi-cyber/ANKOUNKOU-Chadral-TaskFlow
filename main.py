from connexion import *
conn=obtenir_connexion()
if conn:
    print("vous etes connecte")
    fermer_connexion(conn)
else:
    print("la connexion a echoue")