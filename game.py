import pygame
import random
import os

# --- Constantes del Juego ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Constantes de la Grilla ---
# El mundo del juego es una grilla de 25x25 celdas
GRID_WIDTH = 25
GRID_HEIGHT = 25
# Ancho y alto de cada celda en píxeles
CELL_WIDTH = SCREEN_WIDTH // GRID_WIDTH
CELL_HEIGHT = SCREEN_HEIGHT // GRID_HEIGHT

# --- Constantes de Movimiento y Juego ---
BOMB_DROP_CHANCE = 0.002 # Probabilidad de que un invasor lance una bomba en cada paso

# --- Colores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# --- Recursos Gráficos (Imágenes) ---
background_img = None
defender_img = None
invader_img = None

def load_game_images():
    """Carga las imágenes del juego y las escala al tamaño de una celda."""
    global background_img, defender_img, invader_img
    try:
        background_img = pygame.image.load(os.path.join("background.png")).convert()
        
        defender_img = pygame.image.load(os.path.join("defender.png")).convert_alpha()
        defender_img = pygame.transform.scale(defender_img, (CELL_WIDTH, CELL_HEIGHT))

        invader_img = pygame.image.load(os.path.join("invader.png")).convert_alpha()
        invader_img = pygame.transform.scale(invader_img, (CELL_WIDTH, CELL_HEIGHT))

    except pygame.error as e:
        print(f"Advertencia: No se pudieron cargar las imágenes. Se usarán formas de colores. Error: {e}")

class Defender(pygame.sprite.Sprite):
    """Representa la nave del jugador, controlada por la IA."""
    def __init__(self):
        super().__init__()
        if defender_img:
            self.image = defender_img
        else:
            self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        
        # Posición inicial en la grilla
        self.grid_x = GRID_WIDTH // 2
        self.grid_y = GRID_HEIGHT - 2
        self.rect.x = self.grid_x * CELL_WIDTH
        self.rect.y = self.grid_y * CELL_HEIGHT

    def move(self, action):
        # Mueve al defensor una celda a la izquierda (-1) o a la derecha (1)
        if action == -1:
            self.grid_x -= 1
        elif action == 1:
            self.grid_x += 1

        # Asegurarse de que el defensor no se salga de la pantalla
        if self.grid_x < 0:
            self.grid_x = 0
        if self.grid_x >= GRID_WIDTH:
            self.grid_x = GRID_WIDTH - 1
        
        self.rect.x = self.grid_x * CELL_WIDTH

    def shoot(self):
        # Crea un misil una celda por encima del defensor
        return Missile(self.grid_x, self.grid_y - 1)

