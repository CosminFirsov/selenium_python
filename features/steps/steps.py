from facade import LoginFacade
from runner import Runner
from behave import Given, When, Then
from utils.Button import Button

#run with behave
Runner = Runner.Runner()

login = LoginFacade.LoginFacade()
login1 = LoginFacade.LoginFacade()

@Given(u'abro pagina de inicio')
def step_abro_pagina_inicio(context):
    print('vacio de momento')
    
@Given(u'el usuario se loguea')
def step_login_usuario(context):
    print('vacio de momento')    
    #print('======================')
        
@When(u'"{username}" con contraseña "{password}" se loguea')
def log_in_con_usuario_y_contraseña(context, username, password):
    login.iniciar_sesion(username, password)
    
@Then(u'el usuario se ha logueado correctamente')
def step3_impl(context):
    print('##vacio de momento##')
    
#ru.Driver.quit()
#sys.exit()