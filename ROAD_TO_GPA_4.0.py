import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Tạo màn hình
height = 850
width = 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ROAD TO GPA 4.0")

# Âm thanh
CLICK_SOUND = pygame.mixer.Sound("D:/ROAD_TO_GPA_4.0/DATA/SOUND/CLICK.mp3")

# Nhạc nền
pygame.mixer.music.load("D:/ROAD_TO_GPA_4.0/DATA/SOUND/NHAC_NEN.mp3")
pygame.mixer.music.play(-1)

#hình nền 
background_img = pygame.image.load("D:/ROAD_TO_GPA_4.0/DATA/PHOTOS/BACKGROUND_MENU.png")

# Định nghĩa các màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Chữ Font
font = pygame.font.Font(None, 50)

# Hàm vẽ menu
def draw_menu():
    screen.blit(background_img, (0, 0))

    # Vẽ chữ "Start Game" và "Quit"
    start_text = font.render("Start Game", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    # Hiển thị văn bản lên màn hình
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - 100))
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 100))
    pygame.display.update()

# Hàm kiểm tra nếu người dùng nhấp chuột vào một phần của menu
def check_menu_click(mouse_pos):
    start_rect = pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 50)
    quit_rect = pygame.Rect(width // 2 - 150, height // 2 + 100, 300, 50)
    
    if start_rect.collidepoint(mouse_pos):
        return "start"
    elif quit_rect.collidepoint(mouse_pos):
        return "quit"
    return None

# Vòng lặp chính của menu
def run_menu():
    running = True
    in_menu = True

    while running:
        if in_menu:
            # Vẽ menu
            draw_menu()

            # Xử lý các sự kiện trong menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    choice = check_menu_click(mouse_pos)
                    if choice == "start":
                        CLICK_SOUND.play()
                        in_menu = False  # Thoát khỏi menu và bắt đầu game
                        import GAME
                        GAME.game_loop()
                    elif choice == "quit":
                        CLICK_SOUND.play()
                        running = False  # Thoát khỏi chương trình

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Chạy menu
if __name__ == "__main__":
    run_menu()
