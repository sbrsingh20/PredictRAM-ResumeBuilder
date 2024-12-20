import streamlit as st
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

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
        
        # Ensure we check if there's a colon before splitting
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
                data["key_skills"] = para_text.split(":")[1].strip().split(",")  # Assuming skills are comma-separated
        
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

        # For sections that follow the headings
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
def generate_resume_pdf(data, filename="resume.pdf"):
    # Create a PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Create a list to hold the flowable elements
    story = []
    
    # Create a stylesheet for the document
    styles = getSampleStyleSheet()

    # Header Section: Full Name, Phone, Email, LinkedIn, Location
    header_style = styles['Heading1']
    header_style.fontSize = 18
    header_style.leading = 22

    name = data['contact_info'].get('name', 'N/A')
    phone = data['contact_info'].get('phone', 'N/A')
    email = data['contact_info'].get('email', 'N/A')
    linkedin = data['contact_info'].get('linkedin', 'N/A')
    location = data['contact_info'].get('location', 'N/A')
    
    header = f"{name}\n{phone} | {email} | {linkedin} | {location}"
    story.append(Paragraph(header, header_style))
    story.append(Spacer(1, 0.25 * inch))
    
    # Professional Summary Section
    summary_style = styles['Normal']
    summary_style.fontSize = 12
    summary_style.leading = 14
    if data['professional_summary']:
        story.append(Paragraph("<b>Professional Summary:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(data['professional_summary'], summary_style))
        story.append(Spacer(1, 0.25 * inch))
    
    # Key Skills Section
    if data['key_skills']:
        story.append(Paragraph("<b>Key Skills:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        key_skills = ', '.join(data['key_skills'])
        story.append(Paragraph(key_skills, summary_style))
        story.append(Spacer(1, 0.25 * inch))
    
    # Professional Experience Section
    if data['professional_experience']:
        story.append(Paragraph("<b>Professional Experience:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for job in data['professional_experience']:
            job_paragraph = Paragraph(job, summary_style)
            story.append(job_paragraph)
            story.append(Spacer(1, 0.15 * inch))

    # Education Section
    if data['education']:
        story.append(Paragraph("<b>Education:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for edu in data['education']:
            edu_paragraph = Paragraph(edu, summary_style)
            story.append(edu_paragraph)
            story.append(Spacer(1, 0.15 * inch))
    
    # Certifications Section
    if data['certifications']:
        story.append(Paragraph("<b>Certifications:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for cert in data['certifications']:
            cert_paragraph = Paragraph(cert, summary_style)
            story.append(cert_paragraph)
            story.append(Spacer(1, 0.15 * inch))
    
    # Projects Section
    if data['projects']:
        story.append(Paragraph("<b>Projects:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for project in data['projects']:
            project_paragraph = Paragraph(project, summary_style)
            story.append(project_paragraph)
            story.append(Spacer(1, 0.15 * inch))

    # Awards Section
    if data['awards']:
        story.append(Paragraph("<b>Awards:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for award in data['awards']:
            award_paragraph = Paragraph(award, summary_style)
            story.append(award_paragraph)
            story.append(Spacer(1, 0.15 * inch))

    # Volunteer Work Section
    if data['volunteer_work']:
        story.append(Paragraph("<b>Volunteer Work:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for volunteer in data['volunteer_work']:
            volunteer_paragraph = Paragraph(volunteer, summary_style)
            story.append(volunteer_paragraph)
            story.append(Spacer(1, 0.15 * inch))
    
    # Languages Section
    if data['languages']:
        story.append(Paragraph("<b>Languages:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for language in data['languages']:
            language_paragraph = Paragraph(language, summary_style)
            story.append(language_paragraph)
            story.append(Spacer(1, 0.15 * inch))

    # Additional Sections (if any)
    if data['additional']:
        story.append(Paragraph("<b>Additional Sections:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for additional in data['additional']:
            additional_paragraph = Paragraph(additional, summary_style)
            story.append(additional_paragraph)
            story.append(Spacer(1, 0.15 * inch))

    # Build the PDF document
    doc.build(story)

# Streamlit App

def main():
    st.title("Resume Builder - Upload Word Document")
    
    # Upload file
    uploaded_file = st.file_uploader("Upload your Word file", type="docx")
    
    if uploaded_file is not None:
        # Extract text from the uploaded Word document
        user_data = extract_text_from_word(uploaded_file)
        
        # Display extracted data
        st.write("### Extracted Data:")
        st.json(user_data)

        # Generate the PDF button
        if st.button("Generate Resume PDF"):
            filename = "generated_resume.pdf"
            generate_resume_pdf(user_data, filename)
            st.success(f"Resume generated successfully! You can download it [here]({filename}).")
            
if __name__ == "__main__":
    main()
