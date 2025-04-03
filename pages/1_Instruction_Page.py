import streamlit as st

def main():

    # Initialize session state
    if 'comp_check_passed' not in st.session_state:
        st.session_state.comp_check_passed = False
        st.session_state.attempts = 0
        st.session_state.prolific_id = ""

    # Header
    st.title("Consumer Advertising Experience Study")
    st.write("Thank you for participating in this research about digital advertising.")

    # Study information expander
    with st.expander("📋 Click to view full study instructions", expanded=True):
        st.markdown("""
        ### What You'll Do:
        1. **Take** a short survey about your demographics
        2. **Watch** a short video advertisements (1-3 minutes total)
        3. **Answer questions** about your experience and some additional topics after watching the video


        ### Important Rules:
         - Pay close attention; **Failing attention check or device check will disqualify you.**
         - Do not close the browser or skip questions during the study.
         - Refresh the page if you encounter technical issues.
         - You may withdraw at any time without penalty.

        """)

    # Comprehension check (only show if not passed)
    if not st.session_state.comp_check_passed:
        st.divider()
        st.subheader("Before you begin...")
        st.write("Please answer the following questions to continue:")

        prolific_id = st.text_input("Please enter your Unique Prolific ID:", 
                               value=st.session_state.prolific_id)
            

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
                    st.warning('You have failed to pass the Comprehension Check too many times. Thank you for your time. Please close the browser and return to Prolific.')
                    #st.warning("Your redeem code is: EFTR-9M3E-0I6T")
                    st.stop()

                if prolific_id:
                    st.session_state.prolific_id = prolific_id
                    st.session_state.comp_check_passed = True
                    st.success("✓ Correct! You may now begin the study.")
                    st.balloons()
                else:
                    st.warning("Please enter your Prolific ID to continue.")
                    #st.snow()
                #st.snow()
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts >= 2:
                    #st.warning('You have already completed the study. Please copy and keep your redeem code below, then close the browser and return to Prolific.')
                    st.warning('You have failed to pass the Comprehension Check too many times. Thank you for your time. Please close the browser and return to Prolific.')
                    #st.warning("Your redeem code is: EFTR-9M3E-0I6T")
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