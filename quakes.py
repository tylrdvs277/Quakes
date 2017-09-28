# Name:         Tyler Davis
# Course:       CPE 101
# Instructor:   Nupur Garg
# Assignment:   Project 5
# Term:         Spring 2017

import quake_funcs

def main():
    website = ("http://earthquake.usgs.gov/earthquakes"
               "/feed/v1.0/summary/1.0_hour.geojson")
    quakes = quake_funcs.read_quakes_from_file("quakes.txt")
    option = "Y"
    while option not in "qQ":
        if option in "fF":
            quake_funcs.display_quakes(filtered_quakes)
        else:
            quake_funcs.display_quakes(quakes)
        (option, sub_option, search_string, 
         lower_bound, upper_bound) = quake_funcs.get_input()
        if option in "sS":
            quakes = quake_funcs.sort_quakes(
                     list(quakes), sub_option.lower())
        elif option in "fF":
            if sub_option in "mM":
                filtered_quakes = quake_funcs.filter_by_mag(quakes, 
                     lower_bound, upper_bound)
            else:
                filtered_quakes = quake_funcs.filter_by_place(quakes, 
                                       search_string)
        elif option in "nN":
            quakes_dict = quake_funcs.get_json(website)
            new_quakes = quake_funcs.get_new_quakes(
                              quakes_dict["features"])
            temp_quakes = quake_funcs.add_if_new(
                          list(quakes),list(new_quakes))
            quakes = quake_funcs.update_quakes_list(
                     quakes, temp_quakes) 
    quake_funcs.write_new_file(quakes)

if __name__ == "__main__":
    main()
