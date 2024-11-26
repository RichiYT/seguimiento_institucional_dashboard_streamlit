import pandas as pd
import plotly.express as px

def crear_grafico(df):
    ejecucion_mensual = df.set_index('fecha_autorizacion').groupby(pd.Grouper(freq = 'ME'))['valor_soles'].sum().reset_index()
    ejecucion_mensual['Year'] = ejecucion_mensual['fecha_autorizacion'].dt.year
    ejecucion_mensual['Month'] = ejecucion_mensual['fecha_autorizacion'].dt.month_name()
    ejecucion_mensual = ejecucion_mensual[ejecucion_mensual['Year'] > 2023]
  

    fig = px.line(ejecucion_mensual,
        x = 'Month',
        y = 'valor_soles',
        markers= True,
        range_y = (0,ejecucion_mensual.max()),
        color = 'Year',
        line_dash = 'Year',
        title = 'Ejecución Mensual'
        )
    fig.update_layout(yaxis_title = 'Ingresos (S/ )')

    return fig


