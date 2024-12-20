import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO


# Function to generate PDF using ReportLab
def generate_pdf_reportlab(user_data, resume_type):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title of the resume
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, f"{user_data['name']}'s {resume_type}")

    # Personal Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Name: {user_data['name']}")
    c.drawString(50, height - 120, f"Email: {user_data['email']}")
    c.drawString(50, height - 140, f"Phone: {user_data['phone']}")
    c.drawString(50, height - 160, f"Location: {user_data['location']}")

    # Education Section
    if user_data['education']:
        y_position = height - 200
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Education")
        y_position -= 20
        c.setFont("Helvetica", 12)

        for edu in user_data['education']:
            c.drawString(50, y_position, f"{edu['degree']} in {edu['field']} from {edu['institution']} ({edu['year']})")
            y_position -= 20

    # Work Experience Section
    if user_data['work_experience']:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Work Experience")
        y_position -= 20
        c.setFont("Helvetica", 12)

        for work in user_data['work_experience']:
            c.drawString(50, y_position, f"{work['title']} at {work['company']} ({work['years']})")
            y_position -= 20
            c.drawString(50, y_position, f"Description: {work['description']}")
            y_position -= 30

    # Skills Section
    if user_data['skills']:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Skills")
        y_position -= 20
        c.setFont("Helvetica", 12)
        c.drawString(50, y_position, ', '.join(user_data['skills']))

    # Save PDF to buffer
    c.save()

    # Move buffer position to the beginning
    buffer.seek(0)
    return buffer


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

    # Form for personal information
    with st.form(key="personal_info"):
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
            # Input for Education entries
            st.subheader("Education")
            education_count = st.number_input(
                "Number of Education Entries", min_value=1, max_value=5,
                value=max(1, len(st.session_state.user_data['education']))
            )

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

            # Input for Work Experience entries
            st.subheader("Work Experience")
            work_count = st.number_input(
                "Number of Work Experiences", min_value=1, max_value=5,
                value=max(1, len(st.session_state.user_data['work_experience']))
            )

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

            # Input for Skills
            st.subheader("Skills")
            skills = st.text_input("List your skills (comma separated)", value=', '.join(st.session_state.user_data['skills']))
            if skills:
                st.session_state.user_data['skills'] = [skill.strip() for skill in skills.split(",")]

            # Choose between Resume or CV
            resume_type = st.radio("Choose Resume or CV", ["Resume", "Curriculum Vitae"])

            # Generate PDF button
            if st.button("Generate PDF"):
                pdf_buffer = generate_pdf_reportlab(st.session_state.user_data, resume_type)
                st.success("Your PDF has been generated successfully!")
                st.download_button("Download PDF", pdf_buffer, file_name="resume.pdf", mime="application/pdf")


if __name__ == "__main__":
    main()
