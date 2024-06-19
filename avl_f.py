class Vehicle:
    def __init__(self, vehicle_number, seating_capacity):
        self.vehicle_number = vehicle_number
        self.seating_capacity = seating_capacity
        self.trips = []

    def get_vehicle_number(self):
        return self.vehicle_number

    def set_vehicle_number(self, new_vehicle_number):
        self.vehicle_number = new_vehicle_number

    def get_seating_capacity(self):
        return self.seating_capacity

    def set_seating_capacity(self, new_seating_capacity):
        self.seating_capacity = new_seating_capacity

    def get_trips(self):
        return self.trips

    def add_trip(self, trip):
        self.trips.append(trip)


class Trip:
    def __init__(self, vehicle, pick_up_location, drop_location, departure_time):
        self.trip_id = None  
        self.vehicle = vehicle
        self.pick_up_location = pick_up_location
        self.drop_location = drop_location
        self.departure_time = departure_time
        self.booked_seats = 0
        self.passengers = []  

    def get_trip_id(self):
        return self.trip_id

    def set_trip_id(self, trip_id):
        self.trip_id = trip_id

    def get_vehicle(self):
        return self.vehicle

    def get_pick_up_location(self):
        return self.pick_up_location

    def set_pick_up_location(self, new_pick_up_location):
        self.pick_up_location = new_pick_up_location

    def get_drop_location(self):
        return self.drop_location

    def set_drop_location(self, new_drop_location):
        self.drop_location = new_drop_location

    def get_departure_time(self):
        return self.departure_time

    def set_departure_time(self, new_departure_time):
        self.departure_time = new_departure_time

    def get_booked_seats(self):
        return self.booked_seats

    def set_booked_seats(self, new_booked_seats):
        self.booked_seats = new_booked_seats

    def get_passengers(self):
        return self.passengers

    def add_passenger(self, passenger_details):
        self.passengers.append(passenger_details)

    def remove_passenger(self, passenger_details):
        self.passengers.remove(passenger_details)



class Location:
    def __init__(self, name):
        self.name = name
        self.service_ptr = []
        self.trips = []

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_service_ptr(self, drop):
        for i in self.service_ptr:
            if i.get_location_ptr().get_name() == drop:
                return i

    def set_service_ptr(self, service_ptr):
        self.service_ptr.append(service_ptr)

    def add_trip(self, trip):
        self.trips.append(trip)
        pick = None
        if self.service_ptr:
            for i in self.service_ptr:
                if i.get_location_ptr().get_name() == trip.drop_location:
                    pick = i
                    pick.add_trip(trip.departure_time, trip)
                    break

        if pick is None:
            drop = Location(trip.drop_location)
            drop_service = TransportService(drop)
            self.service_ptr.append(drop_service)
            pick = drop_service
            pick.add_trip(trip.departure_time, trip)


class AVLTreeNode:
    def __init__(self, departure_time=0, trip_node_ptr=None, parent_ptr=None):
        self.left_ptr = None
        self.right_ptr = None
        self.parent_ptr = parent_ptr
        self.departure_time = departure_time
        self.trip_node_ptr = trip_node_ptr
        self.height = 1

    def get_left_ptr(self):
        return self.left_ptr

    def set_left_ptr(self, new_left_ptr):
        self.left_ptr = new_left_ptr

    def get_right_ptr(self):
        return self.right_ptr

    def set_right_ptr(self, new_right_ptr):
        self.right_ptr = new_right_ptr

    def get_parent_ptr(self):
        return self.parent_ptr

    def set_parent_ptr(self, new_parent_ptr):
        self.parent_ptr = new_parent_ptr

    def get_departure_time(self):
        return self.departure_time

    def set_departure_time(self, new_departure_time):
        self.departure_time = new_departure_time

    def get_trip_node_ptr(self):
        return self.trip_node_ptr

    def set_trip_node_ptr(self, new_trip_node_ptr):
        self.trip_node_ptr = new_trip_node_ptr


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self):
        return self._get_height(self.root)

    def _get_height(self, node):
        if node is None:
            return 0

        left_height = self._get_height(node.get_left_ptr())
        right_height = self._get_height(node.get_right_ptr())

        return 1 + max(left_height, right_height)

    def get_number_of_nodes(self):
        return self._get_number_of_nodes(self.root)

    def _get_number_of_nodes(self, node):
        if node is None:
            return 0

        return 1 + self._get_number_of_nodes(node.get_left_ptr()) + self._get_number_of_nodes(
            node.get_right_ptr())


