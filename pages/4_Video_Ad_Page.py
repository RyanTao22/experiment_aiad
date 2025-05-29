import streamlit as st
import pandas as pd
import time

def main():
    # st.write(st.session_state)
    
    # Initialize timer in session state if not present
    
    if 'video_finished' not in st.session_state:
        st.session_state.video_finished = None
    if 'watching_video' not in st.session_state:
        st.session_state.watching_video = False

    st.warning("Please confirm your device is working properly and you will watch the entire video ad with sound.")
    if st.button("Click Here to Confirm - I will watch the complete video ad with sound"):
        st.session_state.page_load_time = time.time()
        st.video(st.session_state.data_dict["Video_url"])
        st.session_state.watching_video = True

    if st.session_state.watching_video:
        if st.button("Click Here when you have finished watching the complete video with sound", type="primary"):
            st.session_state.user_time_spent = time.time() - st.session_state.page_load_time
            if st.session_state.user_time_spent >= st.session_state.data_dict["Video_time"]-2:
                st.session_state.video_finished = True
                st.switch_page("pages/5_Score_Video_Page.py")
            else:
                st.session_state.video_finished = False
                st.error("You haven't watched the video long enough. Please click the button 'I confirm - I will watch the complete video with sound' to watch the complete video again before proceeding.")

    # if st.session_state.video_finished == True:
    #     if st.button("Continue to Next Section", type="primary"):
            
    #         st.switch_page("pages/5_Score_Video_Page.py")
    # elif st.session_state.video_finished == False:
    #     st.warning("Please complete all steps: confirm your device is working, play the video, and watch it completely with sound.")
    #     st.session_state.video_finished = None

if __name__ == "__main__":
    if 'survey_complete' not in st.session_state or not st.session_state.survey_complete:
        st.switch_page("pages/3_Survey_1_Page.py")
    else:
        main()