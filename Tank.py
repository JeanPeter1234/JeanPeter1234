import pygame
import random

# 初始化pygame
pygame.init()

# 设置窗口
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("坦克大战")

# 定义颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 定义坦克类
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # 坦克的大小
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# 定义子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7
        self.direction = direction

    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        if self.direction == "DOWN":
            self.rect.y += self.speed
        if self.direction == "LEFT":
            self.rect.x -= self.speed
        if self.direction == "RIGHT":
            self.rect.x += self.speed

        # 删除出屏幕的子弹
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
            self.kill()

# 定义敌人坦克类
class EnemyTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 40)
        self.rect.y = random.randint(0, screen_height - 40)
        self.speed = 3

    def update(self):
        # 随机移动
        direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        if direction == "UP":
            self.rect.y -= self.speed
        elif direction == "DOWN":
            self.rect.y += self.speed
        elif direction == "LEFT":
            self.rect.x -= self.speed
        elif direction == "RIGHT":
            self.rect.x += self.speed

        # 碰到边界时反弹
        if self.rect.x < 0 or self.rect.x > screen_width - 40:
            self.rect.x = random.randint(0, screen_width - 40)
        if self.rect.y < 0 or self.rect.y > screen_height - 40:
            self.rect.y = random.randint(0, screen_height - 40)

# 创建玩家坦克
player_tank = Tank(100, 100, GREEN)
all_sprites = pygame.sprite.Group()
all_sprites.add(player_tank)

# 创建敌人坦克
enemy_tanks = pygame.sprite.Group()
for _ in range(5):  # 创建5个敌人坦克
    enemy_tank = EnemyTank()
    all_sprites.add(enemy_tank)
    enemy_tanks.add(enemy_tank)

# 创建子弹组
bullets = pygame.sprite.Group()

# 游戏主循环
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)  # 填充背景颜色
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 按空格键发射子弹
                bullet = Bullet(player_tank.rect.centerx, player_tank.rect.centery, "UP")
                all_sprites.add(bullet)
                bullets.add(bullet)

    # 获取键盘输入
    keys = pygame.key.get_pressed()

    # 更新所有精灵
    all_sprites.update(keys)

    # 碰撞检测：判断子弹是否击中敌人
    for bullet in bullets:
        if pygame.sprite.spritecollide(bullet, enemy_tanks, True):  # 子弹击中敌人坦克
            bullet.kill()

    # 绘制所有精灵
    all_sprites.draw(screen)

    # 更新屏幕
    pygame.display.flip()

    # 设置帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