class AVLTree(AVLTree):
    def __init__(self):
        super().__init__()

    def get_element_with_minimum_key(self):
        if not self.root:
            return None

        current = self.root
        while current.get_left_ptr() is not None:
            current = current.get_left_ptr()

        return current

    def get_element_with_maximum_key(self):
        if not self.root:
            return None

        current = self.root
        while current.get_right_ptr() is not None:
            current = current.get_right_ptr()

        return current

    def search_node_with_key(self, key):
        current = self.root
        while current is not None:
            if key == current.get_departure_time():
                return current
            elif key < current.get_departure_time():
                current = current.get_left_ptr()
            else:
                current = current.get_right_ptr()

        return None

    def get_successor_node(self, node):
        if node.get_right_ptr() is not None:
            current = node.get_right_ptr()
            while current.get_left_ptr() is not None:
                current = current.get_left_ptr()
            return current

        parent = node.get_parent_ptr()
        while parent is not None and node == parent.get_right_ptr():
            node = parent
            parent = parent.get_parent_ptr()

        return parent

    def get_predecessor_node(self, node):
        if node.get_left_ptr() is not None:
            current = node.get_left_ptr()
            while current.get_right_ptr() is not None:
                current = current.get_right_ptr()
            return current

        parent = node.get_parent_ptr()
        while parent is not None and node == parent.get_left_ptr():
            node = parent
            parent = parent.get_parent_ptr()

        return parent

    def insert(self, departure_time, trip):
        if not self.root:
            self.root = AVLTreeNode(departure_time, trip)
        else:
            self.root = self._insert(self.root, departure_time, trip)

    def _insert(self, node, departure_time, trip):
        if not node:
            return AVLTreeNode(departure_time, trip)

        if departure_time < node.get_departure_time():
            node.set_left_ptr(self._insert(node.get_left_ptr(), departure_time, trip))
        else:
            node.set_right_ptr(self._insert(node.get_right_ptr(), departure_time, trip))

    
        node.height = 1 + max(self._get_height(node.get_left_ptr()), self._get_height(node.get_right_ptr()))

        
        balance = self._get_balance(node)

        
        if balance > 1 and departure_time < node.get_left_ptr().get_departure_time():
            return self._right_rotate(node)

        
        if balance < -1 and departure_time > node.get_right_ptr().get_departure_time():
            return self._left_rotate(node)

        
        if balance > 1 and departure_time > node.get_left_ptr().get_departure_time():
            node.set_left_ptr(self._left_rotate(node.get_left_ptr()))
            return self._right_rotate(node)

    
        if balance < -1 and departure_time < node.get_right_ptr().get_departure_time():
            node.set_right_ptr(self._right_rotate(node.get_right_ptr()))
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        y = z.get_right_ptr()
        T2 = y.get_left_ptr()

    
        y.set_left_ptr(z)
        z.set_right_ptr(T2)

        
        z.height = 1 + max(self._get_height(z.get_left_ptr()), self._get_height(z.get_right_ptr()))
        y.height = 1 + max(self._get_height(y.get_left_ptr()), self._get_height(y.get_right_ptr()))

        
        return y

    def _right_rotate(self, z):
        y = z.get_left_ptr()
        T3 = y.get_right_ptr()

        
        y.set_right_ptr(z)
        z.set_left_ptr(T3)

        
        z.height = 1 + max(self._get_height(z.get_left_ptr()), self._get_height(z.get_right_ptr()))
        y.height = 1 + max(self._get_height(y.get_left_ptr()), self._get_height(y.get_right_ptr()))

        
        return y

    def _get_balance(self, node):
        if node is None:
            return 0

        return self._get_height(node.get_left_ptr()) - self._get_height(node.get_right_ptr())

    def _get_height(self, node):
        if node is None:
            return 0

        return node.height


