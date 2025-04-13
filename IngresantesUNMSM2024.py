import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista de códigos de carrera (ajusta según sea necesario)
codigos_carrera = [f"{i:03}" for i in range(0, 300)]  # Puedes ampliar este rango

# URL base de las carreras
url_base = "https://admision.unmsm.edu.pe/Website20241/A/{}/0.html"

# Lista para almacenar los datos
data = []

for codigo in codigos_carrera:
    url = url_base.format(codigo)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")  # Encuentra la tabla de datos

        if table:
            rows = table.find_all("tr")[1:]  # Omitir encabezados

            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 7:  # Verificar que sean exactamente 7 columnas
                    data.append([col.text.strip() for col in cols])

# Guardar en un DataFrame
df = pd.DataFrame(data, columns=["Código", "Apellidos y Nombres", "Escuela Profesional", "Puntaje final", "Mérito Alcanzado",
                                 "Observaciones","Escuela Segunda Opción"])

# Exportar a CSV
df.to_csv("ingresantes_unmsm_2024.csv", index=False, encoding="utf-8-sig")

print("Datos extraídos y guardados en 'ingresantes_unmsm_2024.csv'.")
