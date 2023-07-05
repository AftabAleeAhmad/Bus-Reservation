#------------BUS MANAGEMENT------------#
import copy
from datetime import datetime
import json
import os
# bus_dictionary = {}
bus_file_name = 'E:\Python\\assignments\Data_file(bus_reservation).json'

def initial_funtion():
    with open(bus_file_name,'r+',encoding='utf-8') as bus_file:
        size = os.path.getsize(bus_file_name)
        if size == 0:
            print("file is empty...")
        else:
            bus_dictionary = dict (json.load(bus_file))
            return bus_dictionary

bus_dictionary =  initial_funtion()

def time_function(date):
    current_date = datetime.now()
    current_date = datetime.strftime(current_date,"%Y-%m-%d")
    current_date = datetime.strptime(current_date,"%Y-%m-%d")
                
    try:
        date_obj = datetime.strptime(date,"%Y-%m-%d")
        if date_obj >= current_date:
            # print("ok")
            return date
        else:
            print(".....You can't reserve any seat in previous date.....")
    except ValueError:
        print("Enter date with correct format....")


def input_seats_empty():
    seats = []
    while True:
        print('Seat number want to reserve(,) (upto 30,type "done" when you finished): ')
        seat = input()
        if seat == "done":
            break
        else:
            seats.append(int(seat))
    return seats


def input_seats(seat_path):
    # totalseats = 0
    total_seats = []
    seats = [] 
    for seat_t in seat_path:
        if "seats" in seat_t:
            total_seats = total_seats+seat_t["seats"]
    print(total_seats)
    while True:
        # for seat_d in seat_path:
        #     if "totalseats" in seat_d:
        #         total = int(seat_d["totalseats"])
        #         totalseats += total
       

        if len(total_seats) < 30:
            print('Seat number want to reserve(,) (upto 30,type "done" when you finished): ')
            seat = input()
            if seat == "done":
                break
            else:
                seat = int(seat)
                if seat > 30:
                    print("You can choose more than 30 seat nummber.....")
                elif seat in total_seats:
                    print(f"{seat} is already reserved, try another")
                else:
                    seats.append(int(seat))

        else:
            print("\t\t\tWe have no More seats on this date,try another date")
            break
    return seats


def check_already_reserve(seats, seats_path):
    for seat in seats:
        for res_seat in seats_path:
            if seat == res_seat:
                seats.remove(seat)
                new = int(input(f" {seat} is already reserved, Enter again seat again (upto 30): "))
                seats.append(new)


def check_available_seats(p_name,desti,date):
    with open(bus_file_name,'r+',encoding='utf-8') as add_res:
        for serial in bus_dictionary:
        
            for route in bus_dictionary[serial]:
        
                if route == "route":
        
                    if bus_dictionary[serial][route] == desti:
        
                        for res_key in bus_dictionary[serial]:
        
                            if res_key == "reservation":
        
                                if bus_dictionary[serial][res_key] == {}:

                                    seats = input_seats_empty()
                                    booker_data = {"passenger":p_name,"seats":seats,"totalseats":len(seats)}

                                    bus_dictionary[serial][res_key][date] = [booker_data]
                                    json.dump (bus_dictionary,add_res)
        
                                else:
        
                                    new_reservation_date = copy.deepcopy(bus_dictionary[serial][res_key])
        
                                    for date_d in new_reservation_date:
                                        
                                        
                                        if date_d == date:

                                            seats = input_seats(new_reservation_date[date_d])     
                                            # seats = check_already_reserve(seats,new_reservation_date[date_d])
                                            booker_data = {"passenger":p_name,"seats":seats,"totalseats":len(seats)}
                                            bus_dictionary[serial][res_key][date].append(booker_data)
                                            json.dump (bus_dictionary,add_res)
                                            break
                                        


                                        elif date_d != date:
                                    
                                            seats = input_seats()
                                            booker_data = {"passenger":p_name,"seats":seats,"totalseats":len(seats)}
                                            bus_dictionary[serial][res_key][date]= []
                                            bus_dictionary[serial][res_key][date].append(booker_data)
                                            json.dump (bus_dictionary,add_res)
                                            break


def matching_routes(des_city):
    for route_1 in bus_dictionary:
        # print(route_1)
        for route_2 in bus_dictionary[route_1]:
            if bus_dictionary[route_1][route_2] == des_city:
                return True
    else:
        print("sorry, don't have any bus available")
        

