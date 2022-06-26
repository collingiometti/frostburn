import pygame,math,random
pygame.init()
pygame.mixer.init()

#initialize variables
width = 1100
height = 700
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
main_group = pygame.sprite.Group()
character_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(main_group,character_group)
        self.image = pygame.image.load('hero_1.png')
        self.original_image = self.image
        self.facing_left = False
        self.walk_cycle = [pygame.image.load('hero_1.png'),
                            pygame.image.load('hero_2.png'),
                            pygame.image.load('hero_3.png'),
                            pygame.image.load('hero_4.png')]
        self.rect = self.image.get_rect(center = ((width/2),(height/2)))
        self.speed = 5
        self.bullet_countdown = .01
        self.animation_countdown = .05
        self.animation_index = 0
        self.warmth = 500
        self.Shooting = False

    def animation(self,dt):
        self.animation_countdown -= dt
        if self.animation_countdown <= 0:
            self.animation_countdown = .05
            if self.animation_index < len(self.walk_cycle) - 1:
                self.animation_index +=1
            else:
                self.animation_index = 0

        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def update(self,dt):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.animation(dt)
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.animation(dt)
        else:
            self.image = self.original_image
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.animation(dt)
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.animation(dt)

        hit = pygame.sprite.spritecollide(self,fire_group,True)
        if hit:
            if self.warmth >= 400:
                self.warmth = 500
            else:
                self.warmth += 100

        mx,my = pygame.mouse.get_pos()
        dx,dy = mx - self.rect.centerx, my - self.rect.centery
        angle = math.degrees(math.atan2(dy,dx))

        if abs(angle) > 90:
            self.facing_left = True
        else:
            self.facing_left = False

        self.bullet_countdown -= dt
        if self.bullet_countdown <= 0:
            self.bullet_countdown = 0
            click = pygame.mouse.get_pressed()
            if click[0]:
                angle = angle + random.randint(-5,5)
                Bullet(math.radians(angle))
                self.bullet_countdown = .01
                self.warmth -= 1.5


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__(main_group,enemy_group)
        self.image = pygame.image.load('spirit_1.png')
        self.animation_cycle = [pygame.image.load('spirit_1.png'),
                                pygame.image.load('spirit_2.png'),
                                pygame.image.load('spirit_3.png'),
                                pygame.image.load('spirit_4.png')]
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 4
        self.health = 10
        self.animation_countdown = .05
        self.animation_index = 0
        self.facing_left = False

    def animation(self,dt):
        self.animation_countdown -= dt
        if self.animation_countdown <= 0:
            self.animation_countdown = .05
            if self.animation_index < len(self.animation_cycle) - 1:
                self.animation_index +=1
            else:
                self.animation_index = 0

        self.image = self.animation_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def update(self,dt):
        dx,dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        hyp = math.sqrt((dx*dx)+(dy*dy))
        xv,yv = (dx / hyp)*self.speed, (dy / hyp)*self.speed
        if xv > 0:
            self.facing_left = False
        elif xv < 0:
            self.facing_left = True

        if hyp >= 100:
            self.rect.x += xv
            self.rect.y += yv
            self.animation(dt)
        elif hyp >= 25:
            self.rect.x += xv*3
            self.rect.y += yv*3
            self.image = pygame.image.load('spirit_charge.png')
        else:
            player.warmth -= 100
            self.kill()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self,angle):
        super().__init__(main_group,bullet_group)
        self.image = pygame.image.load('fire_particle.png')
        self.rect = self.image.get_rect(center = (player.rect.centerx,player.rect.centery+25))
        self.speed = 15
        self.xv = math.cos(angle)*self.speed
        self.yv = math.sin(angle)*self.speed
    
    def update(self,dt):
        self.rect.x += self.xv
        self.rect.y += self.yv

        hit = pygame.sprite.spritecollide(self, enemy_group, False)
        if hit:
            self.kill()
            enemy = hit[0]
            enemy.health-=1
            if enemy.health <= 0:
                enemy.kill()
                Fire(enemy.rect.center)


