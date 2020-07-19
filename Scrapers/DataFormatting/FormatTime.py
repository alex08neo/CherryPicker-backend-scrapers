# Convert a time string of the time range format, eg XX:XXam-YY:YYPM
# into 24 HOURS TIME FORMAT eg, 24:00, 12:00, 03:00
#
# Example input strings:
# 9.00AM – 12.00AM
# 11:30AM – 10:30PM
# 8am – any time

# 9am  – 1130pm
# 11am – 0130am
# 9am  – 1130pm
# 07 AM – 11 PM
# 0900 – 0300
# 12 – 12


def fix(time):
    try:
        # Check if the values are digits
        if(not time.replace("am", "").replace("AM", "").replace(
                "pm", "").replace("PM", "").replace(":", "").replace(".", "").strip().isdigit()):
            return False

        # Handle separator
        time = time.replace(".", ":")
        if(":" in time):
            if("AM" in time or "am" in time):
                # Check if need append 0s
                dotTime = time.split(":")
                if(len(dotTime[0]) == 1):
                    time = "0"+time
                elif(int(dotTime[0]) == 12):  # Special case: 12am
                    time = "24:00"
                time = time.replace("am", "").replace("AM", "")
            elif("PM" in time or "pm" in time):
                # Check if need append 0s
                dotTime = time.split(":")
                firstDotTime = int(dotTime[0])
                secondDotTime = dotTime[1]
                if(firstDotTime < 12):
                    firstDotTime += 12
                time = str(firstDotTime)+":" + \
                    secondDotTime.replace("pm", "").replace("PM", "")
            # IF there isnt any am or pm, we assume that timing is alrdy in 24 hours format
        else:
            # Convert to 4 digits
            isPM = "PM" in time or "pm" in time
            isAM = "AM" in time or "am" in time
            time = time.replace("am", "").replace("AM", "").replace(
                "pm", "").replace("PM", "").strip()
            if(len(time) == 3):
                time = "0"+time
            elif(len(time) == 2):
                time = time+"00"
            elif(len(time) == 1):
                time = "0"+time+"00"
            # Adjust values according to pm am
            if(isPM and int(time[0:2]) < 12):
                time = str(int(time[0:2])+12)+":"+time[2:4]
            elif(isAM and int(time[0:2] == 12)):
                time = "24:00"
            else:
                time = time[0:2]+":"+time[2:4]

        return time.strip()
    except:
        print("Error in formatting time "+str(time))
        return False


def FormatTime(time):
    # Split by dash
    time = time.split("–")
    if(len(time) != 2):
        # Split by another type of dash
        time = time[0].split("-")
    if(len(time) != 2):
        return "Inquire for timing availabilities"

    first = fix(time[0])
    second = fix(time[1])

    if(first == False and second == False):
        return "Inquire for timing availabilities"
    if(first == False):
        return second+" - "+second
    elif(second == False):
        return first+" - "+first
    return first+" - "+second
