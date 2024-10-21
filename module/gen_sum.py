import google.generativeai as genai
def evaluate_resume(extracted_text, jd):
    from gui.frmgetapikey import api_key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
            Act as an advanced ATS (Applicant Tracking System) with extensive expertise in the tech industry, particularly in software engineering, data science, data analysis, and big data engineering. Your task is to meticulously evaluate the provided resume against the given job description.

            Resume: {extracted_text}
            Job Description: {jd}

            If the input is not a valid resume, respond with: "Please provide a valid resume or CV."
            If the input is not a valid job description, respond with: "Please provide a valid job description."

            Perform a rigorous analysis and provide a response in exactly the following format:

            - Job Description Match: [Provide a precise percentage match, considering not just keyword matches but also the depth of experience, relevance of projects, and alignment of skills. Be particularly critical of the quality and relevance of the experience.]

            - Missing Keywords: [List key terms or skills mentioned in the job description that are absent from the resume. Prioritize the most critical missing elements.]

            - Profile Summary: [Offer a concise, critical evaluation of the candidate's suitability for the role. Highlight both strengths and significant gaps. Be direct and objective, avoiding overly positive language unless truly warranted.]

            Ensure your evaluation is highly discerning, considering factors such as:
            - The recency and relevance of the candidate's experience
            - The depth of knowledge demonstrated in key areas
            - The alignment of the candidate's projects with job requirements
            - The candidate's potential to quickly adapt to the required skills

            Your assessment should be more selective than a standard ATS, aiming to identify only the most qualified candidates.
            """
    output = model.generate_content(prompt)
    response = output.text
    return response
def test_connect_api(key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content("Hello, how are you?")
        # print(response.text)
        return True
    except Exception as e:
        # print(f"Error: {e}")
        return False
