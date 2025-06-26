import streamlit as st
import datetime
import pytz
import pandas as pd
import time
import random
from app_utils import fetch_video_detail, fetch_candidate_ads
from app_utils import get_engine

def main():
    # st.write(st.session_state)

    if 'survey_complete' not in st.session_state:
        st.session_state.survey_complete = False
        st.session_state.attn3_attempts = 0
        

    st.subheader("Survey 1 (5 questions)")

    age = st.radio("Your Age Range", ['18-24', '25-44', '45-64', '65+'],index=None)
    gender = st.radio("Your Gender", ['Male', 'Female', 'Non-binary / Third gender'],index=None)
    attn3 = st.radio( "I commute to work by swimming across the Atlantic Ocean every day.",[ "Agree", "So do I", "Disagree", "Not sure"],index=None)
    income = st.radio("Your Household Income Range Before Taxes During the Past 12 Months (US Dollar)", ['<25,000', '25,000 - 150,000', '150,000+'],index=None)
    ethnicity = st.radio("Your Ethnicity", ['American Indian and Alaska Native', 'Asian', 'Black or African American', 
                  'Native Hawaiian and Other Pacific Islander', 'White', 'Multiracial/Mixed ethnicity'],index=None)

    # Privacy and Ethics Questions
 
    if st.button("Submit Results", type="primary"):
        all_rated = True
        for metric in [attn3,age,gender,income,ethnicity]:
            if metric == None:
                all_rated = False
                break
        
        if not all_rated:
            st.error("Please answer all questions before saving.") 
        else:
        # Validate attention check
            if attn3 in ["Disagree"]:
                if st.session_state.attn3_attempts >= 2:
                    # 记录失败状态到数据库
                    engine = get_engine()
                    with engine.begin() as conn:
                        df = pd.DataFrame([{
                            'prolific_id': st.session_state.prolific_id,
                            'status': 'failed',
                            'reason': 'attention_check'
                        }])
                        df.to_sql(name=st.secrets["db_check_user"], con=conn, if_exists='append', index=False)
                    
                    st.warning('You have failed to pass the Attention Check too many times. Thank you for your time. Please close the browser and return to Prolific.')
                    st.stop()
                
                LA_time = datetime.datetime.now(pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S')
                
                # 动态查询数据库获取满足条件的记录，避免在 Python 端过滤
                filters = {
                    'Age_Range': age,
                    'Gender': gender,
                    'Household_Income': income,
                    'Ethnicity': ethnicity,
                }
                if hasattr(st.session_state, 'filter_fields'):
                    # 只保留需要的过滤项
                    filters = {k: v for k, v in filters.items() if k in st.session_state.filter_fields}

                df_candidates = fetch_candidate_ads(st.session_state.excel_team, st.session_state.product, filters)

                sids = df_candidates['sid'].tolist()
                print(sids)
                if len(sids) > 0:
                    
                    if st.session_state.excel_team == 'Condition_1':
                        # for human ad group only
                        sid = int(random.choice(sids))
                    else:
                        # for other groups
                        sid = int(sids[0])
                    
                    prompt = df_candidates.loc[df_candidates['sid'] == sid, 'prompt'].values[0]
                    script = df_candidates.loc[df_candidates['sid'] == sid, 'refine_script'].values[0]

                    video_row = fetch_video_detail(sid)
                    video_url = video_row['bgm_url']
                    video_time = video_row['narrator_start_timestamps'][-1] + video_row['narrator_durations'][-1]
                else:
                    st.error("""
                            ❌ Please answer all the quesions to complete the survey.
                            """)
                

                data_dict =  {
                        'Timestamp_LA': LA_time,
                        'Test_Group': st.session_state.test_group,
                        'Age_Range': age,
                        'Gender': gender,
                        'Household_Income': income,
                        'Ethnicity': ethnicity,
                        "Prompt": prompt,
                        "Script": script,
                        "Video_url": video_url,
                        "Video_time": video_time,
                        "Prolific_ID": st.session_state.prolific_id,
                    }
                

                #add_row_to_responses_df(row_data)
                st.session_state.data_dict = data_dict
                st.session_state.survey_complete = True
                
                st.switch_page("pages/4_Video_Ad_Page.py")
            else:
                st.session_state.attn3_attempts += 1
                if st.session_state.attn3_attempts >= 2:
                    # 记录失败状态到数据库
                    engine = get_engine()
                    with engine.begin() as conn:
                        df = pd.DataFrame([{
                            'prolific_id': st.session_state.prolific_id,
                            'status': 'failed',
                            'reason': 'attention_check'
                        }])
                        df.to_sql(name=st.secrets["db_check_user"], con=conn, if_exists='append', index=False)
                    
                    st.warning('You have failed to pass the Attention Check too many times. Thank you for your time. Please close the browser and return to Prolific.')
                    st.stop()
                else:
                    st.error("Incorrect answer detected. Please review all of your answers and try again.")
                    # time.sleep(2.5)
                    # st.rerun()  
                    
                    #st.rerun()

            
    

if __name__ == "__main__":
    if 'device_test_passed' not in st.session_state :#
        st.switch_page("pages/2_Device_Check_Page.py")
    else:
        main()