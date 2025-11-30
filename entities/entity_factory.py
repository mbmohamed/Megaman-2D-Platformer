"""
Factory Pattern - Création centralisée d'entités
Factories pour créer les ennemis, items et tiles.
"""

from entities.entities import Metall, Blader, Gutsman, Item
from logger import Logger
from config import *
import random


class EntityFactory:
    """
    Classe de base abstraite pour les factories.
    """
    
    def create(self, entity_type: str, x: int, y: int, **kwargs):
        """
        Crée une entité.
        
        Args:
            entity_type: Type d'entité à créer
            x, y: Position
            **kwargs: Arguments supplémentaires
        
        Returns:
            L'entité créée
        """
        raise NotImplementedError("Subclasses must implement create method")


class EnemyFactory(EntityFactory):
    """
    Factory Pattern - Création des ennemis.
    """
    
    def __init__(self, enemy_images):
        """
        Args:
            enemy_images: Dictionnaire d'images des ennemis
        """
        self.images = enemy_images
        Logger.log("FACTORY", "EnemyFactory initialized")
    
    def create(self, entity_type: str, x: int, y: int, **kwargs):
        """
        Crée un ennemi selon son type.
        
        Args:
            entity_type: "metall" ou "blader"
            x, y: Position
        
        Returns:
            Enemy: Instance d'ennemi créée
        """
        enemy = None
        
        if entity_type == "metall":
            enemy = Metall(x, y, self.images["metall"])
            Logger.log("FACTORY", f"EnemyFactory created Metall at ({x}, {y})")
            
        elif entity_type == "blader":
            enemy = Blader(x, y, self.images["blader"])
            Logger.log("FACTORY", f"EnemyFactory created Blader at ({x}, {y})")
            
        elif entity_type == "gutsman":
            enemy = Gutsman(x, y, self.images["gutsman"])
            Logger.log("FACTORY", f"EnemyFactory created Gutsman at ({x}, {y})")
        
        else:
            Logger.error(f"Unknown enemy type: {entity_type}")
        
        return enemy


class ItemFactory(EntityFactory):
    """
    Factory Pattern - Création des objets collectables.
    """
    
    def __init__(self, item_images):
        """
        Args:
            item_images: Dictionnaire d'images des objets
        """
        self.images = item_images
        Logger.log("FACTORY", "ItemFactory initialized")
    
    def create(self, entity_type: str, x: int, y: int, **kwargs):
        """
        Crée un objet selon son type.
        
        Args:
            entity_type: "life_energy", "big_life_energy", ou "score_ball"
            x, y: Position
        
        Returns:
            Item: Instance d'objet créée
        """
        item = None
        
        if entity_type == "life_energy":
            item = Item(
                x, y,
                LIFE_ENERGY_WIDTH, LIFE_ENERGY_HEIGHT,
                "life_energy",
                LIFE_ENERGY_HEAL,
                self.images["life_energy"]
            )
            Logger.log("FACTORY", f"ItemFactory created LifeEnergy at ({x}, {y})")
            
        elif entity_type == "big_life_energy":
            item = Item(
                x, y,
                BIG_LIFE_ENERGY_WIDTH, BIG_LIFE_ENERGY_HEIGHT,
                "big_life_energy",
                BIG_LIFE_ENERGY_HEAL,
                self.images["big_life_energy"]
            )
            Logger.log("FACTORY", f"ItemFactory created BigLifeEnergy at ({x}, {y})")
            
        elif entity_type == "score_ball":
            item = Item(
                x, y,
                TILE_SIZE // 2, TILE_SIZE // 2,
                "score_ball",
                SCORE_BALL_POINTS,
                self.images["score_ball"]
            )
            Logger.log("FACTORY", f"ItemFactory created ScoreBall at ({x}, {y})")
        
        else:
            Logger.error(f"Unknown item type: {entity_type}")
        
        return item
    
    def drop_random_item(self, x: int, y: int):
        """
        Fait apparaître un objet aléatoire (comme drop d'ennemi).
        
        Args:
            x, y: Position
        
        Returns:
            Item or None: Objet créé ou None si pas de drop
        """
        chance = random.randint(1, 100)
        
        if chance <= 20:  # 20% chance de big life energy
            return self.create("big_life_energy", x, y)
        elif chance <= 50:  # 30% chance de life energy
            return self.create("life_energy", x, y)
        elif chance <= ITEM_DROP_CHANCE:  # 25% chance de score ball
            return self.create("score_ball", x, y)
        else:
            Logger.log("INFO", f"No item dropped at ({x}, {y})")
            return None


# Test du pattern Factory
if __name__ == "__main__":
    import pygame
    pygame.init()
    
    from entities.entities import load_enemy_images, load_item_images
    
    # Charge les images
    enemy_images = load_enemy_images()
    item_images = load_item_images()
    
    # Crée les factories
    enemy_factory = EnemyFactory(enemy_images)
    item_factory = ItemFactory(item_images)
    
    # Test de création
    metall = enemy_factory.create("metall", 100, 200)
    blader = enemy_factory.create("blader", 150, 250)
    
    life_energy = item_factory.create("life_energy", 200, 300)
    score_ball = item_factory.create("score_ball", 250, 350)
    
    # Test drop aléatoire
    for i in range(5):
        item = item_factory.drop_random_item(i * 50, 400)
        if item:
            print(f"Dropped: {item.item_type}")
    
    Logger.log("INFO", "Factory pattern test passed!")
