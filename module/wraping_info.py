import google.generativeai as genai

def wraping_resume(extracted_text):
    from gui.frmgetapikey import api_key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Act as an text wraping system for resume, you will response with the following format to help me get information correctly to fill in the database, If none return 'None'.:
    1. Name: (Extract full name. Example: Nguyen Trung Nghia)
    2. Email: (Extract the email address. Example: example@example.com)
    3. Phone: (Extract the phone number in the format 0123456788. Only digits, no spaces or dashes.)
    4. Skills: (Extract the list of skills. Example: Python, C#, SQL)
    5. Project: (Extract only the project names. Example: FDI Analytics, Coffee shop management)
    6. GPA: (Extract the GPA as a single number. Example: If '3/4', return '3'. If not available, return 'None')
    7. Education: (Extract code of university school. Example: HUST, UET, PTIT)
    8. Major: (Extract the major of the candidate. Example: Computer Science, Data Science)
    
    Resume here: {extracted_text}
    
    Ensure the output is formatted as:
    Name: [Name]
    Email: [Email]
    Phone: [Phone]
    Skills: [Skills]
    Project: [Projects]
    GPA: [GPA]"""
    output = model.generate_content(prompt)
    response = output.text
    return response