import pygame
import math
import random
import asyncio
from enum import Enum

# Function to draw a rectangle on the screen
def draw_rectangle(screen, topleft_x, topleft_y, width, height, colour):
    surface = pygame.Surface((width, height))
    surface.fill(colour)
    screen.blit(surface, (topleft_x, topleft_y))

# Player class representing the paddle
class Player():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour

    def render(self, screen):
        draw_rectangle(screen, self.x, self.y, self.width, self.height, self.colour)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # Update method for player movement left and right
    def update(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5

        if self.x < 0:
            self.x = 0

        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

# Function to check if two rectangles are colliding
def is_AABB_colliding(rect_a, rect_b):
    return rect_a.colliderect(rect_b)

# Function to determine the angle between the center points of two rectangles
def get_angle_between_centre_points(rect_a, rect_b):
    centre_a = pygame.math.Vector2(rect_a.center)
    centre_b = pygame.math.Vector2(rect_b.center)
    diff = centre_b - centre_a
    return math.degrees(math.atan2(diff.y, diff.x))

class Axis(Enum):
    X = 1
    Y = 2

# Ball class representing the bouncing ball
class Ball():
    def __init__(self, x, y, height, width, velocity_x, velocity_y, image_path):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y)

        # Load the ball's image
        original_surface = pygame.image.load(image_path).convert_alpha()
        self.surface = pygame.transform.scale(original_surface, (self.width, self.height))

    # Function to update ball position and handle wall collisions
    def update(self, elapsed_seconds):
        self.position += self.velocity * elapsed_seconds

        # Wall collisions
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x = -self.velocity.x

        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y = -self.velocity.y

        if self.position.x + self.width > 400:
            self.position.x = 400 - self.width
            self.velocity.x = -self.velocity.x

    # Function to reflect the ball's velocity along a given axis
    def reflect(self, axis):
        if axis == Axis.X:
            self.velocity.x *= -1
        elif axis == Axis.Y:
            self.velocity.y *= -1

    def render(self, screen):
        screen.blit(self.surface, (self.position.x, self.position.y))

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

# Brick class representing the breakable blocks
class Brick():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.is_active = True

    def render(self, screen):
        if self.is_active:
            draw_rectangle(screen, self.x, self.y, self.width, self.height, self.colour)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Display full-screen image
async def show_image(screen, image_path):
    image = pygame.image.load(image_path).convert()
    screen.blit(pygame.transform.scale(image, (400, 400)), (0, 0))
    pygame.display.flip()

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

        await asyncio.sleep(0)

