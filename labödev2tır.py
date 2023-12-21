import csv
import pandas


class Ship:
    def _init_(self,
                 arrival_time,
                 ship_number,
                 capacity,
                 country):
        self.arrival_time = arrival_time
        self.ship_number = ship_number
        self.capacity = int(capacity)
        self.country = country
        self.current_load = 0
        self.left_port = False
        self.cargo = []

    def remaining_space(self):
        return self.capacity - self.current_load

    def leave_port(self):
        self.left_port = True

    def add_cargo(self, cargo):
        self.cargo.append(cargo)
        self.current_load += cargo.tonnage

class Cargo:
    def _init_(self, destination, tonnage):
        self.destination = destination
        self.tonnage = tonnage

class Stack:
    def _init_(self, capacity):
        self.capacity = capacity
        self.current_load = 0 # Overall tonnage
        self.cargo_list = [] # List of Cargo objects

    def load_cargo_truck(self, truck):
        if (self.current_load + truck.tonnage > self.capacity):
            return False
        self.current_load += truck.tonnage
        self.cargo_list.append(Cargo(truck.destination, truck.tonnage))
        truck.tonnage = 0
        return True

    def is_full(self):
        return int(self.current_load) >= int(self.capacity)

    def is_empty(self):
        return len(self.cargo_list) == 0

    def top(self):
        if len(self.cargo_list)==0:
            return None
        return self.cargo_list[-1]

    def pop(self):
        self.current_load -= self.cargo_list[-1].tonnage
        self.cargo_list = self.cargo_list[0:len(self.cargo_list)-2]

class Truck(object):
    def _init_(self,
                 arrival_time,
                 plate_number,
                 tonnage,
                 cost,
                 destination):
        self.arrival_time = arrival_time
        self.plate_number = plate_number
        self.tonnage = tonnage
        self.cost = cost
        self.destination = destination

class Simulation:
    def _init_(self,trucks,ships,stacks):
        self._trucks = trucks
        self._ships = ships
        self._stacks = stacks
        self.max_crane_ops = 20
        self.ship_loaded_threshold = 0.95

    def run(self):
        # ...
        still_work_to_do = True
        t = 0
        while still_work_to_do:
            num_crane_ops = 0
            print("Simulating time step {}".format(t))
            # Read trucks arriving at current time t or earlier
            trucks = [truck for truck in self._trucks if truck.arrival_time <= t]

            # Ships arriving at current time t or earlier and did not leave yet
            ships = [ship for ship in self._ships if ship.arrival_time <= t and ship.left_port == False]

            # Load truck cargo to stacks if possible
            for truck in trucks:
                if truck.tonnage > 0:
                    for stack in self._stacks:
                        if stack.load_cargo_truck(truck):
                            num_crane_ops += 1
                            print(f"Loading cargo from truck {truck.plate_number} to stack")
                            # Cargo loaded -> Stop iterating over stacks
                            break
                if num_crane_ops == self.max_crane_ops:
                    print(f"Reached 20 crane operations, stopping cargo loading for this iteration..")
                    break

            # Check whether we can load
            for ship in ships:
                for stack in self._stacks:
                    if stack.is_empty():
                        continue
                    cargo = stack.top()
                    if cargo.destination == ship.country and ship.remaining_space() >= cargo.tonnage:
                        print(f"Adding {cargo.tonnage}t cargo to ship {ship.ship_number} to {ship.country}")
                        stack.pop()
                        ship.add_cargo(cargo)
                        if (ship.capacity * self.ship_loaded_threshold) >= ship.current_load:
                            ship.leave_port()
                            print(f"Ship {ship.ship_number} leaving to {ship.country}")




            if t>5000:
                still_work_to_do = False

            t += 1


def main():
    wait_times=[]
    t=3


    GemilerFile = "gemiler.csv"
    dfa = pandas.read_csv(GemilerFile)
    dfa = dfa.sort_values(by="kapasite", ascending=True)

    # Print column names to verify
    print(dfa.columns)

    # If needed, correct the column name (ensure it's correct and contains special characters if any)

    # Access the 'geli_zaman' column

    # Convert 'kapasite' values to strings and extract ship numbers
    dfa['kapasite'] = dfa['kapasite'].astype(str)
    dfa['Ship Number'] = dfa['kapasite'].str.extract('(\d+)$', expand=False)

    # Ensure you are renaming the correct column; 'geli _zaman ' should be replaced with the correct column name

    ship_number_dfa=dfa["Ship Number"]
    time_dfa=dfa["geliş_zamanı"]
    ship_name_dfa=dfa["gemi_adı"]
    capacity_dfa=dfa["kapasite"]
    country_dfa=dfa["gidecek_ülke"]



    OlaylarFile = "olaylar.csv"
    df = pandas.read_csv(OlaylarFile)

    # Construct Truck objects from csv file rows
    trucks = []
    for row in range(len(df)):
        row_data = df.loc[row, :]
        time_of_arrival = row_data["geliş_zamanı"]
        plate_number = row_data["tır_plakası"]
        tonnage = row_data["yük_miktarı"]
        cost = row_data["maliyet"]
        destination = row_data["ülke"]
        truck = Truck(time_of_arrival, plate_number, tonnage, cost, destination)
        trucks.append(truck)

    # Construct Ship objects from csv file rows
    ships = []
    for row in range(len(dfa)):
        row_data = dfa.loc[row, :]
        arrival_time = row_data["geliş_zamanı"]
        ship_number = row_data["gemi_adı"]
        capacity = row_data["kapasite"]
        country = row_data["gidecek_ülke"]
        ship = Ship(arrival_time, ship_number, capacity, country)
        ships.append(ship)

    stacks = [Stack(750), Stack(750)]

    simulation = Simulation(trucks, ships, stacks)
    simulation.run()

if _name_ == "_main_":
    main()




