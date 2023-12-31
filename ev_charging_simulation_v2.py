# son hali
import tkinter as tk
from tkinter import messagebox
from random import randint
import threading
import time

class ChargeStation:
    def __init__(self, station_id, capacity=3):
        self.station_id = station_id
        self.capacity = capacity
        self.current_vehicles = 0
        self.queue = []  # Sıra için liste
        self.busy_until = 0  # Şu anki aracın bitiş zamanı
        self.log = []
        self.wait_time_estimate = 0  # Bekleme süresi tahmini

    def charge_vehicle(self, vehicle):
        if self.current_vehicles < self.capacity:
            entry_time = time.time()
            self.current_vehicles += 1
            self.busy_until = entry_time + 10  # Şarj süresi 10 saniye (örnek için düşürüldü)
            exit_time = self.busy_until  # Çıkış zamanını kaydet
            self.log.append({"vehicle": vehicle, "entry_time": entry_time, "exit_time": exit_time})
            self.wait_time_estimate = 0  # Yeni araç girişinde bekleyen aracın tahmini süresini sıfırla
            return True
        else:
            return False

    def get_available_spots(self):
        return self.capacity - self.current_vehicles

    def is_busy(self):
        return time.time() < self.busy_until

    def add_to_queue(self, vehicle):
        self.queue.append(vehicle)

    def process_queue(self):
        while self.queue:
            if not self.is_busy():
                next_vehicle = self.queue.pop(0)
                self.charge_vehicle(next_vehicle)
                next_vehicle["wait_var"].set("No")
            else:
                time.sleep(1)  # Şarj istasyonu doluysa bir saniye bekle

    def calculate_wait_time(self, current_time):
        # İlk giren aracın şarj süresi bitiş zamanından geçen süreyi hesapla
        return max(0, self.busy_until - current_time)

class Simulation:
    def __init__(self, num_stations=5, num_vehicles=25):
        self.stations = [ChargeStation(i) for i in range(num_stations)]
        self.vehicles = num_vehicles
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Charge Station Simulation")

        self.station_frames = []
        for station in self.stations:
            station_frame = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
            station_frame.pack(side=tk.LEFT, padx=5, pady=5)

            label_text = f"Station {station.station_id}\nAvailable spots: {station.get_available_spots()}"
            station_label = tk.Label(station_frame, text=label_text)
            station_label.pack()

            charge_boxes = []
            for _ in range(station.capacity):
                charge_box = tk.Label(station_frame, text="⚡", width=4, height=2, relief=tk.RAISED)
                charge_box.pack(side=tk.LEFT, padx=5, pady=5)
                charge_boxes.append(charge_box)

            self.station_frames.append({"frame": station_frame, "charge_station": station, "label": station_label, "charge_boxes": charge_boxes})

        self.start_simulation_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_simulation_button.pack(pady=10)

    def start_simulation(self):
        for _ in range(self.vehicles):
            random_station = randint(0, len(self.stations) - 1)
            station = self.stations[random_station]
            vehicle = {"wait_var": tk.StringVar(), "entry_time": None, "exit_time": None}
            vehicle["entry_time"] = time.time()
            if station.charge_vehicle(vehicle):
                message = f"Vehicle charged at Station {station.station_id}"
                self.update_gui()
            else:
                if station.is_busy():
                    available_stations = [s.station_id for s in self.stations if s.get_available_spots() > 0]
                    wait_time = station.calculate_wait_time(time.time())
                    wait_response = self.ask_wait(station, available_stations, wait_time)
                    if wait_response:
                        station.add_to_queue(vehicle)
                        message = f"Vehicle added to the queue at Station {station.station_id}."
                    else:
                        message = f"All stations are full. Try again later."
                        vehicle["wait_var"].set("No")
                else:
                    station.add_to_queue(vehicle)
                    message = f"Vehicle added to the queue at Station {station.station_id}."

            self.root.update()
            time.sleep(1)  # Araçlar arası 1 saniye bekle
            threading.Thread(target=station.process_queue).start()

        self.display_logs()  # Simülasyon tamamlandığında log ekranını göster

    def ask_wait(self, station, available_stations, wait_time):
        response = messagebox.askquestion("Station Full", f"Station {station.station_id} is full. Estimated wait time: {wait_time:.2f} seconds.\nWhat do you want to do?\nAvailable stations: {', '.join(map(str, available_stations))}.", detail="Choose 'Yes' to wait or 'No' to find another station.")
        return response == "yes"

    def update_gui(self):
        for station_data in self.station_frames:
            charge_station = station_data["charge_station"]
            label = station_data["label"]
            charge_boxes = station_data["charge_boxes"]

            label_text = f"Station {charge_station.station_id}\nAvailable spots: {charge_station.get_available_spots()}"
            label.config(text=label_text)

            for i in range(len(charge_boxes)):
                if i < charge_station.current_vehicles:
                    charge_boxes[i].config(bg="green")
                else:
                    charge_boxes[i].config(bg="lightgray")

    def display_logs(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Simulation Logs")

        log_text = tk.Text(log_window, height=20, width=60)
        log_text.pack()

        log_text.insert(tk.END, "Simulation Logs:\n\n")
        for station in self.stations:
            log_text.insert(tk.END, f"Station {station.station_id}:\n")
            for log_entry in station.log:
                entry_time = time.strftime("%H:%M:%S", time.localtime(log_entry["entry_time"]))
                exit_time = time.strftime("%H:%M:%S", time.localtime(log_entry["exit_time"])) if log_entry["exit_time"] else "N/A"
                log_text.insert(tk.END, f"  Vehicle Entry Time: {entry_time} Exit Time: {exit_time}\n")
            log_text.insert(tk.END, "\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
