import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from transformers import pipeline

# Load the Machine Learning Model
# outside the layout and callbacks so it only loads once when the server starts
print("Downloading/Loading the AI Model...")
classifier = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    top_k=None
)

# Dictionary to map the labels to emojis
EMOJI_MAP = {
    "joy": "😊 Joy",
    "anger": "😡 Anger",
    "disgust": "🤢 Disgust",
    "fear": "😨 Fear",
    "sadness": "😢 Sadness",
    "surprise": "😲 Surprise",
    "neutral": "😐 Neutral"
}

# Accuracy vs. Baseline Chart
accuracy_fig = go.Figure(go.Bar(
    x=[14, 66], 
    y=['Random Guess (Baseline)', 'Model Accuracy'], 
    orientation='h', 
    text=['14%', '66%'], 
    textposition='auto',
    textfont=dict(size=20, color='white'),
    marker=dict(
        color=['#6c757d', '#007BFF'], 
        line=dict(color='rgba(0,0,0,0)', width=1)
    )
))

accuracy_fig.update_layout(
    title="Model Performance vs. Random Chance",
    title_x=0.5,
    xaxis=dict(
        title="Accuracy (%)", 
        range=[0, 100], 
        showgrid=True
    ),
    yaxis=dict(showgrid=False),
    plot_bgcolor='white',
    height=300, 
    margin=dict(l=20, r=20, t=50, b=50)
)

# Dash User Interface (Frontend)
app = dash.Dash(__name__)
app.title = "The Vibe Check"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '800px', 'margin': '0 auto', 'padding': '20px'}, children=[
    
    dcc.Store(id='session-history', data=[]), 
    
    html.H1("The Vibe Check: AI Emotion Analyzer", style={'textAlign': 'center'}),
    html.P("Type or paste any text below to see its emotional footprint.", style={'textAlign': 'center'}),
    
    # Input
    dcc.Textarea(
        id='user-input',
        placeholder='Paste a review, a text message, or an email draft here...',
        style={'width': '100%', 'height': '150px', 'fontSize': '16px', 'padding': '10px', 'borderRadius': '5px'}
    ),
    
    html.Br(),
    
    # Submit Button
    html.Button(
        'Analyze Vibe', 
        id='submit-button', 
        n_clicks=0, 
        style={'width': '100%', 'padding': '15px', 'fontSize': '18px', 'backgroundColor': '#007BFF', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'}
    ),
    
    html.Hr(style={'marginTop': '30px', 'marginBottom': '30px'}),
    
    # Output Section (Emoji & Radar Chart)
    html.Div(id='primary-emotion-output', style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': 'bold', 'marginBottom': '20px'}),
    
    html.Div(id='charts-container', style={'display': 'none', 'flexDirection': 'row', 'justifyContent': 'center'}, children=[
        dcc.Graph(id='radar-chart', style={'width': '50%'}),
        dcc.Graph(id='confidence-gauge', style={'width': '50%'})
    ]),

    html.Hr(style={'marginTop': '40px', 'marginBottom': '40px'}),

    # Session History Timeline Section
    html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '40px'}, children=[
        html.H3("Session History Timeline", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Dropdown
        html.Label("Select Emotions to Track:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='emotion-filter',
            options=[{'label': e, 'value': e} for e in ["Anger", "Disgust", "Fear", "Joy", "Neutral", "Sadness", "Surprise"]],
            value=["Joy", "Anger", "Sadness"], # Default emotions to show on startup
            multi=True, 
            style={'marginBottom': '20px'}
        ),
        
        # Timeline Chart
        dcc.Graph(id='history-timeline')
    ]),

    # Model Performance Section  
    html.Details([
        html.Summary(
            "About the AI Model & Accuracy", 
            style={'fontSize': '20px', 'fontWeight': 'bold', 'cursor': 'pointer', 'marginBottom': '10px'}
        ),
        html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'marginTop': '10px'}, children=[
            html.P(
                "This application utilizes a DistilRoBERTa neural network trained on nearly 20,000 observations "
                "across 7 distinct emotion categories.", 
                style={'textAlign': 'center', 'fontSize': '16px', 'color': '#495057', 'maxWidth': '800px', 'margin': '0 auto 20px auto'}
            ),
            
            # Accuracy vs. Baseline Bar Chart
            dcc.Graph(figure=accuracy_fig, config={'displayModeBar': False}) 
        ])
    ])
])

