"""
Entities - Classes de base pour ennemis et objets
"""

import pygame
import os
from logger import Logger
from config import *


class Enemy(pygame.Rect):
    """
    Classe de base pour tous les ennemis.
    """
    
    def __init__(self, x, y, width, height, health):
        super().__init__(x, y, width, height)
        self.health = health
        self.direction = "left"
        self.velocity_y = 0
        self.jumping = False
    
    def update(self):
        """Met à jour l'ennemi - à surcharger"""
        raise NotImplementedError
    
    def draw(self, screen):
        """Dessine l'ennemi - à surcharger"""
        raise NotImplementedError


class Metall(Enemy):
    """
    Ennemi Metall - Tire 3 projectiles et se protège.
    """
    
    class Bullet(pygame.Rect):
        """Projectile de Metall"""
        
        def __init__(self, x, y, velocity_x, velocity_y, image):
            super().__init__(x, y, METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT)
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y
            self.image = image
            self.used = False
        
        def update(self):
            self.x += self.velocity_x
            self.y += self.velocity_y
    
    def __init__(self, x, y, images):
        super().__init__(x, y, METALL_WIDTH, METALL_HEIGHT, METALL_HEALTH)
        self.images = images
        self.guarding = False
        self.bullets = []
        self.last_fired = 0
    
    def update(self, player_x):
        """
        Met à jour le Metall.
        
        Args:
            player_x: Position X du joueur pour viser
        """
        # Détermine la direction
        if player_x < self.x:
            self.direction = "left"
        else:
            self.direction = "right"
        
        # Applique la gravité
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Tir si le joueur est à portée
        if abs(self.x - player_x) <= METALL_DETECTION_RANGE:
            self.guarding = False
            now = pygame.time.get_ticks()
            if now - self.last_fired > METALL_FIRE_RATE:
                self.shoot()
                self.last_fired = now
        else:
            self.guarding = True
        
        # Met à jour les projectiles
        for bullet in self.bullets:
            bullet.update()
        
        self.bullets = [b for b in self.bullets 
                       if not b.used and 0 < b.x < GAME_WIDTH]
    
    def shoot(self):
        """Tire 3 projectiles dans 3 directions"""
        x = self.x if self.direction == "left" else self.x + self.width
        y = self.y + TILE_SIZE / 2
        
        vel_x = -METALL_BULLET_VELOCITY_X if self.direction == "left" else METALL_BULLET_VELOCITY_X
        
        # 3 projectiles: haut, milieu, bas
        self.bullets.append(Metall.Bullet(x, y, vel_x, -METALL_BULLET_VELOCITY_Y, self.images["bullet"]))
        self.bullets.append(Metall.Bullet(x, y, vel_x, 0, self.images["bullet"]))
        self.bullets.append(Metall.Bullet(x, y, vel_x, METALL_BULLET_VELOCITY_Y, self.images["bullet"]))
    
    def on_land(self):
        """Appelé quand l'ennemi atterrit"""
        self.jumping = False
        self.velocity_y = 0
    
    def draw(self, screen):
        """Dessine le Metall"""
        if self.guarding:
            image = self.images["guard"][self.direction]
        else:
            image = self.images["normal"][self.direction]
        
        screen.blit(image, self)
        
        # Dessine les projectiles
        for bullet in self.bullets:
            screen.blit(bullet.image, bullet)


class Blader(Enemy):
    """
    Ennemi Blader - Vole en pattern circulaire.
    """
    
    def __init__(self, x, y, images):
        super().__init__(x, y, BLADER_WIDTH, BLADER_HEIGHT, BLADER_HEALTH)
        self.images = images
        self.start_x = x
        self.start_y = y
        self.velocity_x = BLADER_VELOCITY_X
        self.velocity_y = BLADER_VELOCITY_Y
        self.max_range_x = BLADER_RANGE_X
        self.max_range_y = BLADER_RANGE_Y
    
    def update(self, player_x=None):
        """Met à jour le mouvement du Blader"""
        # Mouvement horizontal
        if abs(self.x + self.velocity_x - self.start_x) >= self.max_range_x:
            self.velocity_x *= -1
            self.direction = "left" if self.velocity_x < 0 else "right"
        else:
            self.x += self.velocity_x
        
        # Mouvement vertical
        if abs(self.y + self.velocity_y - self.start_y) >= self.max_range_y:
            self.velocity_y *= -1
        else:
            self.y += self.velocity_y
    
    def on_land(self):
        """Blader vole, donc ne s'arrête pas au sol"""
        pass  # Blader ignore les collisions verticales car il vole
    
    def draw(self, screen):
        """Dessine le Blader"""
        image = self.images[self.direction]
        screen.blit(image, self)


