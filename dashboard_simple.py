"""
Credit Risk Dashboard - Version Simple que SI funciona
"""

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from datetime import datetime

print("🚀 Iniciando Credit Risk Dashboard...")

# Datos de ejemplo
data = {
    'source': ['Moody\'s', 'Moody\'s', 'Moody\'s', 'S&P Global', 'S&P Global', 'Fitch', 'Fitch'],
    'title': [
        'Private credit volatility intensifies',
        'Global corporate defaults update',
        'Credit conditions outlook',
        'Global Credit Conditions Q2 2026',
        'Corporate Default Transition Study',
        'Global Credit Outlook 2026',
        'European Banking Sector Outlook'
    ],
    'date': ['2026-04-24', '2026-04-24', '2026-04-23', '2026-04-24', '2026-04-23', '2026-04-24', '2026-04-23'],
    'content_type': ['Research', 'Data Story', 'Research', 'Research', 'Research', 'Report', 'Outlook']
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

print(f"✅ Cargados {len(df)} artículos")

# Crear dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Credit Risk Intelligence Dashboard", style={'textAlign': 'center', 'color': '#2C3E50'}),
    html.P("Real-time credit risk news from Moody's, Fitch, and S&P Global", 
           style={'textAlign': 'center', 'color': '#7F8C8D'}),
    html.Hr(),
    
    # Fila de métricas
    html.Div([
        html.Div([
            html.H3("📰 Total Articles", style={'textAlign': 'center'}),
            html.H2(f"{len(df)}", style={'textAlign': 'center', 'color': '#3498DB'})
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': '#F8F9FA', 
                  'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
        
        html.Div([
            html.H3("🏢 Active Sources", style={'textAlign': 'center'}),
            html.H2(f"{df['source'].nunique()}", style={'textAlign': 'center', 'color': '#27AE60'})
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': '#F8F9FA', 
                  'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
        
        html.Div([
            html.H3("📅 Last Update", style={'textAlign': 'center'}),
            html.H2(f"{datetime.now().strftime('%H:%M')}", style={'textAlign': 'center', 'color': '#E74C3C'})
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': '#F8F9FA', 
                  'borderRadius': '10px', 'padding': '10px', 'margin': '10px'})
    ], style={'textAlign': 'center'}),
    
    # Gráfico 1: Artículos por fuente
    dcc.Graph(
        figure=px.bar(
            df['source'].value_counts().reset_index(),
            x='source', y='count',
            title='📊 Articles by Rating Agency',
            color='source',
            color_discrete_map={'Moody\'s': '#00A3E0', 'S&P Global': '#005A9C', 'Fitch': '#FF6600'}
        ).update_layout(showlegend=False)
    ),
    
    # Gráfico 2: Línea de tiempo
    dcc.Graph(
        figure=px.line(
            df.groupby(df['date'].dt.date).size().reset_index(),
            x='date', y=0,
            title='📈 News Timeline (Last 48 Hours)',
            markers=True
        ).update_layout(xaxis_title="Date", yaxis_title="Article Count")
    ),
    
    # Gráfico 3: Top tipos de contenido
    dcc.Graph(
        figure=px.pie(
            df, names='content_type', title='🎯 Content Type Distribution'
        )
    ),
    
    # Últimas noticias
    html.H3("📰 Latest Headlines", style={'marginTop': '30px'}),
    html.Div([
        html.Ul([
            html.Li(f"[{row['source']}] {row['title']} ({row['date'].strftime('%Y-%m-%d')})", 
                   style={'marginBottom': '10px'})
            for _, row in df.head(5).iterrows()
        ])
    ], style={'backgroundColor': '#F8F9FA', 'borderRadius': '10px', 'padding': '20px'})
], style={'fontFamily': 'Arial', 'padding': '20px'})

print("=" * 50)
print("🚀 Dashboard starting...")
print("📊 Open your browser and go to: http://127.0.0.1:8050")
print("=" * 50)

if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1', port=8050)