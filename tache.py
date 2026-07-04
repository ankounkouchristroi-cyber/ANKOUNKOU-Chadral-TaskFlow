from connexion import obtenir_connexion, fermer_connexion
from mysql.connector import Error
from affichage import afficher_erreur, afficher_info, afficher_succes, afficher_alerte

def ajouter_tache(id_user, titre, description, date_echeance, priorite, id_categorie=None):
    if not titre.strip():
        afficher_erreur("Le titre est obligatoire.")
        return None
    
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        sql = """INSERT INTO TACHE (titre, description, date_echeance, priorite, id_user, id_categorie) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        valeurs = (titre.strip(), description.strip() if description else None, 
                   date_echeance if date_echeance else None, priorite, id_user, id_categorie)
        
        cursor.execute(sql, valeurs)
        conn.commit()
        
        id_tache = cursor.lastrowid
        afficher_succes(f"Tache '{titre}' ajoutee avec succes (ID: {id_tache}).")
        return id_tache
        
    except Error as e:
        afficher_erreur(f"Erreur lors de l'ajout de la tache : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def lister_taches(id_user, tri_par_priorite=True):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s
        """
        
        if tri_par_priorite:
            sql += " ORDER BY FIELD(t.priorite, 'urgente', 'haute', 'normale', 'basse'), t.date_echeance ASC"
        else:
            sql += " ORDER BY t.date_creation DESC"
        
        cursor.execute(sql, (id_user,))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur lors du listage des taches : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def voir_detail_tache(id_user, id_tache):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_tache = %s AND t.id_user = %s
        """
        cursor.execute(sql, (id_tache, id_user))
        tache = cursor.fetchone()
        
        if not tache:
            afficher_erreur("Tache introuvable ou vous n'avez pas les droits.")
            return None
        
        sql_etiquettes = """
            SELECT e.nom_etiquette 
            FROM ETIQUETTE e
            JOIN TACHE_ETIQUETTE te ON e.id_etiquette = te.id_etiquette
            WHERE te.id_tache = %s AND e.id_user = %s
        """
        cursor.execute(sql_etiquettes, (id_tache, id_user))
        etiquettes = cursor.fetchall()
        
        tache['etiquettes'] = [e['nom_etiquette'] for e in etiquettes]
        return tache
        
    except Error as e:
        afficher_erreur(f"Erreur lors de la recuperation de la tache : {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def modifier_tache(id_user, id_tache, titre=None, description=None, 
                   date_echeance=None, priorite=None, id_categorie=None):
    if not verifier_propriete_tache(id_user, id_tache):
        return False
    
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        champs = []
        valeurs = []
        
        if titre is not None:
            champs.append("titre = %s")
            valeurs.append(titre.strip() if titre.strip() else None)
        
        if description is not None:
            champs.append("description = %s")
            valeurs.append(description.strip() if description.strip() else None)
        
        if date_echeance is not None:
            champs.append("date_echeance = %s")
            valeurs.append(date_echeance if date_echeance else None)
        
        if priorite is not None:
            champs.append("priorite = %s")
            valeurs.append(priorite)
        
        if id_categorie is not None:
            champs.append("id_categorie = %s")
            valeurs.append(id_categorie)
        
        if not champs:
            afficher_info("Aucune modification specifiee.")
            return False
        
        valeurs.append(id_tache)
        
        sql = f"UPDATE TACHE SET {', '.join(champs)} WHERE id_tache = %s"
        cursor.execute(sql, valeurs)
        conn.commit()
        
        afficher_succes("Tache modifiee avec succes.")
        return True
        
    except Error as e:
        afficher_erreur(f"Erreur lors de la modification : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def changer_statut(id_user, id_tache, nouveau_statut, commentaire=None):
    if not verifier_propriete_tache(id_user, id_tache):
        return False
    
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return False
        
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT statut FROM TACHE WHERE id_tache = %s"
        cursor.execute(sql, (id_tache,))
        resultat = cursor.fetchone()
        
        if not resultat:
            afficher_erreur("Tache introuvable.")
            return False
        
        ancien_statut = resultat['statut']
        if ancien_statut == nouveau_statut:
            afficher_info(f"La tache a deja le statut '{nouveau_statut}'.")
            return False
        
        sql_update = "UPDATE TACHE SET statut = %s WHERE id_tache = %s"
        cursor.execute(sql_update, (nouveau_statut, id_tache))
        sql_historique = """
            INSERT INTO HISTORIQUE (id_tache, ancien_statut, nouveau_statut, commentaire) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_historique, (id_tache, ancien_statut, nouveau_statut, commentaire))
        
        conn.commit()
        afficher_succes(f"Statut change de '{ancien_statut}' a '{nouveau_statut}'.")
        return True
        
    except Error as e:
        afficher_erreur(f"Erreur lors du changement de statut : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def supprimer_tache(id_user, id_tache, confirmation=False):
    if not verifier_propriete_tache(id_user, id_tache):
        return False
    
    if not confirmation:
        afficher_alerte("Suppression annulee.")
        return False
    
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        sql = "DELETE FROM TACHE WHERE id_tache = %s AND id_user = %s"
        cursor.execute(sql, (id_tache, id_user))
        conn.commit()
        
        afficher_succes("Tache supprimee avec succes.")
        return True
        
    except Error as e:
        afficher_erreur(f"Erreur lors de la suppression : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def verifier_propriete_tache(id_user, id_tache):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return False
        
        cursor = conn.cursor()
        sql = "SELECT id_tache FROM TACHE WHERE id_tache = %s AND id_user = %s"
        cursor.execute(sql, (id_tache, id_user))
        resultat = cursor.fetchone()
        
        if not resultat:
            afficher_erreur("Tache introuvable ou vous n'avez pas les droits.")
            return False
        return True
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def filtrer_taches_par_statut(id_user, statut):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s AND t.statut = %s
            ORDER BY FIELD(t.priorite, 'urgente', 'haute', 'normale', 'basse'), t.date_echeance ASC
        """
        cursor.execute(sql, (id_user, statut))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def filtrer_taches_par_priorite(id_user, priorite):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s AND t.priorite = %s
            ORDER BY t.date_echeance ASC
        """
        cursor.execute(sql, (id_user, priorite))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def filtrer_taches_par_categorie(id_user, id_categorie):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s AND t.id_categorie = %s
            ORDER BY FIELD(t.priorite, 'urgente', 'haute', 'normale', 'basse'), t.date_echeance ASC
        """
        cursor.execute(sql, (id_user, id_categorie))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def rechercher_taches_par_mot_cle(id_user, mot_cle):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s AND (t.titre LIKE %s OR t.description LIKE %s)
            ORDER BY FIELD(t.priorite, 'urgente', 'haute', 'normale', 'basse'), t.date_echeance ASC
        """
        motif = f"%{mot_cle}%"
        cursor.execute(sql, (id_user, motif, motif))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def taches_en_retard(id_user):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s 
              AND t.date_echeance < CURDATE() 
              AND t.statut NOT IN ('terminee', 'annulee')
            ORDER BY t.date_echeance ASC
        """
        cursor.execute(sql, (id_user,))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def taches_du_jour(id_user):
    conn = None
    cursor = None
    
    try:
        conn = obtenir_connexion()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT t.*, c.nom_categorie 
            FROM TACHE t
            LEFT JOIN CATEGORIE c ON t.id_categorie = c.id_categorie
            WHERE t.id_user = %s AND t.date_echeance = CURDATE()
            ORDER BY FIELD(t.priorite, 'urgente', 'haute', 'normale', 'basse')
        """
        cursor.execute(sql, (id_user,))
        return cursor.fetchall()
        
    except Error as e:
        afficher_erreur(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            fermer_connexion(conn)

def test_tache():
    print("Test du module tache")
    print("-" * 40)
    
    id_user = 1
    
    print("\nTest 1 - Ajouter une tache :")
    id_tache = ajouter_tache(
        id_user, 
        "Tache de test", 
        "Description de la tache de test", 
        "2025-12-31", 
        "haute"
    )
    
    if id_tache:
        print(f"Tache ajoutee avec l'ID: {id_tache}")
    
    print("\nTest 2 - Lister les taches :")
    taches = lister_taches(id_user)
    if taches:
        print(f"{len(taches)} tache(s) trouvee(s)")
        for t in taches[:3]:
            print(f"  - {t['titre']} ({t['statut']})")
    
    print("\nTest 3 - Voir le detail d'une tache :")
    if id_tache:
        detail = voir_detail_tache(id_user, id_tache)
        if detail:
            print(f"Detail de la tache : {detail['titre']}")
            print(f"  Description: {detail.get('description', 'Aucune')}")
            print(f"  Priorite: {detail['priorite']}")
            print(f"  Statut: {detail['statut']}")
    
    print("\nTest 4 - Changer le statut :")
    if id_tache:
        changer_statut(id_user, id_tache, "en_cours", "Debut du travail")
    
    print("\nTest 5 - Modifier une tache :")
    if id_tache:
        modifier_tache(id_user, id_tache, titre="Tache de test modifiee")
    
    print("\nTest 6 - Supprimer une tache :")
    if id_tache:
        supprimer_tache(id_user, id_tache, confirmation=True)

if __name__ == "__main__":
    test_tache()