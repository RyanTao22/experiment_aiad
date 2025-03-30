import streamlit as st

def main():
    # st.print(st.session_state)
    # st.write(st.session_state)
    # Page setup
    # st.set_page_config(
    #     page_title="Advertisement Study",
    #     page_icon="📺",
    #     layout="centered"
    # )

    # Initialize session state
    if 'comp_check_passed' not in st.session_state:
        st.session_state.comp_check_passed = False
        st.session_state.attempts = 0

    # Header
    st.title("Consumer Advertising Experience Study")
    st.write("Thank you for participating in this research about digital advertising.")

    # Study information expander
    with st.expander("📋 Click to view full study instructions", expanded=True):
        st.markdown("""
        ### What You'll Do:
        1. **Take** a short survey about your demographics
        2. **Watch** a short video advertisements (1-3 minutes total)
        3. **Answer questions** about your experience after each video


        ### Important Rules:
        - Pay close attention to all content and do not skip any questions
        - If you meet any technical issues, please refresh the page to restart the study
        - Do not close the browser during the study
        - You may withdraw anytime without penalty

        """)

    # Comprehension check (only show if not passed)
    if not st.session_state.comp_check_passed:
        st.divider()
        st.subheader("Before you begin...")
        st.write("Please answer this question to continue:")

        answer = st.radio(
            "What is your main task after watching each video?",
            options=[
                "Skip the questions and move to the next video",
                "Answer questions about the video you just watched",
                "Share your opinion on social media"
            ],
            index=None
        )

        if st.button("Submit Answer"):
            if answer == "Answer questions about the video you just watched":
                if st.session_state.attempts >= 2:
                    st.error("""
                    ❌ Thank you for your time. 
                    Please return this study on Prolific by clicking 'Stop Without Completing'.
                    """)
                    st.stop()

                st.session_state.comp_check_passed = True
                st.success("✓ Correct! You may now begin the study.")
                st.balloons()
                #st.snow()
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts >= 2:
                    st.error("""
                    ❌ Thank you for your time. 
                    Please return this study on Prolific by clicking 'Stop Without Completing'.
                    """)
                    st.stop()
                else:
                    st.warning("Incorrect answer. Please review the instructions and try again.")

    # Continue button (only shows after passing)
    if st.session_state.comp_check_passed:
        st.divider()
        if st.button("Let's Go!", type="primary"):
            # Replace with your study flow logic
            st.switch_page("pages/2_Device_Check_Page.py")  

if __name__ == "__main__":
    main()