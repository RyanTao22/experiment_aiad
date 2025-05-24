import streamlit as st
import datetime
import pytz
import pandas as pd
import ast
import time
from sqlalchemy import create_engine
#from helpers import add_row_to_responses_df, initialize_responses_df

if 'product' not in st.session_state:
    st.session_state.product = 'Ice Cream Tub(Breyers)'
    print('product not in session state')
if 'test_group' not in st.session_state:
    st.session_state.test_group = 'A23_icecream_partly_demo_income'
    st.session_state.excel_team = 'Condition_3_one_var'
    # test_group = 'A2_icecream_one_demo'
    # test_group = 'A3_icecream_no_demo'
    # test_group = 'A4_icecream_human_ad'

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
                    engine = create_engine(f'mysql+pymysql://{st.secrets["username"]}:{st.secrets["password"]}@{st.secrets["db_url"]}:{st.secrets["port"]}/{st.secrets["database"]}?charset=utf8mb4')
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
                
                df = pd.read_excel('data/ad_ts_refine_script_df_250203.xlsx')
                mask = (
                    (df['team'] == st.session_state.excel_team) &
                    # (df['Age_Range'] == age)
                    #  (df['Gender'] == gender)
                    (df['Household_Income'] == income)
                    # (df['Ethnicity'] == ethnicity) &
                    # (df['product'] == st.session_state.product)
                )
                sids = df.loc[mask, 'sid'].tolist()
                print(sids)
                if len(sids) > 0:
                    sid = int(sids[0])
                    prompt = df.loc[df['sid'] == sid, 'prompt'].values[0]
                    script = df.loc[df['sid'] == sid, 'refine_script'].values[0]

                    video_df = pd.read_excel('data/bgm_combined_results_df_250203_part1.xlsx')
                    video_df['sid'] = video_df['sid'].astype(int)
                    video_df['narrator_start_timestamps'] = video_df['narrator_start_timestamps'].apply(ast.literal_eval)
                    video_df['narrator_durations'] = video_df['narrator_durations'].apply(ast.literal_eval)

                    video_url = video_df.loc[video_df['sid'] == sid, 'bgm_url'].values[0]
                    video_time = video_df.loc[video_df['sid'] == sid, 'narrator_start_timestamps'].values[0][-1] + video_df.loc[video_df['sid'] == sid, 'narrator_durations'].values[0][-1]
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
                    engine = create_engine(f'mysql+pymysql://{st.secrets["username"]}:{st.secrets["password"]}@{st.secrets["db_url"]}:{st.secrets["port"]}/{st.secrets["database"]}?charset=utf8mb4')
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