async def main():

    # INIT
    pygame.init()
    pygame.mixer.init()

    # Load sounds
    collision_sound = pygame.mixer.Sound("sfx_a.ogg")
    brick_hit_sound = pygame.mixer.Sound("sfx_b.ogg")

    pygame.mixer.music.load("music_a.ogg")
    pygame.mixer.music.play(-1)

    audio_on = True

    player_width = 80
    player_height = 20

    bricks = []

    brick_width = 63
    brick_height = 5
    brick_spacing = 5

    colour_list = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
    ]

    for column_index in range(6):
        for row in range(4):
            a = column_index * (brick_width + brick_spacing)
            b = row * (brick_height + brick_spacing)
            colour_index = (row + column_index) % len(colour_list)
            brick_colour = colour_list[colour_index]
            bricks.append(Brick(a, b, brick_width, brick_height, brick_colour))

    # Create window and set caption
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Brick Breaker")

    # Font and timer setup
    font = pygame.font.SysFont("Arial", 26, bold=True)
    small_font = pygame.font.SysFont("Arial", 18, bold=True)
    neon_green = (57, 255, 20)
    clock = pygame.time.Clock()

    # Start screen
    await show_image(screen, "start.png")

    running = True

    while running:

        # Reset player, ball at the start of each new game
        player = Player(160, 380, player_width, player_height, (0, 255, 0))
        ball = Ball(195, 350, 25, 25, 100, -100, "swan.png")

        for brick in bricks:
            brick.is_active = True

        score = 0
        game_started = False
        start_ticks = pygame.time.get_ticks()

        keep_playing = True

        while keep_playing:
            elapsed_seconds = clock.tick(60) / 1000

            # Mobile button rectangles
            left_button = pygame.Rect(25, 355, 45, 35)
            play_button = pygame.Rect(165, 245, 70, 35)
            right_button = pygame.Rect(330, 355, 45, 35)
            mute_button = pygame.Rect(295, 70, 95, 28)
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_playing = False
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_started = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if left_button.collidepoint(mouse_x, mouse_y):
                        player.x -= 15

                    if right_button.collidepoint(mouse_x, mouse_y):
                        player.x += 15

                    if play_button.collidepoint(mouse_x, mouse_y):
                        game_started = True

                    if mute_button.collidepoint(mouse_x, mouse_y):
                        audio_on = not audio_on

                        if audio_on:
                            pygame.mixer.music.set_volume(1)
                        else:
                            pygame.mixer.music.set_volume(0)

            keys = pygame.key.get_pressed()
            player.update(keys, 400)

            # Mobile touch controls
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if mouse_pressed[0]:
                if left_button.collidepoint(mouse_x, mouse_y):
                    player.x -= 5

                if right_button.collidepoint(mouse_x, mouse_y):
                    player.x += 5

                if play_button.collidepoint(mouse_x, mouse_y):
                    game_started = True

            if player.x < 0:
                player.x = 0

            if player.x > 400 - player.width:
                player.x = 400 - player.width

            # Update game elements
            if game_started:
                ball.update(elapsed_seconds)

            # Ball and paddle collision detection
            if is_AABB_colliding(ball.get_rect(), player.get_rect()):
                if audio_on:
                    collision_sound.play()

                hit_pos = (ball.position.x + ball.width / 2) - (player.x + player.width / 2)
                normalized_hit_pos = hit_pos / (player_width / 2)
                ball.velocity.x = normalized_hit_pos * 50 + random.uniform(-10, 10)
                ball.velocity.y = -abs(ball.velocity.y)

            # Ball and brick collision detection
            for brick in bricks:
                if brick.is_active and is_AABB_colliding(ball.get_rect(), brick.get_rect()):
                    brick.is_active = False

                    if audio_on:
                        brick_hit_sound.play()

                    ball.reflect(Axis.Y)
                    score += 1

            # Check for game over
            if ball.position.y > 400 or all(not brick.is_active for brick in bricks):
                keep_playing = False

            # RENDER
            screen.fill((0, 0, 0))

            player.render(screen)
            ball.render(screen)

            for brick in bricks:
                brick.render(screen)

            # Display score and time
            time_played = int((pygame.time.get_ticks() - start_ticks) / 1000)
            string_score = font.render(f"Score: {score}", True, neon_green)
            string_time = font.render(f"Time: {time_played}s", True, neon_green)

            screen.blit(string_score, ((400 - string_score.get_width()) // 2, 180 - string_score.get_height()))
            screen.blit(string_time, ((400 - string_time.get_width()) // 2, 205))

            # Draw mobile buttons
            pygame.draw.rect(screen, neon_green, left_button, 2, border_radius=8)
            pygame.draw.rect(screen, neon_green, play_button, 2, border_radius=8)
            pygame.draw.rect(screen, neon_green, right_button, 2, border_radius=8)

            left_text = font.render("<", True, neon_green)
            play_text = small_font.render("PLAY", True, neon_green)
            right_text = font.render(">", True, neon_green)

            screen.blit(left_text, (left_button.centerx - left_text.get_width() // 2, left_button.centery - left_text.get_height() // 2))
            screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))
            screen.blit(right_text, (right_button.centerx - right_text.get_width() // 2, right_button.centery - right_text.get_height() // 2))

            # Draw mute button
            pygame.draw.rect(screen, neon_green, mute_button, 2, border_radius=8)

            if audio_on:
                mute_text = small_font.render("SOUND", True, neon_green)
            else:
                mute_text = small_font.render("MUTED", True, neon_green)

            screen.blit(mute_text, (mute_button.centerx - mute_text.get_width() // 2, mute_button.centery - mute_text.get_height() // 2))

            pygame.display.flip()

            await asyncio.sleep(0)

        # Game over screen
        await show_image(screen, "gameover.png")

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())