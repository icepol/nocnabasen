CREATE INDEX 'topic_comment' ON comment(`topic_id`,`comment_id`);
CREATE INDEX 'user' ON comment(`user_id`);