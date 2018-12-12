#!/bin/env python

import os
import re
import datetime
import feedgen
from feedgen.feed import FeedGenerator

CHANGELOGS="../../release-data/changelogs/"

major_versions = [version for version in os.listdir(CHANGELOGS) if (not version.endswith(".md")) and (version != "plugins") ]

print(major_versions)

releases = {}
plugin_releases = {}

for major_version in major_versions:
    plugin_releases[major_version] = {}
    releases[major_version] = {}

    with open(CHANGELOGS+major_version+"/main.adoc", "r") as main:
        lines = main.readlines()
        for line in lines:
            search = re.compile('^== Rudder (\d+\.\d+\.\d+) \((\d{4})-(\d{2})-(\d{2})\)$')
            res = search.search(line)
            if res:
                releases[major_version][res.group(1)] = datetime.date(int(res.group(2)), int(res.group(3)), int(res.group(4)))

    if os.path.isdir(CHANGELOGS+"/"+major_version+"/plugins/"):
        for plugin in os.listdir(CHANGELOGS+"/"+major_version+"/plugins/"):
            plugin_name = plugin[:-5]
            plugin_releases[major_version][plugin_name] = {}

            with open(CHANGELOGS+major_version+"/plugins/"+plugin, "r") as main:
                lines = main.readlines()
                for line in lines:
                    # == change-validation-5.0-1.2 (2018-11-28)
                    search = re.compile('^== '+plugin_name+'-\d+\.\d+\-(\d+\.\d+) \((\d{4})-(\d{2})-(\d{2})\)$')
                    res = search.search(line)
                    if res:
                        plugin_releases[major_version][plugin_name][res.group(1)] = datetime.date(int(res.group(2)), int(res.group(3)), int(res.group(4)))

print(releases)
print(plugin_releases)


fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('Rudder releases')
fg.author( {'name':'Rudder developpers','email':'contact@rudder.io'} )
fg.link( href='http://example.com', rel='alternate' )
fg.logo('https://docs.rudder.io/favicon.ico')
fg.subtitle('This feed contains all Rudder releases')
fg.link( href='https://docs.rudder.io/test.atom', rel='self' )
fg.language('en')

fe = fg.add_entry()
fe.id('Rouder')
fe.title('Rudder 4.2.3')
fe.link(href="http://lernfunk.de/feed")

fg.atom_file('atom.xml') # Write the ATOM feed to a file
fg.rss_file('rss.xml') # Write the RSS feed to a file


for major_version in releases:
    for minor_version in releases[major_version]:
        print(major_version + " " + minor_version + " " + str(releases[major_version][minor_version]))

for major_version in plugin_releases:
    for plugin in plugin_releases[major_version]:
        for version in plugin_releases[major_version][plugin]:
            print(major_version + " " + plugin + " " + version + " " + str(plugin_releases[major_version][plugin][version]))
