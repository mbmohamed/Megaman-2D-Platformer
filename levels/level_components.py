"""
Composite Pattern - Structure hiérarchique des niveaux
Permet de traiter uniformément objets simples et composites.
"""

import pygame
from typing import List
from logger import Logger
from config import *


class GameComponent:
    """
    Interface Component pour le Composite Pattern.
    Définit les opérations communes aux objets simples et composites.
    """
    
    def update(self):
        """Met à jour le composant"""
        raise NotImplementedError
    
    def render(self, screen):
        """Dessine le composant"""
        raise NotImplementedError
    
    def add(self, component: 'GameComponent'):
        """Ajoute un composant enfant (pour les composites)"""
        raise NotImplementedError
    
    def remove(self, component: 'GameComponent'):
        """Retire un composant enfant (pour les composites)"""
        raise NotImplementedError
    
    def get_children(self) -> List['GameComponent']:
        """Retourne les enfants (pour les composites)"""
        raise NotImplementedError


class Tile(GameComponent, pygame.Rect):
    """
    Leaf - Tuile individuelle (objet simple).
    """
    
    def __init__(self, x: int, y: int, image, is_solid: bool = True):
        """
        Args:
            x, y: Position
            image: Image de la tuile
            is_solid: Si True, la tuile a des collisions
        """
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image
        self.is_solid = is_solid
    
    def update(self):
        """Les tuiles statiques ne se mettent pas à jour"""
        pass
    
    def render(self, screen):
        """Dessine la tuile"""
        screen.blit(self.image, self)
    
    def add(self, component):
        """Les feuilles ne peuvent pas avoir d'enfants"""
        raise NotImplementedError("Leaf cannot add children")
    
    def remove(self, component):
        """Les feuilles ne peuvent pas avoir d'enfants"""
        raise NotImplementedError("Leaf cannot remove children")
    
    def get_children(self):
        """Les feuilles n'ont pas d'enfants"""
        return []


class Zone(GameComponent):
    """
    Composite - Zone contenant plusieurs composants.
    Une zone peut contenir des tiles, des hazards, etc.
    """
    
    def __init__(self, name: str):
        """
        Args:
            name: Nom de la zone
        """
        self.name = name
        self._components: List[GameComponent] = []
        Logger.log("COMPOSITE", f"Zone '{name}' created")
    
    def update(self):
        """Met à jour tous les composants de la zone"""
        for component in self._components:
            component.update()
    
    def render(self, screen):
        """Dessine tous les composants de la zone"""
        for component in self._components:
            component.render(screen)
    
    def add(self, component: GameComponent):
        """Ajoute un composant à la zone"""
        self._components.append(component)
        # Logger.log("COMPOSITE", f"Component added to Zone '{self.name}'")  # Trop verbeux
    
    def remove(self, component: GameComponent):
        """Retire un composant de la zone"""
        if component in self._components:
            self._components.remove(component)
            # Logger.log("COMPOSITE", f"Component removed from Zone '{self.name}'")
    
    def get_children(self):
        """Retourne les composants de la zone"""
        return self._components.copy()
    
    def get_solid_tiles(self) -> List[Tile]:
        """Retourne toutes les tuiles solides de cette zone"""
        tiles = []
        for component in self._components:
            if isinstance(component, Tile) and component.is_solid:
                tiles.append(component)
            elif isinstance(component, Zone):
                tiles.extend(component.get_solid_tiles())
        return tiles


class Level(GameComponent):
    """
    Composite - Niveau complet contenant plusieurs zones.
    """
    
    def __init__(self, level_number: int):
        """
        Args:
            level_number: Numéro du niveau
        """
        self.level_number = level_number
        self._zones: List[Zone] = []
        Logger.log("COMPOSITE", f"Level {level_number} created")
    
    def update(self):
        """Met à jour toutes les zones"""
        for zone in self._zones:
            zone.update()
    
    def render(self, screen):
        """Dessine toutes les zones"""
        for zone in self._zones:
            zone.render(screen)
    
    def add(self, zone: Zone):
        """Ajoute une zone au niveau"""
        if isinstance(zone, Zone):
            self._zones.append(zone)
            Logger.log("COMPOSITE", f"Zone '{zone.name}' added to Level {self.level_number}")
        else:
            Logger.error("Only Zone objects can be added to Level")
    
    def remove(self, zone: Zone):
        """Retire une zone du niveau"""
        if zone in self._zones:
            self._zones.remove(zone)
            Logger.log("COMPOSITE", f"Zone '{zone.name}' removed from Level {self.level_number}")
    
    def get_children(self):
        """Retourne les zones du niveau"""
        return self._zones.copy()
    
    def get_all_solid_tiles(self) -> List[Tile]:
        """Retourne toutes les tuiles solides du niveau"""
        tiles = []
        for zone in self._zones:
            tiles.extend(zone.get_solid_tiles())
        return tiles
    
    def get_zone_by_name(self, name: str) -> Zone:
        """Trouve une zone par son nom"""
        for zone in self._zones:
            if zone.name == name:
                return zone
        return None


# Test du pattern Composite
if __name__ == "__main__":
    import os
    
    # Simule des images
    pygame.init()
    test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    test_surf.fill((100, 100, 100))
    
    # Crée un niveau
    level = Level(1)
    
    # Crée des zones
    entrance = Zone("Entrance")
    mid_section = Zone("Middle Section")
    boss_room = Zone("Boss Room")
    
    # Ajoute des tuiles à la zone d'entrée
    for i in range(5):
        tile = Tile(i * TILE_SIZE, GAME_HEIGHT - TILE_SIZE, test_surf)
        entrance.add(tile)
    
    # Ajoute des tuiles à la section du milieu
    for i in range(5, 10):
        tile = Tile(i * TILE_SIZE, GAME_HEIGHT - TILE_SIZE, test_surf)
        mid_section.add(tile)
    
    # Assemble le niveau
    level.add(entrance)
    level.add(mid_section)
    level.add(boss_room)
    
    # Teste la hiérarchie
    print(f"Level has {len(level.get_children())} zones")
    print(f"Total solid tiles: {len(level.get_all_solid_tiles())}")
    
    # Teste le rendu
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    level.render(screen)
    
    Logger.log("INFO", "Composite pattern test passed!")
