from martypy import Marty  # On importe la classe Marty, qui permet de contrôler le robot via la bibliothèque martypy

# Fonction pour se connecter à Marty en Wi-Fi
def connecter_marty(ip):  # Fonction prenant en entrée une adresse IP sous forme de chaîne
    try:
        return Marty("wifi", ip)  # Tente de créer une instance de Marty en mode Wi-Fi avec l'IP donnée
    except:
        return None  # En cas d'erreur (mauvaise IP, robot non accessible...), retourne None

# Fonction pour exécuter un trajet, sous forme de liste de lignes
def executer_trajet(robot, lignes):  # Prend l'objet robot et la liste de lignes du fichier .traj
    for ligne in lignes:
        try:
            code, val = ligne[:2], int(ligne[3:])  # On extrait les 2 premières lettres comme commande, puis on lit l'entier après un espace
            # Exemple : "FW 5" → code = "FW", val = 5

            if code == "FW":  # Si la commande est "FW" (forward), le robot avance
                for _ in range(val):  # On répète val fois
                    robot.walk()
            elif code == "BW":  # Si la commande est "BW" (backward), le robot recule
                for _ in range(val):
                    robot.walk(-1)
            elif code == "LT":  # Si "LT" (left turn), pas chassé à gauche
                for _ in range(val):
                    robot.sidestep("left")
            elif code == "RT":  # Si "RT" (right turn), pas chassé à droite
                for _ in range(val):
                    robot.sidestep("right")
        except:
            # Si une erreur survient (format incorrect, conversion impossible, commande invalide)
            print(f"[ERREUR] Ligne invalide ou mal formatée : {ligne}")

# === Fonction de détection d’obstacle ===
def obstacle_detecte(robot):  # Prend en paramètre l'objet représentant le robot
    try:
        couleur = robot.get_colour_sensor()  # Lit la couleur détectée par le capteur du robot
        return couleur and couleur.lower() == "noir"  # Retourne True si la couleur détectée est "noir", sinon False
    except:
        return False  # En cas d’erreur (capteur non disponible par exemple), on retourne False (pas d’obstacle détecté)
