import pygame
import random
import math
import sys

# Khởi tạo pygame
pygame.init()

# Tạo màn hình
SCREEN_HEIGHT = 850
SCREEN_WIDTH = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ROAD TO GPA 4.0")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tải tệp âm thanh
SHOOT_SOUND = pygame.mixer.Sound("D:/ROAD_TO_GPA_4.0/DATA/SOUND/SHOOT.mp3")
LOSE_SOUND  = pygame.mixer.Sound("D:/ROAD_TO_GPA_4.0/DATA/SOUND/LOSE.mp3")
VICTORY_SOUND = pygame.mixer.Sound("D:/ROAD_TO_GPA_4.0/DATA/SOUND/VICTORY.mp3")

# Tạo clock để điều chỉnh FPS
clock = pygame.time.Clock()

# Nhân vật chính
player_size = 80 
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 10 

# Đạn
bullets = []
bullet_speed = 10
bullet_cooldown = 100  # ms
last_bullet_time = 0

# Kẻ thù
enemies = []
enemy_speed = 1
enemy_spawn_cooldown = 1500  # ms
last_enemy_spawn_time = 0
enemy_maxhp = 50
bosses = []
boss_maxhp = 200
boss_speed = 1/2

# Điểm
score = 0
font = pygame.font.Font(None, 36)

# Ảnh background
background_img = pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/PHOTOS/BACKGROUND_GAME.png")

# Ảnh nhân vật
player_img = pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/PHOTOS/main.png"), (player_size, player_size))  # Thay đổi kích thước cho phù hợp

# Ảnh địch
enemy_img = [
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy1.png"), (player_size, player_size)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy2.png"), (player_size, player_size)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy3.webp"), (player_size, player_size)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy4.png"), (player_size, player_size)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy5.jpg"), (player_size, player_size)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy6.jpg"), (player_size, player_size)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/enemy7.jpg"), (player_size, player_size))
]
boss_img = [
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/boss1.png"), (250, 250)),
    pygame.transform.scale(pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/ENEMY/boss2.png"), (250, 250)),
]

# Ảnh đạn
bullet_img = pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/PHOTOS/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (80, 80))  # Thay đổi kích thước đạn

# Các lệnh vẽ các thành phần hiện thị trong game
def draw_background(x, y):
    screen.blit(background_img, (x, y))  # Hiển thị ảnh nền

def draw_player(x, y):
    screen.blit(player_img, (x, y))  # Hiển thị hình ảnh nhân vật

def draw_boss(x, y, boss_image):
    screen.blit(boss_image, (x, y))  # Hiển thị hình ảnh nhân vật

def draw_bullet(x, y):
    screen.blit(bullet_img, (x, y))  # Hiển thị hình ảnh đạn

def draw_enemy(x, y, image):
    screen.blit(image, (x, y))  # Hiển thị hình ảnh kẻ địch

