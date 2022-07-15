from numpy import double
import pygame,os,json,datetime
from random import randint
from sys import exit

VERSION = '1.0.0'
WHITE = (255,255,255)
WINDOWSIZE = (1080,725)
NORMAL_SIZE_OF_FONT = 20

pygame.init()
screen = pygame.display.set_mode(WINDOWSIZE, 0, 32)
pygame.display.set_caption('EXTEND UNO made by |x|')

total_players = []
exist_players = []
waiting_players = []    # 存放接下来的玩家列表，不包括当前玩家自身
ranking = {'time':{'刘':0,'陈':0,'郭':0,'马':0,'邓':0,'钟':0}} # 记录每次游戏的得分情况，需修改
normal_size_font = pygame.font.SysFont('SimHei',NORMAL_SIZE_OF_FONT)
settingdic = {
    '玩家名':['刘','陈','郭','马','邓','钟'],
    '牌组名':['经典UNO','反弹&pass','决斗&缴械','无限','天选之子','组合','传递','神之手',
        '天弃之子','炸弹','夹子','手榴弹&C4','紧箍咒','复活','跳转','赌怪','抬杠']
} # 设置，包括可选玩家名与可选卡组名
rects = {
    'ranking':[]
}

class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return ''.join(['(',str(self.x),',',str(self.y),')'])
    def __add__(self,other):
        if isinstance(other, Pos):
            return Pos(self.x + other.x,self.y + other.y)
        elif isinstance(other,int) or isinstance(other,double):
            return Pos(self.x + other,self.y + other)
    def __radd__(self, other):
        return self.__add__(other)
    def __mul__(self,other):
        if isinstance(other, int):
            return Pos(self.x * other,self.y * other)
    def __call__(self) -> tuple:
        return (self.x,self.y)
class act_rect:
    def __init__(self,rect:pygame.Rect,activated:bool = False):
        self.rect = rect
        self.activated = activated

class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.ban = 0    # 封禁回合数
        self.card = []  # 手牌
        self.effect = []    # 效果
        self.points = 0 # 得分

class Scene:
    def __init__(self):
        self.type = 'ranking'
        self.act_rects = []

    def display(self):
        screen.fill(WHITE)
        textImage = normal_size_font.render('test',True,(255,0,0))
        screen.blit(textImage,(170,665))

    def update_selected(self,pos:Pos):
        for actrect in self.act_rects:
            if actrect.rect.collidepoint(pos()):
                actrect.activated = True
                break

scene = Scene()

def show_ranking(): # 展示当前排名
    screen.fill(WHITE)
    temp = {}
    for dics in ranking.values():
        for key,value in dics.items():
            temp[key] = temp.get(key,0) + value
    temp_of_y_begins = 20
    for key,value in temp.items():
        textImage = normal_size_font.render(''.join([key,' : ',str(value)]),True,(255,0,0))
        screen.blit(textImage,(10,temp_of_y_begins))
        temp_of_y_begins += NORMAL_SIZE_OF_FONT * 1.1
    
if __name__ == "__main__":
    try:
        with open('./res' + os.sep + 'ranking.json','r',encoding='utf-8') as f:
            ranking = json.load(f)
    except FileNotFoundError:
        with open('./res' + os.sep + 'ranking.json','w',encoding='utf-8') as f:
            json.dump(ranking,f,indent=4)
    try:
        with open('./res' + os.sep + 'settings.json','r',encoding='utf-8') as f:
            settingdic = json.load(f)
    except FileNotFoundError:
        with open('./res' + os.sep + 'settings.json','w',encoding='utf-8') as f:
            json.dump(settingdic,f,indent=4)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                scene.display = show_ranking
                scene.display()

        
        pygame.display.update()