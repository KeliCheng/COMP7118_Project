import numpy as np
import random
import pandas as pd 
import sys

def reading_file():
		f1=pd.read_csv("ratings.csv")
		f2=pd.read_csv("movies.csv")#,encoding="utf8")
		user_id_moviemap={}
		movieid_ratmap={}
		user=[]
		movieid=[]
		mid=[]
		ttl=[]
		str2=[]
		mname={}
		rating=[]
		uniq_user=[]
		duser={}
		dmv={}
		tzone=[]
		mrt={}
		for tt in f2.movieId:
			if tt!='movieId':
				mid.append(tt)
		for tt in f2.title:
			if tt!='title':
				ttl.append(tt)
		for kk in range(0,len(ttl)):
			mname[mid[kk]]=ttl[kk]
		for tt in f1.movieId:
			if tt!='movieId':
				movieid.append(tt)
		for tt in f1.userId:
			if tt!='userId':
				user.append(tt)
		for tt in f1.rating:
			if tt!='rating':
				rating.append(tt)
		for tt in f1.timestamp:
			if tt!='timestamp':
				tzone.append(tt)
		
		ss2=set(movieid)
		mvid1=[]
		mvtzm={}
		str1=[]
		for t in ss2:
			mvid1.append(t)
		for tt in mvid1:
			for e in range(0,len(movieid)):
				if movieid[e]==tt:
					str1.append(tzone[e])
			for q in str1:
				mvtzm[tt]=q
		for tt in mvid1:
			for e in range(0,len(movieid)):
				if movieid[e]==tt:
					str2.append(float(rating[e]))
			for q in str2:
				mrt[tt]=q
		#print(mvtzm)
		s1=set(user)
		for t in s1:
			uniq_user.append(t)
		#uniq_user.sort()
		for tt1 in mid:
			dm={}
			for t in range(0,len(movieid)):
					if tt1==movieid[t]:
						dm[user[t]]=rating[t]
			dmv[tt1]=dm
		return dmv,mid,uniq_user,mname,mvtzm,mrt
def new_user_input(id1):
	dm2,m2,u,mn,tzone,mrt=reading_file()
	random.shuffle(m2)
	uid=id1
	num={}
	nur=[]
	mnr={}
	c1=0
	global cm
	#for i in range(0,mvid):
	cm=0
	#while c<7:
	mvid=random.randint(0,9741)
	
	while c1<7:
			L=[]
			#p=0
			#j=0
			#global cm
			#L.append(mvid)
			random.shuffle(m2)
			mv1=m2[mvid]
			if mv1 not in L:
				L.append(int(mv1))
			#for tt in L:
				#tz=tzone[tt]
			for tt in L:
				print(str(mn[tt])+"\n")
				print("Enter the rating of the movie in the range of 1 to 5:"+"\n")
				i=float(input())
				mnr[tt]=str(i)
				for rt in mrt:
					if int(rt)!=mvid:
							if float(mrt[rt])==i:#Here I am making the choice of next movie id which has same rating intially given by the new user for the first movie appears in console So the choice of the next movie based on previous rating given by the user
								mvid1=int(rt)
								mvid=mvid1#random.randint(mvid1,9741)
								c1=c1+1
								break		
	num[uid]=mnr

	return num,tzone


#print(" Enter S to Take the input from new user "+" Enter Z to stope"+"\n")
def store_new_user():
	for k in range(611,1600):
		print("Enter S for new user input or Enter T to stop"+"\n")
		j=str(input())
		if j=='S':
			new_u_p,tzone=new_user_input(k)
			up_n_user_pr={}
			mtr={}
			for i in new_u_p:
				for j in new_u_p[i]:
					hj=str(tzone[j])
					#for t in j.values():
					print(i,j,new_u_p[i][j],hj)
					df1=pd.read_csv("ratings.csv")	
					df2=pd.DataFrame({'userId':[i],'movieId':[j],'rating':[new_u_p[i][j]],'timestamp':[hj]})
					df4=df1.append(df2) #Appending new Data information Using Pandas
					
					#f_t=f.T
					#f_t['userId']=i
					#Saving updated information in a new file
					print(df4)
					with open('ratings.csv','a') as f:
							(df2).to_csv(f,index=False,header=False)

						#f.write(str(i)+","+str(j)+","+str(new_u_p[i][j])+","+str(hj)+"\n") 
		elif j=='T':
			sys.exit()
#df1=pd.read_csv("ratings.csv")		
store_new_user()