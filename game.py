import pygame
import random
import os

# --- Constantes ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DEFENDER_SPEED = 10
INVADER_SPEED = 10
MISSILE_SPEED = 10
BOMB_SPEED = 10
BOMB_DROP_CHANCE = 0.002
INVADER_DROP_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# --- Variables Globales para Imágenes (se cargarán después) ---
background_img = None
defender_img = None
invader_img = None

def load_game_images():
    """
    Carga y escala las imágenes utilizadas en el juego.

    Las imágenes se cargan desde archivos locales y se escalan a los tamaños apropiados.
    Si las imágenes no se pueden cargar, se mostrará una advertencia en la consola.
    """
    global background_img, defender_img, invader_img
    try:
        background_img = pygame.image.load(os.path.join("background.png")).convert()
        
        defender_img = pygame.image.load(os.path.join("defender.png")).convert_alpha()
        defender_img = pygame.transform.scale(defender_img, (50, 25))

        invader_img = pygame.image.load(os.path.join("invader.png")).convert_alpha()
        invader_img = pygame.transform.scale(invader_img, (40, 30))

    except pygame.error as e:
        print(f"Advertencia: No se pudieron cargar las imágenes. Se usarán formas de colores. Error: {e}")

class Defender(pygame.sprite.Sprite):
    """
    Representa la nave del jugador (defensor) en la parte inferior de la pantalla.

    Atributos:
        image (pygame.Surface): La imagen del defensor.
        rect (pygame.Rect): El rectángulo que define la posición y el tamaño del defensor.
    """
    def __init__(self):
        """Inicializa el defensor, cargando su imagen y estableciendo su posición inicial."""
        super().__init__()
        if defender_img:
            self.image = defender_img
        else:
            self.image = pygame.Surface([50, 25])
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10

    def move(self, action):
        """
        Mueve al defensor hacia la izquierda o hacia la derecha.

        Args:
            action (int): La dirección del movimiento (-1 para la izquierda, 1 para la derecha).
        """
        if action == -1:
            self.rect.x -= DEFENDER_SPEED
        elif action == 1:
            self.rect.x += DEFENDER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        """
        Crea un nuevo misil en la posición del defensor.

        Returns:
            Missile: Un nuevo objeto `Missile`.
        """
        return Missile(self.rect.centerx, self.rect.top)

class Bomb(pygame.sprite.Sprite):
    """
    Representa una bomba lanzada por un invasor.

    Atributos:
        image (pygame.Surface): La imagen de la bomba.
        rect (pygame.Rect): El rectángulo que define la posición y el tamaño de la bomba.
    """
    def __init__(self, x, y):
        """
        Inicializa una nueva bomba en una posición específica.

        Args:
            x (int): La coordenada x de la bomba.
            y (int): La coordenada y de la bomba.
        """
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        """Mueve la bomba hacia abajo y la elimina si sale de la pantalla."""
        self.rect.y += BOMB_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Invader(pygame.sprite.Sprite):
    """
    Representa una nave invasora.

    Atributos:
        image (pygame.Surface): La imagen del invasor.
        rect (pygame.Rect): El rectángulo que define la posición y el tamaño del invasor.
        direction (int): La dirección del movimiento horizontal del invasor (-1 o 1).
    """
    def __init__(self, x, y, direction):
        """
        Inicializa un nuevo invasor en una posición y dirección específicas.

        Args:
            x (int): La coordenada x inicial del invasor.
            y (int): La coordenada y inicial del invasor.
            direction (int): La dirección inicial del movimiento.
        """
        super().__init__()
        if invader_img:
            self.image = invader_img
        else:
            self.image = pygame.Surface([40, 30])
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    def update(self):
        """Mueve al invasor horizontalmente y lo hace descender cuando llega a los bordes."""
        self.rect.x += self.direction * INVADER_SPEED
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += INVADER_DROP_SPEED
    
    def shoot_bomb(self):
        """
        Crea una nueva bomba en la posición del invasor.

        Returns:
            Bomb: Un nuevo objeto `Bomb`.
        """
        return Bomb(self.rect.centerx, self.rect.bottom)

