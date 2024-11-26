import pandas as pd
import plotly.express as px
def crear_grafico(df):
    ejecucion_centro_costo = df.groupby('nombre_cc')[['valor_soles']].sum().sort_values('valor_soles', ascending = True).reset_index()
    fig = px.bar(ejecucion_centro_costo.tail(10),
        x = 'valor_soles',
        y = 'nombre_cc',
        text = 'valor_soles',
        title = 'Top Ejecución Presupuestal por Centro de Costo'
        )
    fig.update_layout(yaxis_title = 'Centro de Costo', xaxis_title='Ejecución Presupuestal (S/)', showlegend=False)
    fig.update_traces(texttemplate = '%{text:.3s}')

    return fig