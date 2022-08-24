
from scrapy import cmdline
import time
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Final.spiders import final
from pymongo import MongoClient
import re
import subprocess
import pandas as pd

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
        self.option = ""

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
                            self.__find_winner(collection, date)
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

    def __find_winner(self, collection, date):
        num_winner = input("How many best winners do you want to look?\n Sample: 3\n")
        try:
            num_winner = int(num_winner)
            if num_winner > 0:
                try:
                    winner_cursor = collection.find(sort=[("Percentage", -1),("Change", -1)]).limit(num_winner)
                    winner_list = [winner_info for winner_info in winner_cursor]
                    for winner in winner_list:
                        winner.pop("_id")
                    max_num = collection.estimated_document_count()
                    if num_winner > max_num:
                        print("The max number in this collection is {}. Please note that you entered {}.".format(max_num, num_winner))
                    else:
                        data_frame = pd.DataFrame(winner_list)
                        print(data_frame[["Code", "Name", "Percentage", "Change"]])
                        stuck = input("Please press 'Enter' key to continue.\n")
                        self.__export_by_condition(data_frame, date, num_winner)
                except:
                    if self.option is True:
                        pass
                    else:
                        print("Unknown error, please enter again.")
            else:
                print("Please enter the positive number.")
        except:
            print("Please enter integer.")

    def export_all_by_date(self):
        str = input("Please enter the date that you want to download:\n Sample as 2022_08_20\n")
        for date in self.client["Stock"].list_collection_names():
            if str in date:
                variables = input("Please input the numbers of variables you want to save:\n1. Name\n2. Code\n3. Price\n4. Change\n5. %Change\n6. Volume\n7. Avg_Vol\n8. Market cap\n9. PE\n(Sample: 1,2,3,4)\n")
                variable_list = ["Code", "Name", "Price", "Change", "Percentage", "Volume", "Avg_Vol", "Market_Cap", "PE"]
                choice_list = re.findall(r"\d", variables)
                try:
                    choice_index_list = [int(i)-1 for i in choice_list]
                    export_variable_list = [variable_list[i] for i in choice_index_list]
                    variable_str = ",".join(export_variable_list)
                    subprocess.Popen("mongoexport -d Stock -c {0}  -f {1} --type=csv -o ./data/{0}.csv".format(date,variable_str))
                    print("The file has been exported successfully!")
                except:
                    print("Please enter the correct number in sample format!")
        else:
            print("Format error\n Please enter the correct format")

    def __export_by_condition(self, data_frame, date, num_winner):
        while True:
            self.option = input("Do you want to save the results?\nPlease input Y/N to continue.\n")
            if self.option == "Y" or self.option == "y":
                file_name = date + "_top_{}".format(num_winner)
                data_frame.to_csv("../results/{}.csv".format(file_name), sep=",", index=True, header=True)
                print("Export successfully!")
                break
            elif self.option == "N" or self.option == "n":
                break
            else:
                print("Please input the correct word.")
                continue


def main():
    while True:
        start = input("Welcome to this system!\nPlease choose the following functions:\n 1. View the data in database.\n 2. Update the database \n 3. Export the data by date \n 4. Quit the system\n")
        target = Mongo()
        try:
            start_num = int(start)
            if start_num == 1:
                print("The following is the available dates:")
                target.show_collections()
                target.find_by_date()
            elif start_num == 2:
                Scrapy_spider()
                stuck = input("Please press 'Enter' key to continue.\n")
            elif start_num == 3:
                target.export_all_by_date()
                stuck = input("Please press 'Enter' key to continue.\n")
            elif start_num == 4:
                print("Thanks for using this system.")
                break
            else:
                print("Please input the correct number.")
                continue
        except:
            print("Please input the correct number.")



if __name__ == "__main__":
    main()