class Missile(pygame.sprite.Sprite):
    """
    Representa un misil disparado por el defensor.

    Atributos:
        image (pygame.Surface): La imagen del misil.
        rect (pygame.Rect): El rectángulo que define la posición y el tamaño del misil.
    """
    def __init__(self, x, y):
        """
        Inicializa un nuevo misil en una posición específica.

        Args:
            x (int): La coordenada x del misil.
            y (int): La coordenada y del misil.
        """
        super().__init__()
        self.image = pygame.Surface([5, 15])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        """Mueve el misil hacia arriba y lo elimina si sale de la pantalla."""
        self.rect.y -= MISSILE_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Game:
    """
    La clase principal que gestiona la lógica y la representación del juego.

    Atributos:
        screen (pygame.Surface): La superficie de la pantalla principal del juego.
        clock (pygame.time.Clock): El reloj para controlar la velocidad de fotogramas.
        background (pygame.Surface): La imagen de fondo del juego.
        all_sprites (pygame.sprite.Group): Un grupo para todos los sprites del juego.
        invaders (pygame.sprite.Group): Un grupo para los sprites de los invasores.
        missiles (pygame.sprite.Group): Un grupo para los sprites de los misiles.
        bombs (pygame.sprite.Group): Un grupo para los sprites de las bombas.
        defender (Defender): El objeto del defensor.
        invader (Invader): El objeto del invasor.
        speed_multiplier (int): Un multiplicador para la velocidad del juego.
    """
    def __init__(self):
        """Inicializa el juego, la pantalla y todos los componentes necesarios."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders - AG")
        
        # Cargar imágenes DESPUÉS de crear la pantalla
        load_game_images()

        self.clock = pygame.time.Clock()
        if background_img:
            self.background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.background = None
        self.all_sprites = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.defender = None
        self.invader = None
        self.speed_multiplier = 1
        self.reset_game()

    def get_state(self):
        """
        Devuelve el estado actual del juego, diseñado para ser utilizado por la IA.

        Returns:
            dict: Un diccionario con la posición del defensor, la posición del invasor y si el invasor está vivo.
        """
        if self.invaders:
            invader = self.invaders.sprites()[0]
            return {
                "defender_x": self.defender.rect.centerx,
                "invader_x": invader.rect.centerx,
                "invader_alive": True
            }
        else:
            return {
                "defender_x": self.defender.rect.centerx,
                "invader_x": -1, # No hay invasor
                "invader_alive": False
            }

    def speed_up(self):
        """Acelera el juego aumentando el multiplicador de velocidad."""
        self.speed_multiplier = 5

    def normal_speed(self):
        """Restablece la velocidad del juego a la normalidad."""
        self.speed_multiplier = 1

    def reset_game(self):
        """Reinicia el juego a su estado inicial, creando un nuevo defensor y un nuevo invasor."""
        self.all_sprites.empty()
        self.invaders.empty()
        self.missiles.empty()
        self.bombs.empty()
        self.normal_speed()


        #self.defender = Defender()
        #self.defender.rect.x = random.randint(0, SCREEN_WIDTH - self.defender.rect.width)
        #self.all_sprites.add(self.defender)

        self.defender = Defender(self)
        self.all_sprites.add(self.defender)

        #Añadir 5 invasores 
        num_invaders = 5 
        invader_spacing = SCREEN_WIDTH // (num_invaders + 1)

        for i in range(num_invaders):
            # Posicion x inicial de cada invasor
            start_x = (i + 1) * invader_spacing - 20  # Centrar el invasor

            # Posicion y inicial aleatoria dentro de un rango
            start_y = random.randint(50, 200)

            # Direccion aleatoria
            direction = random.choice([-1, 1])

            self.invader = Invader(self, start_x, start_y, direction)
            self.all_sprites.add(self.invader)
            self.invaders.add(self.invader)

            # Resetear el reloj
            self.clock.tick()
            self.game_speed = 60


        """ invader_x = random.randint(0, SCREEN_WIDTH - 40)
        invader_y = random.randint(50, 200)
        invader_direction = random.choice([-1, 1])
        self.invader = Invader(invader_x, invader_y, invader_direction)
        self.all_sprites.add(self.invader)
        self.invaders.add(self.invader) """

    def game_step(self, action):
        """
        Avanza el juego un solo paso, procesando la acción del jugador y actualizando el estado del juego.

        Args:
            action (int): La acción a realizar (0: izquierda, 1: derecha, 2: disparar, 3: esperar).

        Returns:
            tuple: Una tupla que contiene un booleano (si el juego ha terminado) y el cambio en el fitness.
        """
        game_over = False
        fitness_delta = 0

        # 0=IZQ, 1=DER, 2=DISPARA, 3=ESPERAR
        if action == 0:
            self.defender.move(-1)
        elif action == 1:
            self.defender.move(1)
        elif action == 2:
            if not self.missiles:
                missile = self.defender.shoot()
                self.all_sprites.add(missile)
                self.missiles.add(missile)
        elif action == 3:
            pass # No hacer nada

        for invader in self.invaders:
            if random.random() < BOMB_DROP_CHANCE:
                bomb = invader.shoot_bomb()
                self.all_sprites.add(bomb)
                self.bombs.add(bomb)

        self.all_sprites.update()

        if self.invaders:
            invader = self.invaders.sprites()[0]
            if self.missiles:
                missile = self.missiles.sprites()[0]
                fitness_delta = ((missile.rect.centerx - invader.rect.centerx)**2 + (missile.rect.centery - invader.rect.centery)**2)**0.5
            else:
                fitness_delta = abs(self.defender.rect.centerx - invader.rect.centerx)
        else:
            fitness_delta = 0

        hits_on_invader = pygame.sprite.groupcollide(self.missiles, self.invaders, True, True)
        if hits_on_invader:
            game_over = True
            fitness_delta = -SCREEN_WIDTH * 20

        hits_on_defender = pygame.sprite.spritecollide(self.defender, self.bombs, True)
        if hits_on_defender:
            game_over = True
            fitness_delta = SCREEN_WIDTH * 5

        if not game_over and self.invaders and self.invader.rect.bottom >= self.defender.rect.top:
            game_over = True
            fitness_delta = SCREEN_WIDTH * 2

        return game_over, fitness_delta

    def render(self):
        """Renderiza todos los elementos del juego en la pantalla."""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30 * self.speed_multiplier)