import type

from pouvoir import Pouvoir


class Personnage:
    def __init__(self,nom:str,_categorie:str, _pv:int, _pv_max:int, pouvoirs:List(Pouvoir),
                 ):
        self.nom = nom
