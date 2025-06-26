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
    if 'willingness_to_pay_submitted' not in st.session_state:
        st.session_state.willingness_to_pay_submitted = False


    score_descriptions = {
        "toothpaste_willingness_to_pay": {
            'min': 0.0,
            'max': 10.0,
            'granularity': 0.01
        },
        "ice_cream_tub_willingness_to_pay": {
            'min': 0.0,
            'max': 10.0,
            'granularity': 0.01
        },
        "wine_willingness_to_pay": {
            'min': 0,
            'max': 3000,
            'granularity': 1
        },
        "laptop_willingness_to_pay": {
            'min': 0,
            'max': 3000,
            'granularity': 1
        }
    }
    
    def create_question(descriptions_dict, key):
        st.divider()
        score = st.slider(
            f"""What is your maximum willingness to pay for the product? (in USD)
            """,
            min_value=descriptions_dict['min'],
            max_value=descriptions_dict['max'],
            value=None,
            step=descriptions_dict['granularity'],
            key=key
        )
        if score is not None:
            st.caption(f"Current choice: ${score}")
        return score

    

    st.warning("Please confirm your device is working properly and you will watch the entire video ad with sound.")
    if st.button("Click Here to Confirm - I will watch the complete video ad with sound"):
        st.session_state.page_load_time = time.time()
        st.session_state.watching_video = True  # 标记开始观看
        st.session_state.video_finished = False  # 重置完成标志

    if st.session_state.watching_video:
        # 始终展示视频窗口
        st.video(st.session_state.data_dict["Video_url"])

        # 尚未通过时长校验 -> 显示完成按钮
        if not st.session_state.video_finished:
            if st.button("Click Here when you have finished watching the complete video with sound", type="primary"):
                st.session_state.user_time_spent = time.time() - st.session_state.page_load_time

                # 若观看时长足够，标记为已完成；否则提示重新观看
                if st.session_state.user_time_spent >= st.session_state.data_dict["Video_time"] * 0.9:
                    st.session_state.video_finished = True
                else:
                    st.error("You haven't watched the video long enough. Please click the button 'I confirm - I will watch the complete video with sound' to watch the complete video again before proceeding.")

        # 已通过时长校验 -> 隐藏按钮，显示 slider
        if st.session_state.video_finished and not st.session_state.willingness_to_pay_submitted:
            if st.session_state.product == "Toothpaste(Colgate)":
                key = "toothpaste_willingness_to_pay"
            elif st.session_state.product == "Ice Cream Tub(Breyers)":
                key = "ice_cream_tub_willingness_to_pay"
            elif st.session_state.product == "Wine(Harlan Estate)":
                key = "wine_willingness_to_pay"
            elif st.session_state.product == "Laptop(MacBook)":
                key = "laptop_willingness_to_pay"

            

            score = create_question(
                score_descriptions[key],
                key)

            # 提交按钮区域
            st.divider()
            _, _, _, col_mid, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])
            with col_mid:
                if st.button("Submit", type="primary"):
                    if score is not None:
                        st.session_state.data_dict['willingness_to_pay'] = score
                        st.session_state.willingness_to_pay_submitted = True
                        st.switch_page("pages/5_Score_Video_Page.py")
                    else:
                        st.error("Please complete the question before submitting")
        else:
            st.success("Responses recorded successfully!")
            if st.button("Continue to Next Section", type="primary"):
                st.switch_page("pages/5_Score_Video_Page.py")

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