import streamlit as st
import requests

st.set_page_config(page_title="Support Ticket Search", layout="centered")
st.title(" Appgallop Customer Support Assistant :mag_right:")

complaint = st.text_area("Enter new customer complaint:")

if st.button(":mag: Search Suggested Responses"):
    if complaint.strip() == "":
        st.warning("Please enter a complaint.")
    else:
        with st.spinner("Searching..."):
            try:
                # Proper POST request with JSON payload
                payload = {
                    "message": complaint,
                    "state": "initial"
                }
                # response = requests.post("http://localhost:8000/chat", json=payload)https://kb-search-app.onrender.com
                response = requests.post("http://localhost:8000/chat", json=payload)
                response.raise_for_status()  # Raise exception for non-200 errors

                response_data = response.json()
                reply = response_data.get("reply", "No reply found.")
                results = response_data.get("results", [])  # Optional - fallback for list

                st.success(":white_check_mark: Response:")
                st.markdown(f" **AG-Bot :scroll: :** {reply}")
                

                if results:
                    st.subheader(":pencil: Similar Complaints & Suggested Responses")
                    for i, res in enumerate(results, start=1):
                        st.markdown(f"**Result {i}**")
                        st.markdown("" f" **Similar Complaint:** {res['complaint']}")
                        st.markdown(":white_check_mark:" f" **Suggested Response:** {res['response']}")
                        st.markdown(f":eyes: **Similarity Score:** {res['similarity']}")
                        st.markdown("---")

            except requests.exceptions.RequestException as e:
                st.error(f":no_entry: Error connecting to backend: {e}")
            except ValueError:
                st.error(":no_entry: Failed to parse backend response.")