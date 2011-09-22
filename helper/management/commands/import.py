from django.core.management.base import BaseCommand, CommandError
import MySQLdb
import sys
from dennych_dvesto.models import Topic, Comment, Category, Photo

class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        topic_type = {
            'text': 1,
            'foto': 2
        }

        try:
            conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '', db = 'nocnabasen_sk_v1', charset = 'UTF8')
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)

            print "importing blog_categories"
            cursor.execute("SELECT * FROM blog_categories")
            rows = cursor.fetchall()
            for row in rows:
                Category(id = row['category_id'], category = row['category'], color = row['color']).save()

            print "importing blog_topics"
            cursor.execute("SELECT * FROM blog_topics")
            rows = cursor.fetchall()
            for row in rows:
                Topic(id = row['topic_id'], topic_type = topic_type[row['type']], topic = row['topic'], inserted = row['inserted'],
                    category_id = row['category_id'], user_id = 0, ip = row['ip'], user_agent = row['user_agent'], enabled = row['enabled']).save()

            print "importing blog_comments"
            cursor.execute("SELECT * FROM blog_comments")
            rows = cursor.fetchall()
            for row in rows:
                Comment(id = row['comment_id'], topic_id = row['topic_id'], comment = row['comment'], inserted = row['inserted'], user_id = 0,
                ip = row['ip'], user_agent = row['user_agent'], enabled = row['enabled']).save()

            print "importing blog_essay_photo"
            cursor.execute("SELECT * FROM blog_essay_photos")
            rows = cursor.fetchall()
            for row in rows:
                Photo(id = row['photo_id'], topic_id = row['topic_id']).save()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
