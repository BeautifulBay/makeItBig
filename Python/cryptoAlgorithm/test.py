
from cryptoAlgorithm import MoveAlgorithm

if __name__ == "__main__":
    test = MoveAlgorithm(5)
    zhen = test.encrypt("testz{|}~")
    print zhen
    hao = test.decrypt(zhen)
    print hao
