# Megaman 2D Platformer - Projet Design Patterns

![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Un jeu de plateforme 2D Megaman développé en Python/Pygame, implémentant 6 design patterns pour un projet académique.

## 🎮 Description

Ce projet est un jeu de plateforme 2D inspiré de Megaman, développé dans le cadre d'un cours sur les design patterns. Le jeu démontre l'utilisation pratique de 6 patterns de conception différents dans une application interactive complète.

## 📋 Design Patterns Implémentés

### 1. **Singleton Pattern** - GameManager
- **Fichier**: `game_manager.py`
- **Utilisation**: Garantit une instance unique du gestionnaire de jeu
- **Logging**: `Logger.log("SINGLETON", "GameManager instance created")`

### 2. **Observer Pattern** - Système d'événements
- **Fichiers**: `events/event_system.py`, `events/observers.py`
- **Utilisation**: Communication event-driven entre systèmes (score, santé, sons, achievements)
- **Observateurs**: ScoreObserver, HealthObserver, SoundObserver, AchievementObserver
- **Logging**: `Logger.log("OBSERVER", "Event ENEMY_DEFEATED notified to X observers")`

### 3. **State Pattern** - États du joueur
- **Fichiers**: `player/player.py`, `player/player_states.py`
- **États**: IdleState, RunningState, JumpingState, ShootingState, RunningShootingState, JumpShootingState
- **Utilisation**: Gère les comportements du joueur selon son état actuel
- **Logging**: `Logger.log("STATE", "Player: IDLE -> JUMPING")`

### 4. **Factory Pattern** - Création d'entités
- **Fichiers**: `entities/entity_factory.py`
- **Factories**: EnemyFactory (Metall, Blader), ItemFactory (LifeEnergy, ScoreBall)
- **Utilisation**: Centralise la création des ennemis et objets
- **Logging**: `Logger.log("FACTORY", "EnemyFactory created Metall at (x, y)")`

### 5. **Decorator Pattern** - Power-ups
- **Fichier**: `powerups/powerup_decorators.py`
- **Décorateurs**: SpeedBoostDecorator, StrengthBoostDecorator, DefenseBoostDecorator, HealthBoostDecorator, MultiShotDecorator
- **Utilisation**: Ajoute dynamiquement des capacités au joueur
- **Logging**: `Logger.log("DECORATOR", "SpeedBoostDecorator applied to Player")`

### 6. **Composite Pattern** - Structure des niveaux
- **Fichiers**: `levels/level_components.py`, `levels/level_loader.py`
- **Structure**: Level → Zone → Tile (hiérarchie composant/composite)
- **Utilisation**: Organisation hiérarchique des éléments de niveau
- **Logging**: `Logger.log("COMPOSITE", "Zone 'Entrance' added to Level 1")`

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Pygame 2.5.2

### Étapes

1. Cloner le dépôt:
```bash
git clone [URL_DU_DEPOT]
cd "projet megaman"
```

2. Installer les dépendances:
```bash
pip install pygame
```

3. Lancer le jeu:
```bash
python main.py
```

## 🎯 Utilisation

### Commandes
- **Flèches Gauche/Droite** ou **A/D**: Déplacement
- **Flèche Haut** ou **W**: Saut
- **Barre d'espace** ou **X**: Tir
- **Échap**: Pause
- **Entrée**: Redémarrer (après Game Over)

### Objectif
Éliminez les ennemis, collectez des objets pour restaurer votre santé et marquez le maximum de points!

## 📁 Structure du Projet

```
projet megaman/
├── main.py                 # Point d'entrée du jeu
├── game_manager.py         # Singleton - Gestionnaire de jeu
├── logger.py               # Système de logging
├── config.py               # Configuration centralisée
├── tile_map.py            # Données des niveaux
├── player/                # State Pattern
│   ├── player.py
│   └── player_states.py
├── entities/              # Factory Pattern
│   ├── entities.py
│   └── entity_factory.py
├── powerups/              # Decorator Pattern
│   └── powerup_decorators.py
├── levels/                # Composite Pattern
│   ├── level_components.py
│   └── level_loader.py
├── events/                # Observer Pattern
│   ├── event_system.py
│   └── observers.py
└── images/                # Assets graphiques
```

## 🔍 Système de Logging

Le jeu implémente un système de traçabilité complet qui enregistre tous les événements liés aux design patterns dans le fichier `game.log`.

### Niveaux de logging:
- `SINGLETON`: Création et accès au GameManager
- `STATE`: Transitions d'états du joueur
- `FACTORY`: Création d'entités
- `DECORATOR`: Application de power-ups
- `COMPOSITE`: Construction de la hiérarchie de niveaux
- `OBSERVER`: Notifications d'événements
- `INFO`: Événements généraux
- `ERROR`: Erreurs

### Exemple de log:
```
[2025-11-30 19:00:00] [SINGLETON] GameManager instance created
[2025-11-30 19:00:01] [FACTORY] EnemyFactory created Metall at (352, 416)
[2025-11-30 19:00:02] [STATE] Player: IDLE -> JUMPING
[2025-11-30 19:00:03] [OBSERVER] Event ENEMY_DEFEATED notified to 3 observer(s)
```

## 🧪 Tests

Pour tester individuellement chaque pattern:

```bash
# Test Singleton
python game_manager.py

# Test Observer
python events/event_system.py

# Test Factory
python entities/entity_factory.py

# Test Decorator
python powerups/powerup_decorators.py

# Test Composite
python levels/level_components.py
```

## 👥 Membres du Groupe

- [Nom de l'étudiant]

## 🛠️ Technologies Utilisées

- **Langage**: Python 3.8+
- **Framework**: Pygame 2.5.2
- **Logging**: Module logging standard Python
- **Assets**: Images du projet de référence

## 📖 Référence

Ce projet s'inspire du tutorial Pygame de Kenny Yip:
- Repository: https://github.com/ImKennyYip/pygame
- Playlist YouTube: [Pygame Programming](https://www.youtube.com/playlist?list=PLnKe36F30Y4Ykmi2jE28BZahMgPAV3Dzv)

## 📝 Notes de Développement

- Architecture entièrement orientée objet (refactorisation du code procédural de référence)
- Séparation claire des responsabilités entre les modules
- Système extensible permettant l'ajout facile de nouveaux ennemis, power-ups, et niveaux
- Documentation complète avec docstrings
- Logging exhaustif pour démontrer l'utilisation des patterns

## 🏆 Critères de Réussite

✅ **4+ Design Patterns** implémentés (6 au total)  
✅ **Système de logging** fonctionnel et documenté  
✅ **Code commenté** et structuré  
✅ **Interface graphique** fonctionnelle avec Pygame  
✅ **Jeu jouable** avec gameplay complet  
✅ **Architecture extensible** et maintenable  
✅ **Git** avec historique de commits  

## 📄 Licence

Ce projet est développé dans un cadre académique. Les assets graphiques proviennent du projet de référence de Kenny Yip.

---

**Projet réalisé dans le cadre du cours de Design Patterns**  
*Module: Design Patterns | Enseignant: Haythem Ghazouani*
