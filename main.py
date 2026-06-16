from datetime import datetime

from pouvoir import Pouvoir
from personnage import Personnage, Gobelin, Chevalier, Archer, Mage, Sage

def duel(p1:Personnage, p2:Personnage):
    historique = []
    print('\n--- Début du combat : '+p1.nom+' vs '+p2.nom+ ' ---')
    while p1.est_vivant() and p2.est_vivant():
        historique.append(p1.attaquer(p2))
        if not p2.est_vivant():
            break
        historique.append(p2.attaquer(p1))
        if not p1.est_vivant():
            break
    if not p2.est_vivant() and p1.est_vivant():
        historique.append(p1.prendre_artefact(p2))
        historique.append('Vainqueur :'+p1.nom)
        return p1.nom, historique
    elif not p1.est_vivant() and  p2.est_vivant():
        historique.append(p2.prendre_artefact(p1))
        historique.append('Vainqueur :' + p2.nom)
        return p2.nom, historique
    else:
        historique.append('Aucun vainqueur ' + p1.nom + ' et ' + p2.nom + ' sont morts')
        return 'Aucun vainqueur', historique

def sauvegarde_resultat(texte:str):
    date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("combats.txt", "a", encoding="utf-8") as f:
        f.write(f"{date_heure} {texte}\n")



def main():
    flamme = Pouvoir('Flamme', 30)
    vent = Pouvoir('Vent', 20)
    ombre = Pouvoir('Ombre', 10)
    sagesse = Pouvoir('Sagesse', 10)

    guillaume = Gobelin('Guillaume', [ombre, vent],['gourde','arc'])
    charline = Chevalier('Charline', [flamme, vent], ['glaive', 'casque'])
    merlin = Mage('Merlin', puissance_magique=25)
    gandalf = Sage('Gandalf', pouvoir=15.0, pv_gagne=30)
    robin = Archer('Robin', pouvoirs=[vent, ombre])
    print(guillaume)
    print(charline)
    print(merlin)
    print(gandalf)
    print(robin)

    combats = ((guillaume, charline),(merlin, gandalf),(charline, robin),(merlin,guillaume),(gandalf, robin))

    for p1,p2 in combats:
        vainqueur, histo= duel(p1, p2)
        print('\n'.join(histo))
        histo_ = histo[0]
        if len(histo)>=2:
            histo_ = histo[-2]
        texte = f"- {p1.nom} vs {p2.nom} -> {histo_}"
        sauvegarde_resultat(texte)

if __name__ == "__main__":
    main()