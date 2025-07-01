import sys  # Module pour accéder à des variables et fonctions liées à l’interpréteur Python
from PyQt6.QtWidgets import (  # On importe les composants d’interface graphique de Qt
    QApplication,  # Le conteneur principal de l’application
    QWidget,QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QPushButton, QListWidget, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer  # Qt pour les constantes d’alignement, QTimer pour les tâches répétitives

from survey_controller import connecter_marty, executer_trajet, obstacle_detecte
# On importe 3 fonctions de contrôle externe : pour se connecter, exécuter une trajectoire, et détecter des obstacles

class SurveyApp(QWidget):  # On crée une classe SurveyApp qui hérite de QWidget (fenêtre)
    def __init__(self):  # Constructeur : ce qui est exécuté lors de la création de l’objet
        super().__init__()  # Appel du constructeur de la classe parent QWidget
        self.setWindowTitle("Survey - Validation 2024/2025")  # Titre de la fenêtre
        self.resize(500, 300)  # Taille par défaut de la fenêtre

        # Interface de connexion
        self.label_statut = QLabel("Déconnecté")  # Affichage de l’état de connexion
        self.label_statut.setStyleSheet("color: red; font-weight: border;")

        self.entree_ip = QLineEdit()  # Champ pour écrire l’adresse IP
        self.entree_ip.setPlaceholderText("Adresse IP de Marty")  # Texte grisé informatif

        self.bouton_connexion = QPushButton("Se connecter")  # Bouton de connexion
        self.bouton_connexion.clicked.connect(self.toggle_connexion)  # Quand on clique : appel de la fonction toggle_connexion()

        ligne_connexion = QHBoxLayout()  # Layout horizontal pour aligner les éléments de connexion
        ligne_connexion.addWidget(self.label_statut)  # Ajout du label
        ligne_connexion.addWidget(self.entree_ip)  # Ajout du champ IP
        ligne_connexion.addWidget(self.bouton_connexion)  # Ajout du bouton

        # Affichage central pour le retour d'état du robot
        self.label_middle = QLabel("Mon Marty")  # Texte central
        self.label_middle.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrage du texte
        self.label_middle.setStyleSheet("background-color: white; color: white;")  # Couleur initiale invisible

        # Contrôles du fichier de trajet (invisible au départ)
        self.bouton_charger = QPushButton("Charger .traj")  # Bouton pour charger un fichier de commandes
        self.bouton_charger.clicked.connect(self.charger_fichier_traj)  # Action sur clic

        self.bouton_exec = QPushButton(" Exécuter la mission")  # Lance l’exécution du trajet
        self.bouton_exec.clicked.connect(self.executer_mission)  # Action sur clic

        self.liste_instr = QListWidget()  # Zone qui affiche les commandes à exécuter

        self.bouton_charger.setVisible(False)  # Caché tant qu’on n’est pas connecté
        self.bouton_exec.setVisible(False)
        self.liste_instr.setVisible(False)

        ligne_controle = QHBoxLayout()  # Layout horizontal pour les boutons de contrôle
        ligne_controle.addWidget(self.bouton_charger)
        ligne_controle.addWidget(self.bouton_exec)

        # Layout principal contenant tous les éléments
        layout = QVBoxLayout()  # Layout vertical
        layout.addLayout(ligne_connexion)  # On y insère la ligne de connexion
        layout.addWidget(self.label_middle)  # Puis le label central
        layout.addLayout(ligne_controle)  # Puis les boutons charger/exécuter
        layout.addWidget(self.liste_instr)  # Enfin la liste des commandes
        self.setLayout(layout)  # On applique ce layout à notre fenêtre

        #  Données internes
        self.robot = None  # Contiendra l’objet robot une fois connecté
        self.trajet = []  # Liste de commandes du fichier .traj

        self.timer = QTimer()  # Minuterie pour surveiller les obstacles régulièrement
        self.timer.timeout.connect(self.maj_obstacle)  # Appelle maj_obstacle() toutes les X ms
        self.timer.start(1000)  # L’intervalle est d’1 seconde (1000 ms)

    def toggle_connexion(self):  # Fonction appelée lors d’un clic sur le bouton de connexion/déconnexion
        if self.robot:  # Si déjà connecté
            self.robot = None  # Déconnexion
            self.label_statut.setText("Déconnecté")
            self.label_statut.setStyleSheet("color: red;")
            self.bouton_connexion.setText("Se connecter")
            self.bouton_charger.setVisible(False)
            self.bouton_exec.setVisible(False)
            self.liste_instr.setVisible(False)
        else:  # Si on est déconnecté
            ip = self.entree_ip.text()  # On récupère l’IP entrée par l’utilisateur
            self.robot = connecter_marty(ip)  # Tentative de connexion
            if self.robot:  # Si connexion réussie
                self.label_statut.setText("Connecté")
                self.label_statut.setStyleSheet("color: green;")
                self.bouton_connexion.setText("Se déconnecter")
                self.bouton_charger.setVisible(True)
                self.bouton_exec.setVisible(True)
                self.liste_instr.setVisible(True)
            else:
                print("[ERREUR] Connexion impossible.")  # Échec de la connexion

    def charger_fichier_traj(self):  # Fonction pour ouvrir un fichier .traj
        try:
            fichier, _ = QFileDialog.getOpenFileName(self, "Charger un fichier .traj", "", "Fichiers TRAJ (*.traj)")  # Boîte de dialogue
            if fichier:
                with open(fichier, "r") as f:
                    self.trajet = [l.strip() for l in f if l.strip()]  # Nettoyage et stockage des lignes non vides
                self.liste_instr.clear()  # Nettoie l’affichage précédent
                self.liste_instr.addItems(self.trajet)  # Ajoute les lignes à la zone graphique
        except:
            print("[ERREUR] Chargement du fichier échoué.")  # Si un problème survient pendant le chargement

    def executer_mission(self):  # Lance l’exécution de la mission si robot connecté et fichier chargé
        if self.robot and self.trajet:
            executer_trajet(self.robot, self.trajet)  # Appelle la fonction d’exécution

    def maj_obstacle(self):  # Fonction appelée toutes les secondes pour mettre à jour l’état des obstacles
        if self.robot and obstacle_detecte(self.robot):
            self.label_middle.setText("Obstacle détecté")
            self.label_middle.setStyleSheet("background-color: red; color: white;")
        elif self.robot:
            self.label_middle.setText("Aucun obstacle")
            self.label_middle.setStyleSheet("background-color: green; color: white;")
        else:
            self.label_middle.setText("middle_cmd")  # Si déconnecté : état neutre
            self.label_middle.setStyleSheet("background-color: grey; color: white;")


#  Point d’entrée du programme
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Crée une instance de l'application Qt
    fenetre = SurveyApp()  # Création de la fenêtre principale
    fenetre.show()  # Affichage de la fenêtre
    sys.exit(app.exec())  # Exécution de la boucle événementielle
