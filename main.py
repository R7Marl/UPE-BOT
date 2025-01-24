import requests
import re
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()
host = os.getenv("HOST")

options = {
    1: "Inscribirme a materias",
    2: "Ver mis datos personales",
    3: "Ver mis asignaturas inscriptas"
}
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, username, password):
        login_url = f"{self.base_url}/upe/acceso"
        payload = {
            "usuario": username,
            "password": password,
            "login": "Ingresar"
        }
        
        response = self.session.post(
            login_url, 
            data=payload,
            params={"auth": "form"},
            allow_redirects=True
        )
        
        return "Ingresá tus datos" not in response.text

    def get_datos_personales(self):
        response = self.session.get(f"{self.base_url}/upe/datos_censales/datos_personales")
        print(f"Status: {response.status_code}")
        print(response.text)
        return response
    def get_cursada(self):
        response = self.session.get(f"{self.base_url}/upe/cursada")
        soup = BeautifulSoup(response.text, 'lxml')
        script_tags = soup.find_all('script', type="text/javascript")
        datos = {}
        for script in script_tags:
            if script.string:
                dni_match = re.search(r'"nro_documento":"(\d+)"', script.string)
                if dni_match: 
                    datos['numero_dni'] = dni_match.group(1)
                nombres_match = re.search(r'"nombres":"([^"]+)"', script.string)
                if nombres_match:
                    datos['nombres'] =  nombres_match.group(1)
                apellido_match = re.search(r'"apellido":"([^"]+)"', script.string)
                if apellido_match:
                    datos['apellido'] = apellido_match.group(1)
                cursada_match = re.search(r'"propuestas":"([^"]+)"', script.string)
                if cursada_match:
                    datos['cursada'] = cursada_match.group(1)
        return datos
    def suscribe_to_asignature(self):
        response = self.session.get(f"{self.base_url}/upe/proximamente") ## Como el periodo de inscripción aún no llega, no puedo ver los endpoints correspondientes, fase final de el bot.
        print(f"Status: {response.status_code}")
        print(response.text)
        return response
if __name__ == "__main__":
    dni = input("Escriba su DNI: ")
    password = input("Escriba su contraseña de ingreso: ")
    client = APIClient(host)
    if client.login(dni, password):
        datos = client.get_cursada()
        if(datos.__len__() == 0):
            print("La sesión no se completó, seguramente colocaste usuario o contraseña incorrectos")
            exit()
        print(f"Encontré tu Nombre: {datos['nombres']}")
        print(f"Encontré tu Apellido: {datos['apellido']}")
        print(f"Encontré tu DNI: {datos['numero_dni']}")
        print(f"Encontré tu cursada: {datos['cursada']}")
        print("¿Qué quieres hacer ahora?")
        print("Por favor, elige una opción:")
        for key, value in options.items():
            print(f"{key}. {value}")
        
        try:
            option = int(input("Ingresa el número de la opción: "))
            if option in options:
                print(f"Opción {option} seleccionada")
                print("Espera... No disponible.")

        except ValueError:
            print("Opción no válida")