# Megaman 2D Platformer - Projet Design Patterns

Jeu de plateforme 2D développé en Python/Pygame, implémentant 6 design patterns pour un projet académique.

## Description

Ce projet démontre l'utilisation pratique de 6 patterns de conception dans une application interactive complète inspirée de Megaman.

## Design Patterns Implémentés

### 1. Singleton Pattern - GameManager
- **Fichier**: `game_manager.py`
- **Rôle**: Instance unique du gestionnaire de jeu.

### 2. Observer Pattern - Système d'événements
- **Fichiers**: `events/event_system.py`, `events/observers.py`
- **Rôle**: Communication découplée entre systèmes (score, santé, sons).

### 3. State Pattern - États du joueur
- **Fichiers**: `player/player_states.py`
- **Rôle**: Gestion des comportements (Idle, Running, Jumping, Shooting).

### 4. Factory Pattern - Création d'entités
- **Fichiers**: `entities/entity_factory.py`
- **Rôle**: Création centralisée des ennemis et objets.

### 5. Decorator Pattern - Power-ups
- **Fichier**: `powerups/powerup_decorators.py`
- **Rôle**: Ajout dynamique de capacités au joueur.

### 6. Composite Pattern - Structure des niveaux
- **Fichiers**: `levels/level_components.py`
- **Rôle**: Hiérarchie Level > Zone > Tile.

## Installation

1. Cloner le dépôt:
```bash
git clone https://github.com/mbmohamed/Megaman-2D-Platformer.git
cd "projet megaman"
```

2. Installer les dépendances:
```bash
pip install pygame
```

3. Lancer le jeu:
```bash
python3 main.py
```

## Commandes

- **Flèches / WASD**: Déplacement et Saut
- **Espace / X**: Tir
- **Echap**: Pause
- **Entrée**: Redémarrer

## Structure du Projet

```
projet megaman/
├── main.py                 # Point d'entrée
├── game_manager.py         # Singleton
├── logger.py               # Logging
├── config.py               # Configuration
├── tile_map.py            # Données niveaux
├── player/                # State Pattern
├── entities/              # Factory Pattern
├── powerups/              # Decorator Pattern
├── levels/                # Composite Pattern
├── events/                # Observer Pattern
└── images/                # Assets
```

## Logging

Le fichier `game.log` trace l'exécution des patterns :
- `SINGLETON`, `STATE`, `FACTORY`, `DECORATOR`, `COMPOSITE`, `OBSERVER`

## Tests

Exécuter les scripts individuels pour tester chaque pattern :
```bash
python game_manager.py
python events/event_system.py
python entities/entity_factory.py
python powerups/powerup_decorators.py
python levels/level_components.py
```

## Crédits

- **Membres**: Mohamed Ben Madhi
- **Cours**: Design Patterns | Enseignant: Haythem Ghazouani
- **Référence**: Inspiré du tutoriel Pygame de Kenny Yip.
