#Intents

AMAZON.CancelIntent
AMAZON.StopIntent
- Close session

LaunchRequest
AMAZON.HelpIntent
- Welcome to pollen count, you can request the pollen count for your current location by saying, "give me an update". You can also ask for the count anywhere in the UK by asking "what the pollen count is in Glasgow". 
- Leave the session open. 

HomeRequestIntent
- Lookup location of originating device
- PollenCount(City)
LocationRequestIntent
- Lookup location of provided device
- PollenCount(City)

PollenCount(City)
- Convert to lat long
- Find pollen count
- The pollen count in {Location} is {pollen_count}
- Close session

Need a service to convert an address to lat + long:
https://developer.yahoo.com/geo/placefinder/

Use pypollen
https://github.com/kylegordon/pypollen

pip install pypollen