def enter_new_seat(list_path,date_path):
    new_list = input_seats(date_path)
    new_list = list_path + new_list
    return new_list


def remove_seat(list_path):
    # print(list_path)
    print("Enter seat number you want to remove: ")
    remove = input()
    remove = int(remove)
    list_path.remove(remove)
    return list_path


def edit_data(name, date, destination):
    with open(bus_file_name,'r+',encoding='utf-8') as edit_res:
        print('''Enter "n" to edit "Name", Enter "s" to edit "Seats"''')
        choice_edit = input(str())
        if choice_edit == 's':
            for serial in bus_dictionary:
                for route in bus_dictionary[serial]:
                    if route == "route":
                        if bus_dictionary[serial][route] == destination:
                            for reser in bus_dictionary[serial]: 
                                if reser == "reservation":
                                    for date_d in bus_dictionary[serial][reser]:
                                        if date_d == date:
                                            for reser_dict in bus_dictionary[serial][reser][date_d]:
                                                for seat_p in reser_dict:
                                                    if seat_p == "passenger":
                                                        if reser_dict [seat_p] == name:
                                                            for seat in reser_dict:
                                                                if seat== "seats":
                                                                    print("You have these seats already booked: ")
                                                                    for seat_no in reser_dict[seat]:
                                                                        print(seat_no)
                                                                    print("Enter 'a' if you want to add seat, 'r' to remove a seat: ")
                                                                    seat_edit = input(str())
                                                                    if seat_edit == 'a':
                                                                        updated_list = enter_new_seat(reser_dict[seat],bus_dictionary[serial][reser][date_d])
                                                                        reser_dict["seats"] = updated_list
                                                                        reser_dict["totalseats"] = len(updated_list)
                                                                        json.dump (bus_dictionary,edit_res)
                                                                    elif seat_edit == 'r':
                                                                        updated_list = remove_seat(reser_dict[seat])
                                                                        reser_dict["seats"] = updated_list
                                                                        reser_dict["totalseats"] = len(updated_list)
                                                                        json.dump (bus_dictionary,edit_res)
                                                                else:
                                                                    pass
                                                        else:
                                                            pass
                                                    else:
                                                        pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    else:
                        pass
        elif choice_edit == "n":
            
            for serial in bus_dictionary:
                for route in bus_dictionary[serial]:
                    if route == "route":
                        if bus_dictionary[serial][route] == destination:
                            for reser in bus_dictionary[serial]: 
                                if reser == "reservation":
                                    for date_d in bus_dictionary[serial][reser]:
                                        if date_d == date:
                                            for reser_dict in bus_dictionary[serial][reser][date_d]:
                                                for seat_p in reser_dict:
                                                    if seat_p == "passenger":
                                                        if reser_dict [seat_p] == name:
                                                            print("Enter new Name: ")
                                                            new_name = input(str())
                                                            reser_dict [seat_p] = new_name
                                                            json.dump (bus_dictionary,edit_res)
                                                        else:
                                                            pass
                                                    else:
                                                        pass
                                        else:
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    else:
                        pass    


def delete_reservation(del_date,del_name,del_detination):
    with open(bus_file_name,'r+',encoding='utf-8') as del_res:
        for serial in bus_dictionary:
            for route in bus_dictionary[serial]:
                if route == "route":
                    if bus_dictionary[serial][route] == del_detination:
                        for reser in bus_dictionary[serial]: 
                            if reser == "reservation":
                                for date_d in bus_dictionary[serial][reser]:
                                    if date_d == del_date:
                                        for reser_dict in bus_dictionary[serial][reser][date_d]:
                                            for seat_p in reser_dict:
                                                if seat_p == "passenger":
                                                    if reser_dict [seat_p] == del_name:
                                                        bus_dictionary[serial][reser][date_d].remove(reser_dict)
                                                        print(bus_dictionary)
                                                        json.dump (bus_dictionary,del_res)
                                                    else:
                                                        pass
                                                else:
                                                    pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
                else:
                    pass


def check_bus_serial(num):
    for serial in bus_dictionary:
        if serial == num:
            print("This serial is already added")
            break
    else:
        return True


def check_bus_num(num):
    for serial in bus_dictionary:
        for number in bus_dictionary[serial]:
            if number == "title":
                if bus_dictionary[serial][number] == num:
                    print("\t\t\t.....Bus with this number plate is already added.....")
                else:
                    pass
            else:
                pass
    else:
        return True


