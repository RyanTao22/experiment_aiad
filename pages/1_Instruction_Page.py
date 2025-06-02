import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import ast

def assign_user_to_group(engine):
   
    with engine.begin() as conn:
        # find the group with the least number of users and the earliest last_update_timestamp
        query = text("""
        SELECT test_group_name, filter_fields, excel_team, product FROM group_counts 
        WHERE is_done = FALSE
        ORDER BY current_count ASC, last_update_timestamp ASC 
        LIMIT 1
        """)
        
        result = conn.execute(query).fetchone()
        
        if result:
            test_group_name = result[0]
            filter_fields = result[1]
            excel_team = result[2]
            product = result[3]

            # update the timestamp
            update_query = text("""
            UPDATE group_counts 
            SET last_update_timestamp = NOW()
            WHERE product = :product AND test_group_name = :test_group_name
            """)
            
            conn.execute(update_query, {
                "product": product, 
                "test_group_name": test_group_name
            })
            
            return product, test_group_name, excel_team, filter_fields
        else:
            # if all groups are completed, return None
            return None, None, None, None

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

        prolific_id = st.text_input("Please enter your Unique Prolific ID, then press Enter to apply:", 
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
            if prolific_id:
                # 检查prolific_id是否在db_check_user表中
                engine = create_engine(f'mysql+pymysql://{st.secrets["username"]}:{st.secrets["password"]}@{st.secrets["db_url"]}:{st.secrets["port"]}/{st.secrets["database"]}?charset=utf8mb4')
                with engine.connect() as conn:
                    query = text(f"SELECT reason FROM {st.secrets['db_check_user']} WHERE prolific_id = :prolific_id")
                    result = conn.execute(query, {"prolific_id": prolific_id}).fetchone()
                    
                    if result:
                        reason = result[0]
                        reason_text = {
                            'comprehension_check': 'failed to pass the Comprehension Check too many times',
                            'device_check': 'failed to pass the Device Check too many times',
                            'attention_check': 'failed to pass the Attention Check too many times',
                            'completed the study': 'have completed the study already',
                        }.get(reason, 'failed to meet the study requirements')
                        
                        st.error(f"This Prolific ID has been disqualified from the study because you {reason_text}. Please close the browser and return to Prolific.")
                        st.stop()

                if answer == "Answer questions about the video you just watched":
                    if st.session_state.attempts >= 2:
                        # 记录失败状态到数据库
                        with engine.begin() as conn:
                            df = pd.DataFrame([{
                                'prolific_id': prolific_id,
                                'status': 'failed',
                                'reason': 'comprehension_check'
                            }])
                            df.to_sql(name=st.secrets["db_check_user"], con=conn, if_exists='append', index=False)
                        
                        st.warning('You have failed to pass the Comprehension Check too many times. Thank you for your time. Please close the browser and return to Prolific.')
                        st.stop()

                    st.session_state.prolific_id = prolific_id
                    st.session_state.comp_check_passed = True
                    
                    # assign user to the group
                    product, test_group_name, excel_team, filter_fields = assign_user_to_group(engine)
            
                    if test_group_name is None:
                        st.error("According to our dataset, the experiment quote is full. We are sorry for the inconvenience. Please close the browser and return to Prolific.")
                        st.stop()
                    
                    # store the group information to session state
                    st.session_state.product = product
                    st.session_state.test_group = test_group_name
                    st.session_state.excel_team = excel_team
                    st.session_state.filter_fields = ast.literal_eval(filter_fields) if filter_fields else []
                    
                    # display the allocation result (optional, for debugging)
                    print(f"DEBUG: User {prolific_id} have been assigned to the experiment group: {test_group_name}")

                    st.success("✓ Correct! You may now begin the study.")
                    st.balloons()
                else:
                    st.session_state.attempts += 1
                    if st.session_state.attempts >= 2:
                        # 记录失败状态到数据库
                        with engine.begin() as conn:
                            df = pd.DataFrame([{
                                'prolific_id': prolific_id,
                                'status': 'failed',
                                'reason': 'comprehension_check'
                            }])
                            df.to_sql(name=st.secrets["db_check_user"], con=conn, if_exists='append', index=False)
                        
                        st.warning('You have failed to pass the Comprehension Check too many times. Thank you for your time. Please close the browser and return to Prolific.')
                        st.stop()
                    else:
                        st.warning("Incorrect answer. Please review the instructions and try again.")
            else:
                st.warning("Please enter your Prolific ID to continue.")

    # Continue button (only shows after passing)
    if st.session_state.comp_check_passed:
        st.divider()
        if st.button("Let's Go!", type="primary"):
            st.switch_page("pages/2_Device_Check_Page.py")

if __name__ == "__main__":
    main()  