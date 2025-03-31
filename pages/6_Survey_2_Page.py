import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import time

def main():
    if 'attn_attempts' not in st.session_state:
        st.session_state.attn_attempts = 0
    st.session_state.survey_2_complete = False

    st.subheader("Survey 2 - Part 1 (5 questions)")

    q1_7 = st.radio(
        "If using an algorithm, can the results be biased against specific groups of people?",
        [
            "No, unlike humans, algorithms are free of emotions and cannot be wrong",
            "Yes, but only if you train them on privileged populations",
            "Yes, but only if you use them with incomplete data",
            "Yes, even with correct data and training, algorithms can provide biased results"
        ],index=None
    )

    q1_14 = st.radio(
        "What information do social media algorithms not typically use when deciding what information to display to a person?",
        [
            "Articles people have previously clicked on",
            "Videos people have previously watched online",
            "Information people have shared on social media",
            "What would benefit society"
        ],index=None
    )

    attn1 = st.radio(
        "To confirm you are paying attention, please select 'Strongly disagree' for this statement.",
        [
            "Strongly agree",
            "Agree",
            "Neutral",
            "Strongly disagree" 
        ],
        index=None
    )

    q2_10 = st.radio(
        "Who is primarily responsible for the ethical considerations of an AI system?",
        [
            "The AI system itself",
            "Data providers",
            "Human developers",
            "End-users"
        ],index=None
    )

    q2_16 = st.radio(
        "Which is a key ethical issue surrounding AI?",
        [
            "Algorithmic efficiency",
            "CPU usage",
            "Privacy",
            "Code readability"
        ],index=None
    )
    st.divider()

    st.subheader("Survey 2 - Part 2 (5 questions)")

    attn2 = st.radio(
        "According to the following instruction, what should you select here? Choose 'Green'.",
        [
            "Red",
            "Green", 
            "Blue"
        ],
        index=None
    )

    q1_2 = st.radio(
        "Which technology is the primary enabler of Artificial Intelligence?",
        [
            "Electric Battery",
            "Machine Learning",
            "Robotics",
            "Engineering"
        ],index=None
    )

    q1_19 = st.radio(
        "What is training data and why is it important?",
        [
            "Training data is used when the model is fully calibrated, to train new users with how to work with the model",
            "Training data is used to calibrate the model during creation, creating a model that performs best according to that data",
            "Training data is used to test the model after it was created, to see how it works with new data",
            "Training data is used to minimize bias in older models and train them to new population types"
        ],index=None
    )

    q2_1 = st.radio(
        "Which of the following is NOT powered by AI?",
        [
            "Self-driving cars",
            "Google's search algorithm",
            "A basic calculator",
            "Chatbots"
        ],index=None
    )

    q2_9 = st.radio(
        "What is the first step in a typical machine learning process?",
        [
            "Data collection",
            "Model selection",
            "Prediction",
            "Model evaluation"
        ],index=None
    )
    
    if st.button("Submit to Complete the Study", type="primary"):
        all_rated = True
        for metric in [attn1, attn2, q1_7, q1_14, q2_10, q2_16, q1_2, q1_19, q2_1, q2_9]:
            if metric == None:
                all_rated = False
                break
        
        if not all_rated:
            st.error("Please answer all questions before saving.") 
        else:
            if attn1 == "Strongly disagree" and attn2 == "Green":  
                if st.session_state.attn_attempts >= 2:  
                    st.warning('You have failed to pass the Attention Checks. Thank you for your time. Please close the browser and return to Prolific.')
                    st.stop()
                
                st.session_state.data_dict['table1_7'] = q1_7
                st.session_state.data_dict['table1_14'] = q1_14
                st.session_state.data_dict['table2_10'] = q2_10
                st.session_state.data_dict['table2_16'] = q2_16
                st.session_state.data_dict['table1_2'] = q1_2
                st.session_state.data_dict['table1_19'] = q1_19
                st.session_state.data_dict['table2_1'] = q2_1
                st.session_state.data_dict['table2_9'] = q2_9
                
                engine = create_engine(f'mysql+pymysql://{st.secrets["username"]}:{st.secrets["password"]}@{st.secrets["db_url"]}:{st.secrets["port"]}/{st.secrets["database"]}?charset=utf8mb4')
                with engine.begin() as conn:
                    df = pd.DataFrame.from_dict([st.session_state.data_dict])
                    df.to_sql(name=st.secrets["db_table"], con=conn, if_exists='append', index=False)
                
                st.session_state.survey_2_complete = True
                st.success('You have successfully completed this survey. Please copy and keep your redeem code below, then close the browser and return to Prolific.')
                st.success("Your redeem code is: PFHQ-2X3F-4G5H")
                st.balloons()
            else:
                st.session_state.attn_attempts += 1
                if st.session_state.attn_attempts >= 2:  # 只允许错误一次
                    st.warning('You have failed to pass the Attention Checks. Thank you for your time. Please close the browser and return to Prolific.')
                    st.stop()
                else:
                    st.error("Incorrect answer/answers detected. Please review your answers and try again.")
                    time.sleep(2.5)
                    st.rerun()

if __name__ == "__main__":
    if 'score_video_complete' not in st.session_state or not st.session_state.score_video_complete:
        st.switch_page("pages/5_Score_Video_Page.py")
    else:
        main()