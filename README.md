# zoe-ha
Setting up ZOE and Home Assistant 

Most of the code comments and variables are in RO language so not much help there

What get_data_new.py does is:
 - creates a basic json reponse (is a string but parsed as json by HA)
 - checks whether you are charging at home or not and increments accordingly
 - does basic calculations based on the mileage and kw consumed
 - will query the db for x days ago (parameter)
 - is fast

Sample output:

![alt text](https://raw.githubusercontent.com/ionmirceamarian/zoe-ha/main/img/ha.JPG)


In order to get to this point you will need to modify your configuration.yaml in Home Asstant

add:
```
sensor:
  - platform: command_line
    scan_interval : 3600
    command_timeout : 60
    name: car_data_7
    json_attributes:
      - kw_7
      - bani_7
      - kw_deplasare_7
      - km_parcursi_7
      - consum_kw_7
      - consum_kw_km_7
    command: " python3 get_data_new.py --dbfile='home-assistant_v2.db' --days=7 "
    value_template: "{{ value_json }}"

  - platform: command_line
    scan_interval : 3600
    command_timeout : 60
    name: car_data_30
    json_attributes:
      - kw_30 
      - bani_30
      - kw_deplasare_30
      - km_parcursi_30
      - consum_kw_30
      - consum_kw_km_30
    command: " python3 get_data_new.py --dbfile='home-assistant_v2.db' --days=30"
    value_template: "{{ value_json }}"


  - platform: command_line
    scan_interval : 3600
    command_timeout : 60
    name: car_data_999
    json_attributes:
      - kw_999
      - bani_999
      - kw_deplasare_999
      - km_parcursi_999
      - consum_kw_999
      - consum_kw_km_999
    command: " python3 get_data_new.py --dbfile='home-assistant_v2.db' --days=999 "
    value_template: "{{ value_json }}"


```

i have created a demo configuration.yaml file, you can use parts of it if you need.

You can change the price by adding the "--price=x.x" parameter (default is ~1).

You can change the battery size by adding the "--battery_kwh=50" (default is 40) parameter.

I have used the docker image for Home Assistant so the below might not apply to you.

You will need to copy get_data_new.py in your /PATH_TO_YOUR_CONFIG/ folder

it should be in the same place with the home assistant db file home-assistant_v2.db

HA dashboard config:

```
  - path: Car
    title: Car
    panel: true
    icon: mdi:car
    theme: ''
    badges: []
    cards:
      - type: horizontal-stack
        cards:
          - type: vertical-stack
            cards:
              - type: entities
                entities: []
                title: Ultimele 7 zile
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_7
                    attribute: kw_7
                    unit: Kw
                    name: Incarcat acasa
                    style: |
                      ha-card {
                        --ha-card-background: grey;
                        color: var(--primary-color);
                      }
                    icon: mdi:power-plug
                  - type: entity
                    entity: sensor.car_data_7
                    attribute: kw_deplasare_7
                    unit: Kw
                    name: Incarcat deplasare
                    style: |
                      ha-card {
                        color: grey;
                      }
                    icon: mdi:power-plug
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_7
                    attribute: consum_kw_7
                    unit: Kw
                    name: Kw consumati
                    icon: mdi:power-plug
                  - type: entity
                    entity: sensor.car_data_7
                    attribute: km_parcursi_7
                    unit: Km
                    name: Km Parcursi
                    style: |
                      ha-card {
                        --ha-card-background: black;
                        color: var(--primary-color);
                      }
                    icon: mdi:car
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_7
                    attribute: consum_kw_km_7
                    name: Kw/ 100 Km
                    icon: mdi:car
                  - type: entity
                    entity: sensor.car_data_7
                    attribute: bani_7
                    name: Cost
                    unit: Lei
                    icon: mdi:currency-usd
          - type: vertical-stack
            cards:
              - type: entities
                entities: []
                title: Ultimele 30 zile
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_30
                    attribute: kw_30
                    unit: Kw
                    name: Incarcat acasa
                    style: |
                      ha-card {
                        --ha-card-background: grey;
                        color: var(--primary-color);
                      }
                    icon: mdi:power-plug
                  - type: entity
                    entity: sensor.car_data_30
                    unit: Kw
                    name: Incarcat deplasare
                    style: |
                      ha-card {
                        color: grey;
                      }
                    icon: mdi:power-plug
                    attribute: kw_deplasare_30
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_30
                    attribute: consum_kw_30
                    unit: Kw
                    name: Kw consumati
                    icon: mdi:power-plug
                  - type: entity
                    entity: sensor.car_data_30
                    unit: Km
                    name: Km Parcursi
                    style: |
                      ha-card {
                        --ha-card-background: black;
                        color: var(--primary-color);
                      }
                    icon: mdi:car
                    attribute: km_parcursi_30
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_30
                    name: Kw/ 100 Km
                    icon: mdi:car
                    attribute: consum_kw_km_30
                  - type: entity
                    entity: sensor.car_data_30
                    name: Cost
                    unit: Lei
                    attribute: bani_30
                    icon: mdi:currency-usd
          - type: vertical-stack
            cards:
              - type: entities
                entities: []
                title: Total
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_999
                    attribute: kw_999
                    unit: Kw
                    name: Incarcat acasa
                    style: |
                      ha-card {
                        --ha-card-background: grey;
                        color: var(--primary-color);
                      }
                    icon: mdi:power-plug
                  - type: entity
                    entity: sensor.car_data_999
                    unit: Kw
                    name: Incarcat deplasare
                    style: |
                      ha-card {
                        color: grey;
                      }
                    icon: mdi:power-plug
                    attribute: kw_deplasare_999
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_999
                    unit: Kw
                    name: Kw consumati
                    icon: mdi:power-plug
                    attribute: consum_kw_999
                  - type: entity
                    entity: sensor.car_data_999
                    unit: Km
                    name: Km Parcursi
                    style: |
                      ha-card {
                        --ha-card-background: black;
                        color: var(--primary-color);
                      }
                    icon: mdi:car
                    attribute: km_parcursi_999
              - type: horizontal-stack
                cards:
                  - type: entity
                    entity: sensor.car_data_999
                    name: Kw/ 100 Km
                    icon: mdi:car
                    attribute: consum_kw_km_999
                  - type: entity
                    entity: sensor.car_data_999
                    name: Cost
                    unit: Lei
                    attribute: bani_999
                    icon: mdi:currency-usd
          - type: vertical-stack
            cards:
              - type: entities
                entities:
                  - entity: sensor.mileage
                    name: Kilometraj
              - type: entities
                entities:
                  - entity: sensor.battery_level
              - type: history-graph
                entities:
                  - entity: sensor.battery_level
                hours_to_show: 168
                refresh_interval: 0
              - type: horizontal-stack
                cards:
                  - type: custom:apexcharts-card
                    header:
                      show: true
                      title: Consum 7 zile
                      show_states: true
                      colorize_states: true
                    series:
                      - entity: sensor.car_data_7
                        attribute: consum_kw_km_7
                        name: ...
                        unit: Kw / 100 Km

```

