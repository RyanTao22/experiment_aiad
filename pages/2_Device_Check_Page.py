import streamlit as st

def main():
    #st.show(st.session_state.product
    # st.write(st.session_state)

    # Initialize test status
    if 'device_test_passed' not in st.session_state:
        st.session_state.device_test_passed = False

    st.title("Device Compatibility Test")
    st.write("To ensure a smooth experience, please check your audio and video devices before proceeding.")

    # Play test video (replace with your actual URL)
    st.video("https://kling-mp4-us.oss-us-west-1.aliyuncs.com/device_check.mp4?OSSAccessKeyId=LTAI5tGhKeyY9jJE8ncCTyfv&Expires=2103339672&Signature=iK3FIhZ31KMMFzlDbavG1cCtWhg%3D")  # Should contain beach scene
    
    st.divider()
    
    # Question 1: Video content
    scene = st.radio(
        "Which scene appears in the video?",
        options=["Forest", "Grassland", "Beach", "Snow Mountain"],
        index=None,
        key="scene_question"
    )
    
    # Question 2: Audio content
    letter = st.radio(
        "What is the second letter according to the audio?",
        options=["f", "d", "e", "p","z","m"],
        index=None,
        key="audio_question"
    )

    # Submit button
    if st.button("Submit Test Results"):
        if scene == "Beach" and letter == "z":
            st.session_state.device_test_passed = True
            st.success("✅ Device test passed!")
            # st.balloons()
            # if st.button("Begin Main Study", type="primary"):
            #     print('yes  yes')
            #     st.switch_page("pages/3_Survey_Page.py")
        else:
            st.error("❌ Test failed. Please check your devices, replay the video and try again")
            st.session_state.device_test_passed = False

    if st.session_state.device_test_passed:
        st.divider()
        if st.button("Begin Main Study", type="primary"):
            # Replace with your study flow logic
            st.switch_page("pages/3_Survey_1_Page.py")

if __name__ == "__main__":
    if 'comp_check_passed' not in st.session_state or st.session_state.comp_check_passed == False:
         st.switch_page("pages/1_Instruction_Page.py")
    else:
        main()