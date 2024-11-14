# i+4-abs(i-5)
import copy
import random

class Game:
    def __init__(self,win,lists,turn,user,board=[[1,2,3],[4,5,6],[7,8,9]],):
        self.win = win
        self.board = board
        self.places={1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1],9:[2,2]}
        self.listHoriz=lists[0]
        self.listVert=lists[1]
        self.listPrinDiag=lists[2]
        self.listSubDiag=lists[3]
        self.turn=turn
        self.user=user
        
    def clear_console(self):
        print("\033[H\033[J")
        
    def UpdateCheckList(self):
        self.listHoriz=[]
        self.listVert=[]
        self.listPrinDiag=[]
        self.listSubDiag=[]
        for i in range(3):
            currHor=[]
            currVer=[]
            for j in range(3):
                currHor.append(self.board[i][j])
                currVer.append(self.board[j][i])
            self.listPrinDiag.append(self.board[i][i])
            self.listSubDiag.append(self.board[i][2-i])
            self.listHoriz.append(currHor)
            self.listVert.append(currVer)
            
    def predictAttack(self):
        p=[]
        newG = Game(self.win, [self.listHoriz, self.listVert, self.listPrinDiag, self.listSubDiag], self.turn, self.user, copy.deepcopy(self.board))
        for i in range(1,10):
            if newG.slot_open(i):
                locs=newG.places[i]
                newG.board[locs[0]][locs[1]]=newG.turn
                newG.UpdateCheckList()
                checkLists=[newG.listHoriz[locs[0]],newG.listVert[locs[1]]]
                if i==5:
                    checkLists.append(newG.listPrinDiag)
                    checkLists.append(newG.listSubDiag)
                elif locs[0]==locs[1]:
                    checkLists.append(newG.listPrinDiag)
                elif i==3 or i==7:
                    checkLists.append(newG.listSubDiag)
                result = newG.checkAttack(checkLists)
                if result!=None:
                        if newG.places[i] in p:
                            continue
                        if result==newG.turn:
                            return locs
                        p.append(locs)
        if len(p)>0:
            return random.choice(p)

    def predictWin(self):
        p=[]
        for i in range (3):
            pos=self.ch2(self.listHoriz[i])
            if pos!=None:
                sam,pos2=pos
                if [i,pos2] in p:
                    continue
                if self.board[i][sam]==self.turn:
                    return [i,pos2]
                p.append([i,pos2])
            pos=self.ch2(self.listVert[i])
            if pos!=None:
                sam,pos2=pos
                if [pos2,i] in p:
                    continue
                if self.board[sam][i]==self.turn:
                    return [pos2,i]
                p.append([pos2,i])
        pos=self.ch2(self.listPrinDiag)
        if pos!=None:
            sam,pos2=pos
            if [pos2,pos2] in p:
                pass
            else:
                p.append([pos2,pos2])
                if self.board[sam][sam]==self.turn:
                    return [pos2,pos2]
        pos=self.ch2(self.listSubDiag)
        if pos!=None:
            sam,pos2=pos
            if [pos2,2-pos2] in p:
                pass
            else:
                p.append([pos2,2-pos2])
                if self.board[sam][2-sam]==self.turn:
                    return [pos2,2-pos2]
        if len(p)>0:
            return random.choice(p)


    def checkAttack(self,checkLists):
        c=0
        for list in checkLists:
            if len(set(list))==2:
                c+=1
        if c>=2:
            for list in checkLists:
                if len(set(list))==2:
                    samePos=self.check_for_odd_place(list)
                    if samePos!=None:
                        return list[samePos[0]]
        
    def slot_open (self,pos):
        x,y=self.places[pos]
        if self.board[x][y]!='X' and self.board[x][y]!='O':
            return True
        else:
            return False
        
    def check_for_win(self):
        for i in range (3):
            if len(set(self.listHoriz[i]))==1 or len(set(self.listVert[i]))==1:
                self.win=True
                break
        if len(set(self.listPrinDiag))==1 or len(set(self.listSubDiag))==1:
            self.win=True

    def show_board(self):
        print("___________________")
        for i in self.board:
            print("|  ",end='')
            for j in i:
                print(f"{j}",end='  |  ')
            print("\n___________________")
            
    def check_for_odd_place(self,lis):
        same_pos=None
        odd_pos=None
        for i in range (3):
            c=0
            for j in range (3):
                if lis[i]==lis[j]:
                    c=c+1
            if c<2:
                if lis[i]=='X' or lis[i]=='O':
                    pass
                else:
                    # print(lis[i])
                    #b=input("Hi")
                    odd_pos=i
            if c==2:
                same_pos=i
        if same_pos!=None and odd_pos!=None:
            return [same_pos,odd_pos]
        
    def make_random_move(self,opt):
        pos=random.choice(opt)
        while not self.slot_open(pos):
            pos=random.choice(opt)
        return self.places[pos]

    def sec_move(self):
        check_piece=[1,3,7,9]
        for i in check_piece:
            if not self.slot_open(i):
                return [1,1]
        check_piece=[2,4,6,8]
        for i in check_piece:
            if not self.slot_open(i):
                return self.make_random_move([1,3,5,7,9,10-i])
        if not self.slot_open(5):
            return self.make_random_move([1,3,7,9])
                 
    def third_move(self):
        check_piece=[1,3,7,9]
        for i in check_piece:
            if self.board[self.places[i][0]][self.places[i][1]]==self.turn:
                if self.slot_open(5):
                    return [1,1]
                else:
                    return self.places[10-i]
        if self.board[1][1]==self.turn:
            check_piece=[2,4,6,8]
            for i in check_piece:
                if not self.slot_open(i):
                    return self.make_random_move([1,3,7,9])
            check_piece=[1,3,7,9]
            for i in check_piece:
                if not self.slot_open(i):
                    return self.places[10-i]
        check_piece=[2,4,6,8]
        for i in range(4):
            # issue below
            if self.board[self.places[check_piece[i]][0]][self.places[check_piece[i]][1]]==self.turn:
                if self.slot_open(5):
                    return [1,1]
                else:
                    neighbors=[]
                    if i > 0:
                        neighbors.append(check_piece[i - 1])  # Previous neighbor
                    if i < 3:
                        neighbors.append(check_piece[i + 1])    
                    return self.make_random_move(neighbors)

    def find_best_choice(self, count):
        if count == 0:
            # print("random move at first")
            return self.make_random_move([1,2,3,4,5,6,7,8,9])
            # return [1,1]
        elif count == 1:
            return self.sec_move()
        elif count == 2:
            return self.third_move()
        else:
            checkPos=self.predictWin()
            if checkPos!=None:
                print("Found win pos")
                return checkPos
            checkPos=self.predictAttack()
            if checkPos!=None:
                print("Found attack pos")
                return checkPos
            # print(f"Randomizing")
            # return self.make_random_move([1,2,3,4,5,6,7,8,9])
           
    def ch2(self,l):
        if len(set(l))==2:
            return self.check_for_odd_place(l)     

    def  make_move(self):
        locs=[]
        pos=1
        count=0
        while True:
                if self.turn==self.user:
                    pos  = int(input(f"Enter the position for(Team {self.turn}):"))
                    locs=self.places[pos]
                else:
                    #print("Finding best choice")
                    self.UpdateCheckList()
                    locs=self.find_best_choice(count)
                    if locs == None:
                        print("Random move coz no input")
                        locs=self.make_random_move([1,2,3,4,5,6,7,8,9])
                    print(f"Bot chose position {locs}")
                if self.board[locs[0]][locs[1]] == 'X' or self.board[locs[0]][locs[1]] == 'O':
                    print('please  enter another one, this place is occupied!')
                    #b=input("Bye")
                    continue
                self.board[locs[0]][locs[1]] = self.turn
                count=count+1
                self.UpdateCheckList()
                # self.clear_console()
                self.show_board()
                if count>4:
                    #print("CCheck win")
                    self.check_for_win()
                    if self.win:
                        print(f"Congratulations, Team {self.turn} won....!!")
                        break
                if count==9 and self.win==False:
                    print("Draw")
                    break
                if self.turn =='X':
                    self.turn ='O'
                elif self.turn=='O':
                    self.turn ='X'
    
if __name__=="__main__":
    user=input("Enter your choice: X or O:\t")
    turn=random.choice(['X','O'])
    if turn==user:
        print("Your turn at first")
    else:
        print("Bot's turn at first")
    obj = Game(False,[[],[],[],[]],turn,user)
    obj.show_board()
    obj.make_move()