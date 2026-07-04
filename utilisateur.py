
import hashlib
from connexion import obtenir_connexion, fermer_connexion
from mysql.connector import Error

def hasher_mdp(mot_de_passe):
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()

def verifier_mdp(mot_de_passe_saisi, hash_stocke):
    return hasher_mdp(mot_de_passe_saisi) == hash_stocke


def inscrire_utilisateur(nom_utilisateur, email, mot_de_passe, confirmation):
    if mot_de_passe != confirmation:
        print(" Les mots de passe ne correspondent pas.")
        return False
    
    if not nom_utilisateur.strip():
        print(" Le nom d'utilisateur ne peut pas être vide.")
        return False
    
    if email and '@' not in email:
        print(" L'adresse email n'est pas valide.")
        return False
    
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        sql_check = "SELECT id_user FROM UTILISATEUR WHERE nom_utilisateur = %s"
        cursor.execute(sql_check, (nom_utilisateur,))
        if cursor.fetchone():
            print(f" Le nom d'utilisateur '{nom_utilisateur}' est déjà pris.")
            return False
        
        if email:
            sql_check_email = "SELECT id_user FROM UTILISATEUR WHERE email = %s"
            cursor.execute(sql_check_email, (email,))
            if cursor.fetchone():
                print(f" L'email '{email}' est déjà utilisé.")
                return False
        
        mot_de_passe_hash = hasher_mdp(mot_de_passe)
        
        sql = """
            INSERT INTO UTILISATEUR (nom_utilisateur, mot_de_passe, email) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nom_utilisateur, mot_de_passe_hash, email if email else None))
        conn.commit()
        
        print(f" Utilisateur '{nom_utilisateur}' inscrit avec succès !")
        return True
        
    except Error as e:
        print(f" Erreur lors de l'inscription : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)



def connecter_utilisateur(nom_utilisateur, mot_de_passe):
    if not nom_utilisateur.strip():
        print(" Veuillez entrer un nom d'utilisateur.")
        return None
    
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT id_user, nom_utilisateur, mot_de_passe, email 
            FROM UTILISATEUR 
            WHERE nom_utilisateur = %s
        """
        cursor.execute(sql, (nom_utilisateur,))
        utilisateur = cursor.fetchone()
        
        if not utilisateur:
            print(f" Utilisateur '{nom_utilisateur}' introuvable.")
            return None
        
        if not verifier_mdp(mot_de_passe, utilisateur['mot_de_passe']):
            print(" Mot de passe incorrect.")
            return None
        

        del utilisateur['mot_de_passe']
        
        print(f" Connexion réussie ! Bienvenue {utilisateur['nom_utilisateur']} !")
        return utilisateur
        
    except Error as e:
        print(f" Erreur lors de la connexion : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)



def deconnecter_utilisateur():
    print(" Déconnexion réussie !")
    return True



def test_utilisateur():
    print(" Test du module utilisateur")
    print("-" * 40)
    
    print("\n Test 1 - Hashage :")
    mdp = "monMotDePasse123"
    hash_mdp = hasher_mdp(mdp)
    print(f"   Mot de passe : {mdp}")
    print(f"   Hash : {hash_mdp}")
    print(f"   Vérification : {' OK' if verifier_mdp(mdp, hash_mdp) else ' Échec'}")
    
    print("\n Test 2 - Inscription :")
    inscrire_utilisateur("test_user", "test@email.com", "password123", "password123")
    
    print("\n Test 3 - Connexion :")
    user = connecter_utilisateur("test_user", "password123")
    if user:
        print(f"   Utilisateur connecté : {user}")

if __name__ == "__main__":
    test_utilisateur()