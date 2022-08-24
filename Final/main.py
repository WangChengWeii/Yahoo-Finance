
from scrapy import cmdline
import time
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Final.spiders import final
from pymongo import MongoClient
import re


def Timer(func):
    def call_func():
        start_time = time.time()
        func()
        stop_time = time.time()
        print("Time spent %f" %(stop_time - start_time))
    return call_func


@Timer
def Scrapy_spider():
    # cmdline.execute("scrapy crawl final".split())
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    process.crawl(final.FinalSpider)
    process.start()  # the script will block here until all crawling jobs are finished


class Mongo(object):

    def __init__(self):
        self.client = MongoClient(host="127.0.0.1", port=27017)
        self.opt_in_find_by_date = "Please choose the following functions:\n 1. Show the top winners in this day\n 2. Show all the winners in this day\n 3. return to the upper level\n \n Enter the single number(e.g. 1)\n"

    def show_collections(self):
        name_list = self.client["Stock"].list_collection_names()
        name_list.sort()
        for name in name_list:
            name = re.match(r"Date_(.*)",name).group(1)
            print(name)

    def find_by_date(self):
        str = input("Please enter the date that you want to view:\n Sample as 2022_08_20\n")
        for date in self.client["Stock"].list_collection_names():
            if str in date:
                collection = self.client["Stock"][date]
                # ask user to choose options
                while True:
                    option_num = input(self.opt_in_find_by_date)
                    try:
                        option_num = int(option_num)
                        # find top winner
                        if option_num == 1:
                            self.__find_winner(collection)
                            stuck = input("Please press 'Enter' key to continue.\n")
                        # find all winners
                        elif option_num == 2:
                            data_list = collection.find()
                            for data in data_list:
                                print("Name: ", data["Name"], "\tPrice: ", data["Price"], "\tChange: ", data["Change"], "\tPercentage: ", data["Percentage"], "\tPE: ", data["PE"])
                            stuck = input("Please press 'Enter' key to continue.\n")
                        elif option_num == 3:
                            break
                        else:
                            print("Please enter the correct number!")
                    except:
                        print("Please enter the correct number!")
            else:
                pass
        else:
            if option_num == 3:
                pass
            else:
                print("Format error\n Please enter the correct format")

    def __find_winner(self, collection):
        num_winner = input("How many best winners do you want to look?\n Sample: 3\n")
        try:
            num_winner = int(num_winner)
            if num_winner > 0:
                try:
                    winner_cursor = collection.find(sort=[("Percentage", -1),("Change", -1)]).limit(num_winner)
                    winner_list = [winner_info for winner_info in winner_cursor]
                    max_num = collection.estimated_document_count()
                    if num_winner > max_num:
                        print("The max number in this collection is {}. Please note that you entered {}.".format(max_num, num_winner))
                    else:
                        for winner in winner_list:
                            print("Winner Name:", winner["Name"], "\t Winner %Change", winner["Percentage"], "\t Winner Change", winner["Change"])
                except:
                    print("Unknown error, please enter again.")
            else:
                print("Please enter the positive number.")
        except:
            print("Please enter integer.")






    def export():
        pass


def main():
    while True:
        start = input("Welcome to this system!\nPlease choose the following functions:\n 1. View the data in database.\n 2. Update the database \n 3. Quit the system\n")
        try:
            start_num = int(start)
            if start_num == 1:
                target = Mongo()
                print("The following is the available dates:")
                target.show_collections()
                target.find_by_date()
            elif start_num == 2:
                Scrapy_spider()
                stuck = input("Please press 'Enter' key to continue.\n")
            elif start_num == 3:
                print("Thanks for using this system.")
                break
            else:
                print("Please input the correct number.")
                continue
        except:
            print("Please input the correct number.")



if __name__ == "__main__":
    main()
