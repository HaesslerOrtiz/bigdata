import pandas as pnd
import matplotlib.pyplot as plt
import os, re

class Estadistico:
    def __init__(self, ruta: str, hoja: str):
        try:
            self._ruta = ruta
            self._hoja = hoja
            self._df = pnd.read_excel(self._ruta, sheet_name=self._hoja)
        except Exception as e:
            raise Exception(f"Ocurrió el error {e}")

    def histogramas(self, campos: list):
        os.makedirs("resultados", exist_ok=True)  # crea la carpeta si no existe
        for campo in campos:
            conteo = self._df[campo].value_counts()
            plt.figure(figsize=(8, 5))
            conteo.plot(kind="barh", color="blue", edgecolor="black")
            plt.title("")
            plt.xlabel("Frecuencia")
            plt.xticks(fontsize=8)
            plt.ylabel("")
            plt.yticks(fontsize=8)
            # limpiar nombre de archivo
            nombre_limpio = re.sub(r'[\\/*?:"<>|¿]', "", campo)
            archivo_salida = f"resultados/{nombre_limpio}.jpg"
            plt.savefig(archivo_salida, dpi=300)
            plt.close()
            print(f"Gráfico guardado en: {archivo_salida}")
    
    def promedios(self, campos: list):
        with open('promedios.txt', mode='w', encoding='utf-8') as archivo:
            for campo in campos:
                promedio = self._df[campo].mean()
                archivo.write(f"{campo}: {promedio}\n")
    
# main
if __name__ == "__main__":
    analisis_ia = Estadistico('taller_1\encuestas.xlsx', 'Respuestas de formulario 1')
    campos_mean = ['3. Del 1 al 5, ¿Qué tan familiarizado está con el término "Inteligencia Artificial"?']
    campos_hist = ['1. ¿En que grupo etario se encuentra?',
                   '2. ¿Cuál es el nivel educativo más alto que ha alcanzado?',
                   '3. Del 1 al 5, ¿Qué tan familiarizado está con el término "Inteligencia Artificial"?', 
                   '4. ¿Puede nombrar algunos ejemplos de IA que encuentre en su vida diaria?', 
                   '5. ¿Confía usted en los sistemas de inteligencia artificial (ej. conducción autónoma, servicio al cliente, bioseguridad)?', 
                   '10. ¿Cree que el gobierno o las empresas están utilizando los datos eficazmente para mejorar estas áreas?']
    
    analisis_ia.histogramas(campos_hist)
    analisis_ia.promedios(campos_mean)
