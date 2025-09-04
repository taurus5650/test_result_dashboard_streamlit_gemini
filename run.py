import streamlit
import plotly.express as plotly
from business import Business
import datetime
import logging

business = Business()

# region [Page Name Params]
all_team_failure_case_summary = 'All Team Failure Case Summary'
faluire_insights = 'Failure Insights'
# endregion [Page Name Params]

# region [Sidebar]
streamlit.sidebar.title('')
page = streamlit.sidebar.radio(
    'Navigation',
    options=[
        all_team_failure_case_summary,
        faluire_insights
    ],
    index=0 # default page
)
# endregion [Sidebar]

# region [Failure Count by Service Team]
if page == all_team_failure_case_summary:

    streamlit.header(all_team_failure_case_summary)
    today = datetime.date.today()
    last_seven_day = today - datetime.timedelta(days=7)

    stard_date, end_date = streamlit.columns(2)

    with stard_date:
        start_date = streamlit.date_input('📅 Start date', value='2025-09-01')  # last_seven_day

    with end_date:
        end_date = streamlit.date_input('📅 End date', value='2025-09-05')  # today

    dataframe = business.get_failure_summary_grouped_by_service(start_date=start_date, end_date=end_date)

    if dataframe.empty:
        streamlit.warning('No failure data found.')
    else:
        figure = plotly.bar(
            data_frame=dataframe,
            x='service_team',
            y='fail_count',
            color='service_team',
            color_discrete_sequence=plotly.colors.qualitative.Pastel2,
            title=f'{start_date} - {end_date}',
            text='fail_count'
        )
        figure.update_layout(showlegend=False)
        streamlit.plotly_chart(figure_or_data=figure, use_container_width=True)

# endregion [Failure Count by Service Team]
