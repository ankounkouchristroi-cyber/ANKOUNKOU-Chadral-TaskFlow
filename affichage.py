
import os

ROUGE = "\033[91m"
VERT = "\033[92m"
JAUNE = "\033[93m"
BLEU = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BLANC = "\033[97m"
RESET = "\033[0m"


GRAS = "\033[1m"
SOULIGNE = "\033[4m"


couleurs_priorite = {
    "basse": BLEU,
    "normale": BLANC,
    "haute": JAUNE,
    "urgente": ROUGE
}


symboles_statut = {
    "a_faire": "[ ]",
    "en_cours": "[~]",
    "terminee": "[X]",
    "annulee": "[-]"
}

couleurs_statut = {
    "a_faire": BLANC,
    "en_cours": JAUNE,
    "terminee": VERT,
    "annulee": ROUGE
}


def vider_ecran():
    os.system("cls" if os.name == "nt" else "clear")

def afficher_succes(message):
    print(f"{VERT}{GRAS}[OK]{RESET}{message}")

def afficher_erreur(message):
    print(f"{ROUGE}{GRAS}[ERREUR]{RESET}{message}")

def afficher_info(message):
    print(f"{CYAN}[INFO]{RESET}{message}")

def afficher_alerte(message):
    print(f"{JAUNE}{GRAS}[!]{RESET}{message}")

def afficher_separateur(caractere="=", longueur=50):
    print(caractere * longueur)

def afficher_titre(titre, couleur=BLEU):
    print(f"{couleur}{GRAS}{titre}{RESET}")

def afficher_sous_titre(titre):
    print(f"\n{GRAS}--- {titre} ---{RESET}")


def afficher_menu_accueil():
    vider_ecran()
    afficher_separateur()
    print(f"{BLEU}{GRAS}          TASKFLOW - Gestionnaire de Tâches{RESET}")
    afficher_separateur()
    print(f"{GRAS}1.{RESET} Inscription")
    print(f"{GRAS}2.{RESET} Connexion")
    print(f"{GRAS}0.{RESET} {ROUGE}Quitter{RESET}")
    afficher_separateur()
    return input("Votre choix : ")

def afficher_menu_principal(nom_utilisateur):
    vider_ecran()
    afficher_separateur()
    print(f"{BLEU}{GRAS} TASKFLOW - Bienvenue, {nom_utilisateur}{RESET}")
    afficher_separateur()
    print(f"{GRAS}1.{RESET} Voir toutes mes tâches")
    print(f"{GRAS}2.{RESET} Ajouter une nouvelle tâche")
    print(f"{GRAS}3.{RESET} Modifier une tâche")
    print(f"{GRAS}4.{RESET} Changer le statut d'une tâche")
    print(f"{GRAS}5.{RESET} Supprimer une tâche")
    print(f"{GRAS}6.{RESET} Gérer mes catégories")
    print(f"{GRAS}7.{RESET} Gérer mes étiquettes")
    print(f"{GRAS}8.{RESET} Voir l'historique d'une tâche")
    print(f"{GRAS}9.{RESET} Rechercher des tâches")
    print(f"{GRAS}10.{RESET} Statistiques personnelles")
    print(f"{GRAS}0.{RESET} {ROUGE}Se déconnecter{RESET}")
    afficher_separateur()
    return input("Votre choix : ")

def afficher_menu_recherche():
    print("\n" + "-" * 40)
    print(f"{GRAS}🔍 Recherche de tâches{RESET}")
    print("-" * 40)
    print(f"{GRAS}1.{RESET} Filtrer par statut")
    print(f"{GRAS}2.{RESET} Filtrer par priorité")
    print(f"{GRAS}3.{RESET} Filtrer par catégorie")
    print(f"{GRAS}4.{RESET} Recherche par mot-clé")
    print(f"{GRAS}5.{RESET} Tâches en retard")
    print(f"{GRAS}6.{RESET} Tâches du jour")
    print(f"{GRAS}0.{RESET} {ROUGE}Retour{RESET}")
    print("-" * 40)
    return input("Votre choix : ")

def afficher_menu_categories():
    print("\n" + "-" * 40)
    print(f"{GRAS}Gestion des catégories{RESET}")
    print("-" * 40)
    print(f"{GRAS}1.{RESET} Créer une catégorie")
    print(f"{GRAS}2.{RESET} Lister mes catégories")
    print(f"{GRAS}3.{RESET} Supprimer une catégorie")
    print(f"{GRAS}0.{RESET} {ROUGE}Retour{RESET}")
    print("-" * 40)
    return input("Votre choix : ")

