# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103
"""
.. module:: app
    :platform:: web
    :synopsis:: flask web app

    This module contains the flask app that provides a web interface

.. Project:: Open Data 2014 Hack
.. Filename:: app.py
.. Description:: flask web application
.. Developer:: Matt Gathu <mattgathu@gmail.com>
.. Date:: 22nd Feb 2014


"""

# import necessary modules
import json

from flask import Flask, render_template, request

from core import create_results_dicts, process_results


# initialize flask app
app = Flask(__name__)


# get csv data
csv_data = open('csvfile.csv').read()

# split data by lines and ignore header line
csv_data = str(csv_data).split('\n')
csv_data = csv_data[1:]


# create dicts from data
data = create_results_dicts(csv_data)


# process dicts
data = process_results(data)

# get list of schools names and sort alphabetically
schs = [str(x).lower() for x in data[-1]]
schs.sort()

# remove school names list from data's mainlist
data.pop()

# transformer list to json dictionar(ies/y)
sch_data = [json.dumps(x) for x in data]


#===============================================================================
#                    app controllers definitions
#==============================================================================
@app.route('/')
@app.route('/index')
def index():
    """
    Application's Landing Page

    """
    
    return render_template('index.html', schools=schs, 
            school_data=None, subheader=None)


@app.route('/visualize', methods=['POST'])
def visualize():
    """
    Visualization Page

    """
    sch = request.form['school']
    
    sch_data = [x for x in data if str(x[0]).lower()==sch][0]
    
    sch_data = json.dumps([ ['Private', sch_data[2]], ['Public', sch_data[1]] ])
    
    subhdr = '{} visualized'.format(sch)

    return render_template('index.html', schools=schs,
            school_data = sch_data, subheader=subhdr)
    

if __name__ == '__main__':
    app.run()
