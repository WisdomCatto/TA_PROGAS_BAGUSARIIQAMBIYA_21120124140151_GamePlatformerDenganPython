import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tugas Akhir')

# Framerate control
clock = pygame.time.Clock()
FPS = 30

# Variabel
GRAVITY = 4
MAX_PLATFORM = 10
PLATFORM_SPACING = 100
SCROLL_SPEED = 2

# Gambar
playa_image = pygame.image.load('asset thingy/playa.png').convert_alpha()
bg_image = pygame.image.load('asset thingy/bgindah.png').convert_alpha()
platform_image = pygame.image.load('asset thingy/platform.png').convert_alpha()

# Warna
Putih = (255, 255, 255)
Merah = (255, 0, 0)


# Fungsi tombol
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, Putih)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


# Class Player
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(playa_image, (45, 45))
        self.width = 45
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0

    def move(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
        if key[pygame.K_RIGHT]:
            dx = 10

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = -50

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Class Platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 21))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Membuat platform
def create_platforms():
    platform_group.empty()
    attempts = 0
    for _ in range(MAX_PLATFORM):
        valid = False
        while not valid and attempts < 100:
            p_w = random.randint(40, 70)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = random.randint(0, SCREEN_HEIGHT)

            valid = True
            for platform in platform_group:
                if abs(platform.rect.y - p_y) < PLATFORM_SPACING:
                    valid = False
                    break
            attempts += 1

        if valid:
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)


# Menu awal
def show_menu():
    menu_run = True

    def start_game():
        nonlocal menu_run
        menu_run = False

    while menu_run:
        screen.blit(bg_image, (0, 0))
        draw_button("Mulai", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, Merah, (200, 0, 0), start_game)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


# Menu game over
def show_game_over():
    over_run = True

    def restart_game():
        nonlocal over_run
        over_run = False

    while over_run:
        screen.blit(bg_image, (0, 0))
        draw_button("Restart", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, Merah, (200, 0, 0), restart_game)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


# Reset game
def reset_game():
    playa.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    playa.vel_y = 0
    create_platforms()
    # Tambahkan platform di bawah pemain
    initial_platform = Platform(playa.rect.centerx - 50, playa.rect.bottom + 10, 100)
    platform_group.add(initial_platform)


# Inisialisasi game
playa = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
platform_group = pygame.sprite.Group()
reset_game()
show_menu()

# Loop utama
run = True
while run:
    clock.tick(FPS)
    screen.blit(bg_image, (0, 0))
    playa.move()

    for platform in platform_group:
        platform.rect.y += SCROLL_SPEED
        if platform.rect.top > SCREEN_HEIGHT:
            platform.rect.y = -random.randint(50, 150)
            platform.rect.x = random.randint(0, SCREEN_WIDTH - platform.rect.width)

    playa.rect.y += SCROLL_SPEED
    platform_group.draw(screen)
    playa.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if playa.rect.top > SCREEN_HEIGHT:
        show_game_over()
        reset_game()

    pygame.display.update()

pygame.quit()
