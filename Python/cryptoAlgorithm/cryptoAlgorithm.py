
class MoveAlgorithm():
    def __init__(self, step):
        self.step = step
        self.min  = 32
        self.max  = 127

    def encrypt(self, srcCode):
        tempSrc = ''
        for eachChar in srcCode:
            tempAscii = ord(eachChar) + self.step
            if tempAscii < self.max:
                tempChar = chr(tempAscii)
            else:
                tempChar = chr(self.min + (tempAscii - self.max) + 1)

            tempSrc = tempSrc + tempChar
        return tempSrc

    def decrypt(self, desCode):
        tempDes = ''
        for eachChar in desCode:
            tempAscii = ord(eachChar) - self.step
            if tempAscii > self.min:
                tempChar = chr(tempAscii)
            else:
                tempChar = chr(self.max - (self.min - tempAscii) - 1)
            
            tempDes = tempDes + tempChar
        return tempDes

class XORAlgorithm():
    def __init__(self, step, factor):
        self.factor = ord(factor)

    def encrypt(self, srcCode):
        tempSrc = ''
        for eachChar in srcCode:
            tempAscii = ord(eachChar)
            tempAscii = tempAscii ^ self.factor
        return tempSrc

    def decrypt(self, desCode):
        tempDes = ''
        for eachChar in desCode:
            tempAscii = ord(eachChar) - self.step
            if tempAscii > self.min:
                tempChar = chr(tempAscii)
            else:
                tempChar = chr(self.max - (self.min - tempAscii) - 1)

            tempDes = tempDes + tempChar
        return tempDes

