import os
import random
from datetime import datetime, timedelta

# Define a list of cities in England
cities = ["London", "Manchester", "Birmingham", "Liverpool", "Leeds", "Sheffield", "Bristol", "Newcastle", "Nottingham", "Southampton"]

# Function to generate random times
def generate_random_time():
    start = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    end = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
    random_time = start + (end - start) * random.random()
    return random_time.strftime("%I:%M %p")

# Generate random departure data
departure_data = [
    {"City": random.choice(cities), "Train Station": f"{random.choice(cities)} Station", "Time": generate_random_time(), "Destination": random.choice(cities)}
    for _ in range(6)
]

# Generate random arrival data
arrival_data = [
    {"City": random.choice(cities), "Train Station": f"{random.choice(cities)} Station", "Time": generate_random_time(), "Origin": random.choice(cities)}
    for _ in range(6)
]

# HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Train Information for Cities in England</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 15px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Train Information for Cities in England</h1>
    <h2>Departures</h2>
    <table>
        <tr>
            <th>City</th>
            <th>Train Station</th>
            <th>Time</th>
            <th>Destination</th>
        </tr>
"""

# Add table rows for each departure
for train in departure_data:
    html_content += f"""
        <tr>
            <td>{train['City']}</td>
            <td>{train['Train Station']}</td>
            <td>{train['Time']}</td>
            <td>{train['Destination']}</td>
        </tr>
    """

html_content += """
    </table>
    <h2>Arrivals</h2>
    <table>
        <tr>
            <th>City</th>
            <th>Train Station</th>
            <th>Time</th>
            <th>Origin</th>
        </tr>
"""

# Add table rows for each arrival
for train in arrival_data:
    html_content += f"""
        <tr>
            <td>{train['City']}</td>
            <td>{train['Train Station']}</td>
            <td>{train['Time']}</td>
            <td>{train['Origin']}</td>
        </tr>
    """

# Close HTML tags
html_content += """
    </table>
</body>
</html>
"""

# Write HTML content to index.html
with open("index.html", "w") as file:
    file.write(html_content)

print("HTML file 'index.html' with random departures and arrivals has been created.")
