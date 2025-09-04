import streamlit
import plotly.express as plotly
from business import Business
import datetime


class StreamLitPage:

    def __init__(self):
        self.business = Business()
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
        last_seven_day = self.today - datetime.timedelta(days=7)
        return today, last_seven_day

    def all_team_failure_case_summary(self):

        start_date, end_date = streamlit.columns(2)

        with start_date:
            start_date = streamlit.date_input('📅 Start date', value='2025-09-01') # elf.common_value.last_seven_day

        with end_date:
            end_date = streamlit.date_input('📅 End date', value='2025-09-07')  # self.common_value.today

        dataframe = self.business.get_failure_summary_grouped_by_service(start_date=start_date, end_date=end_date)

        if dataframe.empty:
            streamlit.warning('No failure data found.')
        else:
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
        streamlit.info('Coming soon.')

    def main(self):
        self.sidebar() # Load sidebar
        streamlit.header(self.page) # All page will set the title
        self.page_handlers[self.page]() # Display all pages


if __name__ == '__main__':
    StreamLitPage().main()
