import datetime
import textwrap

import plotly.express as plotly
import streamlit

from database.business import BusinessLogic
from llm.cache import get_ai_summary_cached
import pandas


class StreamLitPage:

    def __init__(self):
        streamlit.set_page_config(page_title='Dashboard', layout='wide')

        self.biz = BusinessLogic()

        self.page_handlers = {
            "Failure Overview": self.failure_overview,
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

    def failure_overview(self):

        start_date, end_date = streamlit.columns(2)
        with start_date:
            start_date = streamlit.date_input(label='Start date', value='2025-09-01')  # elf.common_value.last_seven_day
        with end_date:
            end_date = streamlit.date_input(label='End date', value='2025-09-07')  # self.common_value.today

        dataframe = self.biz.get_failure_summary_grouped_by_service(
            start_date=start_date,
            end_date=end_date + datetime.timedelta(days=1)
        )

        if dataframe.empty:
            streamlit.warning('No failure data found.')
            return

        # region [Failure Summary by Team]
        expected_teams = self.biz.get_all_service_teams()['service_team'].unique()
        dataframe = dataframe.set_index('service_team').reindex(expected_teams, fill_value=0).reset_index() # Fill 0
        figure = plotly.bar(
            data_frame=dataframe,
            x='service_team',
            y='fail_count',
            color='service_team',
            color_discrete_sequence=plotly.colors.qualitative.T10,
            title=f'Failure Summary by Team ({start_date} - {end_date})',
            text='fail_count'
        )
        figure.update_layout(showlegend=False)
        streamlit.plotly_chart(figure_or_data=figure, use_container_width=True)
        # endregion [Failure Summary by Team]

        # region [Daily Failures by Team]
        all_details = []
        for team in dataframe['service_team'].unique():
            dataframe_team = self.biz.get_failure_details_by_team(
                service_team=team,
                start_date=start_date,
                end_date=end_date + datetime.timedelta(days=1)
            )
            all_details.append(dataframe_team)

        full_dataframe = pandas.concat(all_details)
        full_dataframe['date'] = pandas.to_datetime(full_dataframe['timestamp']).dt.date

        fail_by_day_team = (
            full_dataframe.groupby(['service_team', 'date'])
            .size()
            .reset_index(name='fail_count')
        )
        all_dates = pandas.date_range(start=start_date, end=end_date, freq='D').date
        all_teams = fail_by_day_team['service_team'].unique()

        grid = pandas.MultiIndex.from_product(
            [all_teams, all_dates],
            names=['service_team', 'date']
        )

        dataframe_filled = fail_by_day_team.set_index(['service_team', 'date']).reindex(grid, fill_value=0).reset_index()
        figure = plotly.bar(
            data_frame=dataframe_filled,
            x='date',
            y='fail_count',
            color='service_team',
            color_discrete_sequence=plotly.colors.cyclical.Twilight,
            barmode='group',
            title=f'Daily Failures by Team ({start_date} - {end_date})',
        )
        streamlit.plotly_chart(figure, use_container_width=True)
        # endregion [Daily Failures by Team]

    def failure_insights(self):

        all_team_dataframe = self.biz.get_all_service_teams()
        all_teams = all_team_dataframe['service_team'].tolist()
        service_team = streamlit.selectbox(
            label='service team',
            options=all_teams,
        )

        start_date, end_date = streamlit.columns(2)
        with start_date:
            start_date = streamlit.date_input(label='Start date', value='2025-09-02')  # elf.common_value.last_seven_day
        with end_date:
            end_date = streamlit.date_input(label='End date', value='2025-09-02')  # self.common_value.today

        expand_all = streamlit.checkbox(label='Expand Test Cases', value=False)

        dataframe = self.biz.get_failure_details_by_team(
            service_team=service_team,
            start_date=start_date,
            end_date=end_date + datetime.timedelta(days=1)
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
