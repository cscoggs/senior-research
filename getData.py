# It works
from sys import argv
import praw
import os.path, os
import time
import NBC

def getUser(test):
	user_agent = ("Script to get users' comments")
	errs = open("errors.log", "w")

	r = praw.Reddit(user_agent=user_agent)

	file_name = test #"bluedot951"

	currPath = os.getcwd()

	if(os.path.isfile(file_name)):
		users = open(file_name, "r").read().split("\n")
		users = users[0:len(users)-1]

	else:
		users = [file_name]

	print users

	#users = ["Hardekyn", "Fogram"]

	for user_name in users:
		print "Processing " + user_name
		numErrs = 0

		while True:
			if numErrs > 2:
				break
			try:

				user = r.get_redditor(user_name)

				comms = user.get_comments(limit=None)

				commcount = 0
				postcount = 0

				w = open(currPath+"/"+file_name+"/"+user_name + ".log", "w")
				writeclique = open(currPath+"/"+file_name+"/"+user_name + ".clique", "a")

				clique = []

				while(1):

					try:
						comm = comms.next()
						sentiment, neg, pos = NBC.classify(comm.body)

						mystr = str(int(comm.created_utc)*1000) + "|"
						title = comm.submission.title
						mystr += (title.replace('\n', '') if '\n' in title else title) + "|"
						mystr += comm.subreddit.display_name + "|"
						mystr += sentiment + "|"
						mystr += str(neg) + "|"
						mystr += str(pos) + "|"
						mystr += "comment"

						print(mystr)


						try:
							poster = comm.submission.author

							# print str(poster) 


							if(poster != None):
								# print poster.name
								postername = poster.name
								# print(postername)
								# writeclique.write(postername + "\n")
								if postername not in clique:
									clique.append(postername)

						except AttributeError:
							pass

						try:
							w.write(mystr + "\n")
						except UnicodeEncodeError:
							pass
						commcount+=1
					except StopIteration:
						break

				subs = user.get_submitted(limit=None)

				while(1):
					try:
						sub = subs.next()
						sentiment, neg, pos = NBC.classify(sub.selftext)

						mystr = str(int(sub.created_utc)*1000) + "|"
						mystr += sub.title + "|"
						mystr += sub.subreddit.display_name + "|"
						mystr += sentiment + "|"
						mystr += str(neg) + "|"
						mystr += str(pos) + "|"
						mystr += "post"

						print(mystr)
						try:
							w.write(mystr + "\n")
						except UnicodeEncodeError:
							pass
						postcount+=1

					except StopIteration:
						break

				print "Comments: " + str(commcount)
				print "Posts: " + str(postcount)
				print "Total: " + str(commcount+postcount)

				for ele in clique:
					if(ele != user_name):
						print ele
						writeclique.write(ele + "\n")

				w.close()
				writeclique.close()

			except Exception, e:
				print e
				print "An error occured. Retrying..."
				errs.write(user_name + "\n")
				# time.sleep(30)
				numErrs += 1
				continue
			break
