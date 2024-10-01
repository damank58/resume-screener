from langchain.globals import set_debug
#set_debug(True)
from src.engine import ResumeAI
from candidate_metrics import Metrics

class CandidateProfile(object):
    def __init__(self):
        pass

    def get_llm_response(self, prompt):
        response = self.qa_retriever({"query": prompt})
        return response['result']

    def get_name(self):
        prompt = '''Given resume of a candidate, extract name of the candidate. Output name of the candidate only. No explanation.
        Example: Steve Jobs, John Doel, Angelina Rob, Bobby Klein, Tina'''
        response = self.get_llm_response(prompt=prompt)
        return response

    def get_contact_no(self):
        prompt = '''Given resume of a candidate as context, give phone number of the candidate. 
        Output phone number only and if unknown, give NA.'''
        response = self.get_llm_response(prompt)
        return response

    def get_email(self):
        prompt = '''Given resume of a candidate as context, give email ID of the candidate. Output email ID only, and if
        unknown, give NA. Example: abc12@gmail.com, xyz_12@hotmail.com'''
        response = self.get_llm_response(prompt)
        return response

    def get_address(self):
        prompt = '''Given resume as a context, give address of the candidate. Output only address. No explanation.
        Output example: 33rd street, 14th Avenue, New York, United States-10001'''
        response = self.get_llm_response(prompt)
        return response

    def get_summary_of_exp(self):
        prompt = 'Summarize the work experience of the candidate in bullet points'
        response = self.get_llm_response(prompt)
        return response

    def get_job_title(self):
        prompt = ('''Give present or current job title of the candidate. No explanation in Output.
        Example: Analyst, HR Consultant, Accountant''')
        response = self.get_llm_response(prompt)
        return response

    def get_skills(self):
        prompt = 'List skills of the candidate in bullet points'
        response = self.get_llm_response(prompt)
        return response

    def has_masters(self):
        prompt = 'Does the candidate hold masters degree? Answer "True" if yes, "False" if not or unknown.'
        response = self.get_llm_response(prompt)
        return response

    def run(self, job_id, file_path):
        self.qa_retriever = ResumeAI().run_for_candidate_profile(file_path)
        name = self.get_name()
        work_exp = self.get_summary_of_exp()
        job_title = self.get_job_title()
        skills = self.get_skills()
        has_masters = self.has_masters()
        contact_no = self.get_contact_no()
        email_id = self.get_email()
        address = self.get_address()
        score = 10.00
        status = 'Received'
        data = (name, contact_no, email_id, address, work_exp, job_title, skills, has_masters, score, file_path, job_id, status)
        Metrics().insert_rec(data)

