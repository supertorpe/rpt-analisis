import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter

def compare(ministerio):
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats.xlsx",
        sheet_name="statistics", # 0,
        header=0,
        )

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


# Compare one ministry with others in percentage terms
def compare_pct(ministerio):
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats.xlsx",
        sheet_name="statistics", # 0,
        header=0,
        )

    thisone = df_stats[df_stats['Denominación Ministerio'].str.lower() == ministerio.lower()]
    others = df_stats[df_stats['Denominación Ministerio'].str.lower() != ministerio.lower()]

    # Group by 'grupo' and 'nivel' and get mean values
    thisone_grouped = thisone.groupby(['Gr/Sb', 'Nivel'])['mean'].mean().reset_index()
    others_grouped = others.groupby(['Gr/Sb', 'Nivel'])['mean'].mean().reset_index()

    # Get the maximum "mean" per group and level (for percentage calculation)
    max_mean = df_stats.groupby(['Gr/Sb', 'Nivel'])['mean'].max().reset_index()
    max_mean.rename(columns={'mean': 'max_mean'}, inplace=True)

    # Join with the DataFrame of the ministries to calculate the percentage with respect to the maximum
    thisone_grouped = pd.merge(thisone_grouped, max_mean, on=['Gr/Sb', 'Nivel'])
    others_grouped = pd.merge(others_grouped, max_mean, on=['Gr/Sb', 'Nivel'])

    # Calculate the percentage of "mean" with respect to the maximum "mean"
    thisone_grouped['percentage'] = (thisone_grouped['mean'] / thisone_grouped['max_mean']) * 100
    others_grouped['percentage'] = (others_grouped['mean'] / others_grouped['max_mean']) * 100

    # Merge both DataFrames for comparison
    merged = thisone_grouped.merge(others_grouped, on=['Gr/Sb', 'Nivel'], suffixes=('_this', '_others'))

    # Sort by group and level
    merged = merged.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    print(merged)

    # Plot
    plt.figure(figsize=(16, 8))
    x = range(len(merged))
    plt.plot(x, merged['percentage_this'], label=ministerio, marker='o')
    plt.plot(x, merged['percentage_others'], label='Otros', marker='o')

    # Add values at each point
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

    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats.xlsx",
        sheet_name="statistics", # 0,
        header=0,
        )

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


# Plot the percentage of "mean" over the highest "mean"
def plot_percentage_over_max():
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats.xlsx",
        sheet_name="statistics", # 0,
        header=0,
        )

    # Get the highest "mean" for each group/level
    max_mean = df_stats.groupby(['Gr/Sb', 'Nivel'])['mean'].max().reset_index()
    max_mean.rename(columns={'mean': 'max_mean'}, inplace=True)

    # Join the original DataFrame with the highest "mean" by group/level
    df_merged = pd.merge(df_stats, max_mean, on=['Gr/Sb', 'Nivel'])

    # Calculate the percentage of "mean" over the highest "mean"
    df_merged['percentage'] = (df_merged['mean'] / df_merged['max_mean']) * 100

    # Select the top 5 ministries with the highest and lowest percentages
    top_5_ministerios = df_merged.groupby('Denominación Ministerio')['percentage'].max().nlargest(5).index
    bottom_5_ministerios = df_merged.groupby('Denominación Ministerio')['percentage'].max().nsmallest(5).index

    # Join the ministries with the 5 highest and lowest percentages
    selected_ministerios = list(top_5_ministerios) + list(bottom_5_ministerios)

    # Filter the data to include only these ministries
    df_filtered = df_merged[df_merged['Denominación Ministerio'].isin(selected_ministerios)]

    df_filtered = df_filtered.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    print(df_filtered)

    # Create a list of ministries to plot
    ministries = df_filtered['Denominación Ministerio'].unique()

    plt.figure(figsize=(12, 8))  # Increase figure size

    # Plot a line for each ministry
    for ministry in ministries:
        ministry_data = df_filtered[df_filtered['Denominación Ministerio'] == ministry]
        plt.plot(ministry_data['Gr/Sb'] + '-' + ministry_data['Nivel'].astype(str),
                 ministry_data['percentage'], marker='o', label=ministry)

    # Plot settings
    plt.xlabel('Grupo - Nivel')
    plt.ylabel('Porcentaje sobre el mean máximo (%)')
    plt.title('Porcentaje de C.E. medio sobre el máximo por grupo y nivel')
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Place the legend outside the graph, and with multiple columns
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=8, ncol=2)

    plt.tight_layout()
    plt.savefig("/app/output/00-rpt-std-porcentaje_mean_vs_max_top_bottom.png", dpi=300)
    plt.close()

