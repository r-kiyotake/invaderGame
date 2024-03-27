import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))
# screen.fill((150,150,150))
pygame.display.set_caption('インベーダーゲーム')


# Player
playerImg = pygame.image.load('player.png')
playerX,playerY = 370, 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 0.2, 30

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0,480
bulletX_cange,bulletY_change = 0,3
bullet_state = 'ready' #弾の状態

# Score
score_value = 0

# mixer.Sound('laser.wav').play()

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y):
    screen.blit(enemyImg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y+ 10))

# 敵と弾がぶつかったか計算する関数
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance =math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYが入力されているとき
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # KEYが入力されていないとき
        if event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy
    if enemyY > 440:
        break
    enemyX += enemyX_change
    if enemyX <= 0: #左端に来た時
        enemyX_change = 0.2
        enemyY += enemyY_change
    elif enemyX >= 736: #右端に来た時
        enemyX_change = -0.2
        enemyY += enemyY_change

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Bullet Movement
    if bulletY <= 0: #弾が画面上部を超えた場合再度playerの元に弾をセットするイメージ
        bulletY = 480
        bullet_state = 'ready'
    
    if bullet_state is 'fire': #弾を撃っている状態
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Score
    font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255)) # テキストを描画したSurfaceの作成
    screen.blit(score,(20, 50)) #画面のx20,y50に表示

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()