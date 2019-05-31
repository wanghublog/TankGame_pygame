#ecoding=UTF-8
import pygame,sys,time
from random import randint
from pygame.locals import *
#类属性封装游戏出现对象

'''坦克大战的主界面'''
class TankMain():
    width=800
    heigh=800
    #enemy_list = []
    wall=None
    enemy_list=pygame.sprite.Group()#敌方坦克的族群
    explode_list=[]
    my_tank_missile_list = []
    my_tank=None#表示我方坦克是否存在
    enemy_missile_list=pygame.sprite.Group()
    #开始游戏的方法
    def startGame(self):
        pygame.init()#pygame 初始化资源
        #创建一个窗口，窗口的大小（宽，高），窗口的指针(0(固定),RESIZBLE（可变）,FULLscreen（全屏）)
        screen=pygame.display.set_mode((TankMain.width,TankMain.heigh),0,32)
        #给窗口设置标题
        pygame.display.set_caption("坦克大战")

        TankMain.wall=Wall(screen,550,400,60,60)#墙的位置及大小(screen,left,top,width,heigh)
        TankMain.my_tank=My_Tank(screen)#创建一个坦克 在屏幕中下方
        for i in range(1,6):#游戏初始化创建5个敌方坦克
                TankMain.enemy_list.add(Enemy_Tank(screen))#敌方坦克放入族里

        while True:
            if len(TankMain.enemy_list) < 5:
                TankMain.enemy_list.add(Enemy_Tank(screen))#敌方坦克数量少于5 给敌方加坦克
            #color Rgb(0,0,0)

            # 给窗口背景色
            screen.fill((0,0,0))

            #draw 函数画图
            #pygame.draw.rect(screen,(0,255,0),Rect(400,30,100,30),2)

            #显示左上角文字
            for i,text in enumerate(self.write_text()):
                screen.blit(text,(0,5+(15*i)))
            #screen.blit(self.write_text(),(0,5))

            #显示墙,并且将墙与其他对象进行碰撞检测
            TankMain.wall.display()
            TankMain.wall.hit_other()

            #我方坦克与敌方坦克碰撞检测
            if TankMain.my_tank:
                TankMain.my_tank.my_tank_hit_enemy_tank()
            #敌方坦克直接进行碰撞检测
            self.enemytank_meet_enemytank()

            self.get_event(TankMain.my_tank,screen)#获取事件，根据获取的事情处理
            if TankMain.my_tank:
                TankMain.my_tank.hit_enemy_missile()#我方的坦克和敌方的炮弹进行碰撞检测，赋予my_tank.live

            if TankMain.my_tank and TankMain.my_tank.live:#我方坦克活着且存在
                TankMain.my_tank.move()#在屏幕上移动我方坦克
                TankMain.my_tank.display()#在屏幕上显示我方坦克
            else:
                TankMain.my_tank=None

            #显示和随机移动敌方坦克
            for enemy in TankMain.enemy_list:
                enemy.display()
                enemy.random_move()
                enemy.random_fire()

            #显示所有我方坦克的炮弹
            for m in TankMain.my_tank_missile_list:
                if m.live:
                    m.display()
                    m.hit_tank()#炮弹打中敌方坦克
                    m.move()
                else:
                    TankMain.my_tank_missile_list.remove(m)

            #显示所有敌方坦克炮弹
            for m in TankMain.enemy_missile_list:
                if m.live:
                    m.display()
                    m.move()
                else:
                    TankMain.enemy_missile_list.remove(m)

            for explode in TankMain.explode_list:
                explode.display()

            #显示重置
            time.sleep(0.05)#每次休眠0.05秒 跳到下一帧
            pygame.display.update()

    #获取所有的事件（鼠标点击，键盘敲击）
    def get_event(self,my_tank,screen):
        for event in pygame.event.get():
            if event.type==QUIT:
                self.stopGame()#程序退出
            if event.type==KEYDOWN and not my_tank and event.key==K_n:
                TankMain.my_tank=My_Tank(screen)
            if event.type==KEYDOWN and my_tank:#and my_tank 表示判断我方坦克是否还存在
                if event.key==K_LEFT:
                    my_tank.diretion="L"
                    my_tank.stop=False
                    #my_tank.move()
                if event.key==K_RIGHT:
                    my_tank.diretion="R"
                    my_tank.stop=False
                    #my_tank.move()
                if event.key==K_UP:
                    my_tank.diretion="U"
                    my_tank.stop=False
                    #my_tank.move()
                if event.key==K_DOWN:
                    my_tank.diretion="D"
                    my_tank.stop=False
                    #my_tank.move()
                if event.key==K_ESCAPE:#敲击键盘的esc键
                    self.stopGame()
                if event.key==K_SPACE:
                    m=my_tank.fire()
                    m.good=True#我方坦克发射的炮弹，好炮弹
                    TankMain.my_tank_missile_list.append(m)
            if event.type==KEYUP and my_tank:
                if event.key==K_UP or event.key==K_DOWN or event.key==K_RIGHT or event.key==K_LEFT:
                    my_tank.stop=True



    #关闭游戏
    def stopGame(self):
        sys.exit()



    def write_text(self):
        font=pygame.font.SysFont("simsunnsimsun",12)
        text_sf1=font.render("敌方坦克数量为:%d"%len(TankMain.enemy_list),True,(77,77,77))
        text_sf2=font.render("我方坦克子弹数量为:%d"%len(TankMain.my_tank_missile_list),True,(55,55,55))
        return text_sf1,text_sf2

    def enemytank_meet_enemytank(self):
        for i in TankMain.enemy_list:
            for e in TankMain.enemy_list:
                if e != i:
                    is_hit = pygame.sprite.collide_rect(i, e)
                    if is_hit:
                        i.stop = True
                        i.stay()
                        e.stop = True
                        e.stay()

