import streamlit as st
import pandas as pd
from PIL import Image
import os

# Ensure the "photos" directory exists
if not os.path.exists("photos"):
    os.makedirs("photos")

# Function to load the CSV file into a DataFrame
def load_data(csv_file):
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=[
            "Full Name", "Nickname", "Age", "Date of Birth", "Gender", "Ethnicity", "Nationality",
            "Height", "Weight", "Eye Color", "Hair Color", "Hair Style", "Distinguishing Marks",
            "Tattoos/Scars", "Clothing Last Seen Wearing", "Last Seen Location", "Date Last Seen",
            "Time Last Seen", "Circumstances", "Reporter's Name", "Relationship", "Phone Number",
            "Email Address", "Alternate Contact", "Medical Conditions", "Languages Spoken",
            "Habits/Behavior", "Other Info", "Photo"
        ])

# Function to save data to CSV
def save_data(csv_file, data):
    data.to_csv(csv_file, index=False)

# Load existing data
csv_file = "filtered_lost_persons.csv"
data = load_data(csv_file)

# Sidebar navigation
st.sidebar.title("Home")
page = st.sidebar.radio("Go to", ["Report Lost Person", "View Lost People"])

if page == "Report Lost Person":
    st.title("Lost Person Reporting Form")

    st.markdown("""
    <style>
    .reporting-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .reporting-section h2 {
        color: #003366;
    }
    .reporting-section label {
        font-weight: bold;
        color: #003366;
    }
    </style>
    """, unsafe_allow_html=True)

    def form_section(title):
        st.markdown(f'<div class="reporting-section"><h2>{title}</h2>', unsafe_allow_html=True)

    def end_form_section():
        st.markdown('</div>', unsafe_allow_html=True)

    form_section("1. Basic Information")
    full_name = st.text_input("Full Name of Lost Person")
    nickname = st.text_input("Nickname/Alias (if any)")
    age = st.number_input("Age", min_value=0)
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])
    ethnicity = st.text_input("Ethnicity")
    nationality = st.text_input("Nationality")
    end_form_section()

    form_section("2. Physical Description")
    height = st.text_input("Height")
    weight = st.text_input("Weight")
    eye_color = st.selectbox("Eye Color", ["Brown", "Blue", "Green", "Hazel", "Gray", "Other"])
    hair_color = st.selectbox("Hair Color", ["Black", "Brown", "Blonde", "Red", "Gray", "White", "Other"])
    hair_style = st.text_input("Hair Style")
    distinguishing_marks = st.text_input("Distinguishing Marks")
    tattoos_scars = st.text_input("Tattoos/Scars")
    clothing_last_seen = st.text_input("Clothing Last Seen Wearing")
    end_form_section()

    form_section("3. Last Known Location")
    last_seen_location = st.text_input("Last Seen Location")
    date_last_seen = st.date_input("Date Last Seen")
    time_last_seen = st.time_input("Time Last Seen")
    circumstances = st.text_area("Circumstances of Disappearance")
    end_form_section()

    form_section("4. Contact Information")
    reporter_name = st.text_input("Reporter's Full Name")
    relationship = st.text_input("Relationship to Lost Person")
    phone_number = st.text_input("Phone Number")
    email_address = st.text_input("Email Address")
    alternate_contact = st.text_input("Alternate Contact Information")
    end_form_section()

    form_section("5. Upload Photos")
    photo = st.file_uploader("Recent Photo of Lost Person", type=["jpg", "jpeg", "png"])
    additional_photos = st.file_uploader("Additional Photos (Optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    end_form_section()

    form_section("6. Additional Information")
    medical_conditions = st.text_area("Medical Conditions/Medications")
    languages_spoken = st.text_input("Language(s) Spoken")
    habits_behavior = st.text_area("Known Habits/Behavior")
    other_info = st.text_area("Any Other Relevant Information")
    end_form_section()

    form_section("7. Submission Confirmation")
    consent = st.checkbox("I confirm that the information provided is accurate to the best of my knowledge and I consent to it being used for the purpose of locating the lost person.")
    end_form_section()

    if st.button("Submit"):
        if not consent:
            st.error("You must confirm the information and consent before submitting.")
        else:
            if full_name in data["Full Name"].values:
                st.warning("This person has already been reported.")
            else:
                if photo is not None:
                    photo_path = os.path.join("photos", photo.name)
                    with open(photo_path, "wb") as f:
                        f.write(photo.getbuffer())
                else:
                    photo_path = ""

                new_data = pd.DataFrame({
                    "Full Name": [full_name],
                    "Nickname": [nickname],
                    "Age": [age],
                    "Date of Birth": [dob],
                    "Gender": [gender],
                    "Ethnicity": [ethnicity],
                    "Nationality": [nationality],
                    "Height": [height],
                    "Weight": [weight],
                    "Eye Color": [eye_color],
                    "Hair Color": [hair_color],
                    "Hair Style": [hair_style],
                    "Distinguishing Marks": [distinguishing_marks],
                    "Tattoos/Scars": [tattoos_scars],
                    "Clothing Last Seen Wearing": [clothing_last_seen],
                    "Last Seen Location": [last_seen_location],
                    "Date Last Seen": [date_last_seen],
                    "Time Last Seen": [time_last_seen],
                    "Circumstances": [circumstances],
                    "Reporter's Name": [reporter_name],
                    "Relationship": [relationship],
                    "Phone Number": [phone_number],
                    "Email Address": [email_address],
                    "Alternate Contact": [alternate_contact],
                    "Medical Conditions": [medical_conditions],
                    "Languages Spoken": [languages_spoken],
                    "Habits/Behavior": [habits_behavior],
                    "Other Info": [other_info],
                    "Photo": [photo_path]
                })
                data = pd.concat([data, new_data], ignore_index=True)
                save_data(csv_file, data)
                st.success("Form submitted successfully.")

elif page == "View Lost People":
    st.title("List of Lost People")

    if data.empty:
        st.write("No lost people reported yet.")
    else:
        st.markdown("### Click on a name to see more details")
        cols = st.columns(3)
        col_index = 0

        for i, row in data.iterrows():
            if pd.notna(row["Photo"]) and row["Photo"]:
                if os.path.exists(row["Photo"]):
                    with cols[col_index]:
                        image = Image.open(row["Photo"])
                        st.image(image, caption=row["Full Name"], use_column_width=True)
                        if st.button(row["Full Name"], key=f"btn_{i}"):
                            with st.expander(f"Details of {row['Full Name']}"):
                                st.image(image, caption=row["Full Name"], use_column_width=True)
                                st.write(f"Nickname: {row['Nickname']}")
                                st.write(f"Age: {row['Age']}")
                                st.write(f"Date of Birth: {row['Date of Birth']}")
                                st.write(f"Gender: {row['Gender']}")
                                st.write(f"Ethnicity: {row['Ethnicity']}")
                                st.write(f"Nationality: {row['Nationality']}")
                                st.write(f"Height: {row['Height']}")
                                st.write(f"Weight: {row['Weight']}")
                                st.write(f"Eye Color: {row['Eye Color']}")
                                st.write(f"Hair Color: {row['Hair Color']}")
                                st.write(f"Hair Style: {row['Hair Style']}")
                                st.write(f"Distinguishing Marks: {row['Distinguishing Marks']}")
                                st.write(f"Tattoos/Scars: {row['Tattoos/Scars']}")
                                st.write(f"Clothing Last Seen Wearing: {row['Clothing Last Seen Wearing']}")
                                st.write(f"Last Seen Location: {row['Last Seen Location']}")
                                st.write(f"Date Last Seen: {row['Date Last Seen']}")
                                st.write(f"Time Last Seen: {row['Time Last Seen']}")
                                st.write(f"Circumstances: {row['Circumstances']}")
                                st.write(f"Reporter's Name: {row["Reporter's Name"]}")
                                st.write(f"Relationship: {row['Relationship']}")
                                st.write(f"Phone Number: {row['Phone Number']}")
                                st.write(f"Email Address: {row['Email Address']}")
                                st.write(f"Alternate Contact: {row['Alternate Contact']}")
                                st.write(f"Medical Conditions: {row['Medical Conditions']}")
                                st.write(f"Languages Spoken: {row['Languages Spoken']}")
                                st.write(f"Habits/Behavior: {row['Habits/Behavior']}")
                                st.write(f"Other Info: {row['Other Info']}")
                    
                    col_index = (col_index + 1) % 3
