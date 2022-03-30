# recoding autobilz but smarter
# vanilla 3.8.10

# updated 2/10, added FIXED amount functionality

import csv
import math
from datetime import date
from fpdf import FPDF

def text_to_pdf(text, filename):
    pdf = FPDF(orientation = 'P', format = 'Letter')
    pdf.add_page()
    pdf.set_font(family='Courier', size = 12)
    for line in text:
        pdf.cell(0, h = 4.5, txt = line)
        pdf.ln()
    pdf.output("output/{}.pdf".format(filename), 'F')

# date initialization 
today = date.today()
todays_date = today.strftime("%m/%d/%Y")

# csv data strcuture
# new line
def add_row(row_list, row):
    row_list.append(row)

# insert line
def insert_top_row(row_list, row):
    row_list.insert(0, row)

# returns sum of inputted collumn 
def calc_net_hours(row_list, col):
    sum = 0
    for row in row_list:
        sum += row[col]
    sum /= 60
    return sum

# sorts rows numerically by first collumn then removes search criteria
def sort_day(row_list):
    row_list = sorted(row_list, key=lambda col: (col[0]))
    new_row_list = []
    for row in row_list:
        add_row(new_row_list, row[1:])  
    return new_row_list

# filter data by company to new sheet object (created outside of method scope)
def filtered_copy(row_list, lttr):
    new_row_list = []
    for row in row_list:
        if(row[0] == lttr):
            add_row(new_row_list, row[1:])
    return new_row_list

# writes to actual csv file
def output_to_csv(row_list, csv_name):
    csv_out = open("output/{}.csv".format(csv_name), 'w')
    writer = csv.writer(csv_out)
    for row in row_list:
        writer.writerow(row)
    csv_out.close()

# converts time to hours, minutes
def pretty_time(int_hours):
    hours = math.floor(int_hours)
    minutes = math.floor(round(int_hours % 1 * 60, 0))
    return "{}:{}:00".format(hours, minutes)

# event class
class event():
    company_lttr = "xERR"
    start_timestring = "00000000T000000Z"
    end_timestring = "00000000T000000Z"
    details = "no data found"
    duration = 0
    date = "00/00/0000"
    key = 0
    day = 0

    # event reset to default values
    def reset(self):
        # direct write
        self.company_lttr = "xERR"
        self.start_timestring = "00000000T000000Z"
        self.end_timestring = "00000000T000000Z"
        self.details = "no data found"

        # calculated
        self.duration = 0
        self.date = "00/00/0000"
        self.key = 0
    
    # writing methods
    def write_start_timestring(self, value):
        self.start_timestring = value
    def write_end_timestring(self, value):
        self.end_timestring = value
    def write_company_lttr(self, value):
        self.company_lttr = value
    def write_details(self, info):
        self.details = info

    # return methods
    def get_company_name(self):
        return self.company_lttr
    def get_key(self):
        return self.key
    def generate_row(self):
        row = [self.company_lttr, self.day, self.date, self.duration, self.details]
        return row
    
    # creates row ready for import into dumm_csv after testing for key match
    def run_analysis(self):
        # end timestring breakdown
        end_day = int(self.end_timestring[6:8])
        end_hour = int(self.end_timestring[9:11])
        end_minutes = int(self.end_timestring[11:13])
        
        # start timestring breakdown
        start_year = int(self.start_timestring[0:4])
        start_month = int(self.start_timestring[4:6])
        start_day = int(self.start_timestring[6:8])
        start_hour = int(self.start_timestring[9:11])
        start_minutes = int(self.start_timestring[11:13])
        
        # duration calculation
        self.duration = ((end_day-start_day)*24 + (end_hour-start_hour))*60+(end_minutes-start_minutes)
    
        # timezone correction
        if(start_hour <= 7):
            start_day -= 1
            if(start_day <= 0):
                start_day == 32 # I know this is ugly but it's better than missing it, I'm not writing a library for how many days are in each month
                start_month -= 1
        
        self.date = "{}/{}/{}".format(start_year, start_month, start_day)
        self.key = "{}{}".format(start_year, start_month)
        self.day = start_day

    
# user input initializing 
print("Thank you for using AUTOBILZ on {}!".format(todays_date))
ical_file_name = input("What is the name of the ical file you're using?\n[DO NOT INCLUDE \".ics\" EXTENSION]\n: ")
search_year = input("what year are you searching in? [YYYY]\n: ")
search_month = input("what month are you searching in? [MM]\n: ")
lock = "{}{}".format(int(search_year), int(search_month))
print("Please wait while your file is read... \n")

# ICS file parsing code
all_data = []
company_list = []
new_event = event()

# file open
ical_file = open(ical_file_name+".ics", mode = 'rt', encoding='utf-8')
lines = ical_file.readlines()