# Plot "mean" values
def plot_mean_values():
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats.xlsx",
        sheet_name="statistics", # 0,
        header=0,
        )

    # Select the top 5 ministries with the highest and lowest "mean" values
    top_5_ministerios = df_stats.groupby('Denominación Ministerio')['mean'].max().nlargest(5).index
    bottom_5_ministerios = df_stats.groupby('Denominación Ministerio')['mean'].max().nsmallest(5).index

    # Join the ministries with the 5 highest and lowest "mean" values
    selected_ministerios = list(top_5_ministerios) + list(bottom_5_ministerios)

    # Filter the data to include only these ministries
    df_filtered = df_stats[df_stats['Denominación Ministerio'].isin(selected_ministerios)]

    df_filtered = df_filtered.sort_values(by=['Gr/Sb', 'Nivel'], ascending=[True, False])

    # Create a list of ministries to plot
    ministries = df_filtered['Denominación Ministerio'].unique()

    plt.figure(figsize=(12, 8))  # Increase figure size

    # Plot a line for each ministry
    for ministry in ministries:
        ministry_data = df_filtered[df_filtered['Denominación Ministerio'] == ministry]
        plt.plot(ministry_data['Gr/Sb'] + '-' + ministry_data['Nivel'].astype(str),
                 ministry_data['mean'], marker='o', label=ministry)

    # Plot settings
    plt.xlabel('Grupo - Nivel')
    plt.ylabel('C.E. medio')
    plt.title('C.E. medio por grupo y nivel')
    plt.xticks(rotation=90, ha='center', fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.6)

    # Place the legend outside the graph, and with multiple columns
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize=8, ncol=2)

    plt.tight_layout()
    plt.savefig("/app/output/-00-rpt-std-mean_values_top_bottom.png", dpi=300)
    plt.close()


