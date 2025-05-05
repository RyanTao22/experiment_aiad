import streamlit as st
import random

def main():
    if 'score_submitted' not in st.session_state:
        st.session_state.score_submitted = False

    st.header("Score the Advertising Videos")
    st.subheader("Please score the advertising videos you just watched.")
    
    score_descriptions = {
        "engagement": {
            1: "Very Boring",
            2: "Boring",
            3: "Somewhat Boring",
            4: "Neutral",
            5: "Somewhat Interesting",
            6: "Interesting",
            7: "Very Interesting"
        },
        "credibility": {
            1: "Very Unbelievable",
            2: "Unbelievable",
            3: "Somewhat Unbelievable",
            4: "Neutral",
            5: "Somewhat Believable",
            6: "Believable",
            7: "Very Believable"
        },
        "persuasiveness": {
            1: "Very Unconvincing",
            2: "Unconvincing",
            3: "Somewhat Unconvincing",
            4: "Neutral",
            5: "Somewhat Convincing",
            6: "Convincing",
            7: "Very Convincing"
        },
        "creativity": {
            1: "Very Familiar",
            2: "Familiar",
            3: "Somewhat Familiar",
            4: "Neutral",
            5: "Somewhat Novel", 
            6: "Novel",
            7: "Very Novel"
        },
        "effectiveness": {
            1: "Very Unlikely to Purchase",
            2: "Unlikely to Purchase",
            3: "Somewhat Unlikely to Purchase",
            4: "Neutral",
            5: "Somewhat Likely to Purchase",
            6: "Likely to Purchase",
            7: "Very Likely to Purchase"
        },
        "quality": {
            1: "Very Poor",
            2: "Poor",
            3: "Somewhat Poor",
            4: "Neutral",
            5: "Somewhat Good",
            6: "Good",
            7: "Very Good"
        },
        "relevance": {
            1: "Very Irrelevant",
            2: "Irrelevant", 
            3: "Somewhat Irrelevant",
            4: "Neutral",
            5: "Somewhat Relevant",
            6: "Relevant",
            7: "Very Relevant"
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
    
    if not st.session_state.score_submitted:
        # 定义问题列表
        questions = [
            {
                "label": "Engagement",
                "key": "engagement",
                "descriptions": score_descriptions["engagement"]
            },
            {
                "label": "Credibility/Trustworthiness",
                "key": "credibility",
                "descriptions": score_descriptions["credibility"]
            },
            {
                "label": "Persuasiveness",
                "key": "persuasiveness",
                "descriptions": score_descriptions["persuasiveness"]
            },
            {
                "label": "Creativity",
                "key": "creativity",
                "descriptions": score_descriptions["creativity"]
            },
            {
                "label": "Effectiveness/Purchase Intention",
                "key": "effectiveness",
                "descriptions": score_descriptions["effectiveness"]
            },
            {
                "label": "Quality",
                "key": "quality",
                "descriptions": score_descriptions["quality"]
            },
            {
                "label": "Relevance",
                "key": "relevance",
                "descriptions": score_descriptions["relevance"]
            }
        ]
        
        # 只在第一次运行时打乱问题顺序
        if 'shuffled_score_questions' not in st.session_state:
            shuffled_questions = questions.copy()
            random.shuffle(shuffled_questions)
            st.session_state.shuffled_score_questions = shuffled_questions
        
        # 存储答案的字典
        answers = {}
        
        # 显示随机化后的问题
        for q in st.session_state.shuffled_score_questions:
            score = create_question(
                q["label"],
                q["descriptions"],
                q["key"]
            )
            answers[q["key"]] = score

        if st.button("Submit Assessment", type="primary"):
            if None not in answers.values():
                st.session_state.data_dict.update(answers)
                st.session_state.score_submitted = True
                st.success("Responses recorded successfully!")
                st.switch_page("pages/6_Survey_2_Page.py")
            else:
                st.error("Please rate all criteria before saving.")
    else:
        st.success("Responses recorded successfully!")
        if st.button("Continue to Next Section", type="primary"):
            st.switch_page("pages/6_Survey_2_Page.py")

if __name__ == "__main__":
    if 'video_finished' not in st.session_state or not st.session_state.video_finished:
        st.switch_page("pages/4_Video_Ad_Page.py")
    else:
        main()