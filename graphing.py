import seaborn as sns
import matplotlib
# Prevents async graph gen error
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
import base64

# Pulls column names from excel sheet
def getHeaders(graphData):
    graphData = BytesIO(graphData)
    return np.ndarray.tolist( pd.read_excel(graphData).columns.values);

# Read our CSV and convert it into a pandas dataframe
# data = pd.read_csv("./All tickets.csv")
def makeGraph(graphData, create, resolve, category):
    graphData = BytesIO(graphData)
    data = pd.read_excel(graphData)

    # Will be a dictionary with the key set to support type (ie Badge, KMES, Hardware, etch)
    # and the value will be set to an array where each entry is the amount of time it took to solve that problem
    support = {}

    format = "%m/%d/%Y, %I:%M %p"

    def is_previous_month(dt):
        # Get the current date
        current_date = datetime.now()
        
        # Calculate the date for the start of the previous month
        start_of_previous_month = current_date.replace(day=1) - timedelta(days=1)
        
        # Check if the datetime object is from the previous month
        return dt.year == start_of_previous_month.year and dt.month == start_of_previous_month.month


    # Fill the support dict with data
    for index, row in data.iterrows():
        support_type = row[category]
        created = row[create]
        solved = row[resolve]

        # Skip all entries that don't have a valid date time
        if type(created) is not str or type(solved) is not str:
            continue

        created = datetime.strptime(created, format)
        solved = datetime.strptime(solved, format)

        # Convert all nan type to create an "Uncategorized" string
        if type(support_type) is not str:
            support_type = "Uncategorized"

        # Find out how long it took to do
        time_delta = solved - created

        if is_previous_month(created):
            if support_type not in support.keys():
                support[support_type] = []
            support[support_type].append(time_delta)

    averages = {}

    # Creates a list of entries and finds the average number of hours spent on them
    for key in support.keys():
        averages[key] = 0
        for entry in support[key]:
            averages[key] = averages[key] + entry.total_seconds()  # Convert it to the number of hours it took to solve them

        averages[key] = averages[key] / len(support[key])

        averages[key] = averages[key] / (3600 * 24)

    # Quantitive Bar Graph Creation
    bar_values = []
    bar_keys = []

    size = len(averages.keys())

    for i in range(size):
        max_key = max(averages, key=lambda k: averages[k])
        max_value = averages[max_key]

        bar_keys.append(max_key)
        bar_values.append(max_value)

        del averages[max_key]

    sns.barplot(x=bar_values, y=bar_keys)

    plt.xlabel("Days")
    plt.ylabel("Categories")
    plt.title("Average Task Time")

    # Add the number of tickets to the left
    for index, value in enumerate(bar_keys):
        len_value = len(support[value])
        plt.text(bar_values[index], index, f"{len_value}", va="center")

    plt.xlim(0, max(bar_values) + 5)

    plt.subplots_adjust(left=0.35)

    # Saves the image to BytesIO object rather than saving it to the disk, saves read and right actions
    img_io = BytesIO()
    plt.savefig(img_io, format="png")
    img_io.seek(0)
    plt.close()

    img_io = base64.b64encode(img_io.getvalue()).decode("utf-8")
    return img_io
