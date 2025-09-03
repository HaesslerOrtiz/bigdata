import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from pandas.api.types import is_numeric_dtype
from pandas.api.types import CategoricalDtype

class Eda:
    def __init__(self, ruta_archivo: str, ruta_res: str):
        if not os.path.isfile(ruta_archivo):
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe o la ruta no es válida.")
        self.ruta = ruta_archivo
        self._df = pd.read_csv(ruta_archivo, encoding="latin1", sep=";", on_bad_lines="skip")
        self.ruta_res = ruta_res
        os.makedirs(ruta_res, exist_ok=True)
    
    def _limpieza_datos(self):
        df_limpio = self._df.dropna()
        df_limpio = df_limpio.drop_duplicates()
        return df_limpio
    
    def conteo_registros(self, limpio: bool = False):
        if limpio:
            df = self._limpieza_datos(df)
            return len(df)
        return len(self._df)
    
    @property
    def campos(self):
        return self._df.columns.tolist()
    
    @property
    def tipos_datos(self):
        return self._df.dtypes.to_dict()

    def boxplot(self, column: str):
        if column not in self._df.columns:
            raise ValueError(f"La columna '{column}' no existe en el DataFrame.")
        
        df = self._limpieza_datos()

        # Validar que la columna sea numérica
        if not is_numeric_dtype(df[column]):
            raise TypeError(f"La columna '{column}' no es numérica. No se puede generar un boxplot.")

        plt.boxplot(df[column])
        plt.title(f'Boxplot de {column}')

        ruta_salida = os.path.join(self.ruta_res, f'boxplot_{column}.png')
        plt.savefig(ruta_salida)
        plt.close()

    def histograma(self, column: str, valor_column: str = None):
        if column not in self._df.columns:
            raise ValueError(f"La columna '{column}' no existe en el DataFrame.")

        df = self._limpieza_datos()

        # Filtrado opcional
        if valor_column:
            df = df[df[column] == valor_column]
            if df.empty:
                raise ValueError(f"No hay datos disponibles para la columna '{column}' con el valor '{valor_column}'.")

        if is_numeric_dtype(df[column]):
            # Histograma clásico para variables numéricas
            plt.hist(df[column], bins=10, color="blue", edgecolor="black")
            plt.title(f"Histograma de {column}")
            plt.xlabel(column)
            plt.ylabel("Frecuencia")
        else:
            # Conteo de frecuencias para variables categóricas
            conteo = df[column].value_counts()
            # Paleta de colores para barras, se genera según el número de categorías
            colors = plt.cm.tab20.colors[:len(conteo)]  
            plt.bar(conteo.index, conteo.values, color=colors, edgecolor="black")
            plt.title(f"Frecuencias de {column}")
            plt.xlabel(column)
            plt.ylabel("Frecuencia")
            plt.xticks(rotation=45)  # Rotar etiquetas si son muchas categorías

        ruta_salida = os.path.join(self.ruta_res, f"histograma_{column}.png")
        plt.savefig(ruta_salida, bbox_inches="tight")  # ajustar márgenes
        plt.close()

    def basicas(self, column: str):
        if column not in self._df.columns:
            raise ValueError(f"La columna '{column}' no existe en el DataFrame.")
        df = self._limpieza_datos()
        descripcion = df[column].describe().round(2)
        print(descripcion)
        return descripcion.to_dict()
        
    def correlacion(self, list_cols: list, metodo: str = 'pearson', plot: bool = True):
        for col in list_cols:
            if col not in self._df.columns:
                raise ValueError(f"La columna '{col}' no existe en el DataFrame.")
            if not is_numeric_dtype(self._df[col]):
                raise TypeError(f"La columna '{col}' no es numérica, no se puede calcular correlación.")

        df = self._limpieza_datos()

        # Calcular correlación
        correlacion = df[list_cols].corr(method=metodo)

        if plot:
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlacion, annot=True, cmap="coolwarm", center=0, fmt=".2f")
            plt.title(f"Matriz de correlación de ({metodo})")
            ruta_salida = os.path.join(self.ruta_res, f"correlacion_{metodo}.png")
            plt.savefig(ruta_salida)
            plt.close()

        return correlacion.to_dict()
    
    def dispersion(self, x_col: str, y_col: str):
        if x_col not in self._df.columns or y_col not in self._df.columns:
            raise ValueError(f"Una de las columnas '{x_col}' o '{y_col}' no existe en el DataFrame.")

        df = self._limpieza_datos()

        # Validar que ambas columnas sean numéricas
        if not (is_numeric_dtype(df[x_col]) and is_numeric_dtype(df[y_col])):
            raise TypeError(f"Ambas columnas deben ser numéricas. "
                            f"'{x_col}' es {df[x_col].dtype}, '{y_col}' es {df[y_col].dtype}.")

        # Gráfico de dispersión
        plt.scatter(df[x_col], df[y_col], alpha=0.7, color="blue", edgecolors="k")
        plt.title(f'Dispersión entre {x_col} y {y_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        ruta_salida = os.path.join(self.ruta_res, f'dispersion_{x_col}_vs_{y_col}.png')
        plt.savefig(ruta_salida)
        plt.close()
    
    def contingencia(self, col1: str, col2: str, filtros: dict = None) -> pd.DataFrame:
        if col1 not in self._df.columns or col2 not in self._df.columns:
            raise ValueError(f"Una de las columnas '{col1}' o '{col2}' no existe en el DataFrame.")

        df = self._limpieza_datos()

        # Validar que ambas columnas sean categóricas
        if not (isinstance(df[col1].dtype, CategoricalDtype) or pd.api.types.is_object_dtype(df[col1])):
            raise TypeError(f"La columna '{col1}' no es categórica.")
        if not (isinstance(df[col2].dtype, CategoricalDtype) or pd.api.types.is_object_dtype(df[col2])):
            raise TypeError(f"La columna '{col2}' no es categórica.")

        # Aplicar filtros si se pasan
        if filtros:
            for campo, valores in filtros.items():
                if campo in df.columns:
                    df = df[df[campo].isin(valores)]

        # Generar tabla de contingencia
        tabla = pd.crosstab(df[col1], df[col2])
        print("Tabla de contingencia (filtrada):")
        print(tabla)

        return tabla

if __name__ == "__main__":
    eda = Eda("taller_2/eva_ideam.csv", "taller_2/resultados")
    '''
    print(eda.conteo_registros())
    print(eda.campos)
    print(eda.tipos_datos)
    lista = ["ha_semb", "ha_csda", "t_prod", "t_ha_rend"]
    for el in lista:
        eda.basicas(el)
    '''
    filtros = {"Sub_gr_cult": ["AGUACATE", "BANANO", "CAFE"]}
    eda.contingencia("departamento", "Sub_gr_cult", filtros=filtros)


    