def add_bus():

        with open(bus_file_name,"r+",encoding='utf-8')as save_bus:
            print("Add bus SERIAL: ")
            bus_serial = input(str())
            if check_bus_serial(bus_serial):    
                print("Add bus NUMBER: ")
                bus_num_plate = input(str())
                if check_bus_num(bus_num_plate):
                    print("Add DRIVER NAME: ")
                    bus_driver = input(str())
                    print("Add ROUTE: ")
                    bus_route = input(str())
                    bus_dictionary.update({bus_serial:{"title":bus_num_plate,"driver":bus_driver,"route":bus_route,"reservation":{}}})
                    json.dump(bus_dictionary,save_bus) 


def center_fuction_for_view(data):
    width = 15
    centered_text = data.center(width)
    return centered_text


def view_bus():
    for serial in bus_dictionary:
        width = 5
        centered_text = serial.center(width)
        print("*"*6)
        print(f"|{centered_text}|")
        print("*"*6)
        print("\n")
        # for data in bus_dictionary[serial]:
        #     if data != "driver":
        print("*"*55)
        print("|", center_fuction_for_view(str(bus_dictionary[serial]["title"])),"|",center_fuction_for_view(str(bus_dictionary[serial]["driver"])),"|",center_fuction_for_view(str(bus_dictionary[serial]["route"])),"|")
        print("*"*55)
        print("\n\n")
    # print("view bus function called...")


def search_bus():
    print("Enter bus serial: ")
    search = input()
    for serial in bus_dictionary:
        if serial == search:
            width = 5
            centered_text = serial.center(width)
            print("*"*6)
            print(f"|{centered_text}|")
            print("*"*6)
            print("\n")
            # for data in bus_dictionary[serial]:
            #     if data != "driver":
            print("*"*55)
            print("|", center_fuction_for_view(str(bus_dictionary[serial]["title"])),"|",center_fuction_for_view(str(bus_dictionary[serial]["driver"])),"|",center_fuction_for_view(str(bus_dictionary[serial]["route"])),"|")
            print("*"*55)
            print("\n\n")
            break
    else:
        print("\t\t\t Bus Not Found")


def delete_bus():
        with open (bus_file_name, 'r+', encoding='utf-8') as del_bus_entry:
            print("Enter bus serial: ")
            del_bus = input()
            for serial in bus_dictionary:
                if serial == del_bus:
                    del bus_dictionary[del_bus]
                    json.dump(bus_dictionary,del_bus_entry)
            else:
                print("Bus not found")
        # print("delete bus function called...")


def edit_bus():
    with open(bus_file_name,'r+',encoding='utf-8') as edit_bus:
        print("Enter Bus Serial Number: ")
        num = input()
        for serial in bus_dictionary:
                if serial == num:
                    print("Enter 'd' to change Driver, 'r' to change Route of BUS")
                    choice_edit_bus = input(str())
                    if choice_edit_bus == 'd':
                        print("Enter New Driver name: ")
                        new_driver = input()
                        bus_dictionary[serial]["driver"] = new_driver
                        json.dump(bus_dictionary, edit_bus)
                        break
                    elif choice_edit_bus == 'r':
                        print("Enter New Route: ")
                        new_route = input()
                        bus_dictionary[serial]["route"] = new_route
                        json.dump(bus_dictionary, edit_bus)
                        break
        else:
            print("\t\t\tProvided Serial not found.....")


def search_reservation(date,route,name):
    for serial in bus_dictionary:
        for rote in bus_dictionary[serial]:
            if rote == "route":
                if bus_dictionary[serial][rote] == route:
                    for reser in bus_dictionary[serial]:
                        if reser == "reservation":
                            for date_d in bus_dictionary[serial][reser]:
                                if date_d == date:
                                    for reser_dict in bus_dictionary[serial][reser][date_d]:
                                        for name_d in reser_dict:
                                            if  name_d == "passenger":
                                                if reser_dict[name_d] == name:
                                                    width = 11
                                                    centered_text = date_d.center(width)
                                                    print("-"*13)
                                                    print(f"|{centered_text}|")
                                                    print("-"*13)
                                                    print("\n")
                                                    print("-"*73)
                                                    print("|", center_fuction_for_view("Name"),"|",center_fuction_for_view("Seat no."),"|",center_fuction_for_view("Total seats"),"|",center_fuction_for_view("City"),"|")
                                                    print("-"*73)
                                                    for data in bus_dictionary[serial][reser][date]:
                                                        # print(data["passenger"])
                                                        print("|", center_fuction_for_view(str(data["passenger"])),"|",center_fuction_for_view(str(data["seats"])),"|",center_fuction_for_view(str(data["totalseats"])),"|",center_fuction_for_view(str(bus_dictionary[serial]["route"])),"|")
                                                    print("-"*73)
                                                    print("\n\n")