class TransportService:
    def __init__(self, location_ptr=None):
        self.location_ptr = location_ptr
        self.avl_head = None
        self.avl = AVLTree()

    def get_location_ptr(self):
        return self.location_ptr

    def set_location_ptr(self, new_location_ptr):
        self.location_ptr = new_location_ptr

    def add_trip(self, key, trip):
        if not self.avl_head:
            self.avl.insert(key, trip)
            self.set_avl_head(self.avl.root)
        else:
            self.avl.insert(key, trip)

    def get_avl_head(self):
        return self.avl_head

    def set_avl_head(self, new_avl_head):
        self.avl_head = new_avl_head

    def get_avl(self):
        return self.avl_head


class TravelDesk:
    def __init__(self):
        self.vehicles = []
        self.locations = []
        self.trip_counter = 1

    def add_trip(self, vehicle_number, seating_capacity, pick_up_location, drop_location, departure_time):
        vehicle = None
        for v in self.vehicles:
            if v.vehicle_number == vehicle_number:
                vehicle = v
                break
        if vehicle is None:
            vehicle = Vehicle(vehicle_number, seating_capacity)
            self.vehicles.append(vehicle)

        # Convert departure_time to string in hh:mm format
        departure_time_str = f"{departure_time // 60:02}:{departure_time % 60:02}"

        trip = Trip(vehicle, pick_up_location, drop_location, departure_time_str)  # Updated to string type
        vehicle.add_trip(trip)

        pick_location_exists = False
        for loc in self.locations:
            if loc.name == pick_up_location:
                pick_location_exists = True
                break

        if not pick_location_exists:
            location = Location(pick_up_location)
            self.locations.append(location)
            location.add_trip(trip)

        else:
            for loc in self.locations:
                if loc.name == pick_up_location:
                    loc.add_trip(trip)
    def show_trips(self, pick_up_location, after_time, before_time):
        trips = []
        for vehicle in self.vehicles:
            for trip in vehicle.trips:
                if (trip.pick_up_location == pick_up_location and
                    after_time <= trip.departure_time < before_time):
                    booked_seats = trip.get_booked_seats()
                    remaining_seats = vehicle.seating_capacity - booked_seats  
                    trips.append((trip, remaining_seats))
        return trips

    def show_tripsbydestination(self, pick_up_location, destination, after_time, before_time):
        trips = []
        for vehicle in self.vehicles:
            for trip in vehicle.trips:
                if (trip.pick_up_location == pick_up_location and
                    trip.drop_location == destination and
                    after_time <= trip.departure_time < before_time):
                    trips.append(trip)
        return trips

    def book_trip(self, pick_up_location, drop_location, vehicle_number, departure_time, passenger_name, passenger_age, passenger_gender):
        for vehicle in self.vehicles:
            if vehicle.vehicle_number == vehicle_number:
                for trip in vehicle.trips:
                    if (trip.pick_up_location == pick_up_location and
                        trip.drop_location == drop_location and
                        trip.departure_time == departure_time):
                        booked_seats = trip.get_booked_seats()
                        seating_capacity = vehicle.get_seating_capacity()
                        if booked_seats < seating_capacity:
                            
                            trip_id = self.trip_counter
                            self.trip_counter += 1
                            trip.set_trip_id(trip_id)

            
                            seat_number = booked_seats + 1

        
                            trip.set_booked_seats(booked_seats + 1)
                            vehicle.set_seating_capacity(seating_capacity)
                            trip.add_passenger({
                                'name': passenger_name,
                                'age': passenger_age,
                                'gender': passenger_gender,
                                'seat_number': seat_number
                            })

                
                            booking_details = f"{pick_up_location},{drop_location},{vehicle_number},{departure_time},{passenger_name},{passenger_age},{passenger_gender},{trip_id},{seat_number}"
                            self.book_trip_to_log(booking_details)

                            return trip

        return None

    def cancel_trip(self, pick_up_location, drop_location, vehicle_number, departure_time, passenger_name, passenger_age, passenger_gender):
        for vehicle in self.vehicles:
            if vehicle.vehicle_number == vehicle_number:
                for trip in vehicle.trips:
                    if (trip.pick_up_location == pick_up_location and
                        trip.drop_location == drop_location and
                        trip.departure_time == departure_time):
                        for passenger in trip.get_passengers():
                            if (passenger['name'] == passenger_name and
                                passenger['age'] == passenger_age and
                                passenger['gender'] == passenger_gender):
                            
                                trip.set_booked_seats(trip.get_booked_seats() - 1)
                                vehicle.set_seating_capacity(vehicle.get_seating_capacity() + 1)
                                trip.remove_passenger(passenger)

                            
                                with open("ticket_log.txt", "r") as file:
                                    lines = file.readlines()
                                with open("ticket_log.txt", "w") as file:
                                    for line in lines:
                                        parts = line.strip().split(",")
                                        if parts[:7] != [pick_up_location, drop_location, vehicle_number, str(departure_time), passenger_name, str(passenger_age), passenger_gender]:
                                            file.write(line)

                                return trip

        return None

    def add_trip_to_log(self, trip_details):
        with open("trip_log.txt", "a") as file:
            file.write(trip_details + "\n")

    def book_trip_to_log(self, booking_details):
        with open("ticket_log.txt", "a") as file:
            file.write(booking_details + "\n")

            
    def load_trip_data_from_log(self):
        try:
            with open("trip_log.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        vehicle_number, seating_capacity, pick_up_location, drop_location, departure_time = parts
                        self.add_trip(vehicle_number, int(seating_capacity), pick_up_location, drop_location, int(departure_time))
                    else:
                        pick_up_location, drop_location, vehicle_number, departure_time = parts
                        self.book_trip(pick_up_location, drop_location, vehicle_number, int(departure_time), "", 0, "")  
        except FileNotFoundError:
            print("No trip log found.")
    def load_ticket_data_from_log(self):
        try:
            with open("ticket_log.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    pick_up_location, drop_location, vehicle_number, departure_time, passenger_name, passenger_age, passenger_gender = parts
                    self.book_trip(pick_up_location, drop_location, vehicle_number, int(departure_time), passenger_name, int(passenger_age), passenger_gender)
        except FileNotFoundError:
            print("No ticket log found.")


    def show_booked_ticket_details(self, passenger_name):
        booked_tickets = []
        for vehicle in self.vehicles:
            for trip in vehicle.trips:
                if trip.passenger_details and trip.passenger_details['name'] == passenger_name:
                    booked_tickets.append({
                        'Pick-up Location': trip.pick_up_location,
                        'Drop Location': trip.drop_location,
                        'Departure Time': trip.departure_time,
                        'Passenger Name': trip.passenger_details['name'],
                        'Passenger Age': trip.passenger_details['age'],
                        'Passenger Gender': trip.passenger_details['gender']
                    })
        return booked_tickets
    def book_trip(self, pick_up_location, drop_location, vehicle_number, departure_time, passenger_name, passenger_age, passenger_gender):
        for vehicle in self.vehicles:
            if vehicle.vehicle_number == vehicle_number:
                for trip in vehicle.trips:
                    if (trip.pick_up_location == pick_up_location and
                        trip.drop_location == drop_location and
                        trip.departure_time == departure_time):
                        booked_seats = trip.get_booked_seats()
                        seating_capacity = vehicle.get_seating_capacity()
                        if booked_seats < seating_capacity:
                            trip.set_booked_seats(booked_seats + 1)
                            vehicle.set_seating_capacity(seating_capacity)
                            trip.passenger_details = {
                                'name': passenger_name,
                                'age': passenger_age,
                                'gender': passenger_gender
                            }
                            return trip
        return None

def main():
    travel_desk = TravelDesk()
    travel_desk.load_trip_data_from_log()
    travel_desk.load_ticket_data_from_log()
    while True:
        print("\n1. Add Trip")
        print("2. Show Trips")
        print("3. Book Trip")
        print("4. Cancel Trip")
        print("5. Show Booked Ticket Details")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_number = input("Enter vehicle number: ")
            seating_capacity = int(input("Enter seating capacity: "))
            pick_up_location = input("Enter pick-up location: ")
            drop_location = input("Enter drop location: ")
            departure_time_str = input("Enter departure time (hh:mm): ")
            
    
            try:
                hours, minutes = map(int, departure_time_str.split(":"))
                departure_time = hours * 60 + minutes
            except ValueError:
                print("Invalid time format. Please enter in hh:mm format.")
                continue
            
            travel_desk.add_trip(vehicle_number, seating_capacity, pick_up_location, drop_location, departure_time)
            print("Trip added successfully!")
            trip_details = f"{vehicle_number},{seating_capacity},{pick_up_location},{drop_location},{departure_time}"
            travel_desk.add_trip_to_log(trip_details)

        elif choice == "2":
            pick_up_location = input("Enter pick-up location: ")
            after_time = int(input("Enter time after which to show trips: "))
            before_time = int(input("Enter time before which to show trips: "))
            trips = travel_desk.show_trips(pick_up_location, after_time, before_time)
            print("Trips:")
            for trip, remaining_seats in trips:
                print(f"Vehicle: {trip.vehicle.vehicle_number}, Departure Time: {trip.departure_time}, Remaining Seats: {remaining_seats}")

        elif choice == "3":
            pick_up_location = input("Enter pick-up location: ")
            drop_location = input("Enter drop location: ")
            vehicle_number = input("Enter vehicle number: ")
            departure_time_str = input("Enter departure time (hh:mm): ")
            
            
            try:
                hours, minutes = map(int, departure_time_str.split(":"))
                departure_time = hours * 60 + minutes
            except ValueError:
                print("Invalid time format. Please enter in hh:mm format.")
                continue
            
            passenger_name = input("Enter passenger name: ")
            passenger_age = int(input("Enter passenger age: "))
            passenger_gender = input("Enter passenger gender: ")
            booked_trip = travel_desk.book_trip(pick_up_location, drop_location, vehicle_number, departure_time, passenger_name, passenger_age, passenger_gender)
            if booked_trip:
                print("Trip booked successfully!")
                booking_details = f"{pick_up_location},{drop_location},{vehicle_number},{departure_time},{passenger_name},{passenger_age},{passenger_gender}"
                travel_desk.book_trip_to_log(booking_details)
            else:
                print("Failed to book trip. Please check input details.")

        elif choice == "4":
            pick_up_location = input("Enter pick-up location: ")
            drop_location = input("Enter drop location: ")
            vehicle_number = input("Enter vehicle number: ")
            departure_time_str = input("Enter departure time (hh:mm): ")
            
            
            try:
                hours, minutes = map(int, departure_time_str.split(":"))
                departure_time = hours * 60 + minutes
            except ValueError:
                print("Invalid time format. Please enter in hh:mm format.")
                continue
            
            passenger_name = input("Enter passenger name: ")
            passenger_age = int(input("Enter passenger age: "))
            passenger_gender = input("Enter passenger gender: ")
            canceled_trip = travel_desk.cancel_trip(pick_up_location, drop_location, vehicle_number, departure_time, passenger_name, passenger_age, passenger_gender)
            if canceled_trip:
                print("Trip canceled successfully!")
            else:
                print("Failed to cancel trip. Please check input details.")

        elif choice == "5":
            passenger_name = input("Enter passenger name: ")
            booked_tickets = travel_desk.show_booked_ticket_details(passenger_name)
            if booked_tickets:
                print("Booked Ticket Details:")
                for ticket in booked_tickets:
                    print(ticket)
            else:
                print("No booked tickets found for the given passenger.")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
