import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
from reportlab.lib.units import inch  # Added this import to use 'inch'

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
        para_text = para.text.strip()
        
        if "Full Name" in para_text:
            if ":" in para_text:
                data["contact_info"]["name"] = para_text.split(":")[1].strip()
        elif "Phone Number" in para_text:
            if ":" in para_text:
                data["contact_info"]["phone"] = para_text.split(":")[1].strip()
        elif "Email Address" in para_text:
            if ":" in para_text:
                data["contact_info"]["email"] = para_text.split(":")[1].strip()
        elif "LinkedIn Profile" in para_text:
            if ":" in para_text:
                data["contact_info"]["linkedin"] = para_text.split(":")[1].strip()
        elif "Location" in para_text:
            if ":" in para_text:
                data["contact_info"]["location"] = para_text.split(":")[1].strip()

        elif "Professional Summary" in para_text:
            current_section = "professional_summary"
            if ":" in para_text:
                data["professional_summary"] = para_text.split(":")[1].strip()

        elif "Key Skills" in para_text:
            current_section = "key_skills"
            if ":" in para_text:
                data["key_skills"] = para_text.split(":")[1].strip().split(",")
        
        elif "Professional Experience" in para_text:
            current_section = "professional_experience"
        elif "Education" in para_text:
            current_section = "education"
        elif "Certifications" in para_text:
            current_section = "certifications"
        elif "Projects" in para_text:
            current_section = "projects"
        elif "Awards" in para_text:
            current_section = "awards"
        elif "Volunteer Work" in para_text:
            current_section = "volunteer_work"
        elif "Languages" in para_text:
            current_section = "languages"
        elif "Additional" in para_text:
            current_section = "additional"

        elif current_section == "professional_experience":
            data["professional_experience"].append(para_text)
        elif current_section == "education":
            data["education"].append(para_text)
        elif current_section == "certifications":
            data["certifications"].append(para_text)
        elif current_section == "projects":
            data["projects"].append(para_text)
        elif current_section == "awards":
            data["awards"].append(para_text)
        elif current_section == "volunteer_work":
            data["volunteer_work"].append(para_text)
        elif current_section == "languages":
            data["languages"].append(para_text)
        elif current_section == "additional":
            data["additional"].append(para_text)

    return data

# Function to generate the resume PDF
def generate_resume_pdf(data):
    # Create a PDF document in memory (using BytesIO)
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Create a list to hold the flowable elements
    story = []
    
    # Create a stylesheet for the document
    styles = getSampleStyleSheet()

    # Professional Header Style
    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=32,
        alignment=1,
        spaceAfter=12
    )

    # Contact Info Style
    contact_style = ParagraphStyle(
        "ContactStyle",
        fontName="Helvetica",
        fontSize=10,
        alignment=1,
        spaceAfter=6,
        textColor=colors.black
    )

    # Section Title Style (for Professional Summary, Experience, Education)
    section_title_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=colors.darkblue,
        alignment=0,  # Left align
        spaceBefore=6,
        spaceAfter=3
    )

    # Regular Paragraph Style
    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        spaceAfter=6
    )
    
    # Bold Paragraph Style for specific headings
    bold_style = ParagraphStyle(
        "BoldStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        spaceAfter=6
    )

    # Header Section: Full Name
    name = data['contact_info'].get('name', 'N/A')
    story.append(Paragraph(name, header_style))
    story.append(Spacer(1, 0.25 * inch))

    # Contact Info Section: Phone, Email, LinkedIn, Location
    phone = data['contact_info'].get('phone', 'N/A')
    email = data['contact_info'].get('email', 'N/A')
    linkedin = data['contact_info'].get('linkedin', 'N/A')
    location = data['contact_info'].get('location', 'N/A')
    
    contact_info = f"Phone: {phone} | Email: {email} | LinkedIn: {linkedin} | Location: {location}"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 0.5 * inch))

    # Professional Summary Section
    if data['professional_summary']:
        story.append(Paragraph("<b>Professional Summary:</b>", section_title_style))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(data['professional_summary'], normal_style))
        story.append(Spacer(1, 0.25 * inch))

    # Professional Experience Section
    if data['professional_experience']:
        story.append(Paragraph("<b>Professional Experience:</b>", section_title_style))
        story.append(Spacer(1, 0.1 * inch))
        for job in data['professional_experience']:
            # Ensure the job data is properly formatted and has enough parts
            job_parts = job.split(":")
            if len(job_parts) >= 3:
                job_title = "Job Title: " + job_parts[0].strip()
                dates_of_employment = "Dates of Employment: " + job_parts[1].strip()
                responsibilities = "Responsibilities & Achievements: " + job_parts[2].strip()
                
                story.append(Paragraph(job_title, bold_style))
                story.append(Paragraph(dates_of_employment, bold_style))
                story.append(Paragraph(responsibilities, normal_style))
                story.append(Spacer(1, 0.1 * inch))

    # Education Section
    if data['education']:
        story.append(Paragraph("<b>Education:</b>", section_title_style))
        story.append(Spacer(1, 0.1 * inch))
        for edu in data['education']:
            # Ensure the education data is properly formatted and has enough parts
            edu_parts = edu.split(":")
            if len(edu_parts) >= 3:
                degree = "Degree: " + edu_parts[0].strip()
                major_minor = "Major/Minor: " + edu_parts[1].strip()
                graduation_year = "Graduation Year: " + edu_parts[2].strip()
                story.append(Paragraph(degree, bold_style))
                story.append(Paragraph(major_minor, bold_style))
                story.append(Paragraph(graduation_year, normal_style))
                story.append(Spacer(1, 0.1 * inch))

    # Right-side column with Certifications, Projects, Awards, etc.
    right_column_data = []
    right_column_data.append(("Certifications", data['certifications']))
    right_column_data.append(("Projects", data['projects']))
    right_column_data.append(("Awards", data['awards']))
    right_column_data.append(("Volunteer Work", data['volunteer_work']))
    right_column_data.append(("Languages", data['languages']))
    right_column_data.append(("Additional", data['additional']))

    # Add these sections to the right-side column
    for title, content in right_column_data:
        if content:
            story.append(Spacer(1, 0.25 * inch))  # Add spacing between sections
            story.append(Paragraph(f"<b>{title}:</b>", section_title_style))
            story.append(Spacer(1, 0.1 * inch))
            for item in content:
                story.append(Paragraph(item, normal_style))
                story.append(Spacer(1, 0.1 * inch))

    # Build the PDF document
    doc.build(story)
    
    # Save the PDF to buffer
    buffer.seek(0)
    return buffer

# Streamlit interface
def main():
    st.title("Resume Builder")
    uploaded_file = st.file_uploader("Upload Word file", type=["docx"])

    if uploaded_file:
        user_data = extract_text_from_word(uploaded_file)
        resume_pdf = generate_resume_pdf(user_data)

        # Provide download link for PDF
        st.write("Resume generated successfully! You can download it here.")
        st.download_button(
            label="Download Resume",
            data=resume_pdf,
            file_name="generated_resume.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
