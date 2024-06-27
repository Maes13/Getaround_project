import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.subplots as sp
from plotly.subplots import make_subplots
import json
import statsmodels.api as sm




### Config
st.set_page_config(page_title="My_app_delay_getaround", page_icon="", layout="wide")

delay_df = pd.read_excel('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx',sheet_name='rentals_data')
pricing = pd.read_csv('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv',index_col=0)
pricing = pricing[pricing['mileage'] >= 0]
pricing = pricing[pricing['engine_power'] > 0]


# ---------------------------------------   MENU DEROULANT    -------------------------------------- # 

if __name__ == '__main__': 

    with st.sidebar:
        selected = option_menu("Menu", ["Home", 'Goals','Delays EDA'], 
            icons=['house', 'archive','alarm','activity','app-indicator'], menu_icon="car-front-fill", default_index=0)
        selected

# ---------------------------------------   HOME    -------------------------------------- # 

    if selected == 'Home':
        st.image('photo.jpg')
        st.markdown("<h1 style='text-align: center; color: white;'> Delving into Car Rental Data for Strategic Insights </h1>", unsafe_allow_html=True)
        # st.markdown("<h3 style='text-align: center; color: white;'> The new Airbnb for cars ! </h3>", unsafe_allow_html=True)
        # st.markdown("---")

        st.markdown("---")
        st.write('')
        col1, col2 = st.columns([1,2])
    
        with col1:
            st.write("")
            st.subheader("Get a what ?")
            st.write("")
            st.write("""GetAround is the Airbnb for cars, allowing individuals to rent cars from each other for a few hours or days.

Founded in 2009, the company has rapidly expanded, boasting over 5 million users and approximately 20,000 cars available worldwide as of 2019.

Concept:
GetAround simplifies peer-to-peer car rentals, making vehicle access easier and more economical without the need for traditional rental agencies. Owners can monetize their idle cars by renting them out through the platform.

The company has presented us with this significant challenge:""")
            st_lottie("https://assets9.lottiefiles.com/packages/lf20_eP48EC.json",key='tuture')

        with col2:
            st.write("")
            st.subheader("Context")
            st.write("")
            st.write("""During the car rental process, our users must complete a check-in at the beginning and a check-out at the end of the rental to:

Assess the car's condition and inform the involved parties of any pre-existing damages or damages that occurred during the rental.
Compare fuel levels.
Measure the distance traveled in kilometers.
The check-in and check-out for our rentals can be conducted through three distinct processes:

📱 Mobile rental contract on native apps: The driver and the owner meet, and both sign the rental contract on the owner's smartphone.
Connect: The driver does not meet the owner and unlocks the car using their smartphone.
📝 Paper contract.""")

        st.markdown("---")
        st.write("")
        st.subheader("Projet ")
        st.write("")
        st.write("""In this case study, we invite you to put yourself in our shoes and conduct an analysis 🔮 🪄

With Getaround, drivers reserve cars for a specified period, ranging from one hour to several days. They are expected to return the car at the scheduled time, but sometimes drivers are late for the check-out.

Late returns at check-out can cause numerous inconveniences for the next driver if the car was supposed to be rented again the same day: customer service frequently receives complaints from unhappy users because they had to wait for the car to return from the previous rental, or even from users who had to cancel their rental because the car was not returned on times..""")
        
        st.markdown("---")

