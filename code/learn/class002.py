# Lesson 2: Unit Converter
# Build a simple unit converter for common measurements

# Temperature conversion: Celsius to Fahrenheit
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"{celsius}°C = {fahrenheit}°F")

# Distance conversion: kilometers to miles
kilometers = 10
miles = kilometers * 0.621371
print(f"{kilometers} km = {miles:.2f} miles")

# Weight conversion: kilograms to pounds
kilograms = 50
pounds = kilograms * 2.20462
print(f"{kilograms} kg = {pounds:.2f} lbs")

# Time conversion: minutes to hours and minutes
total_minutes = 135
hours = total_minutes // 60
remaining_minutes = total_minutes % 60
print(f"{total_minutes} minutes = {hours} hours and {remaining_minutes} minutes")

# Challenge: Add a conversion for centimeters to inches (1 inch = 2.54 cm)
# Convert 100 cm to inches