#坦克大战里所有对象的父类 （游戏中出现的对象存在的共同特性和行为，抽象一个基类）
class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        #所有对象共享的属性
        self.screen=screen

        # 坦克把自己显示在窗口上
    def display(self):
        if self.live:
            self.image = self.images[self.diretion]
            self.screen.blit(self.image, self.rect)


#坦克公共父类
class Tank(BaseItem):
    #定义类属性，所有坦克的高度和宽度一样
    height=60
    width=60
    #在窗口左上角写文字
    def __init__(self,screen,left,top):#left左上角坐标
        super().__init__(screen)
        self.screen=screen#坦克在移动过程中需要用到当前的游戏屏幕
        self.diretion="D"#坦克默认方向为下
        self.speed=8
        self.stop=False
        self.images={}#坦克的所有图片 key为方向 value为图片（surface）
        self.images["L"]=pygame.image.load("images/tankL.gif")
        self.images["R"]=pygame.image.load("images/tankR.gif")
        self.images["U"]=pygame.image.load("images/tankU.gif")
        self.images["D"]=pygame.image.load("images/tankD.gif")
        self.image=self.images[self.diretion]#坦克的图片由方向决定
        self.rect=self.image.get_rect()#边界
        self.rect.left=left
        self.rect.top=top
        self.live=True#决定坦克是否被消灭
        #撞墙仍能动后添加代码
        self.oldtop=self.rect.top
        self.oldleft=self.rect.left

    def stay(self):#不给进墙
        self.rect.top=self.oldtop
        self.rect.left=self.oldleft

    def move(self):
        if not self.stop:  # 如果坦克不是停止状态
            self.oldleft=self.rect.left#在变化之前保存原来位置
            self.oldtop=self.rect.top
            if self.diretion == "L":
                if self.rect.left > 0:  # 判断坦克是否在屏幕边界上
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
            elif self.diretion == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankMain.width
            elif self.diretion == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0
            elif self.diretion == "D":
                if self.rect.bottom < TankMain.heigh:
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom=TankMain.heigh
    def fire(self):
        m=Missile(self.screen,self)
        return m

    # 针对我方坦克与敌方坦克之间的碰撞
    def my_tank_hit_enemy_tank(self):
        for e in TankMain.enemy_list:
            is_hit = pygame.sprite.collide_rect(TankMain.my_tank, e)
            if is_hit:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()
                e.stop = True
                e.stay()  # 有碰撞检测则返回原位置

class My_Tank(Tank):
    def __init__(self,screen):
        super().__init__(screen,320,600)#创建一个坦克 在屏幕中下方
        self.stop=True
        self.live=True

    def hit_enemy_missile(self):
        hit_list=pygame.sprite.spritecollide(self,TankMain.enemy_missile_list,False)#碰撞检测 如果碰撞则进入for循环
        for m in hit_list:#我方坦克中弹了
            m.live=False
            TankMain.enemy_missile_list.remove(m)
            self.live=False
            explode=Explode(self.screen,self.rect)
            TankMain.explode_list.append(explode)

class Enemy_Tank(Tank):

    def __init__(self,screen):
        self.step=8#坦克连续移动的步数
        self.speed=4
        super().__init__(screen,randint(1,3)*100,randint(1,5)*100)#随机产生位置
        self.get_random_direction()
        self.images["L"] = pygame.image.load("images/p2tankL.gif")
        self.images["R"] = pygame.image.load("images/p2tankR.gif")
        self.images["U"] = pygame.image.load("images/p2tankU.gif")
        self.images["D"] = pygame.image.load("images/p2tankD.gif")
    #敌方坦克，按照一个确定随机方向，连续移动6步
    def get_random_direction(self):
        r=randint(0, 4)  # 得到一个决定坦克停止运动的随机数
        if r == 4:
            self.stop = True
        elif r == 1:
            self.diretion = "L"
            self.stop=False
        elif r == 2:
            self.diretion = "R"
            self.stop = False
        elif r == 3:
            self.diretion = "U"
            self.stop = False
        elif r == 0:
            self.diretion = "D"
            self.stop = False
    def random_move(self):
        if self.live:
            if self.step==0:
                self.get_random_direction()
                self.step=6
            else:
                self.move()
                self.step-=1

    def random_fire(self):
        r=randint(0,40)
        if r ==10:#敌方坦克发子弹的几率
            m=self.fire()
            TankMain.enemy_missile_list.add(m)
        else:
            return



