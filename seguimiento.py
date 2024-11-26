import streamlit as st
import pandas as pd
import locale
import grafico_lineas as gl
import grafico_barras as gb
import grafico_pizza as gp

locale.setlocale(locale.LC_TIME, "es_ES.utf8") 
st.set_page_config(layout = 'wide')
st.title('Seguimiento Presupuestal :bar_chart: ')

def formata_numero(valor, prefijo = ''):
    for unidad in ['','k']:
        if valor<1000:
            return f'{prefijo}{valor:.2f} {unidad}'
        valor /=1000
    return f'{prefijo}{valor:.2f} M'

# Abrimos  la base de datos
df_seguimientoI = pd.read_excel('https://raw.githubusercontent.com/RichiYT/seguimiento_institucional_dashboard_streamlit/main/ReporteSeguimiento.xlsx')

#df_seguimientoI['fecha_autorizacion'] = pd.to_datetime(df_seguimientoI['fecha_autorizacion'])
df_seguimientoI['tipo_clasificador'] = df_seguimientoI['clasificador'].str.split(' ').str[0]

# Configuramos los Filtros
st.sidebar.image('logoUNSCH.png')
st.sidebar.title('Filtros')
lista_cc = sorted(list(df_seguimientoI['nombre_cc'].unique()))
nombres_cc = st.sidebar.selectbox('Centro de Costo',lista_cc,index=None,placeholder="Ingrese el Centro de Costo")

if nombres_cc:
    lista_ao = sorted(list(df_seguimientoI['nombre_ao'].unique()))
    lista_ao = sorted(list(df_seguimientoI[df_seguimientoI['nombre_cc'] == nombres_cc]['nombre_ao'].unique()))
    nombres_ao = st.sidebar.selectbox('Actividad Operativa',lista_ao,index=None,placeholder="Ingrese Actividad Operativa")
else:
    nombres_ao = None

lista_tipo = sorted(list(df_seguimientoI['tipo'].dropna().unique()))
lista_tipo.insert(0, 'Todos')
tipo_tipo = st.sidebar.selectbox('Tipo',lista_tipo)

lista_fuente = sorted(list(df_seguimientoI['nombre_ff'].dropna().unique()))
lista_fuente.insert(0, 'Todos')
tipo_fuente = st.sidebar.selectbox('Fuente de Finanaciamiento',lista_fuente)

lista_clasificador = sorted(list(df_seguimientoI['tipo_clasificador'].dropna().unique()))
lista_clasificador.insert(0, 'Todos')
tipo_clasificador = st.sidebar.selectbox(' Tipo de Clasificador de Gasto',lista_clasificador)

#Filtrando los datos
if nombres_cc:
    df_seguimientoI = df_seguimientoI[df_seguimientoI['nombre_cc']==nombres_cc]

if nombres_ao:
   df_seguimientoI = df_seguimientoI[df_seguimientoI['nombre_ao']==nombres_ao]

if tipo_tipo!='Todos':
    df_seguimientoI = df_seguimientoI[df_seguimientoI['tipo']==tipo_tipo]

if tipo_fuente!='Todos':
    df_seguimientoI = df_seguimientoI[df_seguimientoI['nombre_ff']==tipo_fuente]

if tipo_clasificador!='Todos':
    df_seguimientoI = df_seguimientoI[df_seguimientoI['tipo_clasificador']==tipo_clasificador]

#Llamar a los gráficos
graf_lineas = gl.crear_grafico(df_seguimientoI)
graf_barras = gb.crear_grafico(df_seguimientoI)
graf_pizza = gp.crear_grafico(df_seguimientoI)

#Ejecución por tipo
df_ejecucion_bien = df_seguimientoI[df_seguimientoI['tipo'] =='Bien']
df_ejecucion_servicio = df_seguimientoI[df_seguimientoI['tipo'] =='Servicio']
df_ejecucion_viatico = df_seguimientoI[df_seguimientoI['tipo'] =='Viatico']

col1, col2 = st.columns(2)
with col1:
    st.metric('**Total de Devengado**', formata_numero(df_seguimientoI['valor_soles'].sum(), 'S/'))
    st.metric('**Viaticos Devengado**',formata_numero(df_ejecucion_viatico['valor_soles'].sum(), 'S/'))
    st.plotly_chart(graf_lineas, use_container_width=True)
    st.plotly_chart(graf_pizza, use_container_width=True)
with col2:
    st.metric('**Bienes Devengado**', formata_numero(df_ejecucion_bien['valor_soles'].sum(), 'S/'))
    st.metric('**Servicios Devengado**',formata_numero(df_ejecucion_servicio['valor_soles'].sum(), 'S/'))
    st.plotly_chart(graf_barras, use_container_width=True)

month_order_es = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
month_translation = {
    "January": "enero", "February": "febrero", "March": "marzo", "April": "abril",
    "May": "mayo", "June": "junio", "July": "julio", "August": "agosto",
    "September": "septiembre", "October": "octubre", "November": "noviembre", "December": "diciembre"
}


df_seguimientoI_ao=df_seguimientoI.copy()
df_seguimientoI_ao['mes'] = df_seguimientoI['fecha_autorizacion'].dt.month_name()  #df_seguimientoI_ao['fecha_autorizacion'].dt.month_name()
df_seguimientoI_ao = df_seguimientoI_ao[['nombre_ao','mes','valor_soles']]
df_pivot_ao= df_seguimientoI_ao.pivot_table(index='nombre_ao',columns='mes',values='valor_soles',aggfunc='sum').reset_index()
df_pivot_ao.columns.name = None
df_pivot_ao = df_pivot_ao.fillna(0)

df_pivot_ao.rename(columns=month_translation, inplace=True)
df_pivot_ao = df_pivot_ao[['nombre_ao'] + [month for month in month_order_es if month in df_pivot_ao.columns]]
totales_ao = df_pivot_ao.iloc[:, 1:].sum()
fila_totales_ao = pd.DataFrame([["TOTAL"] + totales_ao.tolist()], columns=df_pivot_ao.columns)
df_pivot_ao = pd.concat([fila_totales_ao, df_pivot_ao], ignore_index=True)


df_seguimientoI_clasi = df_seguimientoI.copy()
df_seguimientoI_clasi['mes'] = df_seguimientoI['fecha_autorizacion'].dt.month_name()  #df_seguimientoI_clasi['fecha_autorizacion'].dt.month_name()
df_seguimientoI_clasi = df_seguimientoI_clasi[['nombre_clasi','mes','valor_soles']]
df_pivot_clasi= df_seguimientoI_clasi.pivot_table(index='nombre_clasi',columns='mes',values='valor_soles',aggfunc='sum').reset_index()

df_pivot_clasi.columns.name = None
df_pivot_clasi = df_pivot_clasi.fillna(0)
df_pivot_clasi.rename(columns=month_translation, inplace=True)
df_pivot_clasi = df_pivot_clasi[['nombre_clasi'] + [month for month in month_order_es if month in df_pivot_clasi.columns]]
totales_clasi = df_pivot_clasi.iloc[:, 1:].sum()
fila_totales_clasi = pd.DataFrame([["TOTAL"] + totales_clasi.tolist()], columns=df_pivot_clasi.columns)
df_pivot_clasi = pd.concat([fila_totales_clasi, df_pivot_clasi], ignore_index=True)

st.markdown("**ACTIVIDAD OPERATIVA**")
st.dataframe(df_pivot_ao)

st.markdown("**CLASIFICADOR DE GASTO**")

st.dataframe(df_pivot_clasi)