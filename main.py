import hashlib
import sqlite3
from user import UserManager


def afficher_menu_admin(user_manager):
    print("\nMenu :")
    print("1. Créer un utilisateur")
    print("2. Modifier un utilisateur")
    print("3. Supprimer un utilisateur")
    print("4. Consulter les utilisateurs")
    print("5. Quitter l'application")

    choix = input("Choix : ")
    return choix

def login(username, password):
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute("SELECT role, password FROM users WHERE email=?", (username,))
        row = cursor.fetchone()

        if row:
            role, hashed_password = row
            print("Rôle récupéré :", role)
            print("Mot de passe haché récupéré :", hashed_password)
            attempt = 0
            while attempt < 3:
                if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                    print("Connexion réussie.")
                    return role 
                else:
                    attempt += 1
                    print("Mot de passe incorrect. Tentative", attempt, "sur 3.")
                    password = input("Veuillez réessayer le mot de passe : ")
            print("Trop de tentatives infructueuses. Veuillez réessayer plus tard.")
            return None
        else:
            print("Utilisateur non trouvé.")
            return None
    except sqlite3.Error as e:
        print("Erreur lors de la connexion :", e)
        return None
    finally:
        conn.close()

username = input("Nom d'utilisateur : ")
password = input("Mot de passe : ")

user_role = login(username, password)
print("Rôle récupéré :", user_role)

if user_role == 'ADMIN':
    user_manager = UserManager('user.db')

elif user_role == 'user':
    print("Bienvenue utilisateur normal.")

else:
    print("Échec de la connexion.")

if user_role == 'ADMIN':
    user_manager = UserManager('user.db')

    while True:
        choix = choix = afficher_menu_admin(user_manager)

        if choix == '1':
            first_name = input("Entrez le prénom de l'utilisateur : ")
            last_name = input("Entrez le nom de famille de l'utilisateur : ")
            email = input("Entrez l'email de l'utilisateur : ")
            phone = input("Entrez le numéro de téléphone de l'utilisateur : ")
            project_code = input("Entrez le code du projet de l'utilisateur : ")
            role = input("Entrez le rôle de l'utilisateur : ")
            region = input("Entrez la région de l'utilisateur : ")

            nouvel_utilisateur = user_manager.create_user(first_name, last_name, email, phone, project_code, role, region)
            if nouvel_utilisateur:
                print("Utilisateur créé avec succès.")
            else:
                print("L'utilisateur n'a pas été créé en raison d'un rôle non valide.")

        elif choix == '2':
            email = input("Entrez l'email de l'utilisateur à modifier : ")
            print("Quels attributs souhaitez-vous modifier ?")
            print("1. Prénom")
            print("2. Nom de famille")
            print("3. Email")
            print("4. Numéro de téléphone")
            print("5. Code de projet")
            print("6. Rôle")
            print("7. Région")
            
            attributs_a_modifier = input("Entrez les numéros des attributs séparés par des virgules (ex: 1, 3, 5) : ")
            attributs_a_modifier = [int(x.strip()) for x in attributs_a_modifier.split(',')]
            
            modifications = {}
            
            if 1 in attributs_a_modifier:
                modifications['first_name'] = input("Nouveau prénom : ")
            if 2 in attributs_a_modifier:
                modifications['last_name'] = input("Nouveau nom de famille : ")
            if 3 in attributs_a_modifier:
                modifications['email'] = input("Nouvel email : ")
            if 4 in attributs_a_modifier:
                modifications['phone'] = input("Nouveau numéro de téléphone : ")
            if 5 in attributs_a_modifier:
                modifications['project_code'] = input("Nouveau code de projet : ")
            if 6 in attributs_a_modifier:
                new_role = input("Nouveau rôle : ")
                if new_role.lower() not in user_manager.ROLES:
                    print("Erreur : Le rôle spécifié n'est pas valide.")
                modifications['role'] = new_role
            if 7 in attributs_a_modifier:
                modifications['region'] = input("Nouvelle région : ")
            
            confirmation = input("Êtes-vous sûr de vouloir modifier cet utilisateur ? (oui/non) : ")
            if confirmation.lower() == "oui":
                user_manager.modify_user(email, **modifications)
                print("Utilisateur modifié avec succès.")
            else:
                print("Modification annulée.")


        elif choix == '3':
            email = input("Entrez l'email de l'utilisateur à supprimer : ")
            confirmation = input("Êtes-vous sûr de vouloir supprimer cet utilisateur ? (oui/non) : ")
            if confirmation.lower() == "oui":
                user_manager.delete_user(email)
                print("Utilisateur supprimé avec succès.")
            else:
                print("Suppression annulée.")

        elif choix == '4':
            user_manager.display_users()


        elif choix == '5':
            print("Quitting...")
            break