# -*- coding: utf-8 -*-
"""
    longboxed.comics
    ~~~~~~~~~~~~~~

    longboxed comics package
"""
import csv
import gzip
import re

from datetime import datetime, timedelta
from decimal import Decimal
from HTMLParser import HTMLParser
from itertools import groupby

from flask import current_app

from ..core import Service
from .models import Issue, Publisher, Title


class PublisherService(Service):
    __model__ = Publisher


class TitleService(Service):
    __model__ = Title


class IssueService(Service):
    __model__ = Issue

    def find_issues_in_date_range(self, start, end):
        s = start.strftime('%Y-%m-%d')
        e = end.strftime('%Y-%m-%d')
        titles = sorted(self.__model__.query.filter(self.__model__.on_sale_date.between(s,e)))
        sorted_titles = sorted(titles, key=lambda k: k.publisher.name)
        return sorted_titles

    def find_relevent_issues_in_date_range(self, start, end, current_user):
        all_issues = self.find_issues_in_date_range(start, end)
        relevent_issues = all_issues
        matches = []
        if not current_user.is_anonymous():
            if current_user.publishers:
                relevent_issues = [issue for issue in all_issues if issue.publisher in current_user.publishers]
            if current_user.pull_list:
                if current_user.display_pull_list:
                    matches = [c for c in all_issues if c.title in current_user.pull_list]
        return (relevent_issues, matches)