class Gutsman(Enemy):
    """
    Boss Gutsman - Saute et lance des rochers.
    """
    
    def __init__(self, x, y, images):
        super().__init__(x, y, GUTSMAN_WIDTH, GUTSMAN_HEIGHT, GUTSMAN_HEALTH)
        self.images = images
        self.state = "idle"  # idle, jump, throw
        self.timer = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = False
        self.health_bar = HealthBar()
        
    def update(self, player_x):
        """Met à jour le boss"""
        # Direction
        if player_x < self.x:
            self.direction = "left"
            self.facing_right = False
        else:
            self.direction = "right"
            self.facing_right = True
            
        # Gravité
        self.velocity_y += GUTSMAN_GRAVITY
        self.y += self.velocity_y
        
        # Logique simple d'IA
        now = pygame.time.get_ticks()
        
        if self.state == "idle":
            if now - self.timer > 2000:  # 2 secondes d'attente
                # Décision: Sauter ou Lancer
                if abs(self.x - player_x) > GUTSMAN_ATTACK_RANGE:
                    self.state = "jump"
                    self.velocity_y = GUTSMAN_JUMP_FORCE
                    # Sauter vers le joueur
                    self.velocity_x = -GUTSMAN_VELOCITY_X if not self.facing_right else GUTSMAN_VELOCITY_X
                    self.on_ground = False
                    Logger.log("STATE", "Gutsman: IDLE -> JUMP")
                else:
                    self.state = "throw"
                    self.timer = now
                    Logger.log("STATE", "Gutsman: IDLE -> THROW")
                    
        elif self.state == "jump":
            self.x += self.velocity_x
            # Atterrissage géré par on_land
            
        elif self.state == "throw":
            if now - self.timer > 1000:  # 1 seconde d'animation de lancer
                self.state = "idle"
                self.timer = now
                Logger.log("STATE", "Gutsman: THROW -> IDLE")
                # TODO: Créer le projectile ici
    
    def on_land(self):
        """Atterrissage"""
        if not self.on_ground:
            self.on_ground = True
            self.velocity_y = 0
            self.velocity_x = 0
            self.state = "idle"
            self.timer = pygame.time.get_ticks()
            Logger.log("STATE", "Gutsman: JUMP -> IDLE (Landed)")
            
            # Tremblement de terre (optionnel)
            # Logger.log("INFO", "Gutsman caused an earthquake!")

    def draw(self, screen):
        """Dessine Gutsman"""
        # Choix de l'image selon l'état (simplifié pour l'instant)
        # On suppose que self.images est un dictionnaire ou une surface unique
        # Si c'est un dictionnaire, on accède par clé
        
        img = self.images  # Par défaut
        
        if isinstance(self.images, dict):
            if self.state == "jump":
                img = self.images.get("jump", self.images.get("idle"))
            elif self.state == "throw":
                img = self.images.get("throw", self.images.get("idle"))
            else:
                img = self.images.get("idle")
                
            # Flip si nécessaire (si les images sont orientées à droite par défaut)
            # Supposons que les images sont chargées pour les deux directions ou qu'on flip ici
            # Pour l'instant on suppose que le loader gère les directions comme pour les autres ennemis
            if isinstance(img, dict):
                img = img.get(self.direction)
        
        if img:
            screen.blit(img, self)
            
        # Dessine la barre de vie (Composition Pattern)
        self.health_bar.draw(screen, self.x, self.y - 10, self.health, GUTSMAN_HEALTH)


class HealthBar:
    """
    Barre de vie pour entités (Composition Pattern).
    """
    def draw(self, screen, x, y, current_health, max_health):
        width = GUTSMAN_WIDTH
        height = 5
        
        # Fond rouge
        pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        
        # Vie verte
        if current_health > 0:
            ratio = current_health / max_health
            pygame.draw.rect(screen, (0, 255, 0), (x, y, width * ratio, height))
            
        # Bordure noire
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)


