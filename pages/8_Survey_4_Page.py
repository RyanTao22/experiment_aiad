import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import time
import random

def update_group_completion(conn, product, test_group_name):
    # update the group completion count and timestamp, check if the group is completed
    update_query = text("""
    UPDATE group_counts 
    SET current_count = current_count + 1,
        is_done = CASE WHEN current_count + 1 >= max_count THEN TRUE ELSE FALSE END,
        last_update_timestamp = NOW()
    WHERE product = :product AND test_group_name = :test_group_name
    """)
    
    conn.execute(update_query, {
        "product": product, 
        "test_group_name": test_group_name
    })

def main():
    if 'attn_attempts' not in st.session_state:
        st.session_state.attn_attempts = 0
        st.session_state.survey_4_submitted = False

    # 定义问题和选项
    questions_part1 = [
        {
            "question": "If using an algorithm, can the results be biased against specific groups of people?",
            "options": [
                "No, unlike humans, algorithms are free of emotions and cannot be wrong",
                "Yes, but only if you train them on privileged populations",
                "Yes, but only if you use them with incomplete data",
                "Yes, even with correct data and training, algorithms can provide biased results"
            ],
            "key": "q1_7"
        },
        {
            "question": "What information do social media algorithms not typically use when deciding what information to display to a person?",
            "options": [
                "Articles people have previously clicked on",
                "Videos people have previously watched online",
                "Information people have shared on social media",
                "What would benefit society"
            ],
            "key": "q1_14"
        },
        {
            "question": "To confirm you are paying attention, please select 'Strongly disagree' for this statement.",
            "options": [
                "Strongly agree",
                "Agree",
                "Neutral",
                "Strongly disagree" 
            ],
            "key": "attn1"
        },
        {
            "question": "Who is primarily responsible for the ethical considerations of an AI system?",
            "options": [
                "The AI system itself",
                "Data providers",
                "Human developers",
                "End-users"
            ],
            "key": "q2_10"
        },
        {
            "question": "Which is a key ethical issue surrounding AI?",
            "options": [
                "Algorithmic efficiency",
                "CPU usage",
                "Privacy",
                "Code readability"
            ],
            "key": "q2_16"
        },
        {
            "question": "Which technology allows multiple parties to collaboratively train an AI model without sharing users' raw data, thereby protecting data privacy?",
            "options": [
                "Supervised Learning",
                "Ensemble Learning",
                "Federated Learning",
                "Reinforcement Learning"
            ],
            "key": "ryan1_1"
        },
        {
            "question": "An important measure for AI governance and regulation is:",
            "options": [
                "Relying entirely on corporate self-regulation without external oversight",
                "Prohibiting any use of user data in AI applications",
                "Conducting algorithmic audits and enhancing transparency for high-risk AI systems",
                "Requiring all AI algorithm details to be kept absolutely secret from the public"
            ],
            "key": "ryan1_2"
        },
        {
            "question": "What is a potential misuse risk of open-source large AI models?",
            "options": [
                "Allowing commercial companies to use them freely, undermining original developers' rights",
                "Models being used to generate misinformation or harmful content due to lack of usage restrictions",
                "Limited adoption due to non-user-friendly interfaces",
                "Low algorithm transparency prevents independent safety reviews"
            ],
            "key": "ryan1_3"
        },
        {
            "question": "After data anonymization, does privacy leakage risk still exist?",
            "options": [
                "Risk exists only if data includes high-precision geolocation or biometric information",
                "Yes, anonymized data can still be re-identified by combining with other datasets",
                "No, anonymization removes all personal identifiers",
                "No, laws explicitly state anonymized data cannot be traced"
            ],
            "key": "ryan1_4"
        }
    ]

    questions_part2 = [
        {
            "question": "Which mechanism enables Transformer models to solve the long-range dependency problem in traditional RNNs?",
            "options": [
                "Genetic Algorithms",
                "Self-attention Mechanism",
                "Long Short-Term Memory (LSTM) Units",
                "Convolutional Kernels"
            ],
            "key": "ryan2_1"
        },
        {
            "question": "What technical principle does current text-to-image models like DALL-E 2 and Stable Diffusion primarily use?",
            "options": [
                "Generative Adversarial Networks (GANs)",
                "Ensemble Learning",
                "Diffusion Models",
                "Reinforcement Learning"
            ],
            "key": "ryan2_2"
        },
        {
            "question": "Which open-source platform shares pretrained models and NLP tools?",
            "options": [
                "Apache Spark",
                "Hugging Face",
                "TensorFlow",
                "Kaggle"
            ],
            "key": "ryan2_3"
        },
        {
            "question": "With sufficient data, what typically occurs when a deep learning model's parameters increase significantly (e.g., from 100M to 10B)?",
            "options": [
                "Reduced computational resources and storage requirements",
                "Lower demands for testing data quality",
                "Potentially significant improvements in model expressiveness and generalization",
                "Elimination of the need for regularization"
            ],
            "key": "ryan2_4"
        },
        {
            "question": "According to the following instruction, what should you select here? Choose 'Green'.",
            "options": [
                "Red",
                "Green", 
                "Blue"
            ],
            "key": "attn2"
        },
        {
            "question": "Which technology is the primary enabler of Artificial Intelligence?",
            "options": [
                "Electric Battery",
                "Machine Learning",
                "Robotics",
                "Engineering"
            ],
            "key": "q1_2"
        },
        {
            "question": "What is training data and why is it important?",
            "options": [
                "Training data is used when the model is fully calibrated, to train new users with how to work with the model",
                "Training data is used to calibrate the model during creation, creating a model that performs best according to that data",
                "Training data is used to test the model after it was created, to see how it works with new data",
                "Training data is used to minimize bias in older models and train them to new population types"
            ],
            "key": "q1_19"
        },
        {
            "question": "Which of the following is NOT powered by AI?",
            "options": [
                "Self-driving cars",
                "Google's search algorithm",
                "A basic calculator",
                "Chatbots"
            ],
            "key": "q2_1"
        },
        {
            "question": "What is the first step in a typical machine learning process?",
            "options": [
                "Data collection",
                "Model selection",
                "Prediction",
                "Model evaluation"
            ],
            "key": "q2_9"
        }
    ]

    # 只在第一次运行时打乱问题和选项顺序
    if 'shuffled_questions_part1' not in st.session_state:
        shuffled_part1 = questions_part1.copy()
        random.shuffle(shuffled_part1)
        for q in shuffled_part1:
            random.shuffle(q["options"])
        st.session_state.shuffled_questions_part1 = shuffled_part1
        
        shuffled_part2 = questions_part2.copy()
        random.shuffle(shuffled_part2)
        for q in shuffled_part2:
            random.shuffle(q["options"])
        st.session_state.shuffled_questions_part2 = shuffled_part2

    st.subheader("Survey 4 - Part 1 (9 questions)")
    st.info("Please answer the questions based on your current understanding. If unsure, give your best estimate rather than searching for answers or using any tools for the answers. ")
    answers_part1 = {}
    for question in st.session_state.shuffled_questions_part1:
        answer = st.radio(
            question["question"],
            question["options"],
            index=None,
            key=question["key"]
        )
        answers_part1[question["key"]] = answer

    st.divider()

    st.subheader("Survey 4 - Part 2 (9 questions)")
    st.info("Please answer the questions based on your current understanding. If unsure, give your best estimate rather than searching for answers or using any tools for the answers. ")
    answers_part2 = {}
    for question in st.session_state.shuffled_questions_part2:
        answer = st.radio(
            question["question"],
            question["options"],
            index=None,
            key=question["key"]
        )
        answers_part2[question["key"]] = answer

    if st.button("Submit to Complete the Study", type="primary"):
        all_answers = {**answers_part1, **answers_part2}
        all_rated = all(v is not None for v in all_answers.values())
        
        if not all_rated:
            st.error("Please answer all questions before saving.") 
        else:
            if all_answers["attn1"] == "Strongly disagree" and all_answers["attn2"] == "Green":  
                if st.session_state.attn_attempts >= 2:  
                    st.warning('You have failed to pass the Attention Checks. Thank you for your time. Please close the browser and return to Prolific.')
                    st.stop()
                
                st.session_state.data_dict['table1_7'] = all_answers["q1_7"]
                st.session_state.data_dict['table1_14'] = all_answers["q1_14"]
                st.session_state.data_dict['table2_10'] = all_answers["q2_10"]
                st.session_state.data_dict['table2_16'] = all_answers["q2_16"]
                st.session_state.data_dict['table1_2'] = all_answers["q1_2"]
                st.session_state.data_dict['table1_19'] = all_answers["q1_19"]
                st.session_state.data_dict['table2_1'] = all_answers["q2_1"]
                st.session_state.data_dict['table2_9'] = all_answers["q2_9"]
                
                st.session_state.data_dict['ryan1_1'] = all_answers["ryan1_1"]
                st.session_state.data_dict['ryan1_2'] = all_answers["ryan1_2"]
                st.session_state.data_dict['ryan1_3'] = all_answers["ryan1_3"]
                st.session_state.data_dict['ryan1_4'] = all_answers["ryan1_4"]
                st.session_state.data_dict['ryan2_1'] = all_answers["ryan2_1"]
                st.session_state.data_dict['ryan2_2'] = all_answers["ryan2_2"]
                st.session_state.data_dict['ryan2_3'] = all_answers["ryan2_3"]
                st.session_state.data_dict['ryan2_4'] = all_answers["ryan2_4"]

                if not st.session_state.survey_4_submitted:
                    engine = create_engine(f'mysql+pymysql://{st.secrets["username"]}:{st.secrets["password"]}@{st.secrets["db_url"]}:{st.secrets["port"]}/{st.secrets["database"]}?charset=utf8mb4')
                    with engine.begin() as conn:
                        df = pd.DataFrame.from_dict([st.session_state.data_dict])
                        df.to_sql(name=st.secrets["db_table"], con=conn, if_exists='append', index=False)

                        df_user = pd.DataFrame([{
                                'prolific_id': st.session_state.prolific_id,
                                'status': 'completed',
                                'reason': 'completed the study'
                            }])
                        df_user.to_sql(name=st.secrets["db_check_user"], con=conn, if_exists='append', index=False)
                    
                        # update the group completion count and timestamp(only when the study is completed)
                        update_group_completion(conn, st.session_state.product, st.session_state.test_group)
                    
                    st.session_state.survey_4_submitted = True
                    print('submitted')

                
                st.success('Study completed successfully! Please click the link below to return to Prolific and finalize your submission, then close this browser.')
                st.success(f"Completion URL: {st.secrets['completion_url']}")
                st.balloons()
                st.stop()
            else:
                st.session_state.attn_attempts += 1
                if st.session_state.attn_attempts >= 2: 
                    st.warning('You have failed to pass the Attention Checks. Thank you for your time. Please close the browser and return to Prolific.')
                    st.stop()
                else:
                    st.error("Incorrect answer/answers detected. Please review all of your answers and try again.")

if __name__ == "__main__":
    if 'survey3_submitted' not in st.session_state or not st.session_state.survey3_submitted:
        st.switch_page("pages/7_Survey_3_Page.py")
    else:
        main()