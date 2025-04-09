import streamlit as st
import pandas as pd
import pickle

# Load trained model pipeline
pipe = pickle.load(open('model.pkl', 'rb'))

# Modern Streamlit layout
st.set_page_config(page_title="Match Win Predictor", page_icon="🏏", layout="centered")

st.title("🏏 SATORI 💸🤑")
st.markdown("### Predict the win probability of a team during a live IPL match.")
st.write("Enter the match details below:")

with st.form("predict_form"):
    # Create two-column layout for team inputs
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox("Batting Team", sorted([
            'Chennai Super Kings', 'Delhi Capitals', 'Kolkata Knight Riders',
            'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
            'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Lucknow Super Giants',
            'Gujarat Titans'
        ]))

        score = st.number_input("Current Score", min_value=0, value=0)
        target = st.number_input("Target Score", min_value=1, value=180)
        wickets = st.slider("Wickets Lost", min_value=0, max_value=10, value=0)

    with col2:
        bowling_team = st.selectbox("Bowling Team", sorted([
            'Chennai Super Kings', 'Delhi Capitals', 'Kolkata Knight Riders',
            'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
            'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Lucknow Super Giants',
            'Gujarat Titans'
        ]))

        selected_city = st.selectbox("City", sorted([
            'Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Jaipur', 'Kolkata',
            'Lucknow', 'Mumbai', 'Pune', 'Rajkot', 'Visakhapatnam'
        ]))

        
        balls_left = st.slider("Balls Left", min_value=0, max_value=120, value=60)

    submitted = st.form_submit_button("Predict")

if submitted:
    # Derived features
    runs_left = target - score
    wickets_remaining = 10 - wickets
    overs_completed = (120 - balls_left) / 6
    crr = score / overs_completed if overs_completed > 0 else 0
    rrr = runs_left / (balls_left / 6) if balls_left > 0 else 0

    # Prepare input dataframe
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_remaining': [wickets_remaining],
        'total_run_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    # Prediction
    result = pipe.predict_proba(input_df)
    win_prob = round(result[0][1] * 100)
    lose_prob = round(result[0][0] * 100)

    # Show results
    st.subheader(f"📊 Win Probability for **{batting_team}**")
    st.progress(win_prob / 100)

    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="🏆 Win Chance", value=f"{win_prob}%")
    with col4:
        st.metric(label="💔 Lose Chance", value=f"{lose_prob}%")

    # Optional: Show full input for debug
    with st.expander("Show Input Data"):
        st.dataframe(input_df)
