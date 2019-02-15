from screen import TwitterUltimasNoticiasScreen as HOME
from facade import Facade
from singleton_decorator import singleton

@singleton
class TwitterUltimasNoticiasFacade():
    home = HOME.TwitterUltimasNoticiasScreen()
        
    def esperar_carga_pagina(self,):
        self.home.esperar(1, "https://twitter.com/unoticias?lang=es", "20")
        
    def __init__(self):
        print('TWITTER FACADE')
        
    def obtener_tweets(self):
        return self.home.leer_tweet()