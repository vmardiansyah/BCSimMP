
import output_screen
import output_file
import json
import random
from random import randrange

class UserNode:
    def __init__(self, address, parent):
        self.parentAddress = parent
        self.selfAddress = address
        self.tasks = []

    def create_tasks(self, number_of_task_per_user, list_of_end_users):
        persons = ['Agus', 'Budi', 'Chandra', 'Dudi', 'Endang', 'Fahmi', 'Gugun', 'Husain', 'Intan', 'Joni', 'Kevin']
        senderPerson = persons[self.parentAddress-1]
        for i in range(number_of_task_per_user):
            receiverPerson = random.choice(persons)
            while senderPerson == receiverPerson:
                receiverPerson = random.choice(persons)
            random_task = str(senderPerson) + ' sends $ ' + str(randrange(50)) + '.00 to ' + str(receiverPerson)
#            self.tasks.append([self.parentAddress, self.selfAddress, random_task])
            self.tasks.append([senderPerson, receiverPerson, random_task])

    def send_tasks(self, list_of_user_nodes):
        for obj in list_of_user_nodes:
            if obj.address == self.parentAddress:
                obj.receive_tasks(self.tasks, self.selfAddress)
