"""
Player - Utilise le State Pattern
Le joueur Megaman avec gestion d'états dynamique.
"""

import pygame
import os
from player.player_states import IdleState, PlayerState
from logger import Logger
from config import *


class Bullet(pygame.Rect):
    """
    Projectile du joueur.
    """
    
    def __init__(self, x, y, direction, image):
        """
        Args:
            x, y: Position initiale
            direction: Direction du tir ("left" ou "right")
            image: Image du projectile
        """
        super().__init__(x, y, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
        self.direction = direction
        self.velocity_x = -PLAYER_BULLET_VELOCITY_X if direction == "left" else PLAYER_BULLET_VELOCITY_X
        self.image = image
        self.used = False
    
    def update(self):
        """Met à jour la position du projectile"""
        self.x += self.velocity_x


class Player(pygame.Rect):
    """
    Joueur Megaman - Utilise le State Pattern.
    
    Le comportement du joueur change selon son état actuel:
    - IdleState
    - RunningState
    - JumpingState
    - ShootingState
    - RunningShootingState
    - JumpShootingState
    """
    
    def __init__(self, x, y, images):
        """
        Args:
            x, y: Position initiale
            images: Dictionnaire d'images du joueur
        """
        super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        # Images
        self.images = images
        
        # État actuel (State Pattern)
        self.state: PlayerState = IdleState()
        Logger.log("STATE", "Player initialized in IdleState")
        
        # Physique
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
        
        # Santé et invincibilité
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.invincible = False
        self.invincible_start = 0
        
        # Projectiles
        self.bullets = []
        self.last_shot = 0
        
        # Statistiques
        self.score = 0
    
    def set_state(self, new_state: PlayerState):
        """
        Change l'état du joueur (State Pattern).
        
        Args:
            new_state: Nouvel état à appliquer
        """
        self.state = new_state
    
    def handle_input(self, keys):
        """
        Délègue la gestion des entrées à l'état actuel.
        
        Args:
            keys: Touches pressées (pygame.key.get_pressed())
        """
        self.state.handle_input(self, keys)
    
    def update(self):
        """Met à jour le joueur"""
        # Délègue à l'état actuel
        self.state.update(self)
        
        # Applique la gravité
        self.velocity_y += GRAVITY
        
        # Met à jour la position Y
        self.y += self.velocity_y
        
        # Gère l'invincibilité
        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.invincible_start > INVINCIBILITY_DURATION:
                self.invincible = False
                Logger.log("INFO", "Invincibility ended")
        
        # Met à jour les projectiles
        for bullet in self.bullets:
            bullet.update()
        
        # Retire les projectiles hors écran ou utilisés
        self.bullets = [b for b in self.bullets 
                       if not b.used and 0 < b.x < GAME_WIDTH]
    
    def shoot(self):
        """Tire un projectile"""
        now = pygame.time.get_ticks()
        
        # Vérifie le cooldown
        if now - self.last_shot < PLAYER_SHOOT_COOLDOWN:
            return
        
        self.last_shot = now
        
        # Crée le projectile
        if self.direction == "left":
            x = self.x
        else:
            x = self.x + self.width
        
        y = self.y + TILE_SIZE / 2
        
        bullet = Bullet(x, y, self.direction, self.images["bullet"])
        self.bullets.append(bullet)
        Logger.log("INFO", f"Player shot bullet in direction {self.direction}")
    
    def take_damage(self, damage: int):
        """
        Inflige des dégâts au joueur.
        
        Args:
            damage: Quantité de dégâts
        """
        if self.invincible:
            return
        
        self.health -= damage
        self.health = max(0, self.health)
        
        Logger.log("INFO", f"Player took {damage} damage (health: {self.health}/{self.max_health})")
        
        if self.health > 0:
            self.set_invincible()
    
    def heal(self, amount: int):
        """
        Soigne le joueur.
        
        Args:
            amount: Quantité de soin
        """
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        actual_heal = self.health - old_health
        
        if actual_heal > 0:
            Logger.log("INFO", f"Player healed {actual_heal} HP (health: {self.health}/{self.max_health})")
    
    def set_invincible(self):
        """Active l'invincibilité temporaire"""
        self.invincible = True
        self.invincible_start = pygame.time.get_ticks()
        Logger.log("INFO", "Player is now invincible")
    
    def on_land(self):
        """Appelé quand le joueur atterrit"""
        self.jumping = False
        self.velocity_y = 0
    
    def draw(self, screen):
        """
        Dessine le joueur à l'écran.
        
        Args:
            screen: Surface Pygame
        """
        # Obtient l'image de l'état actuel
        image = self.state.get_image(self)
        
        # Effet de clignotement si invincible
        if self.invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:  # Clignote toutes les 100ms
                screen.blit(image, self)
        else:
            screen.blit(image, self)
        
        # Dessine les projectiles
        for bullet in self.bullets:
            screen.blit(bullet.image, bullet)


def load_player_images():
    """
    Charge toutes les images du joueur.
    
    Returns:
        dict: Dictionnaire d'images organisé par état
    """
    def load_image(name, size):
        """Charge une image"""
        try:
            img = pygame.image.load(os.path.join(ASSETS_DIR, name))
            return pygame.transform.scale(img, size)
        except:
            Logger.error(f"Could not load image: {name}")
            # Retourne un surface vide en cas d'erreur
            surf = pygame.Surface(size)
            surf.fill((255, 0, 255))  # Magenta pour indiquer l'erreur
            return surf
    
    images = {
        "idle": {
            "right": load_image("megaman-right.png", (PLAYER_WIDTH, PLAYER_HEIGHT)),
            "left": load_image("megaman-left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        },
        "jump": {
            "right": load_image("megaman-right-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT)),
            "left": load_image("megaman-left-jump.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
        },
        "shoot": {
            "right": load_image("megaman-right-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT)),
            "left": load_image("megaman-left-shoot.png", (PLAYER_SHOOT_WIDTH, PLAYER_HEIGHT))
        },
        "jump_shoot": {
            "right": load_image("megaman-right-jump-shoot.png", (PLAYER_JUMP_SHOOT_WIDTH, PLAYER_JUMP_HEIGHT)),
            "left": load_image("megaman-left-jump-shoot.png", (PLAYER_JUMP_SHOOT_WIDTH, PLAYER_JUMP_HEIGHT))
        },
        "walk": {
            "right": [load_image(f"megaman-right-walk{i}.png", (PLAYER_WALK_WIDTH, PLAYER_WALK_HEIGHT)) 
                     for i in range(4)],
            "left": [load_image(f"megaman-left-walk{i}.png", (PLAYER_WALK_WIDTH, PLAYER_WALK_HEIGHT)) 
                    for i in range(4)]
        },
        "walk_shoot": {
            "right": [load_image(f"megaman-right-walk-shoot{i}.png", (PLAYER_WALK_SHOOT_WIDTH, PLAYER_WALK_HEIGHT)) 
                     for i in range(4)],
            "left": [load_image(f"megaman-left-walk-shoot{i}.png", (PLAYER_WALK_SHOOT_WIDTH, PLAYER_WALK_HEIGHT)) 
                    for i in range(4)]
        },
        "bullet": load_image("bullet.png", (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
    }
    
    Logger.log("INFO", "Player images loaded successfully")
    return images
