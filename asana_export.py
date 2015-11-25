#!/usr/bin/python
#
# Copyright (C) 2015 Elana Hashman
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import json
from urllib2 import Request, urlopen

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

api_token = 'secret'

def make_request(api_call):
    "Makes a request to the Asana API"
    return Request(
        'https://app.asana.com/api/1.0' + api_call,
        headers={'Authorization': 'Bearer ' + api_token})


users = {}

def user_lookup(id_num):
    "Translates a user id into a name and keeps a table to reduce HTTP requests"
    global users
    username = users.get(id_num)

    if username is None:
        user_data = urlopen(make_request('/users/' + str(id_num))).read()
        users[id_num] = json.loads(user_data)['data']['name']

    return users[id_num]


# Now we're going to scrape our Asana projects to extract the tasks.

request = make_request('/projects')
projects = json.loads(urlopen(request).read())['data']

for project in projects:
    request = make_request(
        '/projects/' + str(project['id']) + ('/tasks'
        '?opt_fields=assignee,created_at,completed,due_on,name,notes,parent'))

    tasks = json.loads(urlopen(request).read())['data']

    for task in tasks:
        request = make_request(
            '/tasks/' + str(task['id']) + '/stories')

        story = json.loads(urlopen(request).read())['data']

        print 'Name: ' + task['name']
        if task['assignee'] is not None:
            print 'Assigned to: ' + user_lookup(task['assignee']['id'])
        print 'Created at: ' + task['created_at']
        print 'Completed: ' + str(task['completed'])
        print 'Due on: ' + str(task['due_on'])
        print 'Notes: ' + task['notes']

        for line in story:
            print line['created_by']['name'] + ' ' + line['text']

        print ''
