import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter

df_stats = pd.read_excel(
    io="/app/rpt/rpt_stats.xlsx",
    sheet_name="statistics", # 0,
    header=0,
    )


def compare(ministerio):
    thisone = df_stats[df_stats['Denominación Ministerio'].str.lower() == ministerio.lower()]
    others = df_stats[df_stats['Denominación Ministerio'].str.lower() != ministerio.lower()]

    # Aggregate data by group and level
    thisone_grouped = thisone.groupby(['Gr/Sb', 'Nivel'])['mean'].mean().reset_index()
    others_grouped = others.groupby(['Gr/Sb', 'Nivel'])['mean'].mean().reset_index()

    # Merge for side-by-side comparison
    merged = thisone_grouped.merge(others_grouped, on=['Gr/Sb', 'Nivel'], suffixes=('_this', '_others'))

    # Sort by group and level
    merged = merged.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    print(merged)
        
    # Plot
    x = range(len(merged))
    bar_width = 0.4
    plt.bar([pos - bar_width/2 for pos in x], merged['mean_this'], width=bar_width, label=ministerio, align='center')
    plt.bar([pos + bar_width/2 for pos in x], merged['mean_others'], width=bar_width, label='Otros', align='center')

    plt.xlabel('Grupo - Nivel')
    plt.ylabel("C.E. medio")
    plt.title("Comparación C.E. medio por grupo y nivel")
    plt.xticks(x, [f"{g}-{l}" for g, l in zip(merged['Gr/Sb'], merged['Nivel'])], rotation=90, ha='center', fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"/app/output/00-rpt_comparacion_{ministerio}.png", dpi=300)
    plt.close()