# file stepthrough 
for line in lines:

    # basically everything you need to parse ical files
    line_type = line[0:line.find(':')]
    content = line[line.find(':')+1:].strip()
    
    # corrects for timezone string appended between DTSTART;[ical gibberish]:[timestring]
    if(len(line_type)>7):
        line_type = line_type[0:line.find(';')]
    
    # reset event data
    if(line_type == "BEGIN"):
        new_event.reset()
    
    # store start timestring
    elif(line_type == "DTSTART"):
        new_event.write_start_timestring(content)
    
    # store end timestring
    elif(line_type == "DTEND"):
        new_event.write_end_timestring(content)
    
    # get company LTTR acronym and event details
    elif(line_type == "SUMMARY"):
        new_event.write_company_lttr(content[0:4])
        new_event.write_details(content[5:])
    
    # run analysis, check lock and key, add company to list
    elif(line_type == "END"):
        new_event.run_analysis()
        event_key = new_event.get_key()
        if (event_key == lock):
            add_row(all_data, new_event.generate_row())
            company_acronym = new_event.get_company_name()
            if((company_acronym in company_list)==False):
                company_list.append(company_acronym)
        new_event.reset()

# info printout
print("\"{}\" has been parsed! You worked {} this month for {} clients!\n".format(ical_file_name, pretty_time(calc_net_hours(all_data, 3)), len(company_list)))

# user input output selection for hourly billing
hourly_companies = []
user_input = ""
while(user_input != "done"):
    print("please select companies to bill hourly, enter \"done\" when done")
    print("         options: {}".format(company_list))
    print("     bill hourly: {}".format(hourly_companies))
    user_input = input("                : ")
    print("\n")
    # input check to ensure only companys that exist are added
    if((user_input in company_list) == True):
        hourly_companies.append(user_input)
        company_list.remove(user_input)
    elif((user_input in company_list) == False and (user_input != "done")):
        print("whoops, looks like that's not a valid option!\n")

# user input output selection for minute summaries
not_hourly_companies = []
user_input=""
while(user_input != "done"):
    print("please select companies to generate minutes summaries for, enter \"done\" when done")
    print("         options: {}".format(company_list))
    print("     bill hourly: {}".format(hourly_companies))
    print("not billed houry: {}".format(not_hourly_companies))
    user_input = input("                : ")
    print("\n")
    if((user_input in company_list) == True):
        not_hourly_companies.append(user_input)
        company_list.remove(user_input)
    elif((user_input in company_list) == False and (user_input != "done")):
        print("whoops, looks like that's not a valid option!\n")

# hourly billng code
for company in hourly_companies:
    # read client's billing profile
    client_info = open("reference/clients/{}.txt".format(company), 'r')
    lines = client_info.readlines()

    # parameters sought
    rate = 0
    fixed = 0
    billing_name = ""
    billing_info = []

    # line stepthrough
    for line in lines:
        line_type = line[0:line.find(':')]
        content = line[line.find(':')+1:].strip()
        if(line_type == "RATE"):
            rate = int(content)
        elif(line_type == "FIXED"):
            fixed = int(content)
        else:
            billing_info.append(line)
            if(line_type == "  Company"):
                billing_name = content

    # filter and datesort
    company_csv = filtered_copy(all_data, company)
    company_csv = sort_day(company_csv)
   
    # headder 
    net_hours = calc_net_hours(company_csv, 1)
    if (fixed != 0):
        net_bill = fixed
    else:
        net_bill = rate*net_hours

    insert_top_row(company_csv, ["Date", "Minutes", "Event"])
    insert_top_row(company_csv, [])
    insert_top_row(company_csv, ["Net Bill:", "", "${}".format(round(net_bill, 2))])
    insert_top_row(company_csv, ["Net Hours:", "", round(net_hours, 2)])
    insert_top_row(company_csv, ["Hourly Billing Rate:", "", "${}".format(rate)])

    # coppy in billing info
    billing_info_csv = open("reference/billing_info.csv", 'r')
    lines = billing_info_csv.readlines()
    for line in lines:   
        row = line.strip().split(',') 
        insert_top_row(company_csv, row)
    
    # write headder 2
    insert_top_row(company_csv, ["Billing Date:", "", todays_date])
    insert_top_row(company_csv, ["Client:", "", billing_name])

    # write csv to file
    output_to_csv(company_csv, "01_{}_{}_{}".format(search_month, search_year, company))

    # generate bill txt file
    bill = []
    bill_format = open("reference/bill_format.txt", 'r')
    lines = bill_format.readlines()
    for line in lines:
        line_type = line[0:line.find(':')]
        content = line[line.find(':')+1:].strip()
        if(line_type == "?"):
            if(content == "billing_info"):
                for line in billing_info:
                    bill.append(line)
                bill.append("\n")
            elif(content == "invoice_info"):
                bill.append("          Date: {}\n".format(todays_date))
                bill.append("Invoice Number: 01_{}_{}_{}\n".format(search_month, search_year, company))
                bill.append("        Amount: ${}\n".format(round(net_bill, 2)))
        else:
            bill.append(line)
    
    # write bill text file
    text_to_pdf(bill, "01_{}_{}_{}".format(search_month, search_year, company))
    
# not hourly condensing code
for company in not_hourly_companies:
    # filter and sort data
    company_csv = filtered_copy(all_data, company)
    company_csv = sort_day(company_csv)
    out_csv = []
    minute_list = []
    last_date = ""
    for row in company_csv:
        current_date = row[0]
        duration = int(row[1])
        if(current_date == last_date):
            minute_list.append(duration)
        elif(current_date != last_date):
            minute_list.insert(0, last_date)
            add_row(out_csv, minute_list)
            minute_list = [duration]
            last_date = current_date
    insert_top_row(out_csv, ["Net Time:", pretty_time(calc_net_hours(company_csv, 1))])
    output_to_csv(out_csv, company+"_FFH")
print("done processing! Have a great day!")