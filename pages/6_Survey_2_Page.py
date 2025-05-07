import streamlit as st
import random

def main():
    if 'survey2_submitted' not in st.session_state:
        st.session_state.survey2_submitted = False

    st.subheader("Survey 2 (3 questions)")

    score_descriptions = {
        "ai_attitude": {
            1: "Very Negative",
            2: "Negative",
            3: "Somewhat Negative",
            4: "Neutral",
            5: "Somewhat Positive",
            6: "Positive",
            7: "Very Positive"
        },
        "ai_probability": {
            1: "Certainly Human",
            2: "Likely Human",
            3: "Possibly Human",
            4: "Unsure",
            5: "Possibly AI",
            6: "Likely AI",
            7: "Certainly AI"
        },
        "ai_ad_acceptance": {
            1: "Very Unacceptable",
            2: "Unacceptable",
            3: "Somewhat Unacceptable",
            4: "Neutral",
            5: "Somewhat Acceptable",
            6: "Acceptable",
            7: "Very Acceptable"
        }
    }
    
    def create_question(label, descriptions_dict, key):
        score = st.slider(
            f"{label} (1 = {descriptions_dict[1]}  |  4 = {descriptions_dict[4]}  |  7 = {descriptions_dict[7]})",
            min_value=1,
            max_value=7,
            value=None,
            key=key
        )
        if score is not None:
            st.caption(f"Selected {score} - {descriptions_dict[score]}")
        return score
    
    if not st.session_state.survey2_submitted:
        # 定义问题列表
        questions = [
            {
                "label": "What is your overall attitude towards AI technology?",
                "key": "ai_attitude",
                "descriptions": score_descriptions["ai_attitude"]
            },
            {
                "label": "How likely was this advertisement Human-generated or AI-generated?",
                "key": "ai_probability",
                "descriptions": score_descriptions["ai_probability"]
            },
            {
                "label": "How acceptable do you find AI-generated advertising?",
                "key": "ai_ad_acceptance",
                "descriptions": score_descriptions["ai_ad_acceptance"]
            }
        ]
        
        # 只在第一次运行时打乱问题顺序
        if 'shuffled_survey2_questions' not in st.session_state:
            shuffled_questions = questions.copy()
            random.shuffle(shuffled_questions)
            st.session_state.shuffled_survey2_questions = shuffled_questions
        
        # 存储答案的字典
        answers = {}
        
        # 显示随机化后的问题
        for q in st.session_state.shuffled_survey2_questions:
            score = create_question(
                q["label"],
                q["descriptions"],
                q["key"]
            )
            answers[q["key"]] = score
        
        # Submission section
        if st.button("Submit Assessment", type="primary"):
            if None not in answers.values():
                st.session_state.data_dict.update(answers)
                st.session_state.survey2_submitted = True
                st.success("Responses recorded successfully!")
                st.switch_page("pages/7_Survey_3_Page.py")
            else:
                st.error("Please complete all questions before submitting")
    else:
        st.success("Responses recorded successfully!")
        if st.button("Continue to Next Section", type="primary"):
            st.switch_page("pages/7_Survey_3_Page.py")

if __name__ == "__main__":
    if 'score_submitted' not in st.session_state or not st.session_state.score_submitted:
        st.switch_page("pages/5_Score_Video_Page.py")
    else:
        main()