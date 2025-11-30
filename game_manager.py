"""
Game Manager - Singleton Pattern
Gestionnaire central du jeu garantissant une instance unique.
Coordonne tous les systèmes du jeu.
"""

import pygame
from logger import Logger
from config import *


class GameManager:
    """
    Singleton Pattern - Gestionnaire central du jeu.
    
    Responsabilités:
    - Gestion de l'état global du jeu
    - Coordination entre les systèmes
    - Gestion du score et du niveau actuel
    - Point d'accès centralisé aux ressources
    """
    
    _instance = None
    
    def __new__(cls):
        """
        Implémente le pattern Singleton.
        Garantit qu'une seule instance de GameManager existe.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            Logger.log("SINGLETON", "GameManager instance created")
        return cls._instance
    
    def __init__(self):
        """Initialise le GameManager une seule fois"""
        if self._initialized:
            return
        
        Logger.log("SINGLETON", "GameManager initialization starting")
        
        # État du jeu
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Score et statistiques
        self.score = 0
        self.current_level = 1
        self.enemies_defeated = 0
        self.items_collected = 0
        
        # Configuration Pygame
        self.screen = None
        self.clock = None
        self.font = None
        
        # Références aux systèmes
        self.event_manager = None
        self.player = None
        self.current_level_obj = None
        
        self._initialized = True
        Logger.log("SINGLETON", "GameManager initialization complete")
    
    @classmethod
    def get_instance(cls):
        """
        Méthode statique pour obtenir l'instance unique.
        
        Returns:
            GameManager: L'instance unique du gestionnaire
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def initialize_pygame(self):
        """Initialise Pygame et crée la fenêtre"""
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Megaman - Design Patterns Project")
        
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        except:
            Logger.error(f"Could not load font {FONT_PATH}, using default")
            self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        
        Logger.log("INFO", "Pygame initialized successfully")
    
    def add_score(self, points: int):
        """
        Ajoute des points au score.
        
        Args:
            points: Nombre de points à ajouter
        """
        self.score += points
        Logger.log("INFO", f"Score updated: +{points} (total: {self.score})")
    
    def increment_enemies_defeated(self):
        """Incrémente le compteur d'ennemis vaincus"""
        self.enemies_defeated += 1
        Logger.log("INFO", f"Enemies defeated: {self.enemies_defeated}")
    
    def increment_items_collected(self):
        """Incrémente le compteur d'objets collectés"""
        self.items_collected += 1
        Logger.log("INFO", f"Items collected: {self.items_collected}")
    
    def set_game_over(self, is_over: bool = True):
        """
        Définit l'état game over.
        
        Args:
            is_over: True si le jeu est terminé
        """
        self.game_over = is_over
        if is_over:
            Logger.log("INFO", "Game Over!")
    
    def reset_game(self):
        """Réinitialise le jeu"""
        Logger.log("INFO", "Resetting game...")
        self.score = 0
        self.enemies_defeated = 0
        self.items_collected = 0
        self.game_over = False
        self.paused = False
    
    def toggle_pause(self):
        """Bascule l'état de pause"""
        self.paused = not self.paused
        Logger.log("INFO", f"Game {'paused' if self.paused else 'resumed'}")
    
    def quit(self):
        """Quitte le jeu proprement"""
        Logger.log("INFO", "Shutting down game...")
        self.running = False
        pygame.quit()
    
    def get_formatted_score(self) -> str:
        """
        Retourne le score formaté avec des zéros à gauche.
        
        Returns:
            str: Score formaté (ex: "0001500")
        """
        score_str = str(self.score)
        while len(score_str) < SCORE_DIGITS:
            score_str = "0" + score_str
        return score_str


# Test du Singleton
if __name__ == "__main__":
    # Crée deux instances et vérifie qu'elles sont identiques
    gm1 = GameManager()
    gm2 = GameManager.get_instance()
    
    print(f"gm1 is gm2: {gm1 is gm2}")  # Doit être True
    
    gm1.add_score(100)
    print(f"gm2 score: {gm2.score}")  # Doit être 100
    
    Logger.log("INFO", "Singleton test passed!")
