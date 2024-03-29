from faker import Faker
import random
import pandas as pd
from datetime import timedelta

# Initialize a Faker instance from Australia
fake = Faker('en_AU')

# Pre-defined locations in Melbourne, Victoria
loc = ['Carlton', 'Docklands', 'East Melbourne', 'Kensington', 'North Melbourne',
        'Parkville', 'Southbank', 'West Melbourne', 'Port Melbourne', 'South Wharf']

def impact_probability(driver_score, avg_speed):
    # Impact probability based on driver score (lower score leads to higher probability)
    prob_driver_score = (5 - driver_score) * 0.15

    # Impact probability based on average speed (higher speed leads to higher probability)
    prob_avg_speed = (avg_speed - 20) * 0.01

    # Combine both probabilities
    return prob_driver_score + prob_avg_speed

def data_gen(n=110):
    data = []
    for _ in range(n):
        start_location = random.choice(loc)
        end_location = random.choice(loc)
        while start_location == end_location:
            end_location = random.choice(loc)

        start_time = fake.date_time_this_decade()
        duration = timedelta(minutes=random.randint(5, 120)) # Random trip duration between 5 and 120 minutes
        end_time = start_time + duration

        driver_name = fake.name()
        driver_score = round(random.uniform(1, 5), 2) # Random driver score between 1-5
        avg_speed = round(random.uniform(20, 120), 2) # Random avg speed between 20kmph-120kmph

        # Calculate impact based on the probability function
        impact_prob = impact_probability(driver_score, avg_speed)
        impact = random.random() < impact_prob

        violations = bool(random.getrandbits(1)) 

        # Adjusting driver's score based on violations and impact
        if impact:
            driver_score = driver_score - (driver_score * 0.10) # Decrease score by 10% for impact
        if violations:
            driver_score = driver_score - (driver_score * 0.05) # Decrease score by 5% for violation

        # Make sure the score does not fall below 0
        driver_score = round(max(0, driver_score), 2)

        vehincle_health_perc = round(random.uniform(0, 100), 2) # Vehicle health as a percentage
        if vehincle_health_perc >= 70:
            vehicle_health = 'Good'
        elif 25 < vehincle_health_perc < 70:
            vehicle_health = 'Okay'
        else:
            vehicle_health = 'Urgent'

        trip_date = start_time.date()

        data.append([start_location, end_location, start_time, end_time, duration.total_seconds()/60, driver_name, 
                     driver_score, avg_speed, impact, violations, vehicle_health, trip_date])
        
    df = pd.DataFrame(data, columns=['Start_Location','End_Location', 'Start_Time', 'End_Time', 'Trip_Duration(min)',
                                 'Driver_Name', 'Driver_Score', 'Average_Speed(km/h)', 'Impact', 'Driving_Violations',
                                 'Vehicle_Health', 'Trip_Date'])
    
    return df
        
    
df = data_gen()

# Saving the data (You can update the paths accordingly)
df.to_csv('./Data/indiumSamp.csv', index=False)
df.to_excel('./Data/indiumSamp.xlsx', index=False)

# Returning a preview of the data
df.head()
