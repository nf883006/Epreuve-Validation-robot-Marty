from martypy import Marty

def connecter_marty(ip):
    try:
        return Marty("wifi", ip)
    except:
        return None

def executer_sequence(robot, instructions):
    for action in instructions:
        try:
            if action == "avancer":
                robot.walk()
            elif action == "reculer":
                robot.walk(-1)
            elif action == "tourner_gauche":
                robot.turn(-20)
            elif action == "tourner_droite":
                robot.turn(20)
            elif action == "gauche":
                robot.sidestep("left")
            elif action == "droite":
                robot.sidestep("right")
            elif action == "saluer_gauche":
                robot.wave_left()
            elif action == "saluer_droite":
                robot.wave_right()
            elif action == "se_redresser":
                robot.stand_straight()
            elif action == "danser":
                robot.be_happy()
        except:
            pass

def detecter_couleur(robot):
    try:
        return robot.get_colour_sensor().lower()
    except:
        return None

def detecter_mouvement(robot):
    try:
        return robot.get_accelerometer_data()
    except:
        return None

def reagir_emotion(robot, emotion):
    reactions = {
        "colère": robot.set_eyes_angry,
        "joie": robot.set_eyes_happy,
        "calme": robot.set_eyes_calm,
        "excitation": robot.set_eyes_excited
    }
    action = reactions.get(emotion)
    if action:
        try:
            action()
        except:
            pass
