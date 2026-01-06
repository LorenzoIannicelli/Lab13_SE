from dataclasses import dataclass

@dataclass
class Correlazione:
    crom1 : int
    crom2 : int
    correlazione : float

    def __str__(self):
        return f'{self.crom1} - {self.crom2} : {self.correlazione}'