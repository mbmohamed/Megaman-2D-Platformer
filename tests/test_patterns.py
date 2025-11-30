"""
Quick test script to verify all patterns are working
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_singleton():
    """Test Singleton Pattern"""
    from game_manager import GameManager
    
    gm1 = GameManager()
    gm2 = GameManager.get_instance()
    
    assert gm1 is gm2, "Singleton failed: instances are different"
    print("✅ Singleton Pattern: PASSED")
    return True

def test_observer():
    """Test Observer Pattern"""
    from events.event_system import EventManager, Observer
    from config import EVENT_ENEMY_DEFEATED
    
    class TestObserver(Observer):
        def __init__(self):
            self.notified = False
        
        def notify(self, event_type, data=None):
            self.notified = True
    
    em = EventManager()
    obs = TestObserver()
    em.subscribe(EVENT_ENEMY_DEFEATED, obs)
    em.notify_observers(EVENT_ENEMY_DEFEATED)
    
    assert obs.notified, "Observer not notified"
    print("✅ Observer Pattern: PASSED")
    return True

def test_factory():
    """Test Factory Pattern"""
    import pygame
    pygame.init()
    
    from entities import EnemyFactory, load_enemy_images
    
    images = load_enemy_images()
    factory = EnemyFactory(images)
    
    metall = factory.create("metall", 100, 100)
    blader = factory.create("blader", 200, 200)
    
    assert metall is not None, "Factory failed to create Metall"
    assert blader is not None, "Factory failed to create Blader"
    print("✅ Factory Pattern: PASSED")
    return True

def test_decorator():
    """Test Decorator Pattern"""
    from powerups import BasePlayer, SpeedBoostDecorator, StrengthBoostDecorator
    
    player = BasePlayer()
    base_speed = player.get_speed()
    
    player = SpeedBoostDecorator(player, 2.0)
    boosted_speed = player.get_speed()
    
    assert boosted_speed == base_speed * 2, "Decorator didn't boost speed"
    print("✅ Decorator Pattern: PASSED")
    return True

def test_composite():
    """Test Composite Pattern"""
    import pygame
    pygame.init()
    
    from levels.level_components import Level, Zone, Tile
    
    level = Level(1)
    zone = Zone("Test Zone")
    tile = Tile(0, 0, pygame.Surface((32, 32)))
    
    zone.add(tile)
    level.add(zone)
    
    assert len(level.get_children()) == 1, "Composite failed to add zone"
    assert len(level.get_all_solid_tiles()) == 1, "Composite failed to retrieve tiles"
    print("✅ Composite Pattern: PASSED")
    return True

def test_state():
    """Test State Pattern"""
    import pygame
    pygame.init()
    
    from player.player_states import IdleState, JumpingState
    
    idle = IdleState()
    jumping = JumpingState()
    
    assert idle is not None, "IdleState creation failed"
    assert jumping is not None, "JumpingState creation failed"
    print("✅ State Pattern: PASSED")
    return True

def main():
    """Run all pattern tests"""
    print("\n" + "="*50)
    print("TESTING ALL DESIGN PATTERNS")
    print("="*50 + "\n")
    
    tests = [
        ("Singleton", test_singleton),
        ("Observer", test_observer),
        ("Factory", test_factory),
        ("Decorator", test_decorator),
        ("Composite", test_composite),
        ("State", test_state),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} Pattern: FAILED - {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"RESULTS: {passed}/{len(tests)} patterns passed")
    print("="*50 + "\n")
    
    if failed > 0:
        print(f"⚠️  {failed} test(s) failed!")
        return False
    else:
        print("🎉 ALL PATTERNS WORKING CORRECTLY!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
