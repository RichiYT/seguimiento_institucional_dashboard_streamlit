import pandas as pd
import plotly.express as px

def crear_grafico(df):
    ejecucion_fuente_financiamiento = df.groupby('nombre_ff').agg(
        total_ff = ('valor_soles','sum')
    ).reset_index()

    colors = ['#0077b6', '#1A4D83', '#063970', '#2f567D']
    fig = px.pie(ejecucion_fuente_financiamiento,
        values = 'total_ff',
        names = 'nombre_ff',
        title = 'Ejecución por Fuente de Financiamiento',
        color_discrete_sequence=colors
    )

    fig.update_layout(yaxis_title = 'Fuente de Financiamiento',xaxis_title='Ejecución Presupuestal', showlegend=False)
    fig.update_traces(textposition = 'outside', textinfo = 'percent+label',insidetextfont=dict(size = 12))

    return fig
