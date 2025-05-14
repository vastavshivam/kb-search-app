import streamlit as st
import requests


st.set_page_config(page_title="Appgallop Support Ticket Search", layout="centered")
st.title("Appgallop Customer Support Assistant :mag_right:")

complaint = st.text_area("Enter new customer complaint:")
print("================comaplaint " + complaint)

if st.button(":mag: Search Suggested Responses"):
    if complaint.strip() == "":
        st.warning("Please enter a complaint.")
    else:
        with st.spinner("Searching..."):
            try:
                payload = {
                    "message": complaint,
                    "state": "initial"
                }
                # response = requests.post("http://localhost:8000/chat", json=payload)
                response = requests.post("https://kb-search-app.onrender.com/chat", json=payload)
                response.raise_for_status()

                response_data = response.json()
                reply = response_data.get("reply", "No reply found.")
                results = response_data.get("results", [])

                st.success(":white_check_mark: Response:")
                st.markdown(f" **AG-Bot :scroll: :** {reply}")

                if results:                   
                    st.subheader(":pencil: Similar Complaints & Suggested Responses")
                    for i, res in enumerate(results, start=1):
                        
                        st.markdown(f"**Result {i}**")
                        st.markdown(f"**Similar Complaint:** {res['complaint']}")
                        st.markdown(f":white_check_mark: **Suggested Response:** {res['response']}")
                        st.markdown(f":eyes: **Similarity Score:** {res['similarity']}")

                        col1, col2 = st.columns([1, 1])
                        # print(col1, col2)
                        with col1:
                            st.write(f"Button Useful {i} clicked!")                            
                            if st.button(":thumbsup:", key=f"useful_{i}"):
                                st.write(f"Button Useful {i} clicked!")
                                # st.markdown("You clicked the Material button.")
                                # print(f"Feedback: Useful for result {i}")
                                # st.success(f"Thanks for your positive feedback on Result {i}!")
                                # send_feedback(res, True)
                        with col2:  
                            if st.button(f":thumbsdown: {i}"):
                                # send_feedback(res, False)  # False = Thumbs Down
                                st.info("Thanks! We'll use your feedback to improve.")

                        st.markdown("---")
                        

            except requests.exceptions.RequestException as e:
                st.error(f":no_entry: Error connecting to backend: {e}")
            except ValueError:
                st.error(":no_entry: Failed to parse backend response.")
