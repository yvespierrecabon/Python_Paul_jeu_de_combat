from datetime import datetime

from pouvoir import Pouvoir
from personnage import Personnage, Gobelin, Chevalier, Archer, Mage, Sage

def duel(p1:Personnage, p2:Personnage)->(Personnage|None, list):
    historique = []
    print('\n--- Début du combat : '+p1.nom+' vs '+p2.nom+ ' ---')
    if not  p1.est_vivant() or not p2.est_vivant():
        historique.append('Pas de duel ' + p1.nom + ' ou ' + p2.nom + ' est déjà mort')
        return None, historique

    while p1.est_vivant() and p2.est_vivant():
        historique.append(p1.attaquer(p2))
        if not p2.est_vivant():
            break
        historique.append(p2.attaquer(p1))
        if not p1.est_vivant():
            break

    if not p2.est_vivant() and p1.est_vivant():
        historique.append(p1.prendre_artefact(p2))
        print('Vainqueur :',p1.nom)
        return p1, historique
    elif not p1.est_vivant() and  p2.est_vivant():
        historique.append(p2.prendre_artefact(p1))
        print('Vainqueur :',p2.nom)
        return p2, historique
    else:
        historique.append('Aucun vainqueur ' + p1.nom + ' et ' + p2.nom + ' sont morts')
        return None, historique

def sauvegarde_resultat(texte:str):
    date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("resultats.txt", "a", encoding="utf-8") as f:
        f.write(f"{date_heure} {texte}\n")

def affiche_personnages_vivants(personnages:list[Personnage])->None:
    print('\nPersonnages vivants :')
    for personnage in personnages:
        if personnage.est_vivant():
            print(personnage)
    print('\nPersonnages morts :')
    for personnage in personnages:
        if not personnage.est_vivant():
            print(personnage)


def main():
    flamme = Pouvoir('Flamme', 30)
    vent = Pouvoir('Vent', 20)
    ombre = Pouvoir('Ombre', 10)
    sagesse = Pouvoir('Sagesse', 10)
    print(sagesse)
    personnages = []
    guillaume = Gobelin('Guillaume', [ombre, vent],['gourde','arc'])
    charline = Chevalier('Charline', [flamme, vent], ['glaive', 'casque'])
    merlin = Mage('Merlin', 25,[sagesse],['elixir'])
    gandalf = Sage('Gandalf', 15.0, 30,[sagesse],['baton de lumière'])
    robin = Archer('Robin', [vent, ombre],['arc','fleches'])
    personnages.append(guillaume)
    personnages.append(charline)
    personnages.append(merlin)
    personnages.append(gandalf)
    personnages.append(robin)
    for personnage in personnages:
        print(personnage)


    combats = ((guillaume, charline),(merlin, gandalf),(charline, robin),(merlin,charline),(gandalf, robin))

    for p1,p2 in combats:
        vainqueur, histo= duel(p1, p2)
        print('\n'.join(histo))
        texte = f"- {p1.nom} vs {p2.nom} -> {histo[-1]}"
        sauvegarde_resultat(texte)
        affiche_personnages_vivants(personnages)

if __name__ == "__main__":
    main()