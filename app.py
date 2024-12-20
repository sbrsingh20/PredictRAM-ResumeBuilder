import streamlit as st
from fpdf import FPDF

# Function to generate PDF
def generate_pdf(user_data, resume_type):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt=f"{user_data['name']}'s {resume_type}", ln=True, align='C')
    pdf.ln(10)

    # Personal Information
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Name: {user_data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_data['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user_data['phone']}", ln=True)
    pdf.cell(200, 10, txt=f"Location: {user_data['location']}", ln=True)
    pdf.ln(10)

    # Education
    if user_data['education']:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt="Education", ln=True)
        pdf.set_font('Arial', '', 12)
        for edu in user_data['education']:
            pdf.cell(200, 10, txt=f"{edu['degree']} in {edu['field']} from {edu['institution']} ({edu['year']})", ln=True)
        pdf.ln(10)

    # Work Experience
    if user_data['work_experience']:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt="Work Experience", ln=True)
        pdf.set_font('Arial', '', 12)
        for work in user_data['work_experience']:
            pdf.cell(200, 10, txt=f"{work['title']} at {work['company']} ({work['years']})", ln=True)
            pdf.multi_cell(0, 10, txt=f"Description: {work['description']}")
        pdf.ln(10)

    # Skills
    if user_data['skills']:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt="Skills", ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(200, 10, txt=', '.join(user_data['skills']), ln=True)

    # Save PDF
    pdf.output("resume.pdf")

# Streamlit app UI
def main():
    st.title("Resume / CV Generator")

    # Initialize session state if not already done
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'education': [],
            'work_experience': [],
            'skills': []
        }

    # Input form for personal information
    with st.form(key='user_details'):
        st.session_state.user_data['name'] = st.text_input("Name", value=st.session_state.user_data['name'])
        st.session_state.user_data['email'] = st.text_input("Email", value=st.session_state.user_data['email'])
        st.session_state.user_data['phone'] = st.text_input("Phone", value=st.session_state.user_data['phone'])
        st.session_state.user_data['location'] = st.text_input("Location", value=st.session_state.user_data['location'])
        submit_button = st.form_submit_button("Next")

    if submit_button:
        if not all([st.session_state.user_data['name'], st.session_state.user_data['email'],
                    st.session_state.user_data['phone'], st.session_state.user_data['location']]):
            st.error("Please fill in all personal information fields.")
        else:
            # Input for education
            st.subheader("Education")
            education_count = st.number_input(
                "Number of Education Entries",
                min_value=1, 
                max_value=5, 
                value=max(1, len(st.session_state.user_data['education']))  # Ensure value is >= 1
            )

            # Add Education Entries
            for i in range(education_count):
                if i >= len(st.session_state.user_data['education']):
                    st.session_state.user_data['education'].append({'degree': '', 'field': '', 'institution': '', 'year': ''})

                with st.expander(f"Education Entry {i + 1}"):
                    degree = st.text_input(f"Degree {i + 1}", value=st.session_state.user_data['education'][i]['degree'])
                    field = st.text_input(f"Field of Study {i + 1}", value=st.session_state.user_data['education'][i]['field'])
                    institution = st.text_input(f"Institution {i + 1}", value=st.session_state.user_data['education'][i]['institution'])
                    year = st.text_input(f"Year of Graduation {i + 1}", value=st.session_state.user_data['education'][i]['year'])

                    if degree and field and institution and year:
                        st.session_state.user_data['education'][i] = {'degree': degree, 'field': field, 'institution': institution, 'year': year}

            # Option to add another entry
            if st.button('Add Another Education Entry'):
                st.session_state.user_data['education'].append({'degree': '', 'field': '', 'institution': '', 'year': ''})

            # Input for work experience
            st.subheader("Work Experience")
            work_count = st.number_input(
                "Number of Work Experiences", 
                min_value=1, 
                max_value=5,
                value=max(1, len(st.session_state.user_data['work_experience']))  # Ensure value is >= 1
            )

            # Add Work Experience Entries
            for i in range(work_count):
                if i >= len(st.session_state.user_data['work_experience']):
                    st.session_state.user_data['work_experience'].append({'title': '', 'company': '', 'years': '', 'description': ''})

                with st.expander(f"Work Experience Entry {i + 1}"):
                    title = st.text_input(f"Job Title {i + 1}", value=st.session_state.user_data['work_experience'][i]['title'])
                    company = st.text_input(f"Company {i + 1}", value=st.session_state.user_data['work_experience'][i]['company'])
                    years = st.text_input(f"Years of Employment {i + 1}", value=st.session_state.user_data['work_experience'][i]['years'])
                    description = st.text_area(f"Job Description {i + 1}", value=st.session_state.user_data['work_experience'][i]['description'])

                    if title and company and years:
                        st.session_state.user_data['work_experience'][i] = {'title': title, 'company': company, 'years': years, 'description': description}

            # Option to add another entry
            if st.button('Add Another Work Experience Entry'):
                st.session_state.user_data['work_experience'].append({'title': '', 'company': '', 'years': '', 'description': ''})

            # Input for skills
            st.subheader("Skills")
            skills = st.text_input("List your skills (comma separated)", value=', '.join(st.session_state.user_data['skills']))
            if skills:
                st.session_state.user_data['skills'] = [skill.strip() for skill in skills.split(",")]

            # Choose between Resume or CV
            resume_type = st.radio("Choose Resume or CV", ["Resume", "Curriculum Vitae"])

            # Generate PDF button
            if st.button("Generate PDF"):
                generate_pdf(st.session_state.user_data, resume_type)
                st.success("Your PDF has been generated successfully!")
                with open("resume.pdf", "rb") as f:
                    st.download_button("Download PDF", f, file_name="resume.pdf")

if __name__ == "__main__":
    main()
