#Development

```bash
python3 -m venv env
pip install pytest
pip install mock
```

#Running

```bash
pip install -r requirements.txt
```

## Intents

[x] AMAZON.CancelIntent
[x] AMAZON.StopIntent
[x] LaunchRequest
[x] AMAZON.HelpIntent
[] HomeRequestIntent
[x] LocationRequestIntent

## Helper Functions
GetCity(Device)
[] Look up city or postcode of originating device

PollenCount(City)
[] Convert city or postcode to lat long
[x] Find pollen count from lat long

### Information
Need a service to convert an address to lat + long:
https://developer.yahoo.com/geo/placefinder/

Use pypollen
https://github.com/kylegordon/pypollen