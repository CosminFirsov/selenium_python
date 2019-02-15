from runner import Runner
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as Time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

Runner = Runner.Runner()


class AccionesBasicas:
    """Aqui se realizan todas las acciones sobre el driver como clicar un boton, esperar a que esté en un estado,
    obtener texto, comprobar si un elemento contiene un texto, desplegar un desplegable, etc
    """

    def esperar(self, seg=1, url = None, timeout = 500):
        """Espera 1 milisegundo por defecto. Comprueba que la pagina actual no esta cargando con un spinner ni esta
        bloqueada. Si url esta seteado a la url a la que la navegacion deberia llevar, comprueba cada 500 milisegundos
        la url actual y la compara con la esperada 500 veces o el timeout señalado
            :Args:
             - seg - los segundos que se duerme el hilo principal
             - url - la url que deberia encontrarse actualmente
             - timeout - las veces que quieras que se compruebe la url actual con la deseada
        """
        self.espera(seg)
        if not self.esta_visible(xpath = '//body[@id=\'body\' and @aria-busy=\'false\']') or self.esta_visible(xpath = '//div[contains(@id,\'blocker\') and not(contains(@style,\'block\'))]'):
            self.esperar()
        if url is not None:
            contador = 0;
            while (contador < int(timeout)):
                if (url in self.obtener_pagina_actual()):
                    break
                self.espera(0.5)
                contador+=1
                
    def espera(self, seg=1):
        """Espera 1 segundo por defecto o durante seg segundos
            :Args:
             - seg - los segundos que se duerme el hilo principal
        """
        Time.sleep(seg)
                                
    def esperar_a_que_este_clicable_limpiar_texto_e_introducir_nuevo_texto(self, texto, **paths):
        """Espera a que el elemento de la pantalla actual este en estado clicable,
        limpiar el antiguo texto y mandar uno nuevo
            :Args:
             - texto - el texto que se deasea introducir
             - name - el name del elemento HTML sobre el que se desea introducir el texto
             - identificador - el id del elemento HTML sobre el que se desea introducir el texto
             - xpath - el xpath apuntando al elemento HTML sobre el que se desea introducir el texto
             - class_name - el nombre exacto de la clase
        """
        self.esperar_y_realizar_accion(self.esperar_a_que_este_clicable, self.introducir_texto, texto=texto, **paths)
        
    def esperar_a_que_este_seleccionado_limpiar_texto_e_introducir_nuevo_texto(self, texto, **paths):
        """Espera a que el elemento de la pantalla actual este en estado seleccionado,
        limpiar el antiguo texto y mandar uno nuevo
            :Args:
             - texto - el texto que se deasea introducir
             - name - el name del elemento HTML sobre el que se desea introducir el texto
             - identificador - el id del elemento HTML sobre el que se desea introducir el texto
             - xpath - el xpath apuntando al elemento HTML sobre el que se desea introducir el texto
             - class_name - el nombre exacto de la clase
        """
        self.esperar_y_realizar_accion(self.esperar_a_que_este_seleccionado, self.introducir_texto, texto=texto, **paths)
        
    def esperar_a_que_este_clicable_y_clicarle(self, **paths):
        """Espera a que el elemento de la pantalla actual este en estado clicable y a continuacion le clica
            :Args:
             - name - el name del elemento HTML que se desea clicar
             - identificador - el id del elemento HTML que se desea clicar
             - xpath - el xpath apuntando al elemento HTML que se desea clicar
             - class_name - el nombre exacto de la clase
        """
        return self.esperar_y_realizar_accion(self.esperar_a_que_este_clicable, self.clicar, **paths)
    
    def esperar_a_que_este_clicable_situar_el_raton_encima_y_clicarle(self, **paths):
        """Espera a que elemento de la pantalla actual esté en estado clicable, performa una action de
        mover el raton encima del elemento y le clica
             - name, id, xpath o class_name - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.esperar_y_realizar_accion(self.esperar_a_que_este_clicable, self.mover_raton_encima, **paths)
        
    def esperar_a_que_este_visible_y_obtener_texto(self, **paths):
        """Espera a que el elemento de la pantalla actual este presente en el DOM y a continuacion
        extra el texto de dicho elemento y lo devuelve
            :Args:
             - texto - el texto del elemento de la pantalla principal
             - name - el name del elemento HTML que se desea obtener el texto
             - identificador - el id del elemento HTML que se desea obtener el texto
             - xpath - el xpath apuntando al elemento HTML que se desea obtener el texto
             - class_name - el nombre exacto de la clase
        """
        return self.esperar_y_realizar_accion(self.esperar_a_que_este_visible, self.dame_texto, **paths)
    
    def esperar_a_que_este_visible_y_comparar_texto(self, texto, **paths):
        """Espera a que el elemento de la pantalla actual este presente en el DOM y a continuacion
        extra el texto de dicho elemento y comprueba si el texto contiene el texto deseado
            :Args:
             - texto - el texto parcial o completo que se desea comparar
             - name - el name del elemento HTML que se desea obtener el texto
             - identificador - el id del elemento HTML que se desea obtener el texto
             - xpath - el xpath apuntando al elemento HTML que se desea obtener el texto
             - class_name - el nombre exacto de la clase
        """
        return self.esperar_y_realizar_accion(self.esperar_a_que_este_visible, self.contiene_texto, texto=texto, **paths)
        
    def esperar_y_realizar_accion(self, esperar, accion, texto=None, **args):
        """Realiza una accion de esperar sobre un elemento de la pantalla actual
        al que se le apunta mediante su name, id o xpath. Luego se performa una
        accion sobre ese elemento y lo devuelve
            :Args:
             - esperar - una funcion que se realiza con el xpath, name o id apuntando al elemento
                 de la pantalla actual
             - accion - una funcion que se realiza sobre el objeto que la funcion esperar devuelve
             - texo - el texto que se desea introducir o buscar o comparar
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        element = esperar(**args)
        if texto is None:
            return accion(element)
        else:
            return accion(element, texto)
        
    #########################################################################
    ####################    ACCIONES   ######################################
    #########################################################################
    def clicar(self, element):
        """Realiza una accion de clic sobre el elemento de la pantalla actual
            :Args:
             - element - un WebElement sobre el que se desea realizar la accion
        """
        element.click()
        
    def mover_raton_encima(self, element):
        """Perfoma una accion de mover el raton encima del elemento de la pantalla principal
            :Args:
             - element - un WebElement sobre el que se desea realizar la accion
        """
        action_chains  = ActionChains(Runner.Driver)
        action_chains.move_to_element(element)
        action_chains.perform()
        return element
        
    def mover_raton_encima_y_clicarle(self, element):
        """Perfoma una accion de mover el raton encima del elemento de la pantalla principal y luego
        lo clica
            :Args:
             - element - un WebElement sobre el que se desea realizar la accion
        """
        return self.mover_raton_encima(element).click()
                
    def introducir_texto(self, element, texto):
        """Elimina el texto del elemento de la pantalla actual y manda un texto nuevo
            :Args:
             - element - un WebElement sobre el que se desea realizar la accion
             - texto - El texto que se desea introducir
        """
        element.clear()
        element.send_keys(texto)
        
    def esta_visible(self, element=None, **args):
        if element is None:
            element = self.dame_elemento(**args)
        try:
            return element.is_displayed()
        except WebDriverException:
            return False
        
    def contiene_texto(self, element, texto, **args):
        """comprueba si el texto obtenido del elemento de la pantalla principal contiene parcial o 
        totalmente el texto deseado y devuelve true o false
            :Args:
             - element - el elemento de la pantalla principal sobre el que se le va a comparar el texto
             - texto - el texto que se desea comparar
        """
        return (texto in self.dame_texto(element, **args))
    
    def dame_texto(self, element):
        """Devuelve el texto del elemento de la pantalla principal
           :Args:
             - element - un WebElement sobre el que se recupera el texto
        """
        return element.text
    
    def dame_atributo(self, atributo, element=None, **args):
        """Devuelve el atributo deseado del elemento de la pantalla principal. Si no se pasa el elemento
        como parametro, se contruye de nuevo
            :Args:
             - atributo - el atributo del que se desea sacar el valor
             - element - un WebElement sobre el que se recupera el valor del atributo
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """ 
        if element is None:
            element = self.dame_elemento(**args)
        return element.get_attribute(atributo)
        
    #########################################################################
    ####################    ESPERAR    ######################################
    #########################################################################
        
    def esperar_a(self, esperar, **args):
        """Obtiene el tipo de identificador que se quiere, by.name, by.id, by.xpath y
        se realiza una accion de espera sobre ese elemento de 10 segundos
            :Args:
             - esperar - la funcion de espera que se realiza sobre el elemento de la pantalla
                 principal
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        by = self.obtener_localizador(**args)
        return WebDriverWait(Runner.Driver, 10).until(esperar((by['by'], by['path'])))

    def esperar_a_que_este_clicable(self, **args):
        """Espera a que este en estado clicable y lo devuelve
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.esperar_a(EC.element_to_be_clickable, **args)
    
    def esperar_a_que_este_seleccionado(self, **args):
        """Espera a que este en estado seleccionado. 
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.esperar_a(EC.element_located_to_be_selected, **args)
    
    def esperar_a_que_este_visible(self, **args):
        """Espera a que este en estado seleccionado y lo devuelve 
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.esperar_a(EC.visibility_of_element_located , **args)
    
    def obtener_pagina_actual(self):
        return Runner.Driver.current_url
    
    def dame_elemento(self, **args):
        """Dado tres parametros opcionales, crea el WebElement con el find_element del Driver y el By 
        correspondiente y lo devuelve
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        by = self.obtener_localizador(**args)
        return Runner.Driver.find_element(by['by'], by['path'])
    
    def obtener_localizador(self, name=None, identificador=None, xpath=None, class_name=None, tag_name=None):
        """Dado tres parametros opcionales, mira a ver cual de ellos tiene valor y devuelve el path 
        como clave path y el By correspondiente como clave by
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        d = dict()
        if xpath is not None:
            d['path'] = xpath
            d['by'] = By.XPATH
            return d
        if identificador is not None:
            d['path'] = identificador
            d['by'] = By.ID
            return d
        if name is not None:
            d['path'] = name
            d['by'] = By.NAME
            return d
        if class_name is not None:
            d['path'] = class_name
            d['by'] = By.CLASS_NAME
            return d
        if tag_name is not None:
            d['path'] = tag_name
            d['by'] = By.TAG_NAME
            return d
        #TAG_NAME
        return None
            

    def get_html(self):
        """Obtiene el DOM de la pagina actual
        """
        return Runner.Driver.page_source
    
    def get_start_end_of_all_posible_html5_tags(self, html):
        import re
        all_posible_html5_tags = ['div', 'a', 'button', 'dialog', 'body', 'table', 'td', 'tr', 'u', 'ul', 'form', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'base', 'basefont', 'bdi', 'bdo', 'big', 'blockquote', 'br', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dir', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', ',h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'nofram', 'noscript', 'object', 'ol', ',optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre', 'progres', 'q', 'rp', 'rt', 'ruby', 's', ',samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'tbody', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'track', 'tt', 'var', 'video', 'wbr']
        """Obtengo tres arrays. 
        all_elements_start contiene la apertura de todos los tags html posibles
        all_elements_start_tags contiene todos los tags que tienen apertura en el html que se analiza
        all_elements_end contiene el cierre de todos los tags html posibles
        el html analizado es el DOM de la pagina actual menos el doctype del principio
        """
        all_elements_start = []
        all_elements_start_tags = []
        all_elements_end = []
        all_elements_end_tags = []
        for tag in all_posible_html5_tags:
            if (tag == 'img' or tag == 'hr' or tag == 'input' or tag == 'link' or tag == 'meta'):
                for m in re.finditer(r'<'+tag+'([^<])*>', html):
                    all_elements_start.append(m.start(0))
                    all_elements_start_tags.append(tag)
                continue
            for m in re.finditer(r'<'+tag+'([^a-zA-Z])', html):
                all_elements_start.append(m.start(0))
                all_elements_start_tags.append(tag)
        for tag in all_posible_html5_tags:
            if (tag == 'img' or tag == 'hr' or tag == 'input' or tag == 'link' or tag == 'meta'):
                for m in re.finditer(r'<'+tag+'([^<])*>', html):
                    all_elements_end.append(m.end(0))
                    all_elements_end_tags.append(tag)
                continue
            for m in re.finditer(r'<\/'+tag+'([^<][^a-zA-Z])?>', html):
                all_elements_end.append(m.end(0))
                all_elements_end_tags.append(tag)
                
        return all_elements_start, all_elements_start_tags, all_elements_end
    
    