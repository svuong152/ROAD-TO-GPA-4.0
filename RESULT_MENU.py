import pygame
import sys
from GAME import score

# Khởi tạo pygame
pygame.init()

# Tạo màn hình
SCREEN_HEIGHT = 850
SCREEN_WIDTH = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ROAD TO GPA 4.0")

# Hình nền 
background_img = pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/PHOTOS/BACKGROUND_MENU.png")

# Âm thanh
CLICK_SOUND = pygame.mixer.Sound("D:/ROAD_TO_GPA_4.0/DATA/SOUND/CLICK.mp3")

# Định nghĩa các màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Chữ Font
font = pygame.font.Font(None, 50)

# Tính GPA
GPA = float(score/100)
GPA_new = round(GPA, 1)

def draw_menu():
    screen.blit(background_img, (0, 0))
    
    # Vẽ "result" và "Quit"
    result_text = font.render(f"Your GPA: {GPA_new}", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    # Hiển thị văn bản lên màn hình
    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

# Hàm kiểm tra nếu người dùng nhấp chuột
def check_menu_click(mouse_pos):
    quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)
    
    if quit_rect.collidepoint(mouse_pos):
        return "quit"
    return None

# Hàm chính
def result():
    global GPA_new

    if GPA_new >= 4.0:
        GPA_new = 4.0 
    
    # Vòng lặp chính của menu
    run = True
    in_menu = True
    
    while run:
        if in_menu:
            # Vẽ menu
            draw_menu()

            # Xử lý các sự kiện trong menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    choice = check_menu_click(mouse_pos)
                    if choice == "quit":
                        run = False  # Thoát khỏi chương trình

        pygame.display.flip()
    pygame.quit()
    sys.exit()
result()            