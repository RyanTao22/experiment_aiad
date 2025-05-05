import streamlit as st
import random

def main():
    if 'score_submitted' not in st.session_state:
        st.session_state.score_submitted = False

    st.header("Score the Advertising Videos")
    st.subheader("Please score the advertising videos you just watched.")
    
    score_descriptions = {
        1: "Very Poor",
        2: "Poor",
        3: "Below Average",
        4: "Neutral",
        5: "Above Average",
        6: "Good",
        7: "Excellent"
    }
    
    sliders = [
        {"label": "Creativity", "key": "creativity"},
        {"label": "Memorability", "key": "memorability"},
        {"label": "Effectiveness", "key": "effectiveness"},
        {"label": "Relevance", "key": "relevance"},
        {"label": "Engagement", "key": "engagement"},
        {"label": "Credibility", "key": "credibility"},
        {"label": "Satisfaction", "key": "satisfaction"},
        {"label": "Persuasiveness", "key": "persuasiveness"},
    ]
    
    if 'shuffled_sliders' not in st.session_state:
        shuffled_sliders = sliders.copy()
        random.shuffle(shuffled_sliders)
        st.session_state.shuffled_sliders = shuffled_sliders
    
    max_label_length = max(len(s["label"]) for s in st.session_state.shuffled_sliders)
    
    def create_slider(label, key):
        padding = " " * (max_label_length - len(label))
        score = st.slider(
            f"{label}:{padding} (1 = Very Poor;  4 = Neutral;  7 = Excellent)",
            min_value=1,
            max_value=7,
            value=None,
            format="%d",
            key=key
        )
        if score is not None:
            st.caption(f"{label}: Selected {score} - {score_descriptions[score]}")
        return score
    
    if not st.session_state.score_submitted:
        slider_values = {}
        for slider in st.session_state.shuffled_sliders:
            slider_values[slider["key"]] = create_slider(slider["label"], slider["key"])

        if st.button("Submit Assessment", type="primary"):
            if all(v is not None for v in slider_values.values()):
                st.session_state.data_dict.update(slider_values)
                st.session_state.score_video_complete = True
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