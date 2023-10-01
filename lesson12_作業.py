import random

class Player:
#attribute
    def __init__(self, name:str):
        self.name = name
#method
    def __play(self):
        score = 0
        while score == 0:
            pair = 0
            score_t = 0 
            dice1 = random.randint(1,6)
            dice2 = random.randint(1,6)
            dice3 = random.randint(1,6)
            dice4 = random.randint(1,6)
            dice1 = 1
            dice2 = 1
            dice3 = 1
            dice4 = 1

            D = [dice1, dice2, dice3, dice4]
            for x in range(3):
                for j in range(x+1,4) :
                    if D[x] == D[j] :
                        pair += 1
                        score_t += D[x]
            if pair == 1 :
                score = sum(D)-score_t*2
            elif  pair == 2:
                score = max(D)*2
            elif pair == 6:
                score = D[0] + 12
            else :
                score = 0        
        return f'骰子1:{dice1} 骰子2:{dice2} 骰子3:{dice3} 骰子4:{dice4}\n{D}\n得分:{score}'

#property
    @property
    def value(self):
        return self.__play()

#被呼叫時傳出字串
    def __repr__(self) -> str:
        PlayerName = f"姓名:{self.name}"
        return PlayerName

p1 = Player('玩家1')
print(p1)
print(p1.value)

print()

p2 = Player('玩家2')
print(p2)
print(p2.value)