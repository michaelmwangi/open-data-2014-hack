# -*- coding: utf-8 -*-
"""
.. module:: core
        :platform: web
        :synopsis: Open Data 2014 Hack Core Module

        This modules contain core logic functions.

.. Project:: Open Data 2014 Hack
.. Filename:: core.py
.. Description:: core functions for handling csv data
.. Developer:: Matt Gathu <mattgathu@gmail.com>
.. Date:: 22nd Feb 2014

"""

#=======================================================================
#               process csv data to dicts
#=======================================================================
def create_results_dicts(csv_data):
    """
    Transform csv data to python dictionaries.

    Args:
        csv_data (str): comma separated values 


    Returns:
        res (list): a list of dictionaries

    """
    res = []
    for line in csv_data:
        # split comma separated elements
        data = line.split(',') 
        # ignore lines with fewer than required elements
        if len(data) < 9: 
            pass
        else:
            # convert utf-8 strings to ascii and
            # ignore the fast element of the list (serial no)
            data = [str(x).decode('ascii', 'ignore') for x in data[1:]]
            index = data[0]
            name = data[1]
            gender = data[2]
            primary_sch = data[3]
            cat = data[4]
            marks = data[5]
            hi_sch = data[6]
            district = data[7]
            
            # form dict
            dic = {
                    'index': index,
                    'name': name,
                    'gender':  gender,
                    'primary_school':  primary_sch,
                    'category':  cat,
                    'marks':  marks,
                    'highschool':  hi_sch,
                    'district': district
                    }
            res.append(dic)

    # return list of dicts
    return res

#=============================================================
#           helper function
#============================================================

def is_number(string):
    """
    Determine is string is a number

    Args:
        string (str): string

    Returns:
        True/False (boolean): test results/affirmation

    """
    try:
        float(string)
        return True
    
    except ValueError:
        return False


#===============================================================
#                 data processing
#==============================================================
def process_results(results_dicts):
    """
    Determine Public/Privated Candidates admitted to a Particular School.

    Args:
        results_dicts (list): list of dictionaries

    Returns:
        final_res (list): mainlist with sublists
            sublist = [school, public candidates, private candidates]
            last list in the mainlist is a list of the highschools

    """
    res_dicts = results_dicts
    
    # sort list by highschool name: for faster analysis
    res_dicts.sort(key=lambda x: x['highschool'])
    
    # get highschool names
    hi_schs = list(set([str(x['highschool']) for x in res_dicts if
                    not is_number(x['highschool']) ]))
    
    final_res = []

    for school in hi_schs:
        # get students admitted to a particular school
        sch_data = [x for x in res_dicts if str(x['highschool']) == school]
        
        private = 0
        public = 0
        for data in sch_data:
            # get private and public tally
            if str(data['category']).lower() == 'private':
                private  = private + 1
            else:
                public = public + 1
        
        # calculate percentages
        total = private + public
        public = (float(public)/total) * 100
        private = (float(private)/total) * 100
        
        # form result sublist
        result = [school, public, private]

        # append sublist to mainlist
        final_res.append(result)

    # append highschools names list to mainlist
    final_res.append(hi_schs)
    
    # return mainlist
    return final_res
