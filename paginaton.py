#!/usr/bin/env python
##
# Basic pagination class meant for use with Python based web frameworks
#
# ----------------------------------------
# Example in Bottle with Jinja2 templates
# ----------------------------------------
# from pagination import Pagination
#
# from bottle import request
# from jinja2.enviroment import Environment
# from jinja2.loaders impor FileSystemLoader
#
# env = Environment()
# env.loader = FileSystemLoader('html/')
#
# def paged_search(query, page=1, num_items=25):
#     total = db.count(query)
#
#     if total is None:
#         return (None, 'no items found')
#     if page <= 0:
#         page = 1
#
#     paging = Pagination(total_items)
#
#     results = db.search(query, skip=paging['start'], total=paging['num'])
#     return (results, pagination)
#
# @route('search', method='GET')
# def run_search(query, page=1, num_items=25):
#     if request.query.page and request.query.page != '':
#         if int(request.query.page) <= 0:
#             page = 1
#         else:
#             page = int(request.query.page)
#
#     if request.query.items and request.query.items != '':
#         num_items = request.query.items
#
#
#     results, pagination = paged_search(query, page, num_items)
#     template = env.get_template('search/results.html')
#     return template.render(results=results, pagination=pagination)
##

from math import ceil


class Pagination(object):
    def __init__(self, current_page=0, total_items=None, num_items=25):
        self.total = total_items
        self.page  = current_page
        self.num = num_items
        self.last = self._total_pages
        self.start = self._start
        self.end = self._end
        self.count = self._count
        self.prev = self._previous
        self.next = self._next


    def __repr__(self):
        """ return as dictionary to be used more easily in Python webapp templates """
        if 'total' in self.__dict__:
            del self.__dict__['total']
        return str(self.__dict__)


    @property
    def _start(self):
        return self.page * self.num - self.num


    @property
    def _end(self):
        return ((self.page * self.num - self.num) + self.num - 1)


    @property
    def _count(self):
        return self.total


    @property
    def _total_pages(self):
        return int(ceil(float(self.total) / self.num))


    @property
    def _previous(self):
        return self.page - 1 if self.page > 1 else None


    @property
    def _next(self):
        return self.page + 1 if self.page < self._total_pages else None
