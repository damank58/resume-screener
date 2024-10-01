from main import ResumeScreener
import streamlit as st
import pandas as pd
import base64

st.logo('assets/images/logo.jpeg', icon_image='assets/images/logo.jpeg')
def page1():
    st.markdown("<h1 style='text-align: center; color: black;'>Upload Resume</h1>", unsafe_allow_html=True)

    job_ids = ResumeScreener().get_all_job_ids()
    job_id_list = [id[0] for id in job_ids]
    print(job_id_list)
    input_job_id = st.selectbox("Job ID", job_id_list, index=None, placeholder="Select a Job ID...")

    uploaded_file = st.file_uploader("Here upload resume in PDF format.", type=['pdf'])
    if uploaded_file is not None:
        filebytes = uploaded_file.getvalue()
        uploaded_filename = "uploads/{}".format(uploaded_file.name)
        with open(uploaded_filename, "wb") as datafile:
            datafile.write(filebytes)
        with st.spinner('Processing...'):
            try:
                ResumeScreener().generate_candidate_profile(input_job_id, uploaded_filename)
                st.success("Done!")
            except:
                st.success("Fail!")

def page2():
    st.markdown("<h1 style='text-align: center; color: grey;'>Candidate Resume Screening </h1>", unsafe_allow_html=True)
    row1, row2 = st.columns([1.5, 4])
    job_ids = ResumeScreener().get_all_job_ids()
    job_id_list = [id[0] for id in job_ids]
    job_id = row1.selectbox("Job ID", job_id_list, index=None, placeholder='Enter Job ID...')

    if job_id is not None:
        job_details = ResumeScreener().get_job_details(job_id)
        row2.text_input("Job Title", disabled=True, value=job_details[0][0])

        screener = ResumeScreener().get_dashboard_metrics(job_id)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Resume Received", screener.get('resume_received'))
        col2.metric("Resume Received in Last 5 days", screener.get('resume_received_last_5days'))
        col3.metric("Job Post Start Date", job_details[0][1].date().strftime('%d %b %Y'))
        col4.metric("Job Post End Date", job_details[0][2].date().strftime('%d %b %Y'))
        col5.metric("Candidates in Discussion", screener.get('in_discussion'))

        table = ResumeScreener().get_candidate_table(job_id)
        column_names = ['resume_id', 'Name', 'Summary Of Experience', 'Previous Job Title', 'Skills', 'Holds Masters',
                        'Relevant Score', 'Resume', 'Status']
        df = pd.DataFrame(table, columns=column_names)
        status_categories = ['Received', 'Reviewed', 'In Discussion', 'Offer Extended', 'Rejected']

        edited_df = st.data_editor(
            df.iloc[:, 1:],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="The category of the candidate",
                    width="medium",
                    options=status_categories,
                    required=True
                ),
                "Resume": st.column_config.LinkColumn(display_text='Link')
            },
            hide_index=True,
            disabled=[name for name in column_names if name not in ['Status']]
        )

        for idx_df in range(len(df)):
            if df["Status"][idx_df] != edited_df["Status"][idx_df]:
                ResumeScreener().get_updated_status(status=edited_df["Status"][idx_df],
                                                    resume_id=df['resume_id'][idx_df],
                                                    job_id=job_id)


pg = st.navigation([st.Page(page1, title="Upload Resume"), st.Page(page2, title="Resume Screener")])
pg.run()