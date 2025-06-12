import streamlit as st

# Page to record the willingness to pay for the product using the slider

def main():
    if 'survey2_submitted' not in st.session_state:
        st.session_state.survey2_submitted = False

    st.subheader("Survey 2")

# Product 	Price Range	 granularity
# Toothpaste(Colgate)   $0-8	every $0.01
# Ice Cream Tub(Breyers)  $0-10	every $0.01
# Wine(Harlan Estate)   $0-3120	every $1
# Laptop(MacBook)  $0-2890	every $1

    score_descriptions = {
        "toothpaste_willingness_to_pay": {
            'min': 0.0,
            'max': 8.0,
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
        score = st.slider(
            f"""What is your maximum willingness to pay for the product? (in USD)
            """,
            min_value=descriptions_dict['min'],
            max_value=descriptions_dict['max'],
            value=descriptions_dict['min'],
            step=descriptions_dict['granularity'],
            key=key
        )
        if score is not None:
            st.caption(f"Current choice: ${score}")
        return score
    
    if not st.session_state.survey2_submitted:
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
            key
        )
       
        
        # Submission section
        if st.button("Submit", type="primary"):
            if score is not None:
                st.session_state.data_dict['willingness_to_pay'] = score
                st.session_state.survey2_submitted = True
                st.success("Responses recorded successfully!")
                st.switch_page("pages/7_Survey_3_Page.py")
            else:
                st.error("Please complete all questions before submitting")
    else:
        st.success("Responses recorded successfully!")
        if st.button("Continue to Next Section", type="primary"):
            st.switch_page("pages/7_Survey_3_Page.py")

if __name__ == "__main__":
    if 'score_submitted' not in st.session_state or not st.session_state.score_submitted:
        st.switch_page("pages/5_Score_Video_Page.py")
    else:
        main()