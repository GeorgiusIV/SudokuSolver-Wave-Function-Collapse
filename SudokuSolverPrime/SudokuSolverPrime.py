
# GLOBAL LAYER
from random import randint, choice, seed

# LAYER 1
seed(10)

# LAYER 2

# JUST KEEPING A BACKUP AROUND
INITIALSUDOKU =  [3,0,0,0,0,0,0,0,0,
                  0,9,8,0,5,6,0,7,0,
                  0,0,4,8,2,0,0,0,1,
                  0,5,0,0,9,0,0,2,0,
                  8,0,0,0,0,0,4,0,3,
                  0,1,0,0,3,7,5,9,0,
                  0,4,0,0,0,3,9,8,0,
                  0,0,7,0,0,1,0,4,0,
                  2,0,6,0,0,0,0,0,0]

INITIALSUDOKU = [9,0,8,3,1,0,0,6,0,
                  0,0,0,0,0,6,0,9,7,
                  0,5,0,0,0,0,8,0,0,
                  2,0,0,0,0,0,1,4,0,
                  0,6,4,0,3,0,9,8,0,
                  0,1,9,0,0,0,0,0,3,
                  0,0,5,0,0,0,0,1,0,
                  7,9,0,4,0,0,0,0,0,
                  0,8,0,0,9,2,4,0,5]



HINTS = {}
for key,value in enumerate(INITIALSUDOKU):
    if value != 0:
        HINTS.update({key:value})


class Sudoku():


    def __init__(self):
        self.refresh()
        self.solve()

    def refresh(self):
        self.superpositions = list()
        for i in range(0,81): 
            self.superpositions.append(list(range(1,10)))
        self.hints = HINTS
        self.propagateHints()

    def __repr__(self):
        printString = str()
        for index,entry in enumerate(self.superpositions):
            printString += str(entry)
            if index%9 == 8:
                printString += '\n'
        return printString

    def getRow(self,index):
        row = dict()
        iModded = index%9
        rowBegin = index - iModded
        rowEnd = index + (9 - iModded)
        for k in range(rowBegin,rowEnd):
            row[k] = self.superpositions[k]
        return row

    def getCol(self,index):
        col = dict()
        iModded = index%9
        colBegin = iModded
        colEnd = 72 + iModded
        for k in range(colBegin,colEnd+1,9):
            col[k] = self.superpositions[k]
        return col

    def getBox(self,index):
        box = dict()
        iModded = index%9
        iDivved = index//9
        horizontalShift = iModded%3
        verticalShift = iDivved%3 * 9
        boxBegin = index - horizontalShift - verticalShift
        boxEnd = boxBegin + 18 #bottom left
        for k in range(boxBegin,boxEnd+1,9):
            box[k] = self.superpositions[k]
            box[k+1] = self.superpositions[k+1]
            box[k+2] = self.superpositions[k+2]
        return box

    def getRelatedSquares(self,index):
        relatedSquares = dict()
        relatedSquares.update(self.getRow(index))
        relatedSquares.update(self.getCol(index))
        relatedSquares.update(self.getBox(index))
        return relatedSquares

    def getMinimumEntropy(self):
        minEntropy = 10
        minEntropyIndex = None
        for index,superposition in enumerate(self.superpositions):
            entropy = len(superposition)
            if entropy > 0 and type(superposition) is not type(set()):
                if minEntropy > entropy: 
                    minEntropy = entropy
                    minEntropyIndex = index
                elif minEntropy == entropy: 
                    if randint(0,1) == 0: 
                        minEntropy = entropy
                        minEntropyIndex = index
                else: pass
        if minEntropyIndex:
            return minEntropyIndex
        else:
            return None

    def collapse(self, collapseAt = int(), collapseTo = int()):
        self.superpositions[collapseAt] = {collapseTo}

    def propagateFrom(self, propagateTo = list(), toRemove = int()):
        for index in propagateTo.keys():
            newSuperposition = self.superpositions[index]
            if toRemove in newSuperposition: 
                newSuperposition.remove(toRemove)
            self.superpositions[index] = newSuperposition
       
    def propagateHints(self):
        for index,number in self.hints.items():
            relatedSquares = self.getRelatedSquares(index)
            self.propagateFrom(propagateTo = relatedSquares, toRemove = number)
            self.collapse(collapseAt = index, collapseTo = number)

    def checkForZeroes(self):
        EMPTY = []
        for superposition in self.superpositions:
            if superposition == EMPTY:
                return True
        return False

    def solve(self):
        solved = False
        refreshCount = 1
        while solved == False:
            choicesMade = list()
            EntropyI = self.getMinimumEntropy()
            if EntropyI:
                # ATTEMPTING
                relatedSquares = self.getRelatedSquares(EntropyI)
                number = choice(self.superpositions[EntropyI])
                choicesMade.append(number)
                self.propagateFrom(propagateTo = relatedSquares, toRemove = number)
                self.collapse(collapseAt = EntropyI, collapseTo = number)
            elif self.checkForZeroes():
                # FAILED ATTEMPTS
                print("Refreshed", refreshCount,"time(s).")
                print(self)
                self.refresh()
                refreshCount += 1
            else:
                # SOLUTION
                print("Completed after", refreshCount, "attempt(s).")
                print(self)
                solved = True
            

sudoku = Sudoku()