class Missile(BaseItem):
    width=17
    heigh=17
    def __init__(self,screen,tank):
        super().__init__(screen)
        self.tank=tank

        self.screen = screen  # 坦克在移动过程中需要用到当前的游戏屏幕
        self.diretion =tank.diretion  #
        self.speed =12
        self.images = {}  # 坦克的所有图片 key为方向 value为图片（surface）
        self.images["L"] = pygame.image.load("images/tankmissile.gif")
        self.images["R"] = pygame.image.load("images/tankmissile.gif")
        self.images["U"] = pygame.image.load("images/tankmissile.gif")
        self.images["D"] = pygame.image.load("images/tankmissile.gif")
        self.image = self.images[self.diretion]  # 坦克的图片由方向决定
        self.rect = self.image.get_rect()  # 边界
        if self.diretion=='L':
            self.rect.left = tank.rect.left+(tank.width-self.width)/2-30#炮弹的坐标
            self.rect.top = tank.rect.top+(tank.height-self.heigh)/2
        elif self.diretion=='R':
            self.rect.left = tank.rect.left + (tank.width - self.width)/2+30  # 炮弹的坐标
            self.rect.top = tank.rect.top + (tank.height - self.heigh)/2
        elif self.diretion=='U':
            self.rect.left = tank.rect.left + (tank.width - self.width)/2  # 炮弹的坐标
            self.rect.top = tank.rect.top + (tank.height - self.heigh)/2-30
        elif self.diretion=='D':
            self.rect.left = tank.rect.left + (tank.width - self.width)/2   # 炮弹的坐标
            self.rect.top = tank.rect.top + (tank.height - self.heigh)/2+30

        self.live = True  # 炮弹是否消灭了
        self.good=False

    def move(self):
        if self.live:  # 如果炮弹存在
            if self.diretion == "L":
                if self.rect.left > 0:  # 判断坦克是否在屏幕边界上
                    self.rect.left -= self.speed
                else:
                    self.live=False
            elif self.diretion == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.live=False
            elif self.diretion == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live=False
            elif self.diretion == "D":
                if self.rect.bottom < TankMain.heigh:
                    self.rect.bottom+=self.speed
                else:
                    self.live=False

    #炮弹击中坦克,我方炮弹击中敌方坦克，敌方炮弹击中我方坦克
    def hit_tank(self):
        if self.good:#如果炮弹是我的炮弹
            hit_list=pygame.sprite.spritecollide(self,TankMain.enemy_list,False)
            for e in hit_list:
                e.live=False
                TankMain.enemy_list.remove(e)#如果敌方坦克被击中，则从列表中删除敌方坦克
                self.live=False
                explde=Explode(self.screen,e.rect)#产生一个爆炸对象
                TankMain.explode_list.append(explde)

#爆炸类
class Explode(BaseItem):

    def __init__(self,screen,rect):
        super().__init__(screen)
        self.live=True
        self.images=[pygame.image.load("images/blast1.gif"),\
                     pygame.image.load("images/blast2.gif"),\
                     pygame.image.load("images/blast3.gif"),\
                     pygame.image.load("images/blast4.gif"),\
                     pygame.image.load("images/blast5.gif"),\
                     pygame.image.load("images/blast6.gif"),\
                     pygame.image.load("images/blast7.gif"),\
                     pygame.image.load("images/blast8.gif")]
        self.step=0
        self.rect=rect#爆炸的位置和发生爆炸前，炮弹碰到的坦克位置一样，在构建爆炸的时候把坦克的rect传递进来

    #display方法在整个游戏中循环调用，每隔0.1s调用一次
    def display(self):
        if self.live:
            if self.step==len(self.images):
                self.live=False
            else:
                self.image=self.images[self.step]
                self.screen.blit(self.image,self.rect)
                self.step+=1
        else:
            pass#删除该对象

#游戏中的障碍物
class Wall(BaseItem):
    def __init__(self,screen,left,top,width,height):
        super().__init__(screen)
        self.rect=Rect(left,top,width,height)# 功能为self.top=top  传四个参数
        #self.color=(0,88,88)#墙的颜色
        self.image=pygame.image.load("images/walls.gif")

    def display(self):
        #self.screen.fill(self.image,self.rect)#画矩形墙
        self.screen.blit(self.image,self.rect)

    #针对墙与其他坦克或炮弹的碰撞检测
    def hit_other(self):
        if TankMain.my_tank:
            is_hit=pygame.sprite.collide_rect(self,TankMain.my_tank)#碰撞检测新方法 返回值为True
            if is_hit:
                TankMain.my_tank.stop=True
                TankMain.my_tank.stay()#碰到墙就弹回原位置

        if len(TankMain.enemy_list)!=0:
            hit_list=pygame.sprite.spritecollide(self,TankMain.enemy_list,False)
            for e in hit_list:
                e.stop=True
                e.stay()#有碰撞检测则返回原位置




game=TankMain()
game.startGame()

