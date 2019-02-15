from screen import LoginScreen
from facade import Facade
from singleton_decorator import singleton

@singleton
class LoginFacade():
    login = LoginScreen.LoginScreen()
        
    def iniciar_sesion(self, username, password):
        self.login.introducir_usuario(username)
        self.login.introducir_contraseña(password)
        self.login.aceptar()

        self.login.esperar(1, "https:google.com", "20")
        
    def __init__(self):
        print('LOGIN FACADE')