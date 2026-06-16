from pouvoir import *
from personnage import *

flamme = Pouvoir('Flamme', 30)
vent = Pouvoir('Vent', 20)
ombre = Pouvoir('Ombre', 10)
sagesse = Pouvoir('Sagesse', 10)

guillaume = Gobelin('Guillaume', [ombre, vent],['gourde','arc'])
charline = Chevalier('Charline', [flamme, vent], ['glaive', 'casque'])

print(guillaume)
print(charline)
