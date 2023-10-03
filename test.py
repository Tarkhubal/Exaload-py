class Chrono :
    '''
    Définition d'un chronomètre avec 3 attributs :
    heures, minutes, secondes (des nombres entiers positifs)
    minutes et secondes ne dépassent pas 59
    '''
    
    def __init__(self, heures : int, minutes : int, secondes : int):
        self.check(heures, minutes, secondes)
        
        self.heures = heures
        self.minutes = minutes
        self.secondes = secondes

    def __str__(self):
        return str(self.heures)+'h '+str(self.minutes)+'m '+str(self.secondes)+ 's'
    
    def __eq__(self, other: "Chrono"):
        assert isinstance(other, Chrono)
        self.check(other.heures, other.minutes, other.secondes)
        return (self.heures, self.minutes, self.secondes) == (other.heures, other.minutes, other.secondes)
    
    def check(self, heures: int, minutes: int, secondes: int):
        assert isinstance(heures, int) and isinstance(minutes, int) and isinstance(secondes, int)
        assert heures >= 0 and minutes >= 0 and secondes >= 0
        assert minutes <= 59 and secondes <= 59
        return True
        
    
    def avance(self, seconds=0):
        target_s = self.secondes + seconds
        target_m = self.minutes + target_s // 60
        target_h = self.heures + target_m // 60
        
        target_s %= 60
        target_m %= 60
        
        self.heures = target_h
        self.minutes = target_m
        self.secondes = target_s
        return self.__str__()

chrono = Chrono(0, 0, 3)
chrono_2 = Chrono(0, 0, 4)
print(chrono == chrono_2)
print(chrono.avance(36069))