def manage_bus():    
    while True:
        print("""
            -----MANAGE BUS-----
            Please make a choice...
            1: ADD BUS...
            2: DELETE BUS...
            3: EDIT BUS...
            4: VIEW BUS...
            5: SEARCH BUS...
            6: Back to MAIN MENU...""")
        manage_bus_choice = input(str())
        if manage_bus_choice == "1":
            add_bus()
        elif manage_bus_choice == "2":
            delete_bus()
        elif manage_bus_choice == "3":
            edit_bus()
        elif manage_bus_choice == "4":
            view_bus()
        elif manage_bus_choice == "5":
            search_bus()
        elif manage_bus_choice == "6":
            print("BACK TO MAIN MENU..")
            break
        else:
            print("Make a right choice...")


def manage_reservation():
    while True:
        print("""
            -----MANAGE RESERVATION-----
            Please make a choice...
            1: ADD RESERVATION...
            2: DELETE RESERVATION...
            3: EDIT RESERVATION...
            4: VIEW RESERVATION...
            5: SEARCH RESERVATION...
            6: Back to MAIN MENU...""")
        manage_res_choice = input(str())
        if manage_res_choice == '1':
            print("Enter Date of Reservation (YYYY-MM-DD): ")
            res_date = input(str())
            if time_function(res_date):
                print("Enter PASSENGER NAME: ")
                passenger_name = input(str())
                print("Enter Destination city:")
                city_name = input(str())
                if matching_routes(city_name):
                    check_available_seats(passenger_name,city_name,res_date)
                        
        elif manage_res_choice == '2':
            print("Enter date: ")
            delete_date = input()
            if time_function(delete_date):
                print("Enter name: ")
                delete_name = input()
                print("Enter destination: ")
                delete_destination = input()
                delete_reservation(delete_date,delete_name,delete_destination)

        elif manage_res_choice == '3':
            print("Enter Name: ")
            edit_name = input(str())
            print("Enter Date: ")
            edit_date = input(str())
            if time_function(edit_date):
                print("Enter Destination: ")
                edit_destination = input(str())
                edit_data(edit_name,edit_date,edit_destination)

        elif manage_res_choice == '4':
            for serial in bus_dictionary:
                for reser in bus_dictionary[serial]:
                    if reser == "reservation":
                        for date in bus_dictionary[serial][reser]:
                            width = 11
                            centered_text = date.center(width)
                            print("-"*13)
                            print(f"|{centered_text}|")
                            print("-"*13)
                            print("\n")
                            print("-"*73)
                            print("|", center_fuction_for_view("Name"),"|",center_fuction_for_view("Seat no."),"|",center_fuction_for_view("Total seats"),"|",center_fuction_for_view("City"),"|")
                            print("-"*73)
                            for data in bus_dictionary[serial][reser][date]:
                                # print(data["passenger"])
                                print("|", center_fuction_for_view(str(data["passenger"])),"|",center_fuction_for_view(str(data["seats"])),"|",center_fuction_for_view(str(data["totalseats"])),"|",center_fuction_for_view(str(bus_dictionary[serial]["route"])),"|")
                            print("-"*73)
                            print("\n\n")

        elif manage_res_choice == '5':
            print("Enter date: ")
            search_res_date= input()
            if time_function(search_res_date):
                print("Enter route: ")
                search_res_route = input()
                print("Enter name: ")
                search_res_name = input()
                search_reservation(search_res_date,search_res_route,search_res_name)

                
            # print("search reservation choosed")
        elif manage_res_choice == '6':
            print("main menu choosed")
            break
        else:
            print("make a right choice")


while True:
    print("""
            -----BUS MANAGEMENT SYSTEM-----
            Please make a choice...
            1: Manage BUS...
            2: Manage RESERVATION...
            3: EXIT...""")
    choice = input(str())
    if choice == '1':
        # print("you choosed ADD BUS")
        manage_bus()
    elif choice == '2':
        # print("you choosed ADD RESERVATION")
        manage_reservation()
    elif choice == '3':
        print("you choosed EXIT")
        break
    else:
        print("Make a right choice..")