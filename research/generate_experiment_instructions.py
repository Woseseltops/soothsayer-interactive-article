from copy import copy
from random import shuffle

def get_users_from_list(full_list,nr,exclude=None):
	l = copy(full_list)
	shuffle(l)

	if exclude != None:
		l.remove(exclude)

	return l[:nr]

USER_LIST_DIR = 'user_lists/'
CONNECTED_USERS_DIR = 'references/'

feed_users = [user.strip() for user in open(USER_LIST_DIR+'feed_users.txt')]

#Only train on 1 other user
for feed_user in feed_users:
	for train_user in feed_users:
			print(feed_user,train_user)

#Train on 5 other users
for feed_user in feed_users:
	print(feed_user+' '+','.join(get_users_from_list(feed_users,5,feed_user)))

#Train on 5 users, including yourself
for feed_user in feed_users:
	train_users = get_users_from_list(feed_users,4,feed_user)+[feed_user]
	print(feed_user+' '+','.join(train_users))

#Train on 4 users connected to you and yourself
for feed_user in feed_users:
	train_users = [user.strip() for user in open(CONNECTED_USERS_DIR+feed_user+'.txt')][:4]+[feed_user]

	if len(train_users) > 1:
		print(feed_user+' '+','.join(train_users))