def show_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Hàm chính
def game_loop():
    global player_x, player_y, last_bullet_time, last_enemy_spawn_time, score # Sử dụng các biến toàn cục
    
    running = True
    draw_background(0, 0) # Vẽ ảnh background ở vị trí x = 0, y = 0

    while running:
        draw_background(0, 0)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Điều khiển nhân vật
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_size:
            player_y += player_speed
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
            player_x += player_speed
        
        # Bắn đạn
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_bullet_time > bullet_cooldown:
            angle = -math.pi / 2  # -90 độ trong radian

            bullets.append({
                "x": player_x  ,
                "y": player_y  ,
                "dx": math.cos(angle) * bullet_speed,
                "dy": math.sin(angle) * bullet_speed
            })
            last_bullet_time = pygame.time.get_ticks()
        
        # Cập nhật đạn
        for bullet in bullets[:]:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]
            if bullet["x"] < 0 or bullet["x"] > SCREEN_WIDTH or bullet["y"] < 0 or bullet["y"] > SCREEN_HEIGHT:
                bullets.remove(bullet)

        # Sinh ra boss
        if score >= 30 and len(bosses) == 0: 
            boss_x = random.randint(player_size, SCREEN_WIDTH - 200)
            boss_y = -player_size  
            boss_image = boss_img[random.randint(0,1)]
            bosses.append([boss_x, boss_y, boss_maxhp,boss_image])
         
         # Cập nhật Boss
        for boss in bosses[:]:
            boss[1] += boss_speed 
            
            if boss[1] > SCREEN_HEIGHT-200 :
               LOSE_SOUND.play()
               running = False 

        # Sinh kẻ thù
        if pygame.time.get_ticks() - last_enemy_spawn_time > enemy_spawn_cooldown:
            enemy_x = random.randint(player_size, SCREEN_WIDTH - 200) # để nó spawn không bị lòi ra ngoài màn hình nên bắt đầu từ toạ độ player_size
            enemy_y = -player_size  # Kẻ thù spawn ở phía trên màn hình, ngoài màn hình rồi từ từ đi xuống
            image = enemy_img[random.randint(0,6)]
            enemies.append([enemy_x, enemy_y, enemy_maxhp,image])
            last_enemy_spawn_time = pygame.time.get_ticks()

        # Cập nhật kẻ thù
        for enemy in enemies[:]:
            enemy[1] += enemy_speed # kẻ thù từ từ đi xuống từ toạ độ phía trên
            
            # Kiểm tra nếu kẻ thù ra khỏi màn hình dưới
            if enemy[1] > SCREEN_HEIGHT-80 :
               LOSE_SOUND.play()
               running = False # vừa chạy ra khỏi màn hình là thua 
                
            
            # Kiểm tra va chạm giữa kẻ thù và nhân vật
            if (
                player_x < enemy[0] + player_size and # enemy[0] là toạ độ x, tương tự [1], còn [2] là hp của địch, tất cả trong mảng enemies
                player_x + player_size > enemy[0] and
                player_y < enemy[1] + player_size and
                player_y + player_size > enemy[1]
            ):
                LOSE_SOUND.play()
                running = False  # Chạm nhân vật là thua
            if bosses:
                if (
                    player_x < boss[0] + player_size + 200 and 
                    player_x + 200 > boss[0] and # 250 là kích thước boss
                    player_y < boss[1] + player_size + 200 and
                    player_y + 200 > boss[1]
                ):
                    LOSE_SOUND.play()
                    running = False  # Chạm nhân vật là thua

        # Kiểm tra đạn bắn và kẻ thù
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (
                    bullet["x"] > enemy[0] and # kiểm tra toạ độ của đạn có nằm bên phải địch hay không 
                    bullet["x"] < enemy[0]+ player_size  and  # địch nó spawn từ toạ độ x sang bên phải nên nó phải bé hơn + player_size để nó nằm trong khoảng từ x đến player_size
                    bullet["y"] > enemy[1]  and #    
                    bullet["y"] < enemy[1]+ player_size 
                ):
                    bullets.remove(bullet)
                    enemy[2] -= 10
                    SHOOT_SOUND.play() 
                    if enemy[2] <=0: 
                        enemies.remove(enemy)
                        score += random.randint(1,5)
                        # điều kiện để thắng
                        if score >= 400:
                            score = 400
                            VICTORY_SOUND.play()
                            running = False
                        break
        # Kiểm tra đạn trúng vào boss 
        for bullet in bullets[:]:
            if bosses:
                for boss in bosses[:]:
                    if (
                        bullet["x"] > boss[0] and 
                        bullet["x"] < boss[0]+ 200 and
                        bullet["y"] > boss[1] + 25 and 
                        bullet["y"] < boss[1] + 25 + player_size 
                    ):
                        bullets.remove(bullet)
                        boss[2] -= 10
                        SHOOT_SOUND.play()
                        if boss[2] <=0 :
                            bosses.remove(boss)        
                            score += 30
                            # điều kiện để thắng
                            if score >= 400:
                                score = 400
                                VICTORY_SOUND.play()
                                running = False
                            break
        # Gọi hàm vẽ nhân vật, đạn, và kẻ thù
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1],enemy[3])
        for boss in bosses: 
            draw_boss(boss[0],boss[1],boss[3])    
        for bullet in bullets:
            draw_bullet(int(bullet["x"]), int(bullet["y"]))
        draw_player(player_x, player_y)

        # Hiển thị điểm
        show_score(score)
        
        # Cập nhật màn hình
        pygame.display.flip()
        
        # Điều chỉnh FPS
        clock.tick(60)

    from RESULT_MENU import result
    result()

GPA = float(score/100)
GPA_new = round(GPA, 1)