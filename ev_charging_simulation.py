import random
import time

class ChargingStation:
    def __init__(self, cs_id, location):
        self.cs_id = cs_id
        self.location = location  # Şarj istasyonunun konumu
        self.available_slots = 5  # Her şarj istasyonunda 5 şarj yuvası
        self.last_access_time = time.time()  # Son erişim zamanı

    def check_traffic_anomaly(self):
        current_time = time.time()
        time_diff = current_time - self.last_access_time

        # Eğer belirli bir süre içinde çok sayıda erişim varsa, bu anormal bir durum olarak değerlendirilebilir.
        if time_diff < 5 and self.available_slots < 3:
            print(f"Anomaly detected at CS {self.cs_id} in {self.location}. Possible DoS or DDoS attack.")

class ElectricVehicle:
    def __init__(self, ev_id):
        self.ev_id = ev_id

class GridStation:
    def __init__(self):
        self.cs_list = []

def create_simulation_environment(num_cs, num_ev):
    grid_station = GridStation()

    locations = ["Downtown", "Suburb", "Airport", "Shopping Mall", "Residential Area"]

    for i in range(num_cs):
        cs = ChargingStation(cs_id=f"CS{i+1}", location=random.choice(locations))
        grid_station.cs_list.append(cs)

    ev_list = [ElectricVehicle(ev_id=f"EV{i+1}") for i in range(num_ev)]

    return grid_station, ev_list

def simulate_charging(grid_station, ev_list):
    for ev in ev_list:
        selected_cs = random.choice(grid_station.cs_list)

        if selected_cs.available_slots > 0:
            print(f"EV {ev.ev_id} charging at CS {selected_cs.cs_id} in {selected_cs.location}")
            selected_cs.available_slots -= 1
            selected_cs.last_access_time = time.time()  # Güncellenmiş erişim zamanı
            selected_cs.check_traffic_anomaly()  # Trafik anormalliğini kontrol et
            time.sleep(random.uniform(1, 5))
            selected_cs.available_slots += 1
        else:
            print(f"No available slots at CS {selected_cs.cs_id} in {selected_cs.location} for EV {ev.ev_id}")

if __name__ == "__main__":
    num_charging_stations = 3
    num_electric_vehicles = 5

    simulation_grid, evs = create_simulation_environment(num_charging_stations, num_electric_vehicles)

    simulate_charging(simulation_grid, evs)
