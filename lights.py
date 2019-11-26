import requests
import time
import json

url = 'url_of_api'

class hue:

    def __init__(self, input_data = int):

        self.root = input_data

    def lights_info(self):  # dictionary of all available bulbs

        all_lights = requests.get(url=url + '/lights')
        lights_data = all_lights.json()

        light_info = {}
        for i in range(0, len(lights_data.keys())):
            light_no = list(lights_data.keys())[i]
            name = lights_data[light_no]['name']
            light_info.update({light_no: name})

        return light_info

    def groups_info(self):  # dictionary of all available groups

        all_lights = requests.get(url=url + '/groups')
        lights_data = all_lights.json()

        group_info = {}
        for i in range(0, len(lights_data.keys())):
            group_no = list(lights_data.keys())[i]
            name = lights_data[group_no]['name']
            group_info.update({group_no: name})

        return group_info

    def count_lights(self):  # counts the total amount of lights

        all_lights = requests.get(url=url + '/lights')
        lights_data = all_lights.json()

        count_lights_counter = 0
        for i in range(0, len(lights_data.keys())):
            light_name = list(lights_data.keys())[i]
            is_on = lights_data[light_name]['state']['reachable']

            if is_on == True:
                count_lights_counter += 1

        return count_lights_counter

    def get_colour(self, id): # gets the current hue, saturation and brightness of inputted bulb

        hue = requests.get(url=url + '/lights/' + str(id)).json()['state']['hue']
        sat = requests.get(url=url + '/lights/' + str(id)).json()['state']['sat']
        bri = requests.get(url=url + '/lights/' + str(id)).json()['state']['bri']

        return (hue, sat, bri)

    def count_lights_on(self):  # counts the all_lights of lights that are on

        all_lights = requests.get(url=url + '/lights')
        lights_data = all_lights.json()

        count_lights_on_counter = 0
        for i in range(0, len(lights_data.keys())):
            light_name = list(lights_data.keys())[i]
            is_on = lights_data[light_name]['state']['on']

            if is_on == True:
                count_lights_on_counter += 1

        return count_lights_on_counter

    def switch(self, id, status): # switches the state of the bulb

        if status == 'on':

            requests.put(url=url + '/lights/' + str(id) + '/state', data='{"on": true}')

        elif status == 'off':

            requests.put(url=url + '/lights/' + str(id) + '/state', data='{"on": false}')

        else:
            print('Error')



    def change_colour(self, id, hue, sat, bri):  # changes the colour of the bulb

        requests.put(url=url + '/lights/' + str(id) + '/state', data='{"hue": ' + str(hue)
                                                                     + ', "sat": ' + str(sat)
                                                                     + ', "bri": ' + str(bri) + '}')

    def police(self): # function for fun - flashes like police sirens

        self.switch(1, 'on')
        self.switch(3, 'on')
        prev_col = self.get_colour(1)
        prev_col2 = self.get_colour(3)

        i = 0
        while True:

            self.change_colour(1, 46000, 254, 254)
            self.change_colour(3, 46000, 254, 254)
            time.sleep(0.7)
            self.change_colour(1, 728, 200, 254)
            self.change_colour(3, 728, 200, 254)
            time.sleep(0.6)

            i += 1
            if i >= 4:
                break

        self.change_colour(1, prev_col[0], prev_col[1], prev_col[2])
        self.change_colour(3, prev_col2[0], prev_col2[1], prev_col2[2])

    def get_state(self): # finds out if a bulb is on or off

        status = requests.get(url=url + '/lights/3').json()['state']['on']

        return status



    class groups(): # class to affect groups instead of individual bulbs

        def __init__(self, group_id=int):

            self.group_id = group_id

            if self.group_id != None:
                self.group_url = url + '/groups/' + str(self.group_id) + '/action'
            else:
                self.group_url = url + '/groups/1/action'

        def pulse(self): # all the lights in the group pulse

            pulse_data = {'on': True, 'transitiontime': 40, 'alert': 'select'}
            requests.put(url=self.group_url, data=json.dumps(pulse_data))

        def get_group_colour(self): # gets group colour

            hue = requests.get(url=url + '/groups/' + str(self.group_id)).json()['action']['hue']
            sat = requests.get(url=url + '/groups/' + str(self.group_id)).json()['action']['sat']
            bri = requests.get(url=url + '/groups/' + str(self.group_id)).json()['action']['bri']

            return (hue, sat, bri)

        def change_group_colour(self, hue, sat, bri):  # changes the colour of the group

            requests.put(url=url + '/groups/' + str(self.group_id) + '/action', data='{"hue": ' + str(hue)
                                                                                     + ', "sat": ' + str(sat)
                                                                                     + ', "bri": ' + str(bri) + '}')

        def get_group_state(self): # gets the status of the group

            status = requests.get(url=url + '/lights/3').json()['state']['on']

            return status

        def group_switch(self, status): # switches group lights status

            if status == 'on':

                requests.put(url=self.group_url, data='{"on": true, "transitiontime":10}')

            elif status == 'off':

                requests.put(url=self.group_url, data='{"on": false}')

            else:
                print('Error')


def h_h(hue, sat, bri): # converts hue from long to short
    percentage = 65535 / 360
    hue = round(percentage * hue)
    sat = round(sat * 254)
    bri = round(bri * 245)

    return (hue, sat, bri)


