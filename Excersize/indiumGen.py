import pandas as pd
import random
from faker import Faker
from datetime import timedelta

# Initialize a Faker instance from Australia
fake = Faker('en_AU')

# Pre-defined locations in Melbourne, Victoria
loc = ['Carlton', 'Docklands', 'East Melbourne', 'Kensington', 'North Melbourne',
        'Parkville', 'Southbank', 'West Melbourne', 'Port Melbourne', 'South Wharf']

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

        impact = bool(random.getrandbits(1))
        violations = bool(random.getrandbits(1)) 

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

df.to_csv('./Data/indiumSamp.csv', index=False)
df.to_excel('./Data/indiumSamp.xlsx', index=False)


