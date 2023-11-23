import random

class Joueur:
    def __init__(self):
        self.niveau = 1
        self.points_de_vie = 100
        self.degats = 20
        self.bouclier = 0
        self.points_technique = 0
        self.allies = []

    def attaquer(self, chevalier):
        degats_infliges = random.randint(0, self.degats) + self.points_technique
        chevalier.subir_degats(degats_infliges)

    def gagner_experience(self):
        self.niveau += 1
        self.points_de_vie += 10
        self.degats += 5
        self.bouclier += 5
        self.points_technique += 3

    def ajouter_allie(self, allie):
        self.allies.append(allie)
        self.bouclier += allie.bouclier_bonus
        self.points_technique += allie.points_technique_bonus

    def est_vivant(self):
        return self.points_de_vie > 0

class Allie:
    def __init__(self, nom, bouclier_bonus, points_technique_bonus):
        self.nom = nom
        self.bouclier_bonus = bouclier_bonus
        self.points_technique_bonus = points_technique_bonus

class Chevalier:
    def __init__(self, niveau):
        self.niveau = niveau
        self.points_de_vie = niveau * 50
        self.degats = niveau * 10

    def subir_degats(self, degats):
        degats -= joueur.bouclier
        if degats < 0:
            degats = 0
        self.points_de_vie -= degats

    def est_vivant(self):
        return self.points_de_vie > 0

def combat():
    global joueur
    joueur = Joueur()
    chevaliers = [Chevalier(n) for n in range(1, 4)]  # Créez trois chevaliers de niveaux 1, 2 et 3

    bruce_lee = Allie("Bruce Lee", 10, 5)
    khamzat_chimaev = Allie("Khamzat Chimaev", 15, 8)

    joueur.ajouter_allie(bruce_lee)
    joueur.ajouter_allie(khamzat_chimaev)

    for chevalier in chevaliers:
        while joueur.est_vivant() and chevalier.est_vivant():
            joueur.attaquer(chevalier)
            if chevalier.est_vivant():
                chevalier.attaquer(joueur)

        if joueur.est_vivant():
            joueur.gagner_experience()
            print(f"Vous avez vaincu le chevalier de niveau {chevalier.niveau} !")
        else:
            print("Vous avez été vaincu.")

    troll_geant = Chevalier(6)  # Créez un troll géant de niveau 6 pour le combat final
    while joueur.est_vivant() and troll_geant.est_vivant():
        joueur.attaquer(troll_geant)
        if troll_geant.est_vivant():
            troll_geant.attaquer(joueur)

    if joueur.est_vivant():
        print("Vous avez vaincu le troll géant et gagné le jeu !")
    else:
        print("Le troll géant vous a vaincu. Game over.")

if __name__ == "__main__":
    combat()