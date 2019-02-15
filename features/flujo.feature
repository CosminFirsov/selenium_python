Feature: Login 

Background: Usuario esta logueado 
	Given abro pagina de inicio 

  Scenario: Acceso usuario y claves validos
    When "prueba_1" con contraseña "Prueba_01" se loguea
    Then el usuario se ha logueado correctamente

