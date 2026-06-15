from typing import List
from pouvoir import Pouvoir
import random

class Personnage:
    def __init__(self, nom: str, _categorie: str, _pv: int, pouvoirs: list[Pouvoir] | None = None,
                 artefacts:List[str]|None=None):
        if artefacts is None:
            artefacts = ['Artefact initial']
        self.nom = nom
        self._categorie = _categorie
        self._pv = _pv
        self._pv_max = _pv
        self.pouvoirs = pouvoirs or []
        self.artefacts = artefacts

    def est_vivant(self):
        return self._pv > 0

    def recevoir_degats(self, dmg:int):
        self._pv  = max(0, self._pv - dmg)

    def soigner(self, pts:int):
        self._pv = min(self._pv_max, self._pv + pts)

    def attaquer(self, cible:'Personnage')->str:
        degat = 5
        ancien_pv = cible._pv
        if self.pouvoirs:
            current_pouvoir = random.choice(self.pouvoirs)
            degat = current_pouvoir.degats
        cible.recevoir_degats(degat)
        return self.nom+'('+self._categorie+') lance un sort sur '+cible.nom+'('+str(ancien_pv)+') -- PV '+cible.nom+ ' : '+ str(cible._pv)

    def prendre_artefact(self, perdant:'Personnage')->str:
        if perdant.artefacts:
            self.artefacts.append(perdant.artefacts.pop(0))
        else:
            print(perdant.nom+'n\'avait plus d\'artefact')

    def __str__(self):
        return self.nom