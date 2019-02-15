from utils.AccionesBasicas import AccionesBasicas
from utils.Button import Button

class LoginScreen(AccionesBasicas):  
    def introducir_usuario(self, usuario):
        self.esperar_a_que_este_clicable_limpiar_texto_e_introducir_nuevo_texto(usuario, name = 'username')
        
    def introducir_contraseña(self, contraseña):
        self.esperar_a_que_este_clicable_limpiar_texto_e_introducir_nuevo_texto(contraseña, name = 'password')
        
    def aceptar(self):
        self.esperar_a_que_este_clicable_y_clicarle(identificador = 'btn')