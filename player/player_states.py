"""
State Pattern - États du joueur
Interface et implémentations concrètes des différents états du joueur.
"""

import pygame
from logger import Logger
from config import *


class PlayerState:
    """
    Interface State pour les états du joueur.
    Définit les méthodes que chaque état doit implémenter.
    """
    
    def handle_input(self, player, keys):
        """
        Gère les entrées utilisateur.
        
        Args:
            player: Instance du joueur
            keys: Touches pressées (pygame.key.get_pressed())
        """
        raise NotImplementedError("State must implement handle_input")
    
    def update(self, player):
        """
        Met à jour l'état du joueur.
        
        Args:
            player: Instance du joueur
        """
        raise NotImplementedError("State must implement update")
    
    def get_image(self, player):
        """
        Retourne l'image appropriée pour cet état.
        
        Args:
            player: Instance du joueur
        
        Returns:
            pygame.Surface: Image à afficher
        """
        raise NotImplementedError("State must implement get_image")


class IdleState(PlayerState):
    """
    État: Le joueur est immobile.
    """
    
    def handle_input(self, player, keys):
        """Gère les transitions depuis l'état Idle"""
        from player.player import Player  # Import local pour éviter circular import
        
        # Saut
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
            Logger.log("STATE", "Player: IDLE -> JUMPING")
            player.set_state(JumpingState())
            player.velocity_y = PLAYER_VELOCITY_Y
            player.jumping = True
            return
        
        # Déplacement gauche
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            Logger.log("STATE", "Player: IDLE -> RUNNING")
            player.set_state(RunningState())
            player.direction = "left"
            return
        
        # Déplacement droite
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            Logger.log("STATE", "Player: IDLE -> RUNNING")
            player.set_state(RunningState())
            player.direction = "right"
            return
        
        # Tir
        if keys[pygame.K_SPACE] or keys[pygame.K_x]:
            Logger.log("STATE", "Player: IDLE -> SHOOTING")
            player.set_state(ShootingState())
            player.shoot()
            return
    
    def update(self, player):
        """Met à jour la physique en état Idle"""
        player.velocity_x = 0
    
    def get_image(self, player):
        """Retourne l'image idle selon la direction"""
        return player.images["idle"][player.direction]


class RunningState(PlayerState):
    """
    État: Le joueur court.
    """
    
    def __init__(self):
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
    
    def handle_input(self, player, keys):
        """Gère les transitions depuis l'état Running"""
        # Saut
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
            Logger.log("STATE", "Player: RUNNING -> JUMPING")
            player.set_state(JumpingState())
            player.velocity_y = PLAYER_VELOCITY_Y
            player.jumping = True
            return
        
        # Tir en courant
        if keys[pygame.K_SPACE] or keys[pygame.K_x]:
            Logger.log("STATE", "Player: RUNNING -> RUNNING_SHOOTING")
            player.set_state(RunningShootingState())
            player.shoot()
            return
        
        # Arrêt du mouvement
        if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            Logger.log("STATE", "Player: RUNNING -> IDLE")
            player.set_state(IdleState())
            return
        
        # Mise à jour de la direction
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction = "left"
            player.velocity_x = -PLAYER_VELOCITY_X
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction = "right"
            player.velocity_x = PLAYER_VELOCITY_X
    
    def update(self, player):
        """Met à jour l'animation de course"""
        now = pygame.time.get_ticks()
        if now - self.last_update > PLAYER_ANIMATION_SPEED:
            self.last_update = now
            self.animation_index = (self.animation_index + 1) % len(player.images["walk"][player.direction])
    
    def get_image(self, player):
        """Retourne l'image de course animée"""
        return player.images["walk"][player.direction][self.animation_index]


