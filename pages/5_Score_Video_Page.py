import streamlit as st

def main():
    st.header("Score the Advertising Videos")
    st.subheader("Please score the advertising videos you just watched.")
    #st.subheader("(1 = Lowest, 10 = Highest)")  

    

    satisfaction = st.radio("Satisfaction (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    accuracy = st.radio("Accuracy (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    persuasiveness = st.radio("Persuasiveness (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    credibility = st.radio("Credibility (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    engagement = st.radio("Engagement (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    relevance = st.radio("Relevance (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    creativity = st.radio("Creativity (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    memorability = st.radio("Memorability (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)
    effectiveness = st.radio("Effectiveness (1 = Lowest, 10 = Highest)", options=list(range(1, 11)), horizontal=True,index=None)

    if st.button("Save"):
        all_rated = True
        for metric in [satisfaction, accuracy, persuasiveness, credibility,
                     engagement, relevance, creativity, memorability, effectiveness]:
            if metric == None:
                all_rated = False
                break
        if not all_rated:
            st.error("Please rate all criteria before saving.") 
        else:
            st.session_state.data_dict['satisfaction'] = satisfaction
            st.session_state.data_dict['accuracy'] = accuracy
            st.session_state.data_dict['persuasiveness'] = persuasiveness
            st.session_state.data_dict['credibility'] = credibility 
            st.session_state.data_dict['engagement'] = engagement
            st.session_state.data_dict['relevance'] = relevance
            st.session_state.data_dict['creativity'] = creativity
            st.session_state.data_dict['memorability'] = memorability
            st.session_state.data_dict['effectiveness'] = effectiveness

            st.session_state.score_video_complete = True
           
            st.switch_page("pages/6_Survey_2_Page.py")

if __name__ == "__main__":
    if 'video_finished' not in st.session_state or not st.session_state.video_finished:
        st.switch_page("pages/4_Video_Ad_Page.py")
    else:
        main()