# Callback (Back End)
@app.callback(
    [Output('primary-emotion-output', 'children'),
     Output('radar-chart', 'figure'),
     Output('confidence-gauge', 'figure'),      
     Output('charts-container', 'style'),
     Output('session-history', 'data')],
    [Input('submit-button', 'n_clicks')],
    [State('user-input', 'value'),
     State('session-history', 'data')]
)
def update_dashboard(n_clicks, text_input, history):
    # If the user hasn't typed anything yet, don't do anything
    if n_clicks == 0 or not text_input:
        return "", go.Figure(), go.Figure(), {'display': 'none'}, []
    
    # Run the text through the ML model
    ml_results = classifier(text_input)[0] 
    
    # Logic for the Primary Emoji and Confidence Score
    top_emotion_data = max(ml_results, key=lambda x: x['score'])
    top_emotion = top_emotion_data['label']
    top_score = top_emotion_data['score'] # Extract the raw decimal score
    
    display_emoji = EMOJI_MAP.get(top_emotion, top_emotion)

    percentage_score = top_score * 100
    
    if percentage_score >= 80:
        bar_color = "#28a745"
    elif percentage_score >= 50:
        bar_color = "#ffc107"
    else:
        bar_color = "#dc3545"
    
    # Extract categories and scores for the Radar Chart
    categories = [res['label'].capitalize() for res in ml_results]
    scores = [res['score'] for res in ml_results]
    
    # Match the first category with the last one to close the web 
    categories.append(categories[0])
    scores.append(scores[0])
    
    # Spider Chart
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Emotion Footprint',
        line=dict(color='#8A2BE2'),
        fillcolor='rgba(138, 43, 226, 0.4)'
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title=dict(
            text="Emotional Distribution", 
            font=dict(size=20), 
            y=0.05, x=0.5, xanchor='center', yanchor='bottom'
        ),
        margin=dict(l=60, r=60, t=40, b=70)
    )

    # Confidence Gauge
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage_score,
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': bar_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 0, 0, 0.1)"}, 
                {'range': [50, 80], 'color': "rgba(255, 165, 0, 0.1)"}, 
                {'range': [80, 100], 'color': "rgba(0, 128, 0, 0.1)"}   
            ]
        }
    ))
    gauge_fig.update_layout(
        title=dict(
            text=f"Confidence in '{top_emotion.capitalize()}'", 
            font=dict(size=20), 
            y=0.05, x=0.5, xanchor='center', yanchor='bottom'
        ),
        margin=dict(l=50, r=50, t=40, b=70) 
    )

    # Convert the ML results into a dictionary
    current_scores = {res['label'].capitalize(): res['score'] * 100 for res in ml_results}
    
    # Add the text snippet so we know what the user typed
    current_scores['text_snippet'] = text_input[:30] + "..." if len(text_input) > 30 else text_input
    
    # Append to our memory bank
    history.append(current_scores)
    
    # Return the text, both figures, and change the container style to Flex (visible side-by-side)
    return f"Primary Vibe: {display_emoji}", radar_fig, gauge_fig, {'display': 'flex', 'flexDirection': 'row'}, history

# Session History Timeline Callback
@app.callback(
    Output('history-timeline', 'figure'),
    [Input('session-history', 'data'),
     Input('emotion-filter', 'value')]
)
def update_timeline(history, selected_emotions):
    if not history or not selected_emotions:
        return go.Figure().update_layout(title="No data to display yet.", plot_bgcolor='white')

    timeline_fig = go.Figure()
    
    x_axis_labels = [f"Input {i+1}" for i in range(len(history))]

    for emotion in selected_emotions:
        y_values = [entry[emotion] for entry in history]
        
        timeline_fig.add_trace(go.Scatter(
            x=x_axis_labels,
            y=y_values,
            mode='lines+markers',
            name=emotion,
            line=dict(width=3),
            marker=dict(size=10)
        ))

    timeline_fig.update_layout(
        title="Emotion Tracking Across Inputs",
        yaxis=dict(title="Confidence Score (%)", range=[0, 100], showgrid=True, gridcolor='lightgray'),
        xaxis=dict(showgrid=False),
        plot_bgcolor='white',
        hovermode="x unified",
        margin=dict(l=40, r=40, t=50, b=80)
    )
    
    return timeline_fig

# Run the Server
if __name__ == '__main__':
    # port=7860 is required by Hugging Face Spaces
    app.run_server(host='0.0.0.0', port=7860, debug=False)