# ---------------------------------------   PAGE DE CONSIGNES      -------------------------------------- #  

    if selected == 'Goals':
        st.markdown("<h1 style='text-align: center; color: white;'>Goals for the project</h1>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown(" ")
        col1, col2 = st.columns([3,2])
        with col1:
            st.write("""
        To mitigate these issues, we have decided to implement a minimum time gap between two rentals. A car will not be displayed in the search results if the requested check-in or check-out times are too close to an already booked rental.

While this addresses the problem of late returns, it could potentially impact the revenues of Getaround and the owners: we need to strike the right balance.

Our Product Manager still needs to make a decision:""") 
        with col2:
            st_lottie("https://assets9.lottiefiles.com/private_files/lf30_hsabbeks.json", key="contrat_voiture")
        col1, col2,col3,col4 = st.columns([1,1,1,1])
        with col2:
            st.subheader("""THRESHOLD: 
What should be the minimum duration of the gap?""")
        with col3:
            st.subheader("""SCOPE:
Should we enable this feature for all cars or only for Connect cars?""")
        st.markdown(" ")
        st.write("""To assist them in making the right decision, they are asking you for information and analyses. Here are the initial analyses they have considered to start the discussion. Feel free to conduct additional analyses that you deem relevant:

- What proportion of our owners' revenues would potentially be affected by this feature?
- How many bookings would be impacted by the feature based on the threshold and scope we choose?
- How often are drivers late for the next check-in? What is the impact on the next driver?
- How many problematic cases will the feature resolve based on the chosen threshold and scope?""")

        st.markdown("---")

        col1,col2 = st.columns([1,2])
        with col1:
            st.button('Web dashboard',key='Web dashboard')
            st.write("Tout d'abord, construisons un tableau de bord qui aidera l'équipe de gestion de produit avec les questions mentionnées ci-dessus. Vous pouvez utiliser Streamlit ou toute autre technologie que vous jugez appropriée..")
            st_lottie('https://assets6.lottiefiles.com/packages/lf20_acryqbdv.json',key='dashboard')

        with col2:
            st.button('Machine learning',key='Machine learning')
            st.write("""
In addition to the question above, the Data Science team is working on price optimization. They have collected data to suggest optimal prices for car owners using machine learning.

You need to provide at least one endpoint /predict. The full URL would look something like this: https://your-url.com/predict.

This endpoint accepts the POST method with input data in JSON format and should return predictions.
""")
        st.markdown("---")

# ---------------------------------------   EDA DELAYS      -------------------------------------- #  

    if selected == "Delays EDA":
        st.markdown("<h1 style='text-align: center; color: white;'>Exploratory Data Analysis - DELAYS</h1>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown(" ")


        st.markdown("<h2 style='text-align: center; color: white;'>Overview of delays</h2>", unsafe_allow_html=True)

        st.write("The most important variable for us is the delay, which has missing values. We need to remove them.")
        delay_df.dropna(subset=['delay_at_checkout_in_minutes'],inplace=True)
        st.write(f"We remove the variable 'state', since there is only {len(delay_df[delay_df['state']=='canceled'])} canceled rental and the rest is all normal ended rentals.")
        delay_df.drop(columns="state")
        positive_delay_df = delay_df[delay_df['delay_at_checkout_in_minutes']>0]

        # We cannot use make_subplot in streamlit, and we cannot use sp.subplots for pies. 
        # We need to make separate pies though.

        # All users
        bins = [-float('inf'), 0, float('inf')]
        labels = ['Users on time or in advance', 'Delayed users']
        delay_bins = pd.cut(delay_df.delay_at_checkout_in_minutes, bins=bins, labels=labels)
        section_counts = delay_bins.value_counts()
        # Positive delays only
        bins = [0, 60, 120, 240, float('inf')]
        labels = ['0 to 1h', '1 to 2h', '2h to 4h','>7h']
        delay_bins_positive = pd.cut(positive_delay_df.delay_at_checkout_in_minutes, bins=bins, labels=labels)
        section_counts_positive = delay_bins_positive.value_counts()
        # Subplots & graphs
        specs = [[{'type': 'domain'}, {'type': 'domain'}]]
        fig = make_subplots(rows=1, cols=2, specs=specs, subplot_titles=['There are more delayed users than users on time','Most delayed users have less than 2h delay'])
        fig.add_trace(go.Pie(labels=section_counts.index, values=section_counts, textinfo='label+percent'),row=1, col=1)
        fig.add_trace(go.Pie(labels=section_counts_positive.index, values=section_counts_positive, textinfo='label+percent'),row=1, col=2)
        fig.update_layout(title='Repartition of delay at checkout', title_font=dict(size=20), showlegend=False)
        st.plotly_chart(fig)

        mean_delay = round(delay_df['delay_at_checkout_in_minutes'].mean())
        st.write(f"The average delay is of {mean_delay} minutes ({mean_delay/60} hours).")
        average_delay_for_positive_delay = round(positive_delay_df.delay_at_checkout_in_minutes.mean())
        median_delay_for_positive_delay = round(positive_delay_df.delay_at_checkout_in_minutes.median())
        st.write(f"The average delay of delayed people is of {average_delay_for_positive_delay} minutes ({round(average_delay_for_positive_delay/60)} hours).")
        st.write(f"The median is quite different because of extremes values: {median_delay_for_positive_delay} minutes ({round(median_delay_for_positive_delay/60)} hour).")

        # Create subplots
        fig = sp.make_subplots(rows=1, cols=3, subplot_titles=("Delay is extremely spread", "Users have 60min delay in average","Positive delay: 3h avg vs 1h median"))
        # First graph : Boxplot of delays
        boxplot = go.Box(y=delay_df['delay_at_checkout_in_minutes'],showlegend=False, marker=dict(color='blue'), name='')
        fig.add_trace(boxplot, row=1, col=1)
        fig.update_yaxes(title_text="Delay (minutes)", row=1, col=1)
        # Second graph : Histogram of delays
        histogram1 = go.Histogram(x=delay_df['delay_at_checkout_in_minutes'],showlegend=False, marker=dict(color='blue') )
        fig.add_trace(histogram1, row=1, col=2)
        fig.update_xaxes(title_text="Delay (minutes) zoomed in", range=[-400, 400], row=1, col=2)
        # Add average and its legend
        fig.add_shape(type="line",x0=mean_delay,y0=0,x1=mean_delay,y1=5000,line=dict(color="red", width=2, dash="dash"),row=1,col=2,)
        fig.add_trace(go.Scatter(x=[mean_delay], y=[0], mode="lines", name="Average delay all users (1h)", line=dict(color="red", width=2, dash="dash")), row=1, col=2)
        # Third graph : Histogram of positive delays
        histogram2 = go.Histogram(x=positive_delay_df['delay_at_checkout_in_minutes'],showlegend=False, marker=dict(color='blue'))
        fig.add_trace(histogram2, row=1, col=3)
        fig.update_xaxes(title_text="Delay (minutes) zoomed in", range=[0, 1000], row=1, col=3)
        # Add average and its legend
        fig.add_shape(type="line",x0=average_delay_for_positive_delay,y0=0,x1=average_delay_for_positive_delay,y1=7000,line=dict(color="green", width=2, dash="dash"),row=1,col=3)
        fig.add_trace(go.Scatter(x=[average_delay_for_positive_delay], y=[0], mode="lines", name="Average positive delays (3h)", line=dict(color="green", width=2, dash="dash")), row=1, col=3)
        # Add median and its legend
        fig.add_shape(type="line",x0=median_delay_for_positive_delay,y0=0,x1=median_delay_for_positive_delay,y1=7000,line=dict(color="yellow", width=2, dash="dash"),row=1,col=3)
        fig.add_trace(go.Scatter(x=[median_delay_for_positive_delay], y=[0], mode="lines", name="Median positive delays (1h)", line=dict(color="yellow", width=2, dash="dash")), row=1, col=3)
        fig.update_layout(title="Delay at Checkout",title_font=dict(size=20),legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),width=800)
        st.plotly_chart(fig)


        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: white;'>Impact of delays on next users</h2>", unsafe_allow_html=True)

        # DATA PREPARATION

        sorted_delay = delay_df.sort_values(by=['car_id', 'rental_id'])
        sorted_delay.head(100)
        # Create the column where we will put delay of the previous users:
        # delay['delay_of_previous_user'] = np.nan
        # For everyline, we look if there is a value in "previous_ended_rental_id" column:
        for index, row in sorted_delay.iterrows():
            previous_ended_rental_id = row['previous_ended_rental_id']
            if pd.notnull(previous_ended_rental_id):
        # if there is a value, we look for the corresponding "rental_id" in the table and retrieve the delay associated:
                previous_delay = sorted_delay.loc[sorted_delay['rental_id'] == previous_ended_rental_id, 'delay_at_checkout_in_minutes']
                if not previous_delay.empty:
                    sorted_delay.at[index, 'delay_of_previous_user'] = previous_delay.iloc[0]
        # Now we calculate the difference between the expected timegap between 2 rentals, and the delay of the 1st one.
        sorted_delay['delta_timegap_delay'] = sorted_delay['time_delta_with_previous_rental_in_minutes'] - sorted_delay['delay_of_previous_user']
        # Show table
        pd.set_option('display.max_rows', None)
        sorted_delay.head(10)
        # Check table: for car 159533, we see the delay has indeed been reported.

        # OVERVIEW OF TIMEGAPS

        # Analyzing time_delta_with_previous_rental_in_minutes
        st.write("Timegap is the time expected between 2 rentals.")
        df_timegaps = sorted_delay.dropna(subset='time_delta_with_previous_rental_in_minutes')
        st.write(f"This variable has only {len(df_timegaps)} values, so we create a new dataset df_timegaps")
        average_time_gap = df_timegaps['time_delta_with_previous_rental_in_minutes'].mean()
        # Distribution of time gaps
        fig = px.histogram(df_timegaps, x='time_delta_with_previous_rental_in_minutes')
        # Add the average line
        fig.add_trace(go.Scatter(x=[average_time_gap, average_time_gap],y=[0, 350],mode='lines',line=dict(color='red', dash='dash'),name='Average (5h)'))
        fig.update_layout(title="Distribution of Time Gaps planned between Consecutive Rentals",xaxis_title="Time Gap (minutes)",yaxis_title="Count",showlegend=True)
        st.plotly_chart(fig)
        st.write(f"In average, there is {round(average_time_gap / 60)}h time gap between consecutive rentals.")
        # Short turnaround times:
        short_turnaround = df_timegaps[df_timegaps['time_delta_with_previous_rental_in_minutes'] < 60]
        percentage_short_turnaround = 100 * len(short_turnaround) / len(df_timegaps)
        st.write(f"The most encountered situation is a short turnaround (less than 1h): {round(percentage_short_turnaround)}% of rentals with a timegap.")

        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: white;'>Problematic cases</h2>", unsafe_allow_html=True)


        st.write('Time gaps is the time expected between 2 planned rentals (check out and check in).')
        st.write("A problematic case would be when a car is delayed more than the expected timegap before the next rental.")
        # Distribution of delta (difference between the timegap and the previous user's delay)
        fig = px.histogram(df_timegaps, x='delta_timegap_delay',color='state')
        # Add the average line
        average_delta_timegap_delay = df_timegaps.delta_timegap_delay.mean()
        fig.add_trace(go.Scatter(x=[average_delta_timegap_delay, average_delta_timegap_delay],y=[0, 350],mode='lines',line=dict(color='yellow', dash='dash'),name=f'Average ({round(average_delta_timegap_delay/60)}h)'))
        # Update layout
        fig.update_layout(title="Distribution of delta timegap minus delay",title_font=dict(size=20),xaxis_title="Delta (Timegap - Previous user's delay) in minutes",yaxis_title="Count",showlegend=True)
        # Zoom in on x-axis
        fig.update_xaxes(range=[-2000, 2500])
        st.plotly_chart(fig)
        st.write(f"The difference between timegap and previous user's delay is generaly positive, which means not problematic.")
        st.write(f"The average of this delta is {round(average_delta_timegap_delay/60)}h.")
        
        # Exploration of problematic cases

        problematic_cases = df_timegaps[df_timegaps['delta_timegap_delay']<0]
        percentage_problematic_cases_from_timegaps = round (100 * len(problematic_cases) / len(df_timegaps))
        percentage_problematic_cases_from_all = round (100 * len(problematic_cases) / len(sorted_delay))
        st.write(f"Among {len(df_timegaps)} cases known of 2 subsequent rentals, {len(problematic_cases)} were problematic ({percentage_problematic_cases_from_timegaps}%), which is only {percentage_problematic_cases_from_all}% of all rentals.")
        st.write('Most problematic cases are due to a previous delay of the previous user of less than 2h.')
        # Proportion problematic cases
        labels_1_2 = ['Problematic', 'Not problematic']
        values1 = [len(problematic_cases), len(df_timegaps) - len(problematic_cases)]
        values2 = [len(problematic_cases), len(sorted_delay) - len(problematic_cases)]
        # Delay of previous user in problematic case
        bins = [0, 60, 120, float('inf')]
        labels_3 = ['Less than 1h', '1 to 2h', 'More than 2h']
        delay_bins = pd.cut(problematic_cases['delay_of_previous_user'], bins=bins, labels=labels_3)
        values3 = delay_bins.value_counts(sort=False)
        # Subplots
        specs = [[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]]
        fig = make_subplots(rows=1, cols=3, specs=specs, subplot_titles=(f"Problematic cases represent {percentage_problematic_cases_from_timegaps}% of Time Gaps", f"which is only {percentage_problematic_cases_from_all}% of all rentals", "Delay of Previous User in Problematic Cases"))
        fig.add_trace(go.Pie(labels=labels_1_2, textinfo='label+percent', values=values1), row=1, col=1)
        fig.add_trace(go.Pie(labels=labels_1_2, textinfo='label+percent', values=values2), row=1, col=2)
        fig.add_trace(go.Pie(labels=labels_3, textinfo='label+percent',values=values3), row=1, col=3)
        fig.update_layout(title='Problematic cases', title_font=dict(size=20), showlegend=False,width=800)
        st.plotly_chart(fig)


        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: white;'>Defining a threshold</h2>", unsafe_allow_html=True)


        st.write("Most delayed people have less than 1h delay.")
        st.write("And time gaps between 2 rentals are mostly less than 1h ")
        thresholds = [60,80,100,150,200]
        columns = ['threshold','rentals lost','rentals lost (perc. from timegaps)','rentals lost (perc. from all)','pb cases','pb cases (perc. from timegaps)']

        df_thresholds = []
        for threshold in thresholds:
            rentals_left_in_timegaps = df_timegaps[df_timegaps['time_delta_with_previous_rental_in_minutes'] > threshold]
            rentals_lost = len(df_timegaps) - len(rentals_left_in_timegaps)
            percentage_rentals_lost_in_timegaps = round(100 * rentals_lost / len(df_timegaps))
            percentage_rentals_lost_in_total = round(100 * rentals_lost / len(sorted_delay))
            df_problematic_cases = rentals_left_in_timegaps[rentals_left_in_timegaps['delta_timegap_delay'] < 0]
            problematic_cases_count = len(df_problematic_cases)
            percentage_problematic_cases_in_timegaps = round(100 * problematic_cases_count / len(df_timegaps), 1)
            data = {
                'threshold': threshold,
                'rentals lost': rentals_lost,
                'rentals lost (perc. from timegaps)': percentage_rentals_lost_in_timegaps,
                'rentals lost (perc. from all)': percentage_rentals_lost_in_total,
                'pb cases': problematic_cases_count,
                'pb cases (perc. from timegaps)': percentage_problematic_cases_in_timegaps
            }
            df_thresholds.append(data)
        df_thresholds = pd.DataFrame(df_thresholds,columns=columns)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        st.write(df_thresholds)
        st.write(f"If we choose 80 minutes threshold of timegap minimum between 2 rentals, we will loose 32% of rentals with timegaps (or 3% of total rentals).")
        st.write("However, this will eradicate almost all problematic cases (2.1% of rentals with timegaps compared to 11% before putting a threshold.)")


        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: white;'>Importance of checkin type</h2>", unsafe_allow_html=True)

        fig = sp.make_subplots(rows=1, cols=3, subplot_titles=["Number of contracts by check-in type", "Delays in minutes", "Delays in minutes zoomed-in"])
        # First subplot - Histogram
        histogram = go.Histogram(x=sorted_delay['checkin_type'])
        fig.add_trace(histogram, row=1, col=1)
        # Second subplot - Box plot
        box_plot = go.Box(x=sorted_delay['checkin_type'], y=sorted_delay['delay_at_checkout_in_minutes'])
        fig.add_trace(box_plot, row=1, col=2)
        # Third subplot - Box plot with updated y-axis range
        box_plot_range = go.Box(x=sorted_delay['checkin_type'], y=sorted_delay['delay_at_checkout_in_minutes'])
        fig.add_trace(box_plot_range, row=1, col=3)
        # Update y-axis range for the third subplot
        fig.update_yaxes(range=[-300, 300], row=1, col=3)
        # Update layout with general title
        fig.update_layout(height=400, width=800, title="Impact of check-in type on delays",showlegend=False)
        st.plotly_chart(fig)
        st.write("There are more people subscribing by mobile than by connect app.")
        st.write("The delay for checkout is very spread for contract by mobile than the Connect app.")
        st.write("Generally, people do the checkout late when signing via mobile, and give back the car in advance when using the connect app.")
        
        # Impact of type of checkin on problematic cases
        checkin_type_counts = problematic_cases['checkin_type'].value_counts()
        fig = go.Figure(data=go.Pie(labels=checkin_type_counts.index, values=checkin_type_counts.values))
        fig.update_layout(title='Repartition of Problematic Cases by Check-in Type', title_font=dict(size=20),width=600)
        st.plotly_chart(fig)
        st.write("Most problematic cases are mostly from users using the mobile checkin.")
        st.write("The scope is the following: we will apply our threshold only for people suscribing via mobile.")
        
        
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: white;'>Final Threshold/Scope </h2>", unsafe_allow_html=True)

        # Recalculate lost rentals and problematic cases solved:
        threshold = 80
        scope = 'mobile'
        rentals_lost = len(df_timegaps[df_timegaps['checkin_type'] == scope][df_timegaps['time_delta_with_previous_rental_in_minutes'] < threshold])
        percentage_rentals_lost_in_timegaps = round(100 * rentals_lost / len(df_timegaps))
        percentage_rentals_lost_in_total = round(100 * rentals_lost / len(delay_df))
        df_problematic_cases = rentals_left_in_timegaps[rentals_left_in_timegaps['delta_timegap_delay']<0]
        problematic_cases_count = len(df_problematic_cases)
        percentage_problematic_cases_in_timegaps = round(100 * problematic_cases_count / len(df_timegaps) , 1)
        st.write(f"With a threshold of {threshold}min and a scope by {scope} suscription, we get a loss of {percentage_rentals_lost_in_timegaps}% rentals in timegaps, \nso {percentage_rentals_lost_in_total}% of total rentals. This would decrease problematic cases to {percentage_problematic_cases_in_timegaps}% for rentals with timegaps (compared \nto 11% initially).")
        
        # Money lost
        pricing_average = round(pricing.rental_price_per_day.mean())
        pricing_median = round(pricing.rental_price_per_day.median())
        st.write(f"Average price per day: {pricing_average}€, Median price per day: {pricing_median}€.")
        average_money_won = round(len(delay_df) * pricing_average)
        money_lost = round((2/100) * len(delay_df) * pricing_average)
        malus = round(money_lost / ((2/100) * len(delay_df)))
        st.write(f"With the chosen threshold and scope, we would loose {money_lost}€ per day.")
        st.write(f"If we don't want to loose money, we can make a malus of {malus}€ per person delayed per day.")
        st.write(f"Even though it's not reasonable, given the price of the rental per day.")