def afficher_menu_etiquettes():
    print("\n" + "-" * 40)
    print(f"{GRAS}Gestion des étiquettes{RESET}")
    print("-" * 40)
    print(f"{GRAS}1.{RESET} Ajouter une étiquette à une tâche")
    print(f"{GRAS}2.{RESET} Retirer une étiquette d'une tâche")
    print(f"{GRAS}3.{RESET} Voir les étiquettes d'une tâche")
    print(f"{GRAS}0.{RESET} {ROUGE}Retour{RESET}")
    print("-" * 40)
    return input("Votre choix : ")


def afficher_tache(tache):
    if not tache:
        return
    
    couleur_priorite = couleurs_priorite.get(tache.get("priorite", "normale"), BLANC)
    symbole = symboles_statut.get(tache.get("statut", "a_faire"), "[ ]")
    
    statut = tache.get('statut', 'a_faire')
    couleur_statut = couleurs_statut.get(statut, BLANC)
    
    print(f"\n{symbole} {couleur_priorite}{GRAS}{tache.get('titre', 'Sans titre')}{RESET}")
    print(f"   ID: {tache.get('id_tache', '?')}")
    print(f"   Priorité: {couleur_priorite}{tache.get('priorite', 'non définie')}{RESET}")
    print(f"   Statut: {couleur_statut}{statut}{RESET}")
    print(f"   Échéance: {tache.get('date_echeance', 'Non définie')}")
    print(f"   Catégorie: {tache.get('nom_categorie', 'Aucune')}")
    
    if tache.get("description"):
        print(f"   Description: {tache['description']}")
    
    if tache.get("etiquettes"):
        print(f"  🏷️  Étiquettes: {', '.join(tache['etiquettes'])}")
    
    print()

def afficher_liste_taches(taches, titre=" Mes tâches"):
    if not taches:
        afficher_info("Aucune tâche à afficher.")
        return
    
    print(f"\n{GRAS}{titre} ({len(taches)} tâches){RESET}")
    print("-" * 85)
    print(f"{GRAS}{'ID':<4} {'Titre':<25} {'Statut':<12} {'Priorité':<10} {'Échéance':<12} {'Catégorie':<15}{RESET}")
    print("-" * 85)
    
    for tache in taches:
        couleur_priorite = couleurs_priorite.get(tache.get("priorite", "normale"), BLANC)
        statut = tache.get('statut', 'a_faire')
        couleur_statut = couleurs_statut.get(statut, BLANC)
        
        titre_tache = tache.get('titre', '')
        if len(titre_tache) > 25:
            titre_tache = titre_tache[:22] + '...'
        
        print(f"{tache.get('id_tache', '?'):<4} "
              f"{titre_tache:<25} "
              f"{couleur_statut}{statut}{RESET:<12} "
              f"{couleur_priorite}{tache.get('priorite', '')}{RESET:<10} "
              f"{tache.get('date_echeance', 'N/A'):<12} "
              f"{tache.get('nom_categorie', 'Aucune')[:13]:<15}")
    
    print("-" * 85)


def afficher_historique(historique):
    if not historique:
        afficher_info("Aucun historique disponible pour cette tâche.")
        return
    
    titre = historique[0].get('titre_tache', 'Tâche') if historique else 'Tâche'
    
    print(f"\n{GRAS}📜 Historique de la tâche : {titre}{RESET}")
    print("-" * 70)
    print(f"{GRAS}{'Date':<20} {'Ancien statut':<15} {'Nouveau statut':<15} {'Commentaire':<20}{RESET}")
    print("-" * 70)
    
    for entree in historique:
        date = entree.get('date_changement', '')[:19] if entree.get('date_changement') else 'N/A'
        ancien = entree.get('ancien_statut', 'N/A')
        nouveau = entree.get('nouveau_statut', '')
        commentaire = entree.get('commentaire', '')[:20] if entree.get('commentaire') else ''
        
        couleur_ancien = couleurs_statut.get(ancien, BLANC)
        couleur_nouveau = couleurs_statut.get(nouveau, BLANC)
        
        print(f"{date:<20} "
              f"{couleur_ancien}{ancien}{RESET:<15} "
              f"{couleur_nouveau}{nouveau}{RESET:<15} "
              f"{commentaire:<20}")
    
    print("-" * 70)


