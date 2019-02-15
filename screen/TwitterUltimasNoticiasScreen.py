from utils.AccionesBasicas import AccionesBasicas

class TwitterUltimasNoticiasScreen(AccionesBasicas):
    def leer_tweet(self, usuario):
        return self.esperar_a_que_este_visible_y_obtener_texto(usuario, class_name = 'js-tweet-text-container')
    
    def leer_tweet_test(self, usuario):
        return self.esperar_a_que_este_visible_y_obtener_texto(usuario, tag_name = 'data-original-title')
