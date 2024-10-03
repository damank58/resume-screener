from src.candidate_profile import CandidateProfile
from candidate_metrics import Metrics

class ResumeScreener(object):
    def __init__(self):
        pass

    def get_dashboard_metrics(self, job_id):
        total = Metrics().get_count_rec(type='total', job_id=job_id)
        last_5days = Metrics().get_count_rec(type='last_5days', job_id=job_id)
        in_discussion = Metrics().get_count_rec(type='in_discussion', job_id=job_id)
        return {"resume_received": total, "resume_received_last_5days": last_5days, 'in_discussion': in_discussion}

    def get_candidate_table(self, job_id):
        candidate_data = Metrics().get_candidate_rec(job_id)
        return candidate_data

    def generate_candidate_profile(self, job_id, filename):
        try:
            CandidateProfile().run(job_id, filename)
            return True
        except Exception as err:
            return False

    def get_job_details(self, job_id):
        return Metrics().get_job_details(job_id)

    def get_all_job_ids(self):
        return Metrics().get_distinct_job_ids()

    def get_updated_status(self, status, resume_id, job_id):
        Metrics().update_status(status, resume_id, job_id)

    def get_chat_response(self, prompt, file_path):
        response = CandidateProfile().chat(prompt, file_path)
        return response
