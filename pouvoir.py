class Pouvoir:
    def __init__(self, nom: str, degats: int):
        self.nom = nom
        self.degats = degats

    def __str__(self) -> str:
        return f'Pouvoir : {self.nom} ({str(self.degats)})'
