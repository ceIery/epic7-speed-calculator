"""
Given a base speed value and a list of percentages, calculates the speed value
for each percentage
"""
def get_speeds(percents, base):
    speeds = []
    for percent in percents:
        speeds.append(round(((int)(base) * ((int)(percent) / 100))))

    print(speeds)
    return speeds
