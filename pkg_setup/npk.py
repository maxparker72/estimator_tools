#!/usr/bin/env python
# coding: utf-8

#File Imports
import os
from datetime import date
import zipfile
from shutil import copytree
from os.path import exists
import json
import configparser
import sys

#GUI Imports For File Selection
import tkinter
from tkinter import filedialog
from tkinter import Tk

#Imports for Notion Updates
import requests

#config location
config_path = os.path.join(sys.path[0], "config.ini")
def main(argv):    
    #Check Configuration
    config_exists = exists(config_path)
    home = os.getcwd()
    
    if config_exists:
        configuration = configparser.ConfigParser()
        configuration.read(config_path)
    else: 
        print('Configuration missing! Create configuration file!')
        sys.exit()

    prefix = configuration['DEFAULT']['prefix']
    stages = ['IFC','POS','PRD','30','60','90'] #default stages

    pkg_name = '{}-{}'.format(prefix, input('Name: ').strip().upper())

    print('Stages Available: {}'.format(stages))
    pkg_stage = input('Stage: ').strip().upper()
    while(pkg_stage not in stages):
        print('Stages: {}'.format(stages))
        print('Pick Preset Stage!')
        pkg_stage = input('Stage: ').strip().upper()

    pkg_desc = input('Description: ').strip().upper().replace(' ','_')
    pkg_owner = input('Owner: ').strip().upper()

    #Create a dictionary from package data 
    pkg_info = {
        'pkg_name' : pkg_name,
        'pkg_stage' : pkg_stage,
        'pkg_desc' : pkg_desc,
        'pkg_date' : date.today().isoformat(),
        'pkg_owner' : pkg_owner
    }

    print('PACKAGE INFO:')
    print('-'*20)
    for key in pkg_info:
        print('{}: {}'.format(key,pkg_info[key]))
    print('-'*20)

    #TODO make this text based for selecting files from downloads by listing zips and msgs in downloads folder?
    #Select original files
    application_window = tkinter.Tk()
    application_window.attributes("-topmost", True)
    pkg_original = filedialog.askopenfilename(initialdir=configuration['DEFAULT']['local_downloads'], title="Please select package zip file:", parent=application_window)
    pkg_email = filedialog.askopenfilename(initialdir=configuration['DEFAULT']['local_downloads'], title="Please select package email file:", parent=application_window)
    application_window.destroy()

    #check file extensions and make sure they are correct
    is_zip = pkg_original[-4:]=='.zip'
    is_msg = pkg_email[-4:]=='.msg'

    #prepare package 
    #TODO logic to make sure this valid, add dialog that pops up. 
    if not (is_zip and is_msg):
        print('Incorrect files! Nothing was done.')
        sys.exit()

    pkg_filename = '{}-{} - {}'.format(pkg_info['pkg_name'], pkg_info['pkg_stage'], pkg_info['pkg_date']) #for use in my files
    pkg_filename_bb = 'A - {} - {} - {} - {}'.format(pkg_info['pkg_name'], pkg_info['pkg_stage'], pkg_info['pkg_desc'], pkg_info['pkg_date']) #for use in bluebeam

    print('Creating package folder.')
    #new folder with package name
    os.chdir(configuration['DEFAULT']['local_downloads'])
    os.mkdir(pkg_filename)

    print(' Unzipping package contents to package folder.')
    #unzip contents to that folder
    with zipfile.ZipFile(pkg_original, 'r') as zip_ref:
        zip_ref.extractall(pkg_filename)

    print(' Moving zip into package folder.')
    #move zip file folder with proper name
    os.rename(pkg_original, os.path.join(pkg_filename, pkg_filename+'.zip')) #move

    #TODO: Right here would be where i want to select transmittal files and check against them. 
    
    print('Copying package folder to relevant locations')
    #relative to downloads folder because thats where os is. 
    #yes the last three are the same for clarity of flow and reading. 
    if pkg_info['pkg_stage']==stages[0]:
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['public_ifc'], pkg_filename))
        os.rename(pkg_email, os.path.join(pkg_filename,pkg_filename+'.msg')) #move
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['private_ifc'], pkg_filename))
        # TODO: Create a folder in SBN and Bids for package name with standard folders.
    elif pkg_info['pkg_stage']==stages[1]:
        os.rename(pkg_email, os.path.join(pkg_filename,pkg_filename+'.msg')) #move
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['private_pos'], pkg_filename))
    elif pkg_info['pkg_stage']==stages[2]:
        os.rename(pkg_email, os.path.join(pkg_filename,pkg_filename+'.msg')) #move
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['private_prd'], pkg_filename))
    elif pkg_info['pkg_stage']==stages[3]:
        os.rename(pkg_email, os.path.join(pkg_filename,pkg_filename+'.msg')) #move
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['private_dd'], pkg_filename))
    elif pkg_info['pkg_stage']==stages[4]:
        os.rename(pkg_email, os.path.join(pkg_filename,pkg_filename+'.msg')) #move
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['private_dd'], pkg_filename))
    elif pkg_info['pkg_stage']==stages[5]:
        os.rename(pkg_email, os.path.join(pkg_filename,pkg_filename+'.msg')) #move
        copytree(pkg_filename, os.path.join(configuration['DEFAULT']['private_dd'], pkg_filename))
    else:
        print('Copy failed! Please perform manually!')

    use_notion_input = input('Make Notion entry? (y/n): ').lower()
    use_notion = 'y' == use_notion_input
    
    if use_notion:
        print('Creating Notion entry!')
        #Open Notion Template json for new package
        nt_exists = os.path.exists(os.path.join(home,'new_package.json'))
        if nt_exists:
            with open(os.path.join(home,'new_package.json')) as json_file:
                data = json.load(json_file) #load templated file for new package item


            data['properties']['Name']['title'][0]['text']['content'] = '{}-{}'.format(pkg_info['pkg_name'], pkg_info['pkg_stage'])
            data['properties']['Owner']['rich_text'][0]['text']['content'] = pkg_info['pkg_owner']

            #Authenticate Notion API
            database_id = configuration['DEFAULT']['database_id']
            token = configuration['DEFAULT']['token']

            createurl ='https://api.notion.com/v1/pages'
            cheaders = {
                'Authorization' : 'Bearer ' + token,
                'Content-Type': 'application/json',
                'Notion-Version' : '2021-08-16'
            }
            r = requests.request('POST', createurl, headers = cheaders, data = json.dumps(data))
            print('Status of Notion post: {}'.format(r.status_code))
        else:
            print('Notion template open failed! Notion entry not created!')
    
    #Preparing local version
    print('Preparing local version.')
    os.chdir(pkg_filename)
    wrk_filename = 'work-{}'.format(date.today().isoformat())
    os.mkdir(wrk_filename) #make work folder
    os.chdir(wrk_filename)
    with open(pkg_filename_bb+".pdf",'w') as bbname:
        print('Bluebeam package name empty PDF created.')

    print('Local copy is in downloads folder.')

if __name__ == "__main__":
   main(sys.argv[1:])