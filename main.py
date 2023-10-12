import pygame
from pygame.locals import *
import random
from sys import exit
import os, sys

from tkinter import * 
from tkinter.ttk import *

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys,'frozen',False):
    os.chdir(sys._MEIPASS)
"""
Track: "Damage", empty hop
Música fornecida por https://Slip.stream 
Download grátis/Stream: https://get.slip.stream/2Lb3eN

Track: "Game Over 02"
Música fornecida por https://Slip.stream 
Download grátis/Stream: https://slip.stream/soundfxs/b34b2983-34a5-42d9-858b-444e6f3d05bf

Track: "Buzzy Lasergun 03"
Música fornecida por https://Slip.stream 
Download grátis/Stream: https://slip.stream/soundfxs/f66e1bd0-926d-497a-a91a-7c190e24b69c
"""

# os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# largura = 500
# altura = 700
root = Tk() 
altura = root.winfo_screenheight() 
largura = root.winfo_screenwidth() 

# tela = pygame.display.set_mode((largura, altura-50),pygame.SCALED)
# tela = pygame.display.set_mode((largura, altura-50),pygame.NOFRAME)
# tela = pygame.display.set_mode((largura, altura-50),pygame.OPENGL)
# tela = pygame.display.set_mode((largura, altura-50),pygame.RESIZABLE)
tela = pygame.display.set_mode((largura, altura-50))
pygame.display.set_caption('Space Invaders Protect Earth')
# load_icon = pygame.image.load('./assets/sprites/sprite_Nave11.png').convert_alpha()
load_icon = pygame.image.load('./assets/sprites/enimigo.png').convert_alpha()
load_icon = load_icon.subsurface((160,0),(160,160))
load_icon = pygame.transform.scale(load_icon,(64,64))
pygame.display.set_icon(load_icon)


center = largura//3
velocidade = 2
y_background = -800

x_perso = center+200
y_perso = 500


pygame.mixer.music.set_volume(0.2)
musica_fundo = pygame.mixer.music.load('./assets/musics/Damage.mp3')
pygame.mixer.music.play(-1)

sound_tiro = pygame.mixer.Sound('./assets/musics/Buzzy Lasergun 03.mp3')
sound_tiro.set_volume(0.09)

sound_morte = pygame.mixer.Sound('./assets/musics/Game Over 02.mp3')
sound_morte.set_volume(0.1)


sprite_enimigo = pygame.image.load('./assets/sprites/enimigo.png').convert_alpha()
sprite_tiro = pygame.image.load('./assets/sprites/Lazer_pixel.png').convert_alpha()

class Tiro(pygame.sprite.Sprite):
    def __init__(self,x_tiro, y_tiro):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_tiro
        self.y = y_tiro
        self.image = sprite_tiro.subsurface((0,0), (32,32))
        self.image = pygame.transform.scale(self.image, (16*2,16*3))
        self.rect = self.image.get_rect()
        self.velocidade = 30
        self.rect.x = self.x
        self.rect.y = self.y
        # Cria uma maskara ao redor da sprite Tiro
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        # pygame.time.Clock()
        # pygame.time.wait(100)
        self.rect.y -= self.velocidade
        # print(self.rect.y)
        # Veririfica se a primeira sprite lançada na tela chegou ao final
        if self.rect.y < -20:
            grupo_sprite_2.remove(grupo_sprite_2.sprites()[0])

