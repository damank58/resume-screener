from connectors.postgres import ResumeDB

class Metrics(object):
    def __init__(self):
        pass

    def insert_rec(self, data: tuple):
        ResumeDB().insert(
            """INSERT INTO candidate_details (
            name, contact_no, email_id, address, summary_of_exp,
            previous_job_title, skills, has_masters, score, resume_path, job_id, status)
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)

    def get_candidate_rec(self, job_id):
        response = ResumeDB().select_all(
            """SELECT resume_id, name, summary_of_exp, previous_job_title, skills, has_masters, score, resume_path, status
                FROM candidate_details
                WHERE job_id = %s""", (job_id,)
        )
        return response

    def get_count_rec(self, type: str, job_id):
        if type == 'total':
            count = ResumeDB().select_all("SELECT COUNT(*) AS total_resume FROM candidate_details WHERE job_id = %s", (job_id,))
            count = count[0][0]
        elif type == 'last_5days':
            count = ResumeDB().select_all('''SELECT COUNT(*) AS last_5days FROM candidate_details
            WHERE job_id = %s AND EXTRACT(DAY FROM (NOW() - timestamp)) < 6''', (job_id,))
            count = count[0][0]
        elif type == 'in_discussion':
            count = ResumeDB().select_all('''SELECT COUNT(*) AS in_discussion FROM candidate_details
            WHERE job_id = %s AND status = 'In Discussion' ''', (job_id,))
            count = count[0][0]
        else:
            raise Exception('Invalid count type')
        return count

    def get_job_details(self, job_id):
        response = ResumeDB().select_all('''SELECT job_title, start_date, end_date
                                                    FROM jobs 
                                                    WHERE job_id = %s ''', (job_id,)
                                         )
        return response

    def get_distinct_job_ids(self):
        response = ResumeDB().select_all('''SELECT DISTINCT(job_id) FROM jobs ORDER BY job_id ASC''')
        return response

    def update_status(self, status, resume_id, job_id):
        ResumeDB().update('''UPDATE candidate_details 
                                    SET status = %s 
                                    WHERE resume_id = %s AND job_id = %s''', (status, resume_id, job_id))
