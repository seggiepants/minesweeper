import game.settings as settings
from game import gui

if __name__ == '__main__':
    settings.load_settings(settings.StorageType.RELEASE)
    window = gui.GameWindow()
    window.run_game(settings.storage['default_difficulty'])
    settings.save_settings(settings.StorageType.RELEASE)

