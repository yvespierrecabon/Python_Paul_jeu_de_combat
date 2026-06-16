from typing import List
from pouvoir import Pouvoir
import random


class Personnage:
    def __init__(self, nom: str, _categorie: str, _pv: int, pouvoirs: list[Pouvoir] | None = None,
                 artefacts: List[str] | None = None):
        if artefacts is None:
            artefacts = ['Artefact initial']
        self.nom = nom
        self._categorie = _categorie
        self._pv = _pv
        self._pv_max = _pv
        self.pouvoirs = pouvoirs or []
        self.artefacts = artefacts

    def est_vivant(self)->bool:
        return self._pv > 0

    def recevoir_degats(self, dmg: int)->None:
        self._pv = max(0, self._pv - dmg)

    def soigner(self, pts: int)->None:
        self._pv = min(self._pv_max, self._pv + pts)

    def attaquer(self, cible: 'Personnage') -> str:
        degat = 5
        ancien_pv = cible._pv
        if self.pouvoirs:
            current_pouvoir = random.choice(self.pouvoirs)
            degat = current_pouvoir.degats
        cible.recevoir_degats(degat)
        return self.nom + '(' + self._categorie + ') lance un sort sur ' + cible.nom + '(' + str(
            ancien_pv) + ') --> PV après l\'attaque : ' + cible.nom + ' : ' + str(cible._pv)

    def prendre_artefact(self, perdant: 'Personnage') -> str:
        if perdant.artefacts:
            artefact_pris = perdant.artefacts.pop(0)
            self.artefacts.append(artefact_pris)
            return self.nom + ' a pris ' + str(artefact_pris) + ' à ' + perdant.nom
        else:
            return perdant.nom + ' n\'avait plus d\'artefact'

    def __str__(self)->str:
        artefacts_str = ", ".join(self.artefacts) if self.artefacts else "aucun"
        return f"{self.nom}({self._categorie}) PV {self._pv} Artefacts ({artefacts_str})"

class Gobelin(Personnage):
    def __init__(self, nom: str, pouvoirs: list[Pouvoir] | None = None,
                 artefacts: List[str] | None = None):
        super().__init__(nom, 'Gobelin', 50, pouvoirs, artefacts)


class Chevalier(Personnage):
    def __init__(self, nom: str, pouvoirs: list[Pouvoir] | None = None,
                 artefacts: List[str] | None = None):
        super().__init__(nom, 'Chevalier', 120, pouvoirs, artefacts)
        self._resistance = 0.10

    def recevoir_degats(self, dmg: int)->None:
        self._pv = max(0, self._pv - int(0.9 * dmg))


class Archer(Personnage):
    def __init__(self, nom: str, pouvoirs: list[Pouvoir] | None = None,
                 artefacts: List[str] | None = None):
        super().__init__(nom, 'Archer', 70, pouvoirs, artefacts)


class Mage(Personnage):
    def __init__(self, nom: str, puissance_magique: int, pouvoirs: list[Pouvoir] | None = None,
                 artefacts: List[str] | None = None):
        super().__init__(nom, 'Mage', 60, pouvoirs, artefacts)
        self.puissance_magique = puissance_magique

    def attaquer(self, cible: 'Personnage') -> str:
        degat = self.puissance_magique + random.randint(-5, 5)
        ancien_pv = cible._pv
        if self.pouvoirs:
            current_pouvoir = random.choice(self.pouvoirs)
            degat += current_pouvoir.degats
        cible.recevoir_degats(degat)
        return self.nom + '(' + self._categorie + ') lance un sort sur ' + cible.nom + '(' + str(
            ancien_pv) + ') -- PV ' + cible.nom + ' : ' + str(cible._pv)


class Sage(Personnage):
    def __init__(self, nom: str, pouvoir: float, pv_gagne: int, pouvoirs: list[Pouvoir] | None = None,
                 artefacts: List[str] | None = None):
        super().__init__(nom, 'Sage', 80, pouvoirs, artefacts)
        self.pouvoir = pouvoir
        self.potion = pv_gagne

    def boire_potion(self)->None:
        self._pv += self.potion

    def attaquer(self, cible: 'Personnage') -> str:
        degat = int(self.pouvoir)
        self.pouvoir *= 1.04
        ancien_pv = cible._pv
        if self.pouvoirs:
            current_pouvoir = random.choice(self.pouvoirs)
            degat += current_pouvoir.degats
        cible.recevoir_degats(degat)
        return self.nom + '(' + self._categorie + ') lance un sort sur ' + cible.nom + '(' + str(
            ancien_pv) + ') -- PV ' + cible.nom + ' : ' + str(cible._pv)