class Bomb(pygame.sprite.Sprite):
    """Representa una bomba lanzada por un invasor."""
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.image = pygame.Surface([CELL_WIDTH // 2, CELL_HEIGHT // 2])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        # Centrar la bomba en la celda
        self.rect.x = self.grid_x * CELL_WIDTH + (CELL_WIDTH // 4)
        self.rect.y = self.grid_y * CELL_HEIGHT + (CELL_HEIGHT // 4)

    def update(self):
        # Mueve la bomba una celda hacia abajo
        self.grid_y += 1
        if self.grid_y >= GRID_HEIGHT:
            self.kill() # Eliminar la bomba si sale de la pantalla
        else:
            self.rect.y = self.grid_y * CELL_HEIGHT + (CELL_HEIGHT // 4)

class Invader(pygame.sprite.Sprite):
    """Representa una nave invasora."""
    def __init__(self, grid_x, grid_y, direction):
        super().__init__()
        if invader_img:
            self.image = invader_img
        else:
            self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = self.grid_x * CELL_WIDTH
        self.rect.y = self.grid_y * CELL_HEIGHT
        self.direction = direction

    def update(self):
        # Moverse horizontalmente
        self.grid_x += self.direction
        # Si llega a un borde, cambia de dirección y baja una fila
        if self.grid_x >= GRID_WIDTH -1 or self.grid_x <= 0:
            self.direction *= -1
            self.grid_y += 1
        
        self.rect.x = self.grid_x * CELL_WIDTH
        self.rect.y = self.grid_y * CELL_HEIGHT
    
    def shoot_bomb(self):
        # Crea una bomba una celda por debajo del invasor
        return Bomb(self.grid_x, self.grid_y + 1)

class Missile(pygame.sprite.Sprite):
    """Representa un misil disparado por el defensor."""
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.image = pygame.Surface([CELL_WIDTH // 4, CELL_HEIGHT // 2])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        # Centrar el misil en la celda
        self.rect.x = self.grid_x * CELL_WIDTH + (3 * CELL_WIDTH // 8)
        self.rect.y = self.grid_y * CELL_HEIGHT + (CELL_HEIGHT // 4)

    def update(self):
        # Mueve el misil una celda hacia arriba
        self.grid_y -= 1
        if self.grid_y < 0:
            self.kill() # Eliminar el misil si sale de la pantalla
        else:
            self.rect.y = self.grid_y * CELL_HEIGHT + (CELL_HEIGHT // 4)

class Game:
    """
    La clase principal que gestiona la lógica y la representación del juego.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders - AG")
        
        load_game_images()

        self.clock = pygame.time.Clock()
        if background_img:
            self.background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.background = None
        
        # Grupos de Sprites para gestionar los objetos del juego
        self.all_sprites = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        
        self.defender = None
        self.invader = None # Para el modo de un solo invasor
        self.speed_multiplier = 1
        self.reset_game()

    def reset_game(self):
        # Limpia todos los objetos de la partida anterior
        self.all_sprites.empty()
        self.invaders.empty()
        self.missiles.empty()
        self.bombs.empty()
        self.normal_speed()

        # Crea un nuevo defensor en una posición aleatoria
        self.defender = Defender()
        self.defender.grid_x = random.randint(0, GRID_WIDTH - 1)
        self.all_sprites.add(self.defender)

        # Crea un único invasor en una posición aleatoria en la parte superior
        invader_x = random.randint(0, GRID_WIDTH - 1)
        invader_y = random.randint(0, 5)
        invader_direction = random.choice([-1, 1])
        self.invader = Invader(invader_x, invader_y, invader_direction)
        self.all_sprites.add(self.invader)
        self.invaders.add(self.invader)

    def get_state(self):
        """Devuelve el estado del juego para que la IA tome una decisión."""
        if self.invaders:
            invader = self.invaders.sprites()[0]
            return {
                "defender_x": self.defender.grid_x,
                "invader_x": invader.grid_x,
                "invader_alive": True
            }
        else:
            return {
                "defender_x": self.defender.grid_x,
                "invader_x": -1, # No hay invasor
                "invader_alive": False
            }

    def speed_up(self):
        self.speed_multiplier = 5

    def normal_speed(self):
        self.speed_multiplier = 1

    def game_step(self, action):
        """
        Avanza el juego un solo paso, procesa la acción de la IA y calcula la adaptación.
        Devuelve si el juego ha terminado, el cambio en la adaptación y el resultado.
        """
        game_over = False
        fitness_delta = 0
        game_result = ''

        # --- Procesar Acción de la IA ---
        if action == 0: # Izquierda
            self.defender.move(-1)
        elif action == 1: # Derecha
            self.defender.move(1)
        elif action == 2: # Disparar
            if not self.missiles: # Solo permite un misil en pantalla a la vez
                missile = self.defender.shoot()
                self.all_sprites.add(missile)
                self.missiles.add(missile)

        # --- Actualizar Estado del Juego ---
        # Los invasores tienen una pequeña probabilidad de lanzar una bomba
        for invader in self.invaders:
            if random.random() < BOMB_DROP_CHANCE:
                bomb = invader.shoot_bomb()
                self.all_sprites.add(bomb)
                self.bombs.add(bomb)

        # Actualiza la posición de todos los sprites (invasores, bombas, misiles)
        self.all_sprites.update()

        # --- Calcular Fitness y Comprobar Fin de Juego ---
        # Recompensa base por sobrevivir un paso más
        fitness_delta += 1

        if self.invaders:
            invader = self.invaders.sprites()[0]
            # Pequeña penalización por la distancia horizontal al invasor (incentiva a alinearse)
            fitness_delta -= abs(self.defender.grid_x - invader.grid_x) / GRID_WIDTH

        # Comprobar si un misil ha golpeado a un invasor
        hits_on_invader = pygame.sprite.groupcollide(self.missiles, self.invaders, True, True)
        if hits_on_invader:
            game_over = True
            fitness_delta += 1000  # Gran recompensa por ganar
            game_result = 'WIN'

        # Comprobar si una bomba ha golpeado al defensor
        hits_on_defender = pygame.sprite.spritecollide(self.defender, self.bombs, True)
        if hits_on_defender:
            game_over = True
            fitness_delta -= 500  # Gran penalización por ser golpeado
            game_result = 'LOSS_BOMB'

        # Comprobar si el invasor ha llegado a la fila del defensor
        if not game_over and self.invaders and self.invader.grid_y >= self.defender.grid_y:
            game_over = True
            fitness_delta -= 200  # Penalización si el invasor llega al final
            game_result = 'LOSS_INVADER'

        return game_over, fitness_delta, game_result

    def render(self):
        """Dibuja todos los elementos del juego en la pantalla."""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(10 * self.speed_multiplier)
