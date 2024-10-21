from java.util import Calendar, TimeZone, GregorianCalendar

def SecondsToHoursAndMinutes(value):
    # Transform value in seconds to a string showing hours and minutes only

    hours = (value // 3600) % 24  # Modulo 24 to reset hours after every full day
    minutes = (value % 3600) // 60
    
    # Format the time components to a string with zero-filled hours and minutes
    time_components = str(hours) + ":" + str(minutes).zfill(2)
    
    return time_components
    
def SecondsToHoursMinutesSeconds(value):
    # Transform value in seconds to a string showing hours, minutes, and seconds

    hours = value // 3600  # Total hours
    minutes = (value % 3600) // 60  # Remaining minutes after subtracting hours
    seconds = value % 60  # Remaining seconds after subtracting hours and minutes

    # Format the time components to a string with zero-filled hours, minutes, and seconds
    time_components = "{}:{}:{}".format(str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2))
    
    return time_components
    
def SecondsMinutesSeconds(value):
    # Transform value in seconds to a string showing minutes and seconds

    minutes = value // 60  # Total minutes
    seconds = value % 60  # Remaining seconds after converting to minutes

    # Format the time components to a string with zero-filled minutes and seconds
    time_components = "{}:{}".format(str(minutes).zfill(3), str(seconds).zfill(2))
    
    return time_components
    
	
def get_local_dt(dt,local_timezone):

	# Get the TimeZone object for local timezone
	tz = TimeZone.getTimeZone(local_timezone)
	
	# Convert to milliseconds since epoch if not already
	if (str(type(dt)) == "<type 'java.sql.Timestamp'>"):
		utcMillis = system.date.toMillis(dt)
	else:
	    utcMillis = dt
	    
	# Create a calendar object for UTC timezone
	utcCalendar = GregorianCalendar(TimeZone.getTimeZone("GMT"))
	utcCalendar.setTimeInMillis(utcMillis)
	
	# Determine the offset from UTC at the given date/time
	offset = tz.getOffset(utcCalendar.getTimeInMillis())
	
	# Apply the offset directly to the UTC milliseconds
	local_dt = utcCalendar.getTimeInMillis() + offset
	
	return local_dt
	