class Fire(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__(main_group,fire_group)
        self.image = pygame.image.load('fire_drop_1.png')
        self.rect = self.image.get_rect(center = pos)
        self.animation_cycle = [pygame.image.load('fire_drop_1.png'),
                                pygame.image.load('fire_drop_2.png'),
                                pygame.image.load('fire_drop_3.png'),
                                pygame.image.load('fire_drop_4.png')]
        self.animation_countdown = 0.08
        self.animation_index = 0

    def update(self,dt):
        self.animation_countdown -= dt
        if self.animation_countdown <= 0:
            self.animation_countdown = 0.08
            if self.animation_index < len(self.animation_cycle) - 1:
                self.animation_index +=1
            else:
                self.animation_index = 0
        self.image = self.animation_cycle[self.animation_index]


class Button():
    def __init__(self,image,action,y):
        self.image = image
        self.original_image = self.image
        self.rect = self.image.get_rect(center = ((width/2),y))
        self.action = action
        self.y = y
        self.click_sound = pygame.mixer.Sound('click.wav')


    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.transform.scale(self.original_image,(208,112))
            self.rect = self.image.get_rect(center = ((width/2),self.y))
            click = pygame.mouse.get_pressed()
            if click[0]:
                self.click_sound.play()
                self.action()
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect(center = ((width/2),self.y))

        screen.blit(self.image,self.rect)

class Storage():
    def __init__(self):
        self.high_score = 0
storage = Storage()

def write(word,size,x,y,color):
    text_surf = pygame.font.Font("public_pixel.TTF",size).render(word,True,color)
    text_rect = text_surf.get_rect()
    text_rect.center = (x,y)
    screen.blit(text_surf,text_rect)


def menu():
    play_button = Button(pygame.image.load('play_button.png'),game,(height/2))
    pygame.mixer.music.unload()
    pygame.mixer.music.load('menu_music.wav')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(pygame.image.load('menu_background.png'),(0,0))
        write('Frostburn',80,(width/2),100,(0,0,0))
        write('high score:',20,(width/2),200,(0,0,0))
        write(str(storage.high_score),20,(width/2),240,(0,0,0))
        play_button.update()
        pygame.display.update()
        clock.tick(60)
    
def end(score):

    exit_button = Button(pygame.image.load('exit_button.png'),menu,500)

    if math.floor(score) > storage.high_score:
        storage.high_score = math.floor(score)

    pygame.mixer.music.unload()
    pygame.mixer.music.load('end_music.wav')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(pygame.image.load('background.png'),(0,0))
        write('You Froze',60,(width/2),200,(145,65,49))
        write('score:',30,(width/2)-50,300,(0,0,0))
        write(str(math.floor(score)),30,(width/2)+70,300,(0,0,0))
        exit_button.update()
        screen.blit(pygame.image.load('bar.png'),(50,100))
        screen.blit(pygame.image.load('flame.png'),(0,500))
        pygame.display.update()
        clock.tick(60)

def game():
    main_group.empty()
    character_group.empty()
    bullet_group.empty()
    enemy_group.empty()
    fire_group.empty()

    global player
    player = Player()

    score = 0

    pygame.mixer.music.unload()
    pygame.mixer.music.load('Gameplay_Music.wav')
    pygame.mixer.music.play(-1)

    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        player.warmth -= 1
        if player.warmth <= 0:
            end(score)

        if len(enemy_group.sprites()) < 5:
            if random.randint(1,50) == 1:
                Enemy(random.randint(0,width),random.randint(0,height))

        screen.blit(pygame.image.load('background.png'),(0,0))
        main_group.update(dt)
        fire_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        character_group.draw(screen)

        screen.blit(pygame.image.load('bar.png'),(50,100))
        screen.blit(pygame.image.load('flame.png'),(0,(500-player.warmth)))
        
        score += dt
        write(str(math.floor(score)),40,60,50,(0,0,0))

        pygame.display.update()

menu()