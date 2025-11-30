"""
Megaman 2D Platformer - Main Game
Projet de design patterns avec Pygame

Design Patterns implémentés:
1. Singleton - GameManager
2. Observer - EventManager et observateurs
3. State - États du joueur
4. Factor - Création d'entités
5. Decorator - Power-ups
6. Composite - Structure des niveaux
"""

import pygame
from sys import exit
import os

from game_manager import GameManager
from logger import Logger
from config import *

from player import Player, load_player_images
from entities import load_enemy_images, load_item_images, EnemyFactory, ItemFactory
from levels import LevelLoader, load_tile_images
from events import EventManager, ScoreObserver, HealthObserver, SoundObserver, AchievementObserver


class Game:
    """
    Classe principale du jeu.
    Gère la boucle de jeu et coordonne tous les systèmes.
    """
    
    def __init__(self):
        """Initialise le jeu"""
        Logger.log("INFO", "=== MEGAMAN GAME STARTING ===")
        
        # Récupère le GameManager (Singleton)
        self.game_manager = GameManager.get_instance()
        self.game_manager.initialize_pygame()
        
        # Charge les images
        Logger.log("INFO", "Loading assets...")
        self.player_images = load_player_images()
        self.enemy_images = load_enemy_images()
        self.item_images = load_item_images()
        self.tile_images = load_tile_images()
        
        # Charge le background
        try:
            self.background = pygame.image.load(os.path.join(ASSETS_DIR, "background.png"))
        except:
            self.background = None
            Logger.error("Could not load background image")
        
        # Crée les Factories (Factory Pattern)
        self.enemy_factory = EnemyFactory(self.enemy_images)
        self.item_factory = ItemFactory(self.item_images)
        
        # Crée le level loader (Composite Pattern)
        self.level_loader = LevelLoader(self.enemy_factory, self.tile_images)
        
        # Initialise le système d'événements (Observer Pattern)
        self.event_manager = EventManager()
        self.game_manager.event_manager = self.event_manager
        
        # Initialise le jeu
        self.reset_game()
        
        Logger.log("INFO", "Game initialized successfully")
    
    def reset_game(self):
        """Reinitialise le jeu"""
        # Crée le joueur (State Pattern)
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, self.player_images)
        self.game_manager.player = self.player
        
        # Charge le niveau (Composite Pattern + Factory Pattern)
        self.level, self.enemies, self.spikes = self.level_loader.load_level(1)
        self.game_manager.current_level_obj = self.level
        
        # Liste d'objets collectables
        self.items = []
        
        # Configure les observateurs (Observer Pattern)
        self.score_observer = ScoreObserver(self.game_manager)
        self.health_observer = HealthObserver(self.player)
        self.sound_observer = SoundObserver()
        self.achievement_observer = AchievementObserver(self.game_manager)
        
        # Abonne les observateurs aux événements
        self.event_manager.subscribe(EVENT_ENEMY_DEFEATED, self.score_observer)
        self.event_manager.subscribe(EVENT_ENEMY_DEFEATED, self.sound_observer)
        self.event_manager.subscribe(EVENT_ENEMY_DEFEATED, self.achievement_observer)
        
        self.event_manager.subscribe(EVENT_ITEM_COLLECTED, self.score_observer)
        self.event_manager.subscribe(EVENT_ITEM_COLLECTED, self.health_observer)
        self.event_manager.subscribe(EVENT_ITEM_COLLECTED, self.sound_observer)
        
        self.event_manager.subscribe(EVENT_PLAYER_HIT, self.health_observer)
        self.event_manager.subscribe(EVENT_PLAYER_HIT, self.sound_observer)
        
        self.event_manager.subscribe(EVENT_LEVEL_COMPLETE, self.achievement_observer)
        
        self.game_manager.reset_game()
    
    def handle_input(self):
        """Gère les entrées utilisateur"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_manager.quit()
                return
        
        keys = pygame.key.get_pressed()
        
        # Réinitialisation du jeu
        if self.game_manager.game_over and (keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]):
            self.reset_game()
            return
        
        # Pause
        if keys[pygame.K_ESCAPE]:
            self.game_manager.toggle_pause()
            pygame.time.wait(200)  # Évite la répétition
        
        # Délègue au joueur (State Pattern) et gère le scrolling
        if not self.game_manager.game_over and not self.game_manager.paused:
            # Scrolling horizontal - déplace la map au lieu du joueur
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.move_map_x(PLAYER_VELOCITY_X)
                self.player.direction = "left"
            
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move_map_x(-PLAYER_VELOCITY_X)
                self.player.direction = "right"
            
            # Le reste des contrôles (saut, tir) est géré par le State Pattern
            self.player.handle_input(keys)
    
    def move_map_x(self, velocity_x):
        """
        Déplace tous les éléments de la map horizontalement (scrolling).
        
        Args:
            velocity_x: Vélocité horizontale (positif = droite, négatif = gauche)
        """
        # Déplace les tuiles du niveau
        for zone in self.level.get_children():
            for component in zone.get_children():
                component.x += velocity_x
        
        # Déplace les spikes
        for spike in self.spikes:
            spike.x += velocity_x
        
        # Déplace les ennemis
        for enemy in self.enemies:
            enemy.x += velocity_x
            # Ajuste la position de départ pour les ennemis mobiles
            if hasattr(enemy, 'start_x'):
                enemy.start_x += velocity_x
            # Déplace les projectiles des ennemis
            if hasattr(enemy, 'bullets'):
                for bullet in enemy.bullets:
                    bullet.x += velocity_x
        
        # Déplace les projectiles du joueur
        for bullet in self.player.bullets:
            bullet.x += velocity_x
        
        # Déplace les objets collectables
        for item in self.items:
            item.x += velocity_x
    
    def update(self):
        """Met à jour la logique du jeu"""
        if self.game_manager.game_over or self.game_manager.paused:
            return
        
        # Met à jour le joueur
        self.player.update()
        
        # Applique la gravité et vérifie les collisions
        self.check_collisions()
        
        # Met à jour les ennemis
        for enemy in self.enemies:
            enemy.update(self.player.x)
            
            # Collision joueur-ennemi
            if not self.player.invincible and self.player.colliderect(enemy):
                self.player.take_damage(1)
                self.event_manager.notify_observers(EVENT_PLAYER_HIT, {"damage": 1})
            
            # Collision projectiles joueur - ennemis
            for bullet in self.player.bullets:
                if bullet.colliderect(enemy) and not bullet.used:
                    bullet.used = True
                    enemy.health -= 1
                    
                    if enemy.health <= 0:
                        # Ennemi vaincu
                        self.event_manager.notify_observers(EVENT_ENEMY_DEFEATED, 
                                                           {"enemy": enemy.__class__.__name__, 
                                                            "points": ENEMY_KILL_SCORE})
                        # Drop d'objet (Factory Pattern)
                        dropped_item = self.item_factory.drop_random_item(enemy.x, enemy.y)
                        if dropped_item:
                            self.items.append(dropped_item)
            
            # Collision projectiles ennemis - joueur
            if hasattr(enemy, 'bullets'):
                for bullet in enemy.bullets:
                    if not self.player.invincible and self.player.colliderect(bullet) and not bullet.used:
                        bullet.used = True
                        self.player.take_damage(2)
                        self.event_manager.notify_observers(EVENT_PLAYER_HIT, {"damage": 2})
        
        # Retire les ennemis vaincus
        self.enemies = [e for e in self.enemies if e.health > 0]
        
        # Met à jour les objets
        for item in self.items:
            item.update()
            
            # Collision joueur-objet
            if self.player.colliderect(item) and not item.used:
                item.used = True
                
                if item.item_type in ["life_energy", "big_life_energy"]:
                    self.player.heal(item.value)
                
                self.event_manager.notify_observers(EVENT_ITEM_COLLECTED, 
                                                   {"type": item.item_type, 
                                                    "heal": item.value if "energy" in item.item_type else 0})
        
        # Retire les objets collectés
        self.items = [i for i in self.items if not i.used]
        
        # Collision avec les pièges
        for spike in self.spikes:
            if self.player.colliderect(spike):
                self.player.health = 0
        
        # Vérifie la mort du joueur
        if self.player.health <= 0 or self.player.y > GAME_HEIGHT:
            self.game_manager.set_game_over(True)
    
    def check_collisions(self):
        """Vérifie les collisions avec les tuiles"""
        solid_tiles = self.level.get_all_solid_tiles()
        
        # Collision verticale (joueur)
        for tile in solid_tiles:
            if self.player.colliderect(tile):
                if self.player.velocity_y > 0:  # Tombe
                    self.player.y = tile.y - self.player.height
                    self.player.on_land()
                elif self.player.velocity_y < 0:  # Monte
                    self.player.y = tile.y + tile.height
                    self.player.velocity_y = 0
        
        # Collision pour les ennemis
        for enemy in self.enemies:
            for tile in solid_tiles:
                if enemy.colliderect(tile):
                    if enemy.velocity_y > 0:
                        enemy.y = tile.y - enemy.height
                        enemy.on_land()
                    elif enemy.velocity_y < 0:
                        enemy.y = tile.y + tile.height
                        enemy.velocity_y = 0
        
        # Collision pour les objets
        for item in self.items:
            for tile in solid_tiles:
                if item.colliderect(tile) and item.velocity_y > 0:
                    item.y = tile.y - item.height
                    item.on_land()
    
    def draw(self):
        """Dessine tous les éléments du jeu"""
        # Background
        self.game_manager.screen.fill(COLOR_SKY)
        if self.background:
            self.game_manager.screen.blit(self.background, (0, 80))
        
        # Niveau (Composite Pattern)
        self.level.render(self.game_manager.screen)
        
        # Joueur
        self.player.draw(self.game_manager.screen)
        
        # Ennemis
        for enemy in self.enemies:
            enemy.draw(self.game_manager.screen)
        
        # Objets
        for item in self.items:
            item.draw(self.game_manager.screen)
        
        # HUD - Barre de vie
        health_bar_bg = pygame.Rect(HEALTH_BAR_X, HEALTH_BAR_Y, 
                                    HEALTH_WIDTH, HEALTH_HEIGHT * self.player.max_health)
        pygame.draw.rect(self.game_manager.screen, COLOR_BLACK, health_bar_bg)
        
        for i in range(self.player.health):
            health_rect = pygame.Rect(HEALTH_BAR_X, 
                                      HEALTH_BAR_Y + (self.player.max_health - i - 1) * HEALTH_HEIGHT,
                                      HEALTH_WIDTH, HEALTH_HEIGHT)
            pygame.draw.rect(self.game_manager.screen, COLOR_WHITE, health_rect)
        
        # HUD - Score
        score_text = self.game_manager.get_formatted_score()
        score_surface = self.game_manager.font.render(score_text, False, COLOR_WHITE)
        self.game_manager.screen.blit(score_surface, (GAME_WIDTH // 2, TILE_SIZE // 2))
        
        # Game Over
        if self.game_manager.game_over:
            game_over_text = self.game_manager.font.render("Game Over!", False, COLOR_WHITE)
            restart_text = self.game_manager.font.render("Press [Enter] to Restart", False, COLOR_WHITE)
            
            self.game_manager.screen.blit(game_over_text, (GAME_WIDTH // 8, GAME_HEIGHT // 2))
            self.game_manager.screen.blit(restart_text, (GAME_WIDTH // 8, GAME_HEIGHT // 2 + TILE_SIZE))
        
        # Pause
        if self.game_manager.paused and not self.game_manager.game_over:
            pause_text = self.game_manager.font.render("PAUSED", False, COLOR_WHITE)
            self.game_manager.screen.blit(pause_text, (GAME_WIDTH // 2 - 60, GAME_HEIGHT // 2))
        
        pygame.display.update()
    
    def run(self):
        """Boucle de jeu principale"""
        Logger.log("INFO", "=== GAME LOOP STARTING ===")
        
        while self.game_manager.running:
            self.handle_input()
            self.update()
            self.draw()
            self.game_manager.clock.tick(FPS)
        
        pygame.quit()
        Logger.log("INFO", "=== GAME ENDED ===")


def main():
    """Point d'entrée du jeu"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        Logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        exit(1)


if __name__ == "__main__":
    main()
