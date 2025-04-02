import os
import io
import pandas as pd
from utils import read_zip

def gen_stats():
    output_file = '/app/rpt/rpt_stats.xlsx'
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Skipping generation.")
        return
        
    if not os.path.exists('/app/rpt/rpt_stats.xlsx'):
        rpt = pd.read_excel(
            io=io.BytesIO(read_zip(r'/app/rpt/rpt.zip', 'rpt.xlsx')),
            sheet_name="Resultados", # 0,
            header=0,
            skiprows=[0,1,2] )

        stats = rpt.groupby(["Denominación Ministerio", "Gr/Sb", "Nivel"])["C.Específ."].agg(["count","min", "max", "mean"]).round(0).astype(int).reset_index()
        stats.to_excel(output_file, index=False, sheet_name="statistics")
