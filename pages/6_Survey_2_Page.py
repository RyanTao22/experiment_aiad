import streamlit as st

def main():
    if 'ai_feeling_complete' not in st.session_state:
        st.session_state.ai_feeling_complete = False

    st.subheader("Survey 2 (3 questions)")

    score_descriptions_q1 = {
        1: "Very Negative",
        2: "Negative",
        3: "Somewhat Negative",
        4: "Neutral",
        5: "Somewhat Positive",
        6: "Positive",
        7: "Very Positive"
    }
    
    score_descriptions_q2 = {
        1: "Certainly Human",
        2: "Likely Human",
        3: "Possibly Human",
        4: "Unsure",
        5: "Possibly AI",
        6: "Likely AI",
        7: "Certainly AI"
    }
    
    score_descriptions_q3 = {
        1: "Completely Unacceptable",
        2: "Strongly Opposed",
        3: "Somewhat Opposed",
        4: "Neutral",
        5: "Somewhat Acceptable",
        6: "Generally Acceptable",
        7: "Completely Acceptable"
    }
    

    
    def create_question(question_num, label, descriptions_dict, key):
        #st.markdown(f"**Q{question_num}: {label}**")
        score = st.slider(
            f"{label} ({1} = {descriptions_dict[1]}  |  4 = {descriptions_dict[4]}  |  7 = {descriptions_dict[7]})",
            min_value=1,
            max_value=7,
            value=None,
            key=key
        )
        if score is not None:
            st.caption(f"Selected {score} - {descriptions_dict[score]}")
        return score
    
    # Question 1 - AI Attitude
    q1_score = create_question(
        1,
        "What is your overall attitude towards AI technology?",
        score_descriptions_q1,
        "q1_ai_attitude"
    )
    
    #st.divider()
    
    # Question 2 - AI Probability
    q2_score = create_question(
        2,
        "How likely was this advertisement Human-generated or AI-generated?",
        score_descriptions_q2,
        "q2_ai_probability"
    )
    
    #st.divider()
    
    # Question 3 - AI Acceptance
    q3_score = create_question(
        3,
        "How acceptable do you find AI-generated advertising?",
        score_descriptions_q3,
        "q3_ai_acceptance"
    )
    
    # Submission section
    if st.button("Submit Assessment", type="primary"):
        if None not in [q1_score, q2_score, q3_score]:
            st.session_state.data_dict.update({
                'ai_attitude': q1_score,
                'ai_probability': q2_score,
                'ai_ad_acceptance': q3_score
            })
            st.session_state.ai_feeling_complete = True
            st.success("Responses recorded successfully!")
            st.switch_page("pages/7_Survey_3_Page.py")
        else:
            st.error("Please complete all questions before submitting")

if __name__ == "__main__":
    if 'score_video_complete' not in st.session_state or not st.session_state.score_video_complete:
        st.switch_page("pages/5_Score_Video_Page.py")
    else:
        main()