# Función para comparar el Ministerio de Defensa con otros en porcentaje
def compare_pct(ministerio):
    thisone = df_stats[df_stats['Denominación Ministerio'].str.lower() == ministerio.lower()]
    others = df_stats[df_stats['Denominación Ministerio'].str.lower() != ministerio.lower()]

    # Agrupar por grupo y nivel, y obtener el "mean" promedio
    thisone_grouped = thisone.groupby(['Gr/Sb', 'Nivel'])['mean'].mean().reset_index()
    others_grouped = others.groupby(['Gr/Sb', 'Nivel'])['mean'].mean().reset_index()

    # Obtener el "mean" máximo por grupo y nivel (para hacer el cálculo porcentual)
    max_mean = df_stats.groupby(['Gr/Sb', 'Nivel'])['mean'].max().reset_index()
    max_mean.rename(columns={'mean': 'max_mean'}, inplace=True)

    # Unir con el DataFrame de los ministerios para calcular el porcentaje respecto al máximo
    thisone_grouped = pd.merge(thisone_grouped, max_mean, on=['Gr/Sb', 'Nivel'])
    others_grouped = pd.merge(others_grouped, max_mean, on=['Gr/Sb', 'Nivel'])

    # Calcular el porcentaje de "mean" respecto al máximo "mean"
    thisone_grouped['percentage'] = (thisone_grouped['mean'] / thisone_grouped['max_mean']) * 100
    others_grouped['percentage'] = (others_grouped['mean'] / others_grouped['max_mean']) * 100

    # Hacer el merge de ambos DataFrames para comparación
    merged = thisone_grouped.merge(others_grouped, on=['Gr/Sb', 'Nivel'], suffixes=('_this', '_others'))

    # Ordenar por grupo y nivel
    merged = merged.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    print(merged)
        
    # Graficar
    plt.figure(figsize=(16, 8))
    x = range(len(merged))
    plt.plot(x, merged['percentage_this'], label=ministerio, marker='o')
    plt.plot(x, merged['percentage_others'], label='Otros', marker='o')

     # Añadir los valores en cada punto
    for i, (this_percentage, others_percentage) in enumerate(zip(merged['percentage_this'], merged['percentage_others'])):
        plt.text(i, this_percentage, f"{this_percentage:.1f}%", color='blue', ha='center', va='bottom', fontsize=8)
        plt.text(i, others_percentage, f"{others_percentage:.1f}%", color='orange', ha='center', va='bottom', fontsize=8)


    plt.xlabel('Grupo - Nivel')
    plt.ylabel("Porcentaje respecto al mayor C.E. medio")
    plt.title("Comparación porcentual C.E. medio por grupo y nivel")
    plt.xticks(x, [f"{g}-{l}" for g, l in zip(merged['Gr/Sb'], merged['Nivel'])], rotation=90, ha='center', fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
    plt.tight_layout()
    plt.savefig(f"/app/output/00-rpt_comparacion_porcentaje_{ministerio}.png", dpi=300)
    plt.close()


def print_lowest_and_highest_ce():

    ministry_ce_means = df_stats.groupby('Denominación Ministerio')['mean'].mean()
        
    # Identify ministries with the lowest mean C.E.
    min_ministries = ministry_ce_means.nsmallest(5)
    min_ministry_1, min_value_1 = min_ministries.index[0], min_ministries.iloc[0]
    min_ministry_2, min_value_2 = min_ministries.index[1], min_ministries.iloc[1]
    min_ministry_3, min_value_3 = min_ministries.index[2], min_ministries.iloc[2]
    min_ministry_4, min_value_4 = min_ministries.index[3], min_ministries.iloc[3]
    min_ministry_5, min_value_5 = min_ministries.index[4], min_ministries.iloc[4]

    # Identify ministries with the highest mean C.E.
    max_ministries = ministry_ce_means.nlargest(5)
    max_ministry_1, max_value_1 = max_ministries.index[0], max_ministries.iloc[0]
    max_ministry_2, max_value_2 = max_ministries.index[1], max_ministries.iloc[1]
    max_ministry_3, max_value_3 = max_ministries.index[2], max_ministries.iloc[2]
    max_ministry_4, max_value_4 = max_ministries.index[3], max_ministries.iloc[3]
    max_ministry_5, max_value_5 = max_ministries.index[4], max_ministries.iloc[4]

    print(f"Los ministerios con el menor C.E. medio son:")
    print(f"1. {min_ministry_1} con un C.E. medio de {min_value_1:.2f}")
    print(f"2. {min_ministry_2} con un C.E. medio de {min_value_2:.2f}")
    print(f"3. {min_ministry_3} con un C.E. medio de {min_value_3:.2f}")
    print(f"4. {min_ministry_4} con un C.E. medio de {min_value_4:.2f}")
    print(f"5. {min_ministry_5} con un C.E. medio de {min_value_5:.2f}")
    print(f"\nLos ministerios con el mayor C.E. medio son:")
    print(f"1. {max_ministry_1} con un C.E. medio de {max_value_1:.2f}")
    print(f"2. {max_ministry_2} con un C.E. medio de {max_value_2:.2f}")
    print(f"3. {max_ministry_3} con un C.E. medio de {max_value_3:.2f}")
    print(f"4. {max_ministry_4} con un C.E. medio de {max_value_4:.2f}")
    print(f"5. {max_ministry_5} con un C.E. medio de {max_value_5:.2f}")

"""
Los ministerios con el menor C.E. medio son:
1. MINISTERIO DE PRESIDENCIA, RELACIONES CON LAS CORTES Y MEMORIA DEMOCRATICA con un C.E. medio de 7261.00
2. MINISTERIO DE DEFENSA con un C.E. medio de 7700.03
3. CONSEJO SUPERIOR DE INVESTIGACIONES CIENTIFICAS - CSIC con un C.E. medio de 7831.74
4. MINISTERIO DE TRABAJO Y ECONOMIA SOCIAL con un C.E. medio de 7904.19
5. MINISTERIO DE INCLUSION, SEGURIDAD SOCIAL Y MIGRACIONES con un C.E. medio de 8306.63

Los ministerios con el mayor C.E. medio son:
1. CASA DE SU MAJESTAD EL REY con un C.E. medio de 22116.20
2. AGENCIA ESTATAL AGENCIA ESPAÑOLA DE SUPERVISION DE INTELIGENCIA ARTIFICIAL con un C.E. medio de 21316.57
3. AGENCIA ESTATAL DE ADMINISTRACION TRIBUTARIA con un C.E. medio de 15545.04
4. CONSEJO DE SEGURIDAD NUCLEAR con un C.E. medio de 14161.88
5. AGENCIA ESTATAL AGENCIA ESPACIAL ESPAÑOLA con un C.E. medio de 12378.91
"""


# Función para graficar el porcentaje de "mean" sobre el "mean" más alto
def plot_percentage_over_max():
    # Obtener el "mean" más alto para cada grupo/nivel
    max_mean = df_stats.groupby(['Gr/Sb', 'Nivel'])['mean'].max().reset_index()
    max_mean.rename(columns={'mean': 'max_mean'}, inplace=True)

    # Unir el DataFrame original con el máximo "mean" por grupo/nivel
    df_merged = pd.merge(df_stats, max_mean, on=['Gr/Sb', 'Nivel'])

    # Calcular el porcentaje de "mean" sobre el máximo "mean"
    df_merged['percentage'] = (df_merged['mean'] / df_merged['max_mean']) * 100

    # Seleccionar los 5 ministerios con mayores y menores porcentajes
    top_5_ministerios = df_merged.groupby('Denominación Ministerio')['percentage'].max().nlargest(5).index
    bottom_5_ministerios = df_merged.groupby('Denominación Ministerio')['percentage'].max().nsmallest(5).index

    # Unir los ministerios de los 5 mayores y menores porcentajes
    selected_ministerios = list(top_5_ministerios) + list(bottom_5_ministerios)

    # Filtrar los datos para solo incluir estos ministerios
    df_filtered = df_merged[df_merged['Denominación Ministerio'].isin(selected_ministerios)]

    df_filtered = df_filtered.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    print(df_filtered)

    # Crear una lista de ministerios para graficar
    ministries = df_filtered['Denominación Ministerio'].unique()

    plt.figure(figsize=(12, 8))  # Aumentar el tamaño de la figura

    # Graficar una línea por ministerio
    for ministry in ministries:
        ministry_data = df_filtered[df_filtered['Denominación Ministerio'] == ministry]
        plt.plot(ministry_data['Gr/Sb'] + '-' + ministry_data['Nivel'].astype(str),
                 ministry_data['percentage'], marker='o', label=ministry)

    # Ajustes de la gráfica
    plt.xlabel('Grupo - Nivel')
    plt.ylabel('Porcentaje sobre el mean máximo (%)')
    plt.title('Porcentaje de C.E. medio sobre el máximo por grupo y nivel')
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Colocar la leyenda fuera de la gráfica, y con múltiples columnas
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=8, ncol=2)

    plt.tight_layout()
    plt.savefig("/app/output/00-rpt-std-porcentaje_mean_vs_max_top_bottom.png", dpi=300)
    plt.close()