class Item(pygame.Rect):
    """
    Classe de base pour les objets collectables.
    """
    
    def __init__(self, x, y, width, height, item_type, value, image):
        """
        Args:
            x, y: Position
            width, height: Dimensions
            item_type: Type d'objet ("life_energy", "score_ball", etc.)
            value: Valeur (soin ou points)
            image: Image de l'objet
        """
        super().__init__(x, y, width, height)
        self.item_type = item_type
        self.value = value
        self.image = image
        self.velocity_y = ITEM_VELOCITY_Y
        self.jumping = True  # L'objet vole vers le haut au départ
        self.used = False
    
    def update(self):
        """Met à jour la physique de l'objet"""
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
    
    def on_land(self):
        """Appelé quand l'objet atterrit"""
        self.jumping = False
        self.velocity_y = 0
    
    def draw(self, screen):
        """Dessine l'objet"""
        screen.blit(self.image, self)


def load_enemy_images():
    """Charge les images des ennemis"""
    def load_image(name, size):
        try:
            img = pygame.image.load(os.path.join(ASSETS_DIR, name))
            return pygame.transform.scale(img, size)
        except:
            Logger.error(f"Could not load image: {name}")
            surf = pygame.Surface(size)
            surf.fill((255, 0, 0))  # Rouge pour erreur
            return surf
    
    images = {
        "metall": {
            "normal": {
                "right": load_image("metall-right.png", (METALL_WIDTH, METALL_HEIGHT)),
                "left": load_image("metall-left.png", (METALL_WIDTH, METALL_HEIGHT))
            },
            "guard": {
                "right": load_image("metall-right-guard.png", (METALL_WIDTH, METALL_HEIGHT)),
                "left": load_image("metall-left-guard.png", (METALL_WIDTH, METALL_HEIGHT))
            },
            "bullet": load_image("metall-bullet.png", (METALL_BULLET_WIDTH, METALL_BULLET_HEIGHT))
        },
        "blader": {
            "right": load_image("blader-right.png", (BLADER_WIDTH, BLADER_HEIGHT)),
            "left": load_image("blader-left.png", (BLADER_WIDTH, BLADER_HEIGHT))
        },
        "gutsman": {
            "idle": {
                "right": load_image("gutsman.png", (GUTSMAN_WIDTH, GUTSMAN_HEIGHT)),
                "left": pygame.transform.flip(load_image("gutsman.png", (GUTSMAN_WIDTH, GUTSMAN_HEIGHT)), True, False)
            },
            "jump": {
                "right": load_image("gutsman.png", (GUTSMAN_WIDTH, GUTSMAN_HEIGHT)),
                "left": pygame.transform.flip(load_image("gutsman.png", (GUTSMAN_WIDTH, GUTSMAN_HEIGHT)), True, False)
            },
            "throw": {
                "right": load_image("gutsman.png", (GUTSMAN_WIDTH, GUTSMAN_HEIGHT)),
                "left": pygame.transform.flip(load_image("gutsman.png", (GUTSMAN_WIDTH, GUTSMAN_HEIGHT)), True, False)
            }
        }
    }
    
    Logger.log("INFO", "Enemy images loaded successfully")
    return images


def load_item_images():
    """Charge les images des objets"""
    def load_image(name, size):
        try:
            img = pygame.image.load(os.path.join(ASSETS_DIR, name))
            return pygame.transform.scale(img, size)
        except:
            Logger.error(f"Could not load image: {name}")
            surf = pygame.Surface(size)
            surf.fill((0, 255, 0))  # Vert pour erreur
            return surf
    
    images = {
        "life_energy": load_image("life-energy.png", (LIFE_ENERGY_WIDTH, LIFE_ENERGY_HEIGHT)),
        "big_life_energy": load_image("big-life-energy.png", (BIG_LIFE_ENERGY_WIDTH, BIG_LIFE_ENERGY_HEIGHT)),
        "score_ball": load_image("score-ball.png", (TILE_SIZE // 2, TILE_SIZE // 2))
    }
    
    Logger.log("INFO", "Item images loaded successfully")
    return images
