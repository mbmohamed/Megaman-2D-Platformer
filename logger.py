"""
Système de logging pour tracer les événements du jeu.
Utilisé pour démontrer l'utilisation des design patterns.
"""

import logging
from datetime import datetime
from pathlib import Path


class Logger:
    """
    Classe de logging centralisée pour le projet.
    Trace les événements liés aux design patterns et au gameplay.
    """
    
    # Niveaux de logging personnalisés pour les design patterns
    SINGLETON = "SINGLETON"
    STATE = "STATE"
    DECORATOR = "DECORATOR"
    FACTORY = "FACTORY"
    COMPOSITE = "COMPOSITE"
    OBSERVER = "OBSERVER"
    ERROR = "ERROR"
    INFO = "INFO"
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implémente un Singleton pour le logger"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialise le logger une seule fois"""
        if not Logger._initialized:
            self._setup_logger()
            Logger._initialized = True
    
    def _setup_logger(self):
        """Configure le système de logging"""
        # Crée le logger
        self.logger = logging.getLogger("MegamanGame")
        self.logger.setLevel(logging.DEBUG)
        
        # Format du message
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler pour fichier
        file_handler = logging.FileHandler('game.log', mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Ajoute les handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    @classmethod
    def log(cls, level: str, message: str):
        """
        Log un message avec un niveau personnalisé.
        
        Args:
            level: Niveau de log (SINGLETON, STATE, DECORATOR, etc.)
            message: Message à logger
        """
        instance = cls()
        formatted_message = f"[{level}] {message}"
        instance.logger.info(formatted_message)
    
    @classmethod
    def error(cls, message: str):
        """Log une erreur"""
        instance = cls()
        instance.logger.error(f"[ERROR] {message}")
    
    @classmethod
    def info(cls, message: str):
        """Log une information"""
        instance = cls()
        instance.logger.info(f"[INFO] {message}")


# Test du logger au démarrage
if __name__ == "__main__":
    Logger.log("INFO", "Logger system initialized")
    Logger.log("SINGLETON", "Test singleton pattern")
    Logger.log("STATE", "Test state pattern")
    Logger.error("Test error message")