# Función para graficar los valores de "mean"
def plot_mean_values():
    # Seleccionar los 5 ministerios con mayores y menores valores de "mean"
    top_5_ministerios = df_stats.groupby('Denominación Ministerio')['mean'].max().nlargest(5).index
    bottom_5_ministerios = df_stats.groupby('Denominación Ministerio')['mean'].max().nsmallest(5).index

    # Unir los ministerios de los 5 mayores y menores valores de "mean"
    selected_ministerios = list(top_5_ministerios) + list(bottom_5_ministerios)

    # Filtrar los datos para solo incluir estos ministerios
    df_filtered = df_stats[df_stats['Denominación Ministerio'].isin(selected_ministerios)]

    df_filtered = df_filtered.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    # Crear una lista de ministerios para graficar
    ministries = df_filtered['Denominación Ministerio'].unique()

    plt.figure(figsize=(12, 8))  # Aumentar el tamaño de la figura

    # Graficar una línea por ministerio
    for ministry in ministries:
        ministry_data = df_filtered[df_filtered['Denominación Ministerio'] == ministry]
        plt.plot(ministry_data['Gr/Sb'] + '-' + ministry_data['Nivel'].astype(str),
                 ministry_data['mean'], marker='o', label=ministry)

    # Ajustes de la gráfica
    plt.xlabel('Grupo - Nivel')
    plt.ylabel('C.E. medio')
    plt.title('C.E. medio por grupo y nivel')
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Colocar la leyenda fuera de la gráfica, y con múltiples columnas
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=8, ncol=2)

    plt.tight_layout()
    plt.savefig("/app/output/-00-rpt-std-mean_values_top_bottom.png", dpi=300)
    plt.close()




# # Calcular la media global (sin distinguir ministerios)
# global_mean = df_stats.groupby(["Gr/Sb", "Nivel"])["mean"].mean().reset_index()
# global_mean.rename(columns={"mean": "global_mean"}, inplace=True)

# # Unir la media global con los datos originales
# df_stats = df_stats.merge(global_mean, on=["Gr/Sb", "Nivel"])

# # Calcular la desviación porcentual respecto a la media global
# df_stats["percent_diff"] = (df_stats["mean"] - df_stats["global_mean"]) / df_stats["global_mean"] * 100

# # Obtener el ministerio con la mayor caída porcentual promedio
# ministry_with_lowest_mean = df_stats.groupby("Denominación Ministerio")["percent_diff"].mean().idxmin()

# # Mostrar el ministerio que está más por debajo en términos porcentuales
# print(f"El ministerio más por debajo de la media es: {ministry_with_lowest_mean}")