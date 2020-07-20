# Example
# (INPUT)
# [
#     {
#         "pricing": "Room booking for 3 hours minimum spending should be SGD250++",
#          "dayOfWeek": "Wed-Sat",
#          "time": "07:00 - 23:00"
#      },
#      {
#          "pricing": "Room booking for 3 hours minimum spending should be SGD250++",
#           "dayOfWeek": "Holidays",
#           "time": "07:00 - 23:00"
#       }
# ]

# The function below will convert the price object above to below
# (OUTPUT)
# [{'pricing': 'Room booking for 3 hours minimum spending should be SGD250++', 'dayOfWeek': 'Wednesday', 'time': '07:00 - 23:00'},
# {'pricing': 'Room booking for 3 hours minimum spending should be SGD250++', 'dayOfWeek': 'Thursday', 'time': '07:00 - 23:00'},
# {'pricing': 'Room booking for 3 hours minimum spending should be SGD250++', 'dayOfWeek': 'Friday', 'time': '07:00 - 23:00'},
# {'pricing': 'Room booking for 3 hours minimum spending should be SGD250++', 'dayOfWeek': 'Saturday', 'time': '07:00 - 23:00'},
# {'pricing': 'Room booking for 3 hours minimum spending should be SGD250++', 'dayOfWeek': 'Holidays', 'time': '07:00 - 23:00'}]

def FormatPrice(allPricing):
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday", "Holidays"]
    MAP_DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday",
                "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
    allPricingWithAppendedObj = []
    for priceObj in allPricing:
        day = priceObj["dayOfWeek"]
        pricing = priceObj["pricing"]
        time = priceObj["time"]
        if(not day in DAYS):
            # inputs are assumed to be date range: XX - YY
            days = day.split("–")
            if(len(days) == 2):
                start = days[0]
                end = days[1]
                continueFinding = False
                for key, value in MAP_DAYS.items():
                    if(key == start):
                        continueFinding = True
                    if(continueFinding == True):
                        allPricingWithAppendedObj.append({
                            "pricing": pricing,
                            "dayOfWeek": value,
                            "time": time
                        })
                    if(key == end):
                        break
            else:
                # Convert day to long form
                try:
                    allPricingWithAppendedObj.append({
                        "pricing": pricing,
                        "dayOfWeek": MAP_DAYS[day],
                        "time": time
                    })
                except:
                    # Unable to format data. Returning original.
                    allPricingWithAppendedObj.append(priceObj)
        else:
            allPricingWithAppendedObj.append(priceObj)
    return allPricingWithAppendedObj
