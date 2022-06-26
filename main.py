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
#interface_group = pygame.sprite.Group()


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
                angle = angle + random.randint(-10,10)
                Bullet(math.radians(angle))
                self.bullet_countdown = .01


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__(main_group,enemy_group)
        self.image = pygame.Surface((100,100))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 2
        self.health = 10
    
    def update(self,dt):
        dx,dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        hyp = math.sqrt((dx*dx)+(dy*dy))
        xv,yv = (dx / hyp)*self.speed, (dy / hyp)*self.speed
        self.rect.x += xv
        self.rect.y += yv
        

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
        self.image = pygame.Surface((50,50))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect(center = pos)



def game():
    main_group.empty()
    character_group.empty()
    bullet_group.empty()
    enemy_group.empty()
    fire_group.empty()
    #interface_group.empty()

    global player
    player = Player()

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
            pygame.quit()

        if len(enemy_group.sprites()) < 5:
            if random.randint(1,100) == 1:
                Enemy(random.randint(0,width),random.randint(0,height))

        screen.fill((0,0,0))
        main_group.update(dt)
        fire_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        character_group.draw(screen)

        bar = pygame.Surface((20,500))
        bar.fill((232,150,149))
        screen.blit(bar,(50,100))

        box = pygame.Surface((60,60))
        box.fill((209,19,17))
        screen.blit(box,(30,(600-player.warmth)))

        pygame.display.update()

game()