class JumpingState(PlayerState):
    """
    État: Le joueur saute.
    """
    
    def handle_input(self, player, keys):
        """Gère les transitions depuis l'état Jumping"""
        # Contrôle horizontal en l'air
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction = "left"
            player.velocity_x = -PLAYER_VELOCITY_X
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction = "right"
            player.velocity_x = PLAYER_VELOCITY_X
        else:
            player.velocity_x = 0
        
        # Tir en sautant
        if keys[pygame.K_SPACE] or keys[pygame.K_x]:
            Logger.log("STATE", "Player: JUMPING -> JUMP_SHOOTING")
            player.set_state(JumpShootingState())
            player.shoot()
            return
    
    def update(self, player):
        """Met à jour la physique du saut"""
        # L'atterrissage est géré par le système de collision
        if not player.jumping:  # Le joueur a atterri
            if player.velocity_x == 0:
                Logger.log("STATE", "Player: JUMPING -> IDLE")
                player.set_state(IdleState())
            else:
                Logger.log("STATE", "Player: JUMPING -> RUNNING")
                player.set_state(RunningState())
    
    def get_image(self, player):
        """Retourne l'image de saut"""
        return player.images["jump"][player.direction]


class ShootingState(PlayerState):
    """
    État: Le joueur tire (immobile).
    """
    
    def __init__(self):
        self.shoot_time = pygame.time.get_ticks()
        self.duration = PLAYER_SHOOT_COOLDOWN
    
    def handle_input(self, player, keys):
        """Gère les transitions depuis l'état Shooting"""
        # Retour à Idle après le cooldown
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.duration:
            Logger.log("STATE", "Player: SHOOTING -> IDLE")
            player.set_state(IdleState())
    
    def update(self, player):
        """Maintient le joueur immobile pendant le tir"""
        player.velocity_x = 0
    
    def get_image(self, player):
        """Retourne l'image de tir"""
        return player.images["shoot"][player.direction]


class RunningShootingState(PlayerState):
    """
    État: Le joueur tire en courant.
    """
    
    def __init__(self):
        self.shoot_time = pygame.time.get_ticks()
        self.duration = PLAYER_SHOOT_COOLDOWN
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
    
    def handle_input(self, player, keys):
        """Gère les transitions depuis l'état RunningShoot"""
        now = pygame.time.get_ticks()
        
        # Retour à Running après le cooldown
        if now - self.shoot_time > self.duration:
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                Logger.log("STATE", "Player: RUNNING_SHOOTING -> RUNNING")
                player.set_state(RunningState())
            else:
                Logger.log("STATE", "Player: RUNNING_SHOOTING -> IDLE")
                player.set_state(IdleState())
            return
        
        # Mise à jour direction
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction = "left"
            player.velocity_x = -PLAYER_VELOCITY_X
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction = "right"
            player.velocity_x = PLAYER_VELOCITY_X
        else:
            player.velocity_x = 0
    
    def update(self, player):
        """Met à jour l'animation"""
        now = pygame.time.get_ticks()
        if now - self.last_update > PLAYER_ANIMATION_SPEED:
            self.last_update = now
            self.animation_index = (self.animation_index + 1) % len(player.images["walk_shoot"][player.direction])
    
    def get_image(self, player):
        """Retourne l'image de course + tir animée"""
        return player.images["walk_shoot"][player.direction][self.animation_index]


class JumpShootingState(PlayerState):
    """
    État: Le joueur tire en sautant.
    """
    
    def __init__(self):
        self.shoot_time = pygame.time.get_ticks()
        self.duration = PLAYER_SHOOT_COOLDOWN
    
    def handle_input(self, player, keys):
        """Gère les transitions depuis l'état JumpShooting"""
        # Contrôle horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction = "left"
            player.velocity_x = -PLAYER_VELOCITY_X
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction = "right"
            player.velocity_x = PLAYER_VELOCITY_X
        else:
            player.velocity_x = 0
        
        # Retour à Jumping après le cooldown
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.duration:
            Logger.log("STATE", "Player: JUMP_SHOOTING -> JUMPING")
            player.set_state(JumpingState())
    
    def update(self, player):
        """Vérifie l'atterrissage"""
        if not player.jumping:
            if player.velocity_x == 0:
                Logger.log("STATE", "Player: JUMP_SHOOTING -> IDLE")
                player.set_state(IdleState())
            else:
                Logger.log("STATE", "Player: JUMP_SHOOTING -> RUNNING")
                player.set_state(RunningState())
    
    def get_image(self, player):
        """Retourne l'image de saut + tir"""
        return player.images["jump_shoot"][player.direction]
