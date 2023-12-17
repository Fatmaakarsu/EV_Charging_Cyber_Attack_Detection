import random
import time

class ChargingStation:
    def __init__(self, cs_id, location, capacity):
        self.cs_id = cs_id
        self.location = location
        self.capacity = capacity
        self.available_slots = capacity
        self.last_access_time = time.time()

    def check_traffic_anomaly(self):
        current_time = time.time()
        time_diff = current_time - self.last_access_time

        if time_diff < 5 and self.available_slots < 3:
            print(f"Anomaly detected at CS {self.cs_id} in {self.location}. Possible DoS or DDoS attack.")

class ElectricVehicle:
    def __init__(self, ev_id, location, model, charging_time):
        self.ev_id = ev_id
        self.location = location
        self.model = model
        self.charging_time = charging_time

class GridStation:
    def __init__(self):
        self.cs_list = []

def create_simulation_environment(cs_data, ev_data):
    grid_station = GridStation()

    for cs_info in cs_data:
        cs = ChargingStation(cs_id=cs_info["cs_id"], location=cs_info["location"], capacity=cs_info["capacity"])
        grid_station.cs_list.append(cs)

    ev_list = [ElectricVehicle(ev_id=ev_info["ev_id"], location=ev_info["location"], model=ev_info["model"], charging_time=ev_info["charging_time"]) for ev_info in ev_data]

    return grid_station, ev_list

def simulate_charging(grid_station, ev_list):
    suspect_vehicles = []  # Şüpheli araçları saklamak için bir dizi

    for ev in ev_list:
        selected_cs = random.choice(grid_station.cs_list)

        if selected_cs.available_slots > 0:
            print(f"EV {ev.ev_id} (Model: {ev.model}) charging at CS {selected_cs.cs_id} in {selected_cs.location} for {ev.charging_time} minutes")
            selected_cs.available_slots -= 1
            selected_cs.last_access_time = time.time()
            selected_cs.check_traffic_anomaly()

            if ev.charging_time > 60:
                suspect_vehicles.append(ev.ev_id)

            time.sleep(random.uniform(1, 5))
            selected_cs.available_slots += 1
        else:
            print(f"No available slots at CS {selected_cs.cs_id} in {selected_cs.location} for EV {ev.ev_id}")

    return suspect_vehicles  # Şüpheli araçları döndür

if __name__ == "__main__":
    # Güncellenmiş veri seti
    cs_data = [
        {"cs_id": "CS1", "location": "Downtown", "capacity": 5},
        {"cs_id": "CS2", "location": "Suburb", "capacity": 5},
        {"cs_id": "CS3", "location": "Airport", "capacity": 5}
    ]
    ev_data = [
        {"ev_id": "EV1", "location": "Downtown", "model": "Model1", "charging_time": random.randint(30, 100)},
        {"ev_id": "EV2", "location": "Suburb", "model": "Model2", "charging_time": random.randint(30, 100)},
        {"ev_id": "EV3", "location": "Airport", "model": "Model3", "charging_time": random.randint(30, 100)},
        {"ev_id": "EV4", "location": "Downtown", "model": "Model4", "charging_time": random.randint(30, 100)},
        {"ev_id": "EV5", "location": "Suburb", "model": "Model5", "charging_time": random.randint(30, 100)}
    ]

    simulation_grid, evs = create_simulation_environment(cs_data, ev_data)

    suspect_vehicles = simulate_charging(simulation_grid, evs)

    print("\nAll Electric Vehicles:")
    for ev in evs:
        print(f"EV {ev.ev_id} (Model: {ev.model}) - Charging time: {ev.charging_time} minutes")

    if suspect_vehicles:
        print("\nWarning: Charging time more than 60 minutes! Suspect Vehicles:", ", ".join(suspect_vehicles))
    else:
        print("\nNo suspect vehicles detected.")
