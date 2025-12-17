"""
États du joueur (State Pattern)
"""

import pygame
from logger import Logger
from config import *


class PlayerState:
    """
    Interface pour les états du joueur.
    """
    def handle_input(self, player, keys):
        """
        Gère les entrées utilisateur.
        """
        raise NotImplementedError("State must implement handle_input")

    def update(self, player):
        """
        Met à jour l'état du joueur.
        """
        raise NotImplementedError("State must implement update")

    def get_image(self, player):
        """
        Retourne l'image pour cet état.
        """
        raise NotImplementedError("State must implement get_image")


class IdleState(PlayerState):
    """
    Joueur immobile.
    """
    def handle_input(self, player, keys):
        from player.player import Player  # Import local pour éviter boucle
        # Saut
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
            Logger.log("STATE", "Player: IDLE -> JUMPING")
            player.set_state(JumpingState())
            player.velocity_y = PLAYER_VELOCITY_Y
            player.jumping = True
            return
        # Gauche
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            Logger.log("STATE", "Player: IDLE -> RUNNING")
            player.set_state(RunningState())
            player.direction = "left"
            return
        # Droite
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
        player.velocity_x = 0
    def get_image(self, player):
        return player.images["idle"][player.direction]


class RunningState(PlayerState):
    """
    Joueur court.
    """
    def __init__(self):
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
    def handle_input(self, player, keys):
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
        # Arrêt
        if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            Logger.log("STATE", "Player: RUNNING -> IDLE")
            player.set_state(IdleState())
            return
            player.velocity_x = player.get_speed()
    def update(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_update > PLAYER_ANIMATION_SPEED:
            self.last_update = now
            self.animation_index = (self.animation_index + 1) % len(player.images["walk"][player.direction])
    def get_image(self, player):
        return player.images["walk"][player.direction][self.animation_index]


class JumpingState(PlayerState):
    """
    Joueur saute.
    """
    def handle_input(self, player, keys):
        # Tir en sautant
        if keys[pygame.K_SPACE] or keys[pygame.K_x]:
            Logger.log("STATE", "Player: JUMPING -> JUMP_SHOOTING")
            player.set_state(JumpShootingState())
            player.shoot()
            return
    def update(self, player):
        # Atterrissage géré par collision
        if not player.jumping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                Logger.log("STATE", "Player: JUMPING -> RUNNING")
                player.set_state(RunningState())
            else:
                Logger.log("STATE", "Player: JUMPING -> IDLE")
                player.set_state(RunningState())
    def get_image(self, player):
        return player.images["jump"][player.direction]


class ShootingState(PlayerState):
    """
    Joueur tire (immobile).
    """
    def __init__(self):
        self.shoot_time = pygame.time.get_ticks()
        self.duration = PLAYER_SHOOT_COOLDOWN
    def handle_input(self, player, keys):
        # Retour à Idle après le cooldown
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.duration:
            Logger.log("STATE", "Player: SHOOTING -> IDLE")
            player.set_state(IdleState())
    def update(self, player):
        player.velocity_x = 0
    def get_image(self, player):
        return player.images["shoot"][player.direction]


class RunningShootingState(PlayerState):
    """
    Joueur tire en courant.
    """
    def __init__(self):
        self.shoot_time = pygame.time.get_ticks()
        self.duration = PLAYER_SHOOT_COOLDOWN
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()
    def handle_input(self, player, keys):
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
    def update(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_update > PLAYER_ANIMATION_SPEED:
            self.last_update = now
            self.animation_index = (self.animation_index + 1) % len(player.images["walk_shoot"][player.direction])
    def get_image(self, player):
        return player.images["walk_shoot"][player.direction][self.animation_index]


class JumpShootingState(PlayerState):
    """
    Joueur tire en sautant.
    """
    def __init__(self):
        self.shoot_time = pygame.time.get_ticks()
        self.duration = PLAYER_SHOOT_COOLDOWN
    def handle_input(self, player, keys):
        # Retour à Jumping après le cooldown
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.duration:
            Logger.log("STATE", "Player: JUMP_SHOOTING -> JUMPING")
            player.set_state(JumpingState())
    def update(self, player):
        # Vérifie l'atterrissage
        if not player.jumping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                Logger.log("STATE", "Player: JUMP_SHOOTING -> RUNNING")
                player.set_state(RunningState())
            else:
                Logger.log("STATE", "Player: JUMP_SHOOTING -> IDLE")
                player.set_state(RunningState())
    def get_image(self, player):
        return player.images["jump_shoot"][player.direction]
