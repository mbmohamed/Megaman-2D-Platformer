"""
Observer Pattern - Système d'événements
Permet aux objets de s'abonner et de réagir aux événements du jeu.
"""

from typing import Dict, List, Callable
from logger import Logger
from config import *


class Observer:
    """
    Interface Observer.
    Les observateurs doivent implémenter cette méthode pour recevoir les notifications.
    """
    
    def notify(self, event_type: int, data: dict = None):
        """
        Méthode appelée quand un événement se produit.
        
        Args:
            event_type: Type d'événement (EVENT_ENEMY_DEFEATED, etc.)
            data: Données optionnelles liées à l'événement
        """
        raise NotImplementedError("Observer must implement notify method")


class EventManager:
    """
    Subject (Observable) - Gestionnaire d'événements centralisé.
    
    Implémente le pattern Observer pour permettre aux objets
    de s'abonner aux événements du jeu.
    """
    
    def __init__(self):
        """Initialise le gestionnaire d'événements"""
        # Dictionnaire: event_type -> liste d'observateurs
        self._observers: Dict[int, List[Observer]] = {}
        Logger.log("OBSERVER", "EventManager initialized")
    
    def subscribe(self, event_type: int, observer: Observer):
        """
        Abonne un observateur à un type d'événement.
        
        Args:
            event_type: Type d'événement (EVENT_ENEMY_DEFEATED, etc.)
            observer: Observateur à abonner
        """
        if event_type not in self._observers:
            self._observers[event_type] = []
        
        if observer not in self._observers[event_type]:
            self._observers[event_type].append(observer)
            event_name = self._get_event_name(event_type)
            Logger.log("OBSERVER", 
                      f"Observer {observer.__class__.__name__} subscribed to {event_name}")
    
    def unsubscribe(self, event_type: int, observer: Observer):
        """
        Désabonne un observateur d'un type d'événement.
        
        Args:
            event_type: Type d'événement
            observer: Observateur à désabonner
        """
        if event_type in self._observers and observer in self._observers[event_type]:
            self._observers[event_type].remove(observer)
            event_name = self._get_event_name(event_type)
            Logger.log("OBSERVER", 
                      f"Observer {observer.__class__.__name__} unsubscribed from {event_name}")
    
    def notify_observers(self, event_type: int, data: dict = None):
        """
        Notifie tous les observateurs d'un événement.
        
        Args:
            event_type: Type d'événement qui s'est produit
            data: Données optionnelles liées à l'événement
        """
        if event_type in self._observers:
            event_name = self._get_event_name(event_type)
            observer_count = len(self._observers[event_type])
            Logger.log("OBSERVER", 
                      f"Event {event_name} notified to {observer_count} observer(s)")
            
            for observer in self._observers[event_type]:
                observer.notify(event_type, data)
    
    def _get_event_name(self, event_type: int) -> str:
        """Retourne le nom lisible d'un type d'événement"""
        event_names = {
            EVENT_ENEMY_DEFEATED: "ENEMY_DEFEATED",
            EVENT_ITEM_COLLECTED: "ITEM_COLLECTED",
            EVENT_PLAYER_HIT: "PLAYER_HIT",
            EVENT_LEVEL_COMPLETE: "LEVEL_COMPLETE"
        }
        return event_names.get(event_type, f"UNKNOWN_EVENT_{event_type}")


# Test du pattern Observer
if __name__ == "__main__":
    # Observateur de test
    class TestObserver(Observer):
        def __init__(self, name):
            self.name = name
        
        def notify(self, event_type, data=None):
            print(f"{self.name} received event {event_type} with data: {data}")
    
    # Test
    event_manager = EventManager()
    
    obs1 = TestObserver("Observer1")
    obs2 = TestObserver("Observer2")
    
    event_manager.subscribe(EVENT_ENEMY_DEFEATED, obs1)
    event_manager.subscribe(EVENT_ENEMY_DEFEATED, obs2)
    event_manager.subscribe(EVENT_ITEM_COLLECTED, obs1)
    
    event_manager.notify_observers(EVENT_ENEMY_DEFEATED, {"enemy": "Metall", "points": 500})
    event_manager.notify_observers(EVENT_ITEM_COLLECTED, {"item": "LifeEnergy"})
    
    Logger.log("INFO", "Observer pattern test passed!")
