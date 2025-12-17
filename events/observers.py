"""
Observateurs concrets - Observer Pattern
Implémentations concrètes des observateurs pour différents systèmes.
"""

from events.event_system import Observer
from logger import Logger
from config import *
import pygame
import os


class ScoreObserver(Observer):
    """
    Observateur qui gère le score du jeu.
    Réagit aux événements d'ennemis vaincus et d'objets collectés.
    """
    
    def __init__(self, game_manager):
        """
        Args:
            game_manager: Instance du GameManager
        """
        self.game_manager = game_manager
        Logger.log("OBSERVER", "ScoreObserver created")
    
    def notify(self, event_type: int, data: dict = None):
        """Réagit aux événements liés au score"""
        if event_type == EVENT_ENEMY_DEFEATED:
            points = data.get("points", ENEMY_KILL_SCORE) if data else ENEMY_KILL_SCORE
            self.game_manager.add_score(points)
            self.game_manager.increment_enemies_defeated()
            
        elif event_type == EVENT_ITEM_COLLECTED:
            if data and data.get("type") == "score_ball":
                self.game_manager.add_score(SCORE_BALL_POINTS)
            self.game_manager.increment_items_collected()


class HealthObserver(Observer):
    """
    Observateur qui gère la santé du joueur.
    Réagit aux dégâts et aux soins.
    """
    
    def __init__(self, player):
        """
        Args:
            player: Instance du Player
        """
        self.player = player
        Logger.log("OBSERVER", "HealthObserver created")
    
    def notify(self, event_type: int, data: dict = None):
        """Réagit aux événements liés à la santé"""
        if event_type == EVENT_PLAYER_HIT:
            damage = data.get("damage", 1) if data else 1
            # La logique de dégâts est gérée ailleurs pour éviter les dépendances circulaires
            Logger.log("INFO", f"Player hit for {damage} damage")
        
        elif event_type == EVENT_ITEM_COLLECTED:
            if data and data.get("type") in ["life_energy", "big_life_energy"]:
                heal_amount = data.get("heal", 0)
                # La logique de soin est gérée par le joueur
                Logger.log("INFO", f"Player healed for {heal_amount} HP")


class SoundObserver(Observer):
    """
    Observateur qui gère les effets sonores.
    (Implémentation simplifiée sans sons réels pour ce projet)
    """
    
    def __init__(self):
        try:
            pygame.mixer.init()
            Logger.log("OBSERVER", "SoundObserver initialized (Mixer ready)")
        except:
            Logger.error("Could not initialize pygame mixer")
    
    def notify(self, event_type: int, data: dict = None):
        """Réagit aux événements pour jouer des sons"""
        sound_map = {
            EVENT_ENEMY_DEFEATED: "enemy_defeat.wav",
            EVENT_ITEM_COLLECTED: "item_collect.wav",
            EVENT_PLAYER_HIT: "player_hit.wav",
            EVENT_LEVEL_COMPLETE: "level_complete.wav"
        }
        
        if event_type in sound_map:
            sound_file = sound_map[event_type]
            # Vérifie si le fichier existe
            if os.path.exists(sound_file):
                try:
                    pygame.mixer.Sound(sound_file).play()
                except:
                    pass
            else:
                # Logger.log("INFO", f"Sound file missing: {sound_file}")
                pass


class AchievementObserver(Observer):
    """
    Observateur qui gère les succès/achievements.
    """
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.achievements = {
            "first_kill": False,
            "10_kills": False,
            "perfect_health": False
        }
        Logger.log("OBSERVER", "AchievementObserver created")
    
    def notify(self, event_type: int, data: dict = None):
        """Vérifie et débloque les succès"""
        if event_type == EVENT_ENEMY_DEFEATED:
            if not self.achievements["first_kill"]:
                self.achievements["first_kill"] = True
                Logger.log("INFO", "Achievement unlocked: First Kill!")
            
            if self.game_manager.enemies_defeated >= 10 and not self.achievements["10_kills"]:
                self.achievements["10_kills"] = True
                Logger.log("INFO", "Achievement unlocked: 10 Enemies Defeated!")
        
        elif event_type == EVENT_LEVEL_COMPLETE:
            if self.game_manager.player and self.game_manager.player.health == PLAYER_MAX_HEALTH:
                if not self.achievements["perfect_health"]:
                    self.achievements["perfect_health"] = True
                    Logger.log("INFO", "Achievement unlocked: Perfect Health!")
