import os
import io
import pandas as pd
from utils import read_zip

def gen_stats():
    output_file = '/app/rpt/rpt_stats.xlsx'
    output_file_2 = '/app/rpt/rpt_stats_2.xlsx'
    if os.path.exists(output_file) and os.path.exists(output_file_2):
        print(f"File {output_file} already exists. Skipping generation.")
        return
        
    rpt = pd.read_excel(
        io=io.BytesIO(read_zip(r'/app/rpt/rpt.zip', 'rpt.xlsx')),
        sheet_name="Relación de puestos", # 0,
        header=0,
        skiprows=[0,1,2] )

    af_col = rpt.columns[31]
    rpt = rpt[rpt[af_col] != "V"]
    print(rpt.columns)

    if not os.path.exists(output_file):
        stats = rpt.groupby(["Denominación Ministerio", "Gr/Sb", "Nivel"])["C.Específ."].agg(["count","min", "max", "mean"]).round(0).astype(int).reset_index()
        stats.to_excel(output_file, index=False, sheet_name="statistics")

    if not os.path.exists(output_file_2):
        stats = rpt.groupby(["Denominación Ministerio", "Denominación Larga", "Gr/Sb", "Nivel"])["C.Específ."].agg(["count","min", "max", "mean"]).round(0).astype(int).reset_index()
        stats.to_excel(output_file_2, index=False, sheet_name="statistics")



