"""
Decorator Pattern - Système de power-ups
Permet d'ajouter dynamiquement des capacités au joueur.
"""

from logger import Logger
from config import *


class Character:
    """
    Interface Component pour le Decorator Pattern.
    Définit les méthodes que tous les personnages doivent avoir.
    """
    
    def get_speed(self) -> int:
        """Retourne la vitesse du personnage"""
        raise NotImplementedError
    
    def get_strength(self) -> int:
        """Retourne la force (dégâts) du personnage"""
        raise NotImplementedError
    
    def get_defense(self) -> int:
        """Retourne la défense du personnage"""
        raise NotImplementedError
    
    def get_max_health(self) -> int:
        """Retourne la santé maximale"""
        raise NotImplementedError


class BasePlayer(Character):
    """
    Composant concret de base - Le joueur sans améliorations.
    """
    
    def __init__(self):
        Logger.log("DECORATOR", "BasePlayer created (no power-ups)")
    
    def get_speed(self) -> int:
        """Vitesse de base"""
        return PLAYER_VELOCITY_X
    
    def get_strength(self) -> int:
        """Force de base (dégâts des tirs)"""
        return 1
    
    def get_defense(self) -> int:
        """Défense de base (réduction de dégâts)"""
        return 0
    
    def get_max_health(self) -> int:
        """Santé maximale de base"""
        return PLAYER_MAX_HEALTH


class PowerUpDecorator(Character):
    """
    Décorateur abstrait pour les power-ups.
    Tous les power-ups concrets héritent de cette classe.
    """
    
    def __init__(self, character: Character, powerup_name: str):
        """
        Args:
            character: Le personnage à améliorer
            powerup_name: Nom du power-up pour le logging
        """
        self._character = character
        Logger.log("DECORATOR", f"{powerup_name} applied to {character.__class__.__name__}")
    
    def get_speed(self) -> int:
        """Par défaut, retourne la vitesse du personnage décoré"""
        return self._character.get_speed()
    
    def get_strength(self) -> int:
        """Par défaut, retourne la force du personnage décoré"""
        return self._character.get_strength()
    
    def get_defense(self) -> int:
        """Par défaut, retourne la défense du personnage décoré"""
        return self._character.get_defense()
    
    def get_max_health(self) -> int:
        """Par défaut, retourne la santé max du personnage décoré"""
        return self._character.get_max_health()


class SpeedBoostDecorator(PowerUpDecorator):
    """
    Power-up: Augmente la vitesse du joueur.
    """
    
    def __init__(self, character: Character, multiplier: float = 2.0):
        """
        Args:
            character: Personnage à améliorer
            multiplier: Multiplicateur de vitesse (défaut: x2)
        """
        super().__init__(character, f"SpeedBoostDecorator(x{multiplier})")
        self.multiplier = multiplier
    
    def get_speed(self) -> int:
        """Multiplie la vitesse"""
        return int(self._character.get_speed() * self.multiplier)


class StrengthBoostDecorator(PowerUpDecorator):
    """
    Power-up: Augmente les dégâts du joueur.
    """
    
    def __init__(self, character: Character, multiplier: float = 2.0):
        """
        Args:
            character: Personnage à améliorer
            multiplier: Multiplicateur de force (défaut: x2)
        """
        super().__init__(character, f"StrengthBoostDecorator(x{multiplier})")
        self.multiplier = multiplier
    
    def get_strength(self) -> int:
        """Multiplie la force"""
        return int(self._character.get_strength() * self.multiplier)


class DefenseBoostDecorator(PowerUpDecorator):
    """
    Power-up: Augmente la défense du joueur (réduit les dégâts reçus).
    """
    
    def __init__(self, character: Character, defense_bonus: int = 2):
        """
        Args:
            character: Personnage à améliorer
            defense_bonus: Points de défense à ajouter
        """
        super().__init__(character, f"DefenseBoostDecorator(+{defense_bonus})")
        self.defense_bonus = defense_bonus
    
    def get_defense(self) -> int:
        """Ajoute de la défense"""
        return self._character.get_defense() + self.defense_bonus


class HealthBoostDecorator(PowerUpDecorator):
    """
    Power-up: Augmente la santé maximale du joueur.
    """
    
    def __init__(self, character: Character, health_bonus: int = 10):
        """
        Args:
            character: Personnage à améliorer
            health_bonus: Points de santé max à ajouter
        """
        super().__init__(character, f"HealthBoostDecorator(+{health_bonus})")
        self.health_bonus = health_bonus
    
    def get_max_health(self) -> int:
        """Augmente la santé maximale"""
        return self._character.get_max_health() + self.health_bonus


class MultiShotDecorator(PowerUpDecorator):
    """
    Power-up: Permet de tirer plusieurs projectiles à la fois.
    Note: Cette fonctionnalité nécessiterait une modification du système de tir.
    Pour l'instant, elle augmente juste la force.
    """
    
    def __init__(self, character: Character):
        super().__init__(character, "MultiShotDecorator")
    
    def get_strength(self) -> int:
        """Augmente significativement la force (simule plusieurs tirs)"""
        return self._character.get_strength() + 2


# Test du pattern Decorator
if __name__ == "__main__":
    # Crée un joueur de base
    player = BasePlayer()
    print(f"Base - Speed: {player.get_speed()}, Strength: {player.get_strength()}, "
          f"Defense: {player.get_defense()}, Max Health: {player.get_max_health()}")
    
    # Ajoute un boost de vitesse
    player = SpeedBoostDecorator(player)
    print(f"With Speed - Speed: {player.get_speed()}, Strength: {player.get_strength()}, "
          f"Defense: {player.get_defense()}, Max Health: {player.get_max_health()}")
    
    # Ajoute un boost de force
    player = StrengthBoostDecorator(player)
    print(f"With Speed+Strength - Speed: {player.get_speed()}, Strength: {player.get_strength()}, "
          f"Defense: {player.get_defense()}, Max Health: {player.get_max_health()}")
    
    # Ajoute de la défense
    player = DefenseBoostDecorator(player, defense_bonus=3)
    print(f"With All - Speed: {player.get_speed()}, Strength: {player.get_strength()}, "
          f"Defense: {player.get_defense()}, Max Health: {player.get_max_health()}")
    
    # Ajoute de la santé
    player = HealthBoostDecorator(player, health_bonus=15)
    print(f"With Health - Speed: {player.get_speed()}, Strength: {player.get_strength()}, "
          f"Defense: {player.get_defense()}, Max Health: {player.get_max_health()}")
    
    Logger.log("INFO", "Decorator pattern test passed!")
