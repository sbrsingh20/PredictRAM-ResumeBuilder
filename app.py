import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO


# Function to extract text from Word file
def extract_text_from_word(file):
    doc = Document(file)
    data = {
        "contact_info": {},
        "professional_summary": "",
        "key_skills": [],
        "professional_experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "awards": [],
        "volunteer_work": [],
        "languages": [],
        "additional": []
    }
    
    current_section = None
    for para in doc.paragraphs:
        if "Full Name" in para.text:
            data["contact_info"]["name"] = para.text.split(":")[1].strip()
        elif "Phone Number" in para.text:
            data["contact_info"]["phone"] = para.text.split(":")[1].strip()
        elif "Email Address" in para.text:
            data["contact_info"]["email"] = para.text.split(":")[1].strip()
        elif "LinkedIn Profile" in para.text:
            data["contact_info"]["linkedin"] = para.text.split(":")[1].strip()
        elif "Location" in para.text:
            data["contact_info"]["location"] = para.text.split(":")[1].strip()

        elif "Professional Summary" in para.text:
            current_section = "professional_summary"
            data["professional_summary"] = para.text.split(":")[1].strip()

        elif "Key Skills" in para.text:
            current_section = "key_skills"
            data["key_skills"] = para.text.split(":")[1].strip().split(",")  # Assuming skills are comma-separated
        
        elif "Professional Experience" in para.text:
            current_section = "professional_experience"
        elif "Education" in para.text:
            current_section = "education"
        elif "Certifications" in para.text:
            current_section = "certifications"
        elif "Projects" in para.text:
            current_section = "projects"
        elif "Awards" in para.text:
            current_section = "awards"
        elif "Volunteer Work" in para.text:
            current_section = "volunteer_work"
        elif "Languages" in para.text:
            current_section = "languages"
        elif "Additional" in para.text:
            current_section = "additional"

        # For sections that follow the headings
        elif current_section == "professional_experience":
            data["professional_experience"].append(para.text.strip())
        elif current_section == "education":
            data["education"].append(para.text.strip())
        elif current_section == "certifications":
            data["certifications"].append(para.text.strip())
        elif current_section == "projects":
            data["projects"].append(para.text.strip())
        elif current_section == "awards":
            data["awards"].append(para.text.strip())
        elif current_section == "volunteer_work":
            data["volunteer_work"].append(para.text.strip())
        elif current_section == "languages":
            data["languages"].append(para.text.strip())
        elif current_section == "additional":
            data["additional"].append(para.text.strip())

    return data


# Function to generate PDF using ReportLab
def generate_pdf_reportlab(user_data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title of the resume
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, f"{user_data['contact_info']['name']}'s Resume")

    # Contact Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Name: {user_data['contact_info']['name']}")
    c.drawString(50, height - 120, f"Email: {user_data['contact_info']['email']}")
    c.drawString(50, height - 140, f"Phone: {user_data['contact_info']['phone']}")
    c.drawString(50, height - 160, f"LinkedIn: {user_data['contact_info']['linkedin']}")
    c.drawString(50, height - 180, f"Location: {user_data['contact_info']['location']}")

    # Professional Summary
    if user_data["professional_summary"]:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 220, "Professional Summary")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 240, user_data["professional_summary"])

    # Key Skills
    if user_data["key_skills"]:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 280, "Key Skills")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 300, ', '.join(user_data["key_skills"]))

    # Professional Experience
    if user_data["professional_experience"]:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 340, "Professional Experience")
        y_position = height - 360
        c.setFont("Helvetica", 12)
        for experience in user_data["professional_experience"]:
            c.drawString(50, y_position, experience)
            y_position -= 20

    # Education
    if user_data["education"]:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Education")
        y_position -= 20
        c.setFont("Helvetica", 12)
        for edu in user_data["education"]:
            c.drawString(50, y_position, edu)
            y_position -= 20

    # Certifications
    if user_data["certifications"]:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position, "Certifications")
        y_position -= 20
        c.setFont("Helvetica", 12)
        for cert in user_data["certifications"]:
            c.drawString(50, y_position, cert)
            y_position -= 20

    # Additional sections can be added similarly...

    # Save PDF to buffer
    c.save()

    # Move buffer position to the beginning
    buffer.seek(0)
    return buffer


# Streamlit app UI
def main():
    st.title("Resume / CV Generator from Word File")

    # Upload Word File
    uploaded_file = st.file_uploader("Upload a Word File", type="docx")

    if uploaded_file:
        # Extract content from the uploaded Word file
        user_data = extract_text_from_word(uploaded_file)
        st.success("Content extracted successfully!")

        # Display the extracted data (optional)
        st.write(user_data)

        # Generate PDF button
        if st.button("Generate Resume PDF"):
            pdf_buffer = generate_pdf_reportlab(user_data)
            st.success("Your PDF has been generated successfully!")
            st.download_button("Download Resume PDF", pdf_buffer, file_name="resume.pdf", mime="application/pdf")


if __name__ == "__main__":
    main()
