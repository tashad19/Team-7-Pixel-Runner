import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self, game_active):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        if not game_active:
            self.gravity = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        if self.rect.bottom == 210:
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        else:
            self.animation_index += 1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = (pygame.time.get_ticks() - start_time)//1000
    score_surf = font.render('Score: ' + str(current_time), False, text_colour)
    score_rect = score_surf.get_rect(center = (400, 50))
    win.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                win.blit(snail_surf, obstacle_rect)
            else:
                win.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    # play walking animation if the player is on floor
    # display the jump surface when player is not on floor
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()

screen_width, screen_height = 800, 400

win = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
#obstacle_group.add(Obstacle('fly'))
#obstacle_group.add(Obstacle('snail'))

font = pygame.font.Font('font/PixelType.ttf', 50)

red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
text_colour = (64, 64, 64)
text_bg_colour = 0xc0e8ec   # may also use pygame.Color('#rrggbb')
game_over_colour = (94, 129, 160)

sky_surface = pygame.image.load('graphics/Sky.png').convert()    # .convert helps the game run a bit faster
ground_surface = pygame.image.load('graphics/ground.png').convert()

#score_surf = font.render('My game', False, text_colour)
#score_rect = score_surf.get_rect(center = (400, 50))

# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = [] 

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))  # you can also use pygame.Rect() 
                                                            # If you dont give kwargs .get_rect() places the rectangel at (0,0) by default
player_gravity = 0     # note that we are not using accurate physics of gravity, just imitating it

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)    # rotozoom method also filters the image a little
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

instructions = font.render('Press space to start', False, (111, 196, 169))
instructions_rect = instructions.get_rect(center = (400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)  # trigger obstacle_timer event every 900 ms

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:   # anything input of mouse or keyboard can be done from bth the event loop or from main loop
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                #if randint(0,2):            # either 0 or 1
                #    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 300)))
                #else:
                #    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900, 1100), 210)))
            
            if event.type == snail_animation_timer:      # We have used this timer method for animation so that we dont have change the frame for each snail separately.
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
                    

    if game_active:
        win.blit(sky_surface, (0, 0))
        win.blit(ground_surface, (0, 300))

        #pygame.draw.rect(win, text_bg_colour, score_rect)
        #pygame.draw.rect(win, text_bg_colour, score_rect, 10)
        #win.blit(score_surf, score_rect)
        score = display_score()

        #snail_rect.x -= 4
        #if snail_rect.right <= 0:
        #    snail_rect.left = 800
        #win.blit(snail_surf, snail_rect)

        # player
        #player_gravity += 1
        #player_rect.y += player_gravity
        #if player_rect.bottom >= 300:
        #    player_rect.bottom = 300
        #player_animation()
        #win.blit(player_surf, player_rect)    # can also write (player_rect.x, player_rect.y)

        player.draw(win)   
        player.update(game_active)     # This is the benefit of using a sprite class.. we only have to use player.update() to run all player methods

        obstacle_group.draw(win)
        obstacle_group.update()

        # obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_sprite()
        #game_active = collisions(player_rect, obstacle_rect_list)
        
    else:
        win.fill(game_over_colour)
        win.blit(player_stand, player_stand_rect)
        win.blit(game_name, game_name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        #player_gravity = 0
        
        score_message = font.render('Your score: ' + str(score), False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        
        if score == 0:
            win.blit(instructions, instructions_rect)
        else:
            win.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)