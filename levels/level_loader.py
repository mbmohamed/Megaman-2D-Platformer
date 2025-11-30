"""
Level Loader - Charge les niveaux depuis le tile map
Utilise les Factories pour créer les entités et le Composite Pattern pour la structure.
"""

import pygame
import os
from typing import List
from levels.level_components import Level, Zone, Tile
from entities import EnemyFactory, ItemFactory, Enemy
from logger import Logger
from config import *
import tile_map


def load_tile_images():
    """Charge les images des tuiles"""
    def load_image(name, size):
        try:
            img = pygame.image.load(os.path.join(ASSETS_DIR, name))
            return pygame.transform.scale(img, size)
        except:
            Logger.error(f"Could not load tile image: {name}")
            surf = pygame.Surface(size)
            surf.fill((128, 128, 128))
            return surf
    
    images = {
        "floor": load_image("floor-tile.png", (TILE_SIZE, TILE_SIZE)),
        "wall": load_image("wall-tile.png", (TILE_SIZE, TILE_SIZE)),
        "beam": load_image("beam-tile.png", (TILE_SIZE, TILE_SIZE)),
        "rock1": load_image("rock-tile1.png", (TILE_SIZE, TILE_SIZE)),
        "rock2": load_image("rock-tile2.png", (TILE_SIZE, TILE_SIZE)),
        "rock3": load_image("rock-tile3.png", (TILE_SIZE, TILE_SIZE)),
        "rock4": load_image("rock-tile4.png", (TILE_SIZE, TILE_SIZE)),
        "door": load_image("door-tile.png", (TILE_SIZE, TILE_SIZE)),
        "room": load_image("room-tile.png", (TILE_SIZE, TILE_SIZE)),
        "spike": load_image("spike.png", (TILE_SIZE, TILE_SIZE)),
    }
    
    Logger.log("INFO", "Tile images loaded successfully")
    return images


class LevelLoader:
    """
    Charge un niveau depuis une tile map et utilise le Composite Pattern.
    """
    
    def __init__(self, enemy_factory: EnemyFactory, tile_images: dict):
        """
        Args:
            enemy_factory: Factory pour créer les ennemis
            tile_images: Dictionnaire d'images de tuiles
        """
        self.enemy_factory = enemy_factory
        self.tile_images = tile_images
        Logger.log("INFO", "LevelLoader initialized")
    
    def load_level(self, level_number: int = 1) -> tuple[Level, List[Enemy], List[Tile]]:
        """
        Charge un niveau complet depuis le tile map.
        
        Args:
            level_number: Numéro du niveau (défaut: 1)
        
        Returns:
            tuple: (Level, liste d'ennemis, liste de spikes)
        """
        Logger.log("COMPOSITE", f"Loading level {level_number}...")
        
        # Récupère la carte du niveau
        game_map = tile_map.OPTIMIZED_GAME_MAP1
        
        # Crée le niveau (Composite Pattern)
        level = Level(level_number)
        
        # Crée les zones
        background_zone = Zone("Background")
        solid_zone = Zone("Solid Tiles")
        hazard_zone = Zone("Hazards")
        
        # Listes pour les entités
        enemies = []
        spikes = []
        
        # Parse la tile map
        for row_idx in range(len(game_map)):
            for col_idx in range(len(game_map[row_idx])):
                map_code = game_map[row_idx][col_idx]
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                
                if map_code == TILE_EMPTY:
                    continue
                
                # Traite les codes négatifs (background)
                is_background = map_code < 0
                abs_code = abs(map_code)
                
                # Tuiles rock
                if abs_code == TILE_ROCK1:
                    tile = Tile(x, y, self.tile_images["rock1"], is_solid=not is_background)
                    if is_background:
                        background_zone.add(tile)
                    else:
                        solid_zone.add(tile)
                
                elif abs_code == TILE_ROCK2:
                    tile = Tile(x, y, self.tile_images["rock2"], is_solid=not is_background)
                    if is_background:
                        background_zone.add(tile)
                    else:
                        solid_zone.add(tile)
                
                elif abs_code == TILE_ROCK3:
                    tile = Tile(x, y, self.tile_images["rock3"], is_solid=not is_background)
                    if is_background:
                        background_zone.add(tile)
                    else:
                        solid_zone.add(tile)
                
                elif abs_code == TILE_ROCK4:
                    tile = Tile(x, y, self.tile_images["rock4"], is_solid=not is_background)
                    if is_background:
                        background_zone.add(tile)
                    else:
                        solid_zone.add(tile)
                
                elif abs_code == TILE_FLOOR:
                    tile = Tile(x, y, self.tile_images["floor"], is_solid=not is_background)
                    if is_background:
                        background_zone.add(tile)
                    else:
                        solid_zone.add(tile)
                
                elif abs_code == TILE_WALL:
                    tile = Tile(x, y, self.tile_images["wall"], is_solid=not is_background)
                    if is_background:
                        background_zone.add(tile)
                    else:
                        solid_zone.add(tile)
                
                elif map_code == TILE_BEAM:
                    tile = Tile(x, y, self.tile_images["beam"], is_solid=False)
                    background_zone.add(tile)
                
                elif map_code == TILE_DOOR:
                    tile = Tile(x, y, self.tile_images["door"], is_solid=False)
                    background_zone.add(tile)
                
                elif map_code == TILE_ROOM:
                    tile = Tile(x, y, self.tile_images["room"], is_solid=False)
                    background_zone.add(tile)
                
                elif map_code == TILE_SPIKE:
                    spike = Tile(x, y, self.tile_images["spike"], is_solid=False)
                    hazard_zone.add(spike)
                    spikes.append(spike)
                
                # Ennemis (utilise Factory Pattern)
                elif map_code == TILE_METALL:
                    metall = self.enemy_factory.create("metall", x, y)
                    enemies.append(metall)
                
                elif map_code == TILE_BLADER:
                    blader = self.enemy_factory.create("blader", x, y)
                    enemies.append(blader)
        
        # Assemble le niveau (Composite Pattern)
        level.add(background_zone)
        level.add(solid_zone)
        level.add(hazard_zone)
        
        Logger.log("COMPOSITE", 
                  f"Level {level_number} loaded: {len(enemies)} enemies, "
                  f"{len(spikes)} spikes, {len(level.get_all_solid_tiles())} solid tiles")
        
        return level, enemies, spikes


# Test du loader
if __name__ == "__main__":
    pygame.init()
    
    from entities import load_enemy_images
    
    # Charge les images
    enemy_images = load_enemy_images()
    tile_images = load_tile_images()
    
    # Crée la factory
    enemy_factory = EnemyFactory(enemy_images)
    
    # Crée le loader
    loader = LevelLoader(enemy_factory, tile_images)
    
    # Charge le niveau
    level, enemies, spikes = loader.load_level(1)
    
    print(f"Loaded {len(enemies)} enemies")
    print(f"Loaded {len(spikes)} spikes")
    print(f"Level has {len(level.get_all_solid_tiles())} solid tiles")
    
    Logger.log("INFO", "LevelLoader test passed!")