def print_scatter():
    # Read Excel
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats_2.xlsx",
        sheet_name="statistics",
        header=0,
    )

    # Filter by Gr/Sb and Nivel
    df_filtered = df_stats[
        (df_stats['Gr/Sb'].isin(['A2', 'A2C1'])) &
        (df_stats['Nivel'].isin([20, 22, 24]))
    ].copy()

    #df_filtered = df_filtered.sort_values(by='count', ascending=False)

    # Function to assign color by row
    def asignar_color(row):
        if row['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA':
            if row['Denominación Larga'] == 'INGENIERO TECNICO / INGENIERA TECNICA DE ARSENALES':
                return 'red'
            return 'green'
        return 'lightgrey'  # Optional: you can exclude these if you don't want to show them

    # Assign colors and sizes
    df_filtered['color'] = df_filtered.apply(asignar_color, axis=1)
    df_filtered['size'] = df_filtered['count'] * 10
    df_defensa = df_filtered[df_filtered['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA'].sort_values(by='count', ascending=False)
    df_otros = df_filtered[df_filtered['Denominación Ministerio'] != 'MINISTERIO DE DEFENSA'].sort_values(by='count', ascending=False)

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    # Paint others first, then defense
    plt.scatter(
        x=df_otros['mean'],
        y=df_otros['Nivel'],
        s=df_otros['size'],
        c=df_otros['color'],
        alpha=0.7,
        edgecolors='black',
        linewidth=0.5,
        label='Otros Ministerios'
    )

    plt.scatter(
        x=df_defensa['mean'],
        y=df_defensa['Nivel'],
        s=df_defensa['size'],
        c=df_defensa['color'],
        alpha=0.9,
        edgecolors='black',
        linewidth=0.7,
        label='Ministerio de Defensa'
    )
    plt.title('Complemento específico medio por Nivel (A2 y A2C1)')
    plt.xlabel('Complemento específico medio (mean)')
    plt.ylabel('Nivel')
    plt.yticks([20, 22, 24])
    plt.grid(True)
    plt.tight_layout()    

    plt.savefig("/app/output/scatter.png", dpi=300)
    plt.close()


def print_scatter_2():
    # Read Excel
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats_2.xlsx",
        sheet_name="statistics",
        header=0,
    )

    # Levels of interest, from highest to lowest
    niveles_ordenados = [28, 26, 24, 22, 20, 18, 16]

    # Filter by levels
    df_filtered = df_stats[df_stats['Nivel'].isin(niveles_ordenados)].copy()

    # Assign colors
    def asignar_color(row):
        if row['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA':
            return 'green'
        return 'lightgrey'

    df_filtered['color'] = df_filtered.apply(asignar_color, axis=1)
    df_filtered['size'] = df_filtered['count'] * 10

    # Separate Defense and others
    df_defensa = df_filtered[df_filtered['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA'].sort_values(by='count', ascending=False)
    df_otros = df_filtered[df_filtered['Denominación Ministerio'] != 'MINISTERIO DE DEFENSA'].sort_values(by='count', ascending=False)

    # Convert 'Nivel' to ordered category
    df_otros['Nivel_cat'] = pd.Categorical(df_otros['Nivel'], categories=niveles_ordenados, ordered=True)
    df_defensa['Nivel_cat'] = pd.Categorical(df_defensa['Nivel'], categories=niveles_ordenados, ordered=True)

    # Create plot
    plt.figure(figsize=(12, 8))

    plt.scatter(
        x=df_otros['mean'],
        y=df_otros['Nivel_cat'],
        s=df_otros['size'],
        c=df_otros['color'],
        alpha=0.7,
        edgecolors='black',
        linewidth=0.5,
        
    )

    plt.scatter(
        x=df_defensa['mean'],
        y=df_defensa['Nivel_cat'],
        s=df_defensa['size'],
        c=df_defensa['color'],
        alpha=0.9,
        edgecolors='black',
        linewidth=0.7,
        
    )

    plt.title('Complemento específico medio por Nivel')
    plt.xlabel('Complemento específico medio (mean)')
    plt.ylabel('Nivel')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig("/app/output/scatter_2.png", dpi=300)
    plt.close()


def print_scatter_3():
    # Read Excel
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats_2.xlsx",
        sheet_name="statistics",
        header=0,
    )

    # Levels of interest, from highest to lowest
    niveles_ordenados = [28, 26, 24, 22, 20, 18, 16]

    # Filter by levels
    df_filtered = df_stats[df_stats['Nivel'].isin(niveles_ordenados)].copy()

    # Assign colors
    def asignar_color(row):
        if row['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA':
            return 'green'
        if row['Denominación Ministerio'] == 'MINISTERIO DE CULTURA':
            return 'blue'
        return 'lightgrey'

    df_filtered['color'] = df_filtered.apply(asignar_color, axis=1)
    df_filtered['size'] = df_filtered['count'] * 10

    # Separate Defense and others
    df_defensa = df_filtered[df_filtered['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA'].sort_values(by='count', ascending=False)
    df_cultura = df_filtered[df_filtered['Denominación Ministerio'] == 'MINISTERIO DE CULTURA'].sort_values(by='count', ascending=False)
    df_otros = df_filtered[
        ~df_filtered['Denominación Ministerio'].isin(['MINISTERIO DE DEFENSA', 'MINISTERIO DE CULTURA'])
    ].sort_values(by='count', ascending=False)

    # Convert 'Nivel' to ordered category
    df_otros['Nivel_cat'] = pd.Categorical(df_otros['Nivel'], categories=niveles_ordenados, ordered=True)
    df_defensa['Nivel_cat'] = pd.Categorical(df_defensa['Nivel'], categories=niveles_ordenados, ordered=True)
    df_cultura['Nivel_cat'] = pd.Categorical(df_cultura['Nivel'], categories=niveles_ordenados, ordered=True)

    # Create plot
    plt.figure(figsize=(12, 8))

    plt.scatter(
        x=df_otros['mean'],
        y=df_otros['Nivel_cat'],
        s=df_otros['size'],
        c=df_otros['color'],
        alpha=0.7,
        edgecolors='black',
        linewidth=0.5,
        
    )

    plt.scatter(
        x=df_defensa['mean'],
        y=df_defensa['Nivel_cat'],
        s=df_defensa['size'],
        c=df_defensa['color'],
        alpha=0.9,
        edgecolors='black',
        linewidth=0.7,
        
    )

    plt.scatter(
        x=df_cultura['mean'],
        y=df_cultura['Nivel_cat'],
        s=df_cultura['size'],
        c=df_cultura['color'],
        alpha=0.9,
        edgecolors='black',
        linewidth=0.7,
        
    )

    plt.title('Complemento específico medio por Nivel')
    plt.xlabel('Complemento específico medio (mean)')
    plt.ylabel('Nivel')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig("/app/output/scatter_3.png", dpi=300)
    plt.close()


def print_scatter_4():
    # Read Excel
    df_stats = pd.read_excel(
        io="/app/rpt/rpt_stats_2.xlsx",
        sheet_name="statistics",
        header=0,
    )

    # Levels of interest, from highest to lowest
    niveles_ordenados = [28, 26, 24, 22, 20, 18, 16]

    # Filter by levels of interest
    df_filtered = df_stats[df_stats['Nivel'].isin(niveles_ordenados)].copy()

    # Assign color
    def asignar_color(row):
        return 'green' if row['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA' else 'lightgrey'

    df_filtered['color'] = df_filtered.apply(asignar_color, axis=1)
    df_filtered['size'] = df_filtered['count'] * 10

    # Create output folder if it doesn't exist
    os.makedirs("/app/output/scatter_por_nivel", exist_ok=True)

    # Generate a plot for each level
    for nivel in niveles_ordenados:
        df_nivel = df_filtered[df_filtered['Nivel'] == nivel]

        df_defensa = df_nivel[df_nivel['Denominación Ministerio'] == 'MINISTERIO DE DEFENSA']
        df_otros = df_nivel[df_nivel['Denominación Ministerio'] != 'MINISTERIO DE DEFENSA']

        plt.figure(figsize=(10, 6))

        plt.scatter(
            x=df_otros['mean'],
            y=[nivel] * len(df_otros),
            s=df_otros['size'],
            c=df_otros['color'],
            alpha=0.7,
            edgecolors='black',
            linewidth=0.5,
            
        )

        plt.scatter(
            x=df_defensa['mean'],
            y=[nivel] * len(df_defensa),
            s=df_defensa['size'],
            c=df_defensa['color'],
            alpha=0.9,
            edgecolors='black',
            linewidth=0.7,
            
        )

        plt.title(f'Complemento específico medio - Nivel {nivel}')
        plt.xlabel('Complemento específico medio')
        plt.yticks([])
        plt.ylabel('')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"/app/output/scatter_por_nivel/scatter_nivel_{nivel}.png", dpi=300)
        plt.close()


# # Calculate the overall average (without distinguishing ministries)
# global_mean = df_stats.groupby(["Gr/Sb", "Nivel"])["mean"].mean().reset_index()
# global_mean.rename(columns={"mean": "global_mean"}, inplace=True)

# # Match the overall mean with the original data
# df_stats = df_stats.merge(global_mean, on=["Gr/Sb", "Nivel"])

# # Calculate the percentage deviation from the global mean
# df_stats["percent_diff"] = (df_stats["mean"] - df_stats["global_mean"]) / df_stats["global_mean"] * 100

# # Obtain the ministry with the largest average percentage drop
# ministry_with_lowest_mean = df_stats.groupby("Denominación Ministerio")["percent_diff"].mean().idxmin()

# # Show the ministry that is furthest below the average
# print(f"The ministry furthest below the average is: {ministry_with_lowest_mean}")