class Enimigo(pygame.sprite.Sprite):
    def __init__(self,x_enimigo, y_enimigo):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_enimigo
        self.y = y_enimigo
        
        self.imagens_enimigo = []
        self.index_lista = 0
        # self.img = sprite_sheet.subsurface((0,0), (32, 32))
        # self.img2 = sprite_sheet.subsurface((32,0), (32,32))
        # self.img3 = sprite_sheet.subsurface((64,0), (32,32))
        # x_sprite = 
        for x in range(5):
            img = sprite_enimigo.subsurface((x * 160,0), (160,160))
            img = pygame.transform.scale(img, (53,53))
            self.imagens_enimigo.append(img)
        self.image = self.imagens_enimigo[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.velocidade = 4.5
        
        
    def update(self):
        if self.index_lista > 4:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_enimigo[int(self.index_lista)]
        self.rect.y = self.rect.y + self.velocidade

        # Cria uma maskara/malha em pixel ao redor dos pixel criado na sprite sheet para usar em colisões etc
        self.mask = pygame.mask.from_surface(self.image)

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x_nave, y_nave):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_nave
        self.y = y_nave
        self.contador = self.y
        self.sprites = []
        # self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave00.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave01.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave02.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave03.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave04.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave05.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave06.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave07.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave08.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave09.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave10.png'))
        self.sprites.append(pygame.image.load('assets/sprites/sprite_Nave11.png'))
        
        self.index = 0
        self.image = self.sprites[self.index]
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))

        # Criar a condição para a nave se mover
        self.velocidade = 10
        self.move_direita = False
        self.move_esquerda = False
        self.move_cima = False
        self.move_baixo = False

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.index = self.index + 0.5
        if self.index >= len(self.sprites)-6:
        # if self.index >= len(self.sprites)-6:
            self.index = 0
        self.image = self.sprites[int(self.index)]
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.mask = pygame.mask.from_surface(self.image)
        # Veririca se os valores foram alterados
        # if self.move_direita and self.rect.x < tela.get_width()-90:
        # Limite 942
        # if self.move_direita and self.rect.x < center+942:
        if self.move_direita and self.rect.x < 942:
            self.rect.x += self.velocidade 
        elif self.move_esquerda and self.rect.x > center:
            self.rect.x -= self.velocidade
        elif self.move_cima and self.rect.y > 0:
            self.rect.y -= self.velocidade
        elif self.move_baixo and self.rect.y < tela.get_height()-120:
            self.rect.y += self.velocidade
            for x in range(7, len(self.sprites)):
                self.image = self.sprites[int(x)]     
                self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        
    def atirando(self,evento):
        if evento.key == K_SPACE:
            # pygame.time.set_timer()
            tiro = Tiro(self.rect.x+31, self.rect.y-20 )
            sound_tiro.play()
            grupo_sprite_2.add(tiro)
            
            
                 
    def movimento(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_RIGHT:
                nave.move_direita = True
                # print(self.rect.x)
            elif evento.key == K_LEFT:
                nave.move_esquerda = True
            elif evento.key == K_UP:
                nave.move_cima = True
            elif evento.key == K_DOWN:
                nave.move_baixo = True
        # Verificar se a tecla foi solta
        if evento.type == KEYUP:
            if evento.key == K_RIGHT:
                nave.move_direita = False
            elif evento.key == K_LEFT:
                nave.move_esquerda = False
            elif evento.key == K_UP:
                nave.move_cima = False
            elif evento.key == K_DOWN:
                nave.move_baixo = False

def drawSprites():
        grupo_sprite_2.draw(tela)
        todas_as_sprites.draw(tela)

        todas_as_sprites.update()
        grupo_sprite_2.update()
todas_as_sprites = pygame.sprite.Group()
grupo_sprite_2 = pygame.sprite.Group()

sprites_nave = pygame.sprite.Group()

# Sprites do Personagem
nave = Personagem(x_perso,y_perso)
sprites_nave.add(nave)
todas_as_sprites.add(nave)

distancia = 50
enimigos = []
relogio = pygame.time.Clock()

background_image = pygame.image.load('./assets/images/Background_spaco.png').convert()
background_image = pygame.transform.scale(background_image, (center, altura*2))

pontos = 0

def DrawTexto(txt="text",fontType='arial',color=(0,0,0), size=18, bold=False,Italic=False, antialias=True, x=0,y=0):
    pygame.font.init()
    fonte = pygame.font.SysFont(fontType,size,bold,Italic)
    texto_formatado = fonte.render(txt,antialias,color)
    return tela.blit(texto_formatado, (x, y)) 
fonte = pygame.font.SysFont('arial',32,True,False)
def reiniciar_jogo(m:bool = False):
    global morreu, pontos, enimigos, distancia, x_perso, y_perso, enimigos, y_background, todas_as_sprites, nave, sprites_nave, menu
    pygame.mixer.music.play(-1)
    enimigos = []
    x_perso = largura//3+200
    y_perso = 500
    y_background = -800
    pontos = 0
    distancia = 50
    morreu = False
    todas_as_sprites = pygame.sprite.Group()
    # grupo_sprite_2 = pygame.sprite.Group()
    if m == True:
        menu = True
    sprites_nave = pygame.sprite.Group()

    # Sprites do Personagem
    nave = Personagem(x_perso,y_perso)
    sprites_nave.add(nave)
    todas_as_sprites.add(nave)
    enimigos_gerar(distancia,10)

def enimigos_gerar(distancia=50,y_pos = -30):
    # print(no_gerar)
    for x in range(5):
            no_gerar = random.randint(1,5)
            if no_gerar != 2:
                enimigo = Enimigo(largura//3+distancia,y_pos)
                enimigos.append(enimigo)
                todas_as_sprites.add(enimigo)            
                distancia += 100
enimigos_gerar(distancia,10)
morreu = False
menu = True
def tela_GameOver(fim_de_jogo:bool):
    # tela.fill((255,255,255))
    pygame.mixer.music.stop()
    grupo_sprite_2.remove(grupo_sprite_2)
    todas_as_sprites.remove(todas_as_sprites)
    while fim_de_jogo:
        # tela.fill((255,255,255))
        global maior_pontos 
        # tela.fill((0,0,0))
        background = pygame.draw.rect(tela,(0,0,0), (center,0, center, altura))
        DrawTexto("GAME OVER",'Lucidaconsole',(255,0,0),50,True,False,True,largura//3+120,200)
        DrawTexto(f"score: {pontos}".upper(), 'Lucidaconsole', (0,255,0), 28, True,False, True, center+75,300)
        DrawTexto("Pressione R para Reiniciar",'Lucidaconsole',(255,255,255),19,True,False,True,center+75,350)
        DrawTexto("ou M para voltar ao menu",'Lucidaconsole',(255,255,255),19,True,False,True,center+75,400)
        if maior_pontos < pontos:
            maior_pontos = pontos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    # print("Reiniciando")
                    return reiniciar_jogo()
                if event.key == K_m:
                    return reiniciar_jogo(True)
                    # break
            
        pygame.display.flip()
        # return reiniciar_jogo()

def verificarJanelaMinimizada(event):
    if event.type == ACTIVEEVENT:
        # print(event.__dict__)
        if event.gain == 0 and  event.state == 2:
            # print("janela Fechou")
            pygame.mixer.music.stop()
            # pygame.display.
        elif event.gain == 1 and event.state == 2:
            pygame.mixer.music.play(-1)
            
maior_pontos = 0
while True:
    tela.fill((30,30,30))
    relogio.tick(30)
    while menu:
        # global musica_fundo
        # tela.fill((0,0,0))
        background = pygame.draw.rect(tela,(0,0,0), (center,0, center, altura))
        quadrado_limite = pygame.draw.rect(tela,(255,255,255),(center-2,0,center+6,altura),1) 
        DrawTexto('Space Invaders'.upper(), 'Lucidaconsole',(40,255,255), 55, True,False,True,center+20,150)
        # DrawTexto('Space Invaders'.upper(), 'Lucidaconsole',(40,255,255), 55, True,False,True,20,200)
        # DrawTexto('Protect the Earth'.upper(), 'Lucidaconsole',(0,255,0), 40, True,False,True,50,255)
        DrawTexto('Protect Earth'.upper(), 'Lucidaconsole',(0,255,0), 40, True,False,True,center+100,210)

        # linha = pygame.draw.line(tela,(0,255,0), (40, 300),(470,300), 5)
        ponto_y = 260
        linha = pygame.draw.line(tela,(0,255,0), (center+40, ponto_y),(center+460, ponto_y), 2)

        DrawTexto('* Precione a tecla ENTER do Seu teclado'.upper(), 'Lucidaconsole',(255,255,255), 18, True,False,True,center+15,400)
        DrawTexto('para começar o jogo'.upper(), 'Lucidaconsole',(255,255,255), 18, True,False,True,center+15,450)
        # DrawTexto('para começar o jogo'.upper(), 'Lucidaconsole',(255,255,255), 18, True,False,True,50,450)
        if maior_pontos != 0:
            # DrawTexto(f'MELHOR SCORE: {maior_pontos}','Lucidaconsole',(0,255,0), 28,True,False,True,100, 580)
            DrawTexto(f'MELHOR SCORE: {maior_pontos}','Lucidaconsole',(0,255,0), 28,True,False,True,center+100, 580)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    menu = False
                    break
            verificarJanelaMinimizada(event)
                # if event.state == SDL:
                #     print("Janela Aberta")
                #     musica_fundo.stop()
        pygame.display.flip()
    quadrado_limite = pygame.draw.rect(tela,(255,255,255),(center-2,0,center+6,altura),1) 
    mensagem = f"score: {pontos}".upper()
    
    if  enimigos[len(enimigos)-1].rect.y > 55:
        enimigos_gerar(distancia)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            nave.movimento(event)
            nave.atirando(event)
        elif event.type == KEYUP:
            nave.movimento(event)
        verificarJanelaMinimizada(event)
            # print(pygame.USEREVENT+1)
    # print(pygame.event.get())
    # print(pygame.time.get_ticks())
    for x in enimigos:
        colisao_enimigo = pygame.sprite.spritecollide(x,sprites_nave, False, pygame.sprite.collide_mask )
        # print(x.rect.y)
        if x.rect.y > tela.get_height()-90:
            pygame.mixer.music.stop()
            morreu = True
            sound_morte.play()
            pygame.time.delay(1000)
            tela_GameOver(morreu)
            break
            
        # colisao_entre_enimigos = pygame.sprite.spritecollide(x, enimigos, False, pygame.sprite.collide_mask)
        # if colisao_entre_enimigos:
        #     print("Enimigos colidiram")
        if colisao_enimigo:
            pygame.mixer.music.stop()
            morreu = True
            sound_morte.play()
            tela_GameOver(morreu)
        colisao_tiro = pygame.sprite.spritecollide(x, grupo_sprite_2, False, pygame.sprite.collide_mask)
        if colisao_tiro:
            enimigos.remove(x)
            pontos = pontos + 1
            todas_as_sprites.remove(x)
            grupo_sprite_2.remove(grupo_sprite_2.sprites()[0])
    
    # tela.blit(background_image, (center,y_background)) 
    tela.blit(background_image, (center,y_background)) 
    y_background += 10 
    if y_background > -1:
        y_background = -tela.get_height()
    # print(center)
    # print(nave.rect.x)
    drawSprites()
    
    # DrawTexto(mensagem,'Lucidaconsole',(255,255,255),32,True,False,True,tela.get_width()-300, 0)
    DrawTexto(mensagem,'Lucidaconsole',(255,255,255),32,True,False,True,center+300, 0)

    pygame.display.flip()