from typing import List, Optional
from pouvoir import Pouvoir
import random

class Personnage:
    def __init__(self, nom: str, _categorie: str, _pv: int, pouvoirs: Optional[List[Pouvoir]] = None,
                 artefacts: List[str] = ['Artefact initial']):
        self.nom = nom
        self._categorie = _categorie
        self._pv = _pv
        self._pv_max = _pv
        self.pouvoirs = pouvoirs
        self.artefacts = artefacts

    def est_vivant(self):
        return self._pv > 0

    def recevoir_degats(self, dmg:int):
        self._pv  = max(0, self._pv - dmg)

    def soigner(self, pts:int):
        self._pv = min(self._pv_max, self._pv + pts)

    def attaquer(self, cible:'Personnage')->str:
        degat = 5
        cible_pv = cible._pv
        if self.pouvoirs:
            current_pouvoir = random.choice(self.pouvoirs)
            degat = current_pouvoir.degats
        cible.recevoir_degats(degat)
        return self.nom+'('+self._categorie+') lance un sort sur '+cible.nom+'('+str(cible_pv)+') -- PV '+cible.nom+ ' : '+ str(cible._pv)

