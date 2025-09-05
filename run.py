import datetime
import textwrap

import plotly.express as plotly
import streamlit

from database.business import BusinessLogic
from llm.cache import get_ai_summary_cached


class StreamLitPage:

    def __init__(self):
        streamlit.set_page_config(page_title='Dashboard', layout='wide')

        self.biz = BusinessLogic()

        self.page_handlers = {
            "All Team Failure Case Summary": self.all_team_failure_case_summary,
            "Failure Insights": self.failure_insights
        }

    def sidebar(self):
        streamlit.sidebar.title('')
        self.page = streamlit.sidebar.radio(
            'Navigation',
            options=list(self.page_handlers.keys()),
            index=0  # Default radio
        )

    def common_value(self):
        today = datetime.date.today()
        last_seven_day = today - datetime.timedelta(days=7)
        return today, last_seven_day

    def all_team_failure_case_summary(self):

        start_date, end_date = streamlit.columns(2)
        with start_date:
            start_date = streamlit.date_input(label='Start date', value='2025-09-01')  # elf.common_value.last_seven_day
        with end_date:
            end_date = streamlit.date_input(label='End date', value='2025-09-07')  # self.common_value.today

        dataframe = self.biz.get_failure_summary_grouped_by_service(start_date=start_date, end_date=end_date)

        if dataframe.empty:
            streamlit.warning('No failure data found.')
            return

        figure = plotly.bar(
            data_frame=dataframe,
            x='service_team',
            y='fail_count',
            color='service_team',
            color_discrete_sequence=plotly.colors.cyclical.Twilight,
            title=f'{start_date} - {end_date}',
            text='fail_count'
        )
        figure.update_layout(showlegend=False)
        streamlit.plotly_chart(figure_or_data=figure, use_container_width=True)

    def failure_insights(self):

        all_team_dataframe = self.biz.get_all_service_teams()
        all_teams = all_team_dataframe['service_team'].tolist()
        service_team = streamlit.selectbox(
            label='service team',
            options=all_teams,
        )

        start_date, end_date = streamlit.columns(2)
        with start_date:
            start_date = streamlit.date_input(label='Start date', value='2025-09-01')  # elf.common_value.last_seven_day
        with end_date:
            end_date = streamlit.date_input(label='End date', value='2025-09-03')  # self.common_value.today

        expand_all = streamlit.checkbox(label='Expand Test Cases', value=False)

        dataframe = self.biz.get_failure_details_by_team(
            service_team=service_team,
            start_date=start_date,
            end_date=end_date
        )

        if dataframe.empty:
            streamlit.warning('No failure data found.')
            return

        # AI Section
        streamlit.subheader('AI Suggetions')

        with streamlit.status('AI analysis in progress...', state='running', expanded=False) as status:
            try:
                ai_team_summary = get_ai_summary_cached(
                    service_team=service_team,
                    error_list=dataframe['error_message'].tolist(),
                    date=str(start_date)
                )

                suggestions = '\n'.join([f"- {s}" for s in ai_team_summary['suggestions']])
                summary_text = textwrap.dedent(f"""\
Summary: {ai_team_summary['summary']}

Root Cause Analysis: {ai_team_summary['root_cause_analysis']}

Suggestions:
{suggestions}
                """).strip()

                streamlit.text_area(
                    label='AI Summary',
                    value=summary_text.strip(),
                    height=300,
                    disabled=True
                )
                status.update(label='completed', state='complete', expanded=True)
            except Exception as e:
                streamlit.error(f'AI Analysis failed: {e}')
                status.update(label='failed', state='error')

        # Test Case Section
        streamlit.subheader('Failure Details')

        for idx, row in dataframe.iterrows():
            with streamlit.expander(label=f'❌  {row['service']} | {row['case_name']} | {row['timestamp']}', expanded=expand_all):
                streamlit.error(row['error_message'])
                streamlit.code(row['traceback'])

    def main(self):
        self.sidebar()  # Load sidebar
        streamlit.header(self.page)  # All page will set the title
        self.page_handlers[self.page]()  # Display all pages


if __name__ == '__main__':
    StreamLitPage().main()