class ComicService(object):
    def __init__(self):
        self.publishers = PublisherService()
        self.titles = TitleService()
        self.issues = IssueService()

    # def insert_comic(self, p=None, t=None, i=None):
    #     publisher = self.publishers.first(name=p['name'])
    #     if not publisher:
    #         # print 'Adding Publisher: %s' % p['name']
    #         publisher = self.publishers.create(**p)

    #     title = self.titles.first(name=t['name'])
    #     if not title:
    #         # print 'Adding Title: %s' % t['name']
    #         t['publisher'] = publisher
    #         title = self.titles.create(**t)

    #     i['publisher'] = publisher
    #     i['title'] = title
    #     issue = self.issues.first(diamond_id=i['diamond_id'])
    #     if issue:
    #         # print 'Updating: %s' % issue.complete_title
    #         issue = self.issues.update(issue, **i)
    #     else:
    #         # print 'Adding Issue: %s' % i['complete_title']
    #         issue = self.issues.create(**i) 
    #     return

    def insert_publisher(self, raw_publisher=None):
        publisher = self.publishers.first(name=raw_publisher)
        if not publisher:
            publisher = self.publishers.create(name=raw_publisher)
        return publisher

    def insert_title(self, raw_title, publisher_object):
        title = self.titles.first(name=raw_title)
        if not title:
            title = self.titles.create(name=raw_title, publisher=publisher_object)
        return title

    def insert_issue(self, raw_issue_dict, title_object, publisher_object):
        # TODO save off issues siblings as well
        issue = self.issues.first(diamond_id=raw_issue_dict['diamond_id'])
        raw_issue_dict['title'] = title_object
        raw_issue_dict['publisher'] = publisher_object
        if issue:
            issue = self.issues.update(issue, **raw_issue_dict) # Create
        else:
            issue = self.issues.create(**raw_issue_dict) # Update
        return issue


    def get_raw_issues(self, ffile):
        print 'Checking for comics'
        # open gzip archive and extract only comics
        with gzip.open(ffile, 'rb') as f:
            comics = []
            reader = csv.reader(f, delimiter='|')
            for item in reader:
                if item[-5] == 'Comics':
                    item = [element for element in item]
                    if item[19] in current_app.config['SUPPORTED_PUBS'] and self.is_diamond_id(item[20]):
                        release_date = datetime.strptime(item[12], '%Y-%m-%d')
                        if release_date.date() > datetime.now().date() and release_date.date() < (datetime.now().date() + timedelta(days=21)):
                            comics.append(item)
        print '...Done'
        return comics


    def extract_issue_information(self, raw_issue):
        # Setup
        p = {}
        t = {}
        i = {}
        parser = HTMLParser()
        # Extract Title Information
        t_info = self.title_regex(raw_issue[1])
        # Publisher
        p = raw_issue[19]
        # Title
        t = t_info['title']
        # Issue
        i['product_id'] = raw_issue[0]
        i['issue_number'] = t_info['issue_number']
        i['issues'] = t_info['issues']
        i['other'] = t_info['other']
        i['complete_title'] = t_info['complete_title']
        # i['one_shot'] = t_info['one_shot']
        i['a_link'] = re.sub('YOURUSERID', current_app.config['AFFILIATE_ID'], raw_issue[4])
        i['thumbnail'] = raw_issue[5]
        i['big_image'] = raw_issue[6]
        i['retail_price'] = float(raw_issue[8]) if self.is_float(raw_issue[8]) else None
        i['description'] = parser.unescape(raw_issue[11])
        try:
            i['on_sale_date'] = datetime.strptime(raw_issue[12], '%Y-%m-%d')
        except:
            i['on_sale_date'] = None
        i['genre'] = raw_issue[13]
        i['people'] = None #### Fixme
        i['popularity'] = float(raw_issue[16]) if self.is_float(raw_issue[16]) else None
        try:
            i['last_updated'] = datetime.strptime(raw_issue[17], '%Y-%m-%d %H:%M:%S')
        except:
            i['last_updated'] = None
        i['diamond_id'] = raw_issue[20]
        i['category'] = raw_issue[21]
        i['upc'] = raw_issue[25]

        return (i, t, p)


    def is_float(self, number):
        try: 
            float(number)
            return True
        except (ValueError, TypeError):
            return False


    def is_diamond_id(self, possible_id):
        """Detects if possible_id is a verifiable DiamondID"""
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        # 'BAG' is checked so as to not include Grab Bags
        if any(month in possible_id for month in months) and 'BAG' not in possible_id:
            return True
        else:
            return False


    def group_issues(self, issues):
        # Sort by title name
        issues = sorted(issues, key=lambda x: x.title)
        # Group by title name
        title_groups = groupby(issues, key=lambda x: x.title)
        # Sort and group by issue number
        issue_number_groups = []
        for k, g in title_groups:
            group = list(g)
            group = sorted(group, key=lambda x: x.issue_number)
            issue_number_group = groupby(group, key=lambda x: x.issue_number)
            issue_number_groups.append(issue_number_group)
        return issue_number_groups


    def title_regex(self, title):
        try:
            # m = re.match(r'(?P<title>[^#]*[^#\s])\s*(?:#(?P<issue_number>(\d+))\s*)?(?:\(of (?P<issues>(\d+))\)\s*)?(?P<other>(.+)?)', title).groupdict()
            m = re.match(r'(?P<title>[^#]*[^#\s])\s*(?:#(?P<issue_number>([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?))\s*)?(?:\(of (?P<issues>(\d+))\)\s*)?(?P<other>(.+)?)', title).groupdict()
            m['complete_title'] = title
            if m['issue_number']:
                m['issue_number'] = Decimal(m['issue_number'])
            if m['issues']:
                m['issues'] = Decimal(m['issues'])
            # print '\n--------------'
            # print 'Full:    ', title
            # print 'Name:    ', m.get('title')
            # print 'Issue #: ', m.get('issue_number')
            # print 'Issues:  ', m.get('issues')
            # print 'Other:   ', m.get('other')
        except (AttributeError, TypeError):
            m = None
        return m


    def test_grouping(self):
        # Get raw text data from daily download
        raw_issues = self.get_raw_issues('dd.gz')
        # Insert raw comic book into the database
        issue_list = []
        for q, raw_issue in enumerate(raw_issues):
            (i, t, p) = self.extract_issue_information(raw_issue)
            publisher = self.insert_publisher(p)
            title = self.insert_title(t, publisher)
            issue = self.insert_issue(i, title, publisher)
            issue_list.append(issue)
            if q % 250 == 0:
                print 'Saved %d / %d comics' % (q, len(raw_issues))
        # Group new issues based on title and issue_number
        groups = self.group_issues(issue_list)
        # Process grouped issues
        for group in groups:
            for k, g in group:
                # Look for pre-exisiting issue in the database but not in new download
                new_issues = list(g)
                w = self.issues.__model__.query.filter_by(title=new_issues[0].title, issue_number=k)
                for i in w:
                    if i not in new_issues:
                        new_issues.append(i)
                # Sort group based on Diamond ID and set a parent for display purposes
                matches = []
                for issue in new_issues:
                    match = re.search(r'\d+', issue.diamond_id)
                    matches.append((int(match.group()), match.string))
                matches.sort(key=lambda x: x[0])
                for issue in new_issues:
                    if issue.diamond_id == matches[0][1]:
                        issue.is_parent = True
                    else:
                        issue.is_parent = False
                    if len(new_issues) > 1:
                        issue.has_alternates = True
                    self.issues.save(issue)
        print 'DONE!'