def afficher_statistiques(stats):
    total = stats.get('total', 0)
    par_statut = stats.get('par_statut', {})
    par_priorite = stats.get('par_priorite', {})
    
    print(f"\n{GRAS} Statistiques personnelles{RESET}")
    afficher_separateur("-", 50)
    
    print(f" Total des tâches: {total}")
    
    print("\n Par statut:")
    if par_statut:
        for statut, count in par_statut.items():
            pourcentage = (count / total * 100) if total > 0 else 0
            couleur = couleurs_statut.get(statut, BLANC)
            print(f"   {couleur}{statut}{RESET}: {count} ({pourcentage:.1f}%)")
    else:
        print("   Aucune donnée")
    
    print("\n Par priorité:")
    if par_priorite:
        for priorite, count in par_priorite.items():
            pourcentage = (count / total * 100) if total > 0 else 0
            couleur = couleurs_priorite.get(priorite, BLANC)
            print(f"   {couleur}{priorite}{RESET}: {count} ({pourcentage:.1f}%)")
    else:
        print("   Aucune donnée")
    
    terminees = par_statut.get('terminee', 0)
    taux = (terminees / total * 100) if total > 0 else 0
    
    if taux == 100 and total > 0:
        print(f"\n Taux de complétion: {taux:.1f}% - BRAVO !")
    elif taux >= 50:
        print(f"\n Taux de complétion: {taux:.1f}% ({terminees}/{total})")
    else:
        print(f"\n Taux de complétion: {taux:.1f}% ({terminees}/{total})")
    
    afficher_separateur("-", 50)


def afficher_categories(categories):
    if not categories:
        afficher_info("Aucune catégorie.")
        return
    
    print(f"\n{GRAS} Mes catégories{RESET}")
    print("-" * 40)
    for cat in categories:
        nb = cat.get('nb_taches', 0)
        couleur = cat.get('couleur', 'blanc')
        print(f"  {cat['id_categorie']}: {cat['nom_categorie']} ({couleur}) - {nb} tâche(s)")
    print("-" * 40)

def afficher_couleurs_disponibles():
    couleurs = ['blanc', 'rouge', 'vert', 'bleu', 'jaune', 'orange', 'violet', 'rose', 'gris']
    print(" Couleurs disponibles : " + ", ".join(couleurs))


def afficher_etiquettes(etiquettes, titre="🏷️ Mes étiquettes"):
    if not etiquettes:
        afficher_info("Aucune étiquette.")
        return
    
    print(f"\n{titre}")
    print("-" * 30)
    for etiq in etiquettes:
        print(f"  {etiq['id_etiquette']}: {etiq['nom_etiquette']}")
    print("-" * 30)

def demander_priorite():
    print("\n Priorités disponibles : basse, normale, haute, urgente")
    while True:
        choix = input("Priorité (défaut: normale) : ").strip().lower()
        if choix == "":
            return "normale"
        if choix in ["basse", "normale", "haute", "urgente"]:
            return choix
        afficher_erreur("Priorité invalide. Choisissez parmi : basse, normale, haute, urgente")

def demander_statut():
    print("\n Statuts disponibles : a_faire, en_cours, terminee, annulee")
    while True:
        choix = input("Statut : ").strip().lower()
        if choix in ["a_faire", "en_cours", "terminee", "annulee"]:
            return choix
        afficher_erreur("Statut invalide. Choisissez parmi : a_faire, en_cours, terminee, annulee")

def demander_confirmation(message="Confirmer (o/n) : "):
    reponse = input(message).strip().lower()
    return reponse in ['o', 'oui', 'y', 'yes']

if __name__ == "__main__":
    vider_ecran()
    afficher_titre("Test du module affichage.py", BLEU)
    afficher_separateur()
    
    afficher_succes("Ceci est un message de succès")
    afficher_erreur("Ceci est un message d'erreur")
    afficher_info("Ceci est un message d'information")
    afficher_alerte("Ceci est un message d'alerte")
    
    print("\nCouleurs de priorité :")
    for priorite, couleur in couleurs_priorite.items():
        print(f"  {couleur}{priorite}{RESET}")
    
    print("\nSymboles de statut :")
    for statut, symbole in symboles_statut.items():
        print(f"  {statut}: {symbole}")
    
    input("\nAppuyez sur Entrée pour quitter...")