from twitter_news import trends_and_volumes, location_to_woeid
from matplotlib import pyplot as plt
import numpy as np
location = input('Please enter a woeid or location: ')
if not location.isnumeric():
    try:
        location = location_to_woeid(location)
    except:
        raise ValueError("This is not a valid location")
trends = []
volume = []
values = trends_and_volumes(location)
for key in values.keys():
    if values[key] is not None:
        trends.append(key)
    else:
        trends.append(key)

for value in values.values():
    if value is not None:
        volume.append(value)
    else:
        volume.append(0)

print(trends, volume)

fig, ax = plt.subplots()
ax.set_yticklabels(trends)
y_pos = np.arange(len(trends))
graph = plt.barh(y_pos, volume)
plt.show()



