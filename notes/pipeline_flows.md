# METAR Station Data Processing

[Mermaid.js basic syntax](https://mermaid-js.github.io/mermaid/#/./flowchart?id=flowcharts-basic-syntax)

## Raw Data Pipeline
```mermaid
flowchart TD;
    A[fetch_monthly_data];
    A --> B0([Station Info]);
    B0 --> B1{check_station_exists};
    B1 --> |Yes| B2((Pipeline End));
    B1 --> |No| B3[build_station_details];
    B3 --> B4[(load station to DB)];
    B4 --> B2;
    B2 --> C0([Obs Dates]);
    C0 --> C0A[Load station from DB];
    C0A --> C1[build_station_observation_dates];
    C1 --> C2[add_sunrise_sunset_to_dates];
    C2 --> C3[calc_num_daylight_hours];
    C3 --> C4[weekday or weekend];
    C4 --> C5[(load dates to DB)];
    C5 --> C6((Pipeline End));
    A --> D0([Obs Features]);
    D0 --> D1[add_observation_features];
```

## Hour Aggregation Pipeline
```mermaid
flowchart TD;
    A([Resample Hourly]);
```

## VFR Suitable Pipeline
```mermaid
flowchart TD;
    A[Load Hourly Data];
    A --> B0([Features]);
    B0 --> B1[weather_check];
    B0 --> B2[time of day check];
    B0 --> B3[visibility check];
    B0 --> B4[wind check];
    B0 --> B5[icing check];
    B1 & B2 & B3 & B4 & B5--> B8[Is VFR Suitable];
    B8 --> B9((Pipeline End));
```
