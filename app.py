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

    # Header Section: Full Name, Phone, Email, LinkedIn, Location
    header_style = styles['Heading1']
    header_style.fontSize = 24
    header_style.leading = 28

    name = data['contact_info'].get('name', 'N/A')
    phone = data['contact_info'].get('phone', 'N/A')
    email = data['contact_info'].get('email', 'N/A')
    linkedin = data['contact_info'].get('linkedin', 'N/A')
    location = data['contact_info'].get('location', 'N/A')
    
    header = f"{name}"
    story.append(Paragraph(header, header_style))
    story.append(Spacer(1, 0.25 * inch))

    # Contact Info: Phone, Email, LinkedIn, Location (Smaller Font)
    contact_style = styles['Normal']
    contact_style.fontSize = 10
    contact_info = f"Phone: {phone} | Email: {email} | LinkedIn: {linkedin} | Location: {location}"
    story.append(Paragraph(contact_info, contact_style))
    story.append(Spacer(1, 0.25 * inch))

    # Professional Summary Section
    if data['professional_summary']:
        story.append(Paragraph("<b>Professional Summary:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(data['professional_summary'], styles['Normal']))
        story.append(Spacer(1, 0.25 * inch))

    # Professional Experience Section
    if data['professional_experience']:
        story.append(Paragraph("<b>Professional Experience:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for job in data['professional_experience']:
            story.append(Paragraph(job, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
    
    # Education Section
    if data['education']:
        story.append(Paragraph("<b>Education:</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        for edu in data['education']:
            story.append(Paragraph(edu, styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

    # Right side section (Certifications, Projects, Awards, Volunteer Work, Languages)
    right_column_data = []
    
    # Add certifications, projects, awards, volunteer work, languages, additional to right column
    right_column_data.append(("Certifications", data['certifications']))
    right_column_data.append(("Projects", data['projects']))
    right_column_data.append(("Awards", data['awards']))
    right_column_data.append(("Volunteer Work", data['volunteer_work']))
    right_column_data.append(("Languages", data['languages']))
    right_column_data.append(("Additional", data['additional']))

    for title, content in right_column_data:
        if content:
            story.append(Spacer(1, 0.25 * inch))  # Add spacing between sections
            story.append(Paragraph(f"<b>{title}:</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1 * inch))
            for item in content:
                story.append(Paragraph(item, styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

    # Build the PDF document
    doc.build(story)
    
    # Return the buffer so we can serve the file in Streamlit
    buffer.seek(0)
    return buffer

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
            resume_pdf = generate_resume_pdf(user_data)
            
            # Provide download button
            st.download_button(
                label="Download Resume PDF",
                data=resume_pdf,
                file_name="resume.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
