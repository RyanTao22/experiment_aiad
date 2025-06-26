import streamlit as st

# Sidebar navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", ["Instructions","Device Check","Survey 1", "Video", "Score the Video","Survey 2","Survey 3"], key='page')





if page_selection == "Instructions":          st.switch_page("pages/1_Instruction_Page.py")
elif page_selection == "Device Check":
    if st.session_state.comp_check_passed:    st.switch_page("pages/2_Device_Check_Page.py")
    else: st.warning("Please complete the instructions first")
elif page_selection == "Survey 1":
    if st.session_state.device_test_passed:   st.switch_page("pages/3_Survey_1_Page.py")
    else: st.warning("Please complete the device check first")
elif page_selection == "Video":
    if st.session_state.survey_1_complete:    st.switch_page("pages/4_Video_Ad_Page.py")
    else: st.warning("Please complete the demographics survey first")
elif page_selection == "Score the Video":
    if st.session_state.video_finished:       st.switch_page("pages/5_Score_Video_Page.py")
    else: st.warning("Please complete the survey and watch the video first")
elif page_selection == "Survey 2":
    if st.session_state.score_submitted: st.switch_page("pages/6_Survey_2_Page.py")
    else: st.warning("Please complete the device check first")
elif page_selection == "Survey 3":
    if st.session_state.survey2_submitted:    st.switch_page("pages/7_Survey_3_Page.py")
    else: st.warning("Please complete the survey 2 first")


