#!/usr/bin/env python
#   coding:utf-8

import web
import time

urls = (
    '/', 'Index',
    '/todo/new', 'New',
    '/todo/(\d+)/edit', 'Edit',
    '/todo/(\d+)/delete', 'Delete',
    '/todo/(\d+)/finished', 'Finished',
)

render = web.template.render('templates')
app = web.application(urls, globals())

db = web.database(dbn='mysql', user='root', pw='lifayi', db='todo')

def get_by_id(id):
    s = db.select('todo', where='id=$id', vars=locals())
    if not s:
        return False
    return s[0]

class Index(object):
    def GET(self):
        todos = db.select('todo', order='finished ASC, id ASC')
        return render.index(todos)

class New(object):
    def POST(self):
        i = web.input()
        title = i.get('title', 0)
        if not title:
            return render.error('Title is needed!!!')
        db.insert('todo', title=title, post_date=time.strftime('%Y-%m-%d %X'))
        raise web.seeother('/')

class Edit(object):
    def GET(self, id):
        s = get_by_id(id)
        if not s:
            return render.error('Item not exist!!!')
        return render.edit(id,s.title) 

    def POST(self, id):
        if not get_by_id(id):
            return render.error('Item not exist!!!')
        i = web.input()
        title = i.get('title', None)
        if not title:
            return render.error('Title is needed!!!')
        db.update('todo', where='id=$id', title=title, post_date=time.strftime('%Y-%m-%d %X',time.localtime()), vars=locals())
        raise web.seeother('/')

class Delete(object):
    def GET(self, id):
        if not get_by_id(id):
            return render.error('Item not exist!!!')
        else:
            db.delete('todo', where='id=$id', vars=locals())
        raise web.seeother('/')
    
class Finished(object):
    def GET(self, id):
        if not get_by_id(id):
            return render.error('Item not exist!!!')
        i = web.input()
        status = int(i.get('status', 0))
        db.update('todo', where='id=$id', finished=status, vars=locals())
        raise web.seeother('/')

if __name__ == '__main__':
    app.run()
