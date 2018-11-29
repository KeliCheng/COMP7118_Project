import numpy as np
import random
import pandas as pd 
import sys

id1=611
def reading_file():
		f1=pd.read_csv("ratings_recommend.csv")
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
		duser={}
		for tt in f2.movieId:
			mid.append(tt)
		for tt in f2.title:
			ttl.append(tt)
		for kk in range(0,len(ttl)):
			mname[mid[kk]]=ttl[kk]
		for tt in f1.movieId:
			movieid.append(tt)
		for tt in f1.userId:
			user.append(tt)
		for tt in f1.rating:
			rating.append(tt)
		for tt in f1.timestamp:
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
					str1.append(int(tzone[e]))
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
		uniq_user.sort()
		for i in uniq_user:
			du={}
			for t  in range(0,len(user)):
				if i==user[t]:
					du[movieid[t]]=rating[t]
			duser[i]=du
		return dmv,mid,uniq_user,mname,mvtzm,mrt,duser
def new_user_input(m3):
	dm2,m2,u,mn,tzone,mrt,duser=reading_file()
	#global id1
	random.shuffle(m2)
	uid1=m3
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
				print("Enter the rating of the movie within the range from 1 to 5:"+"\n")
				i=float(input())
				mnr[tt]=str(i)
				for rt in mrt:
					if int(rt)!=mvid:
							if float(mrt[rt])==i:
								mvid1=int(rt)
								mvid=mvid1#random.randint(mvid1,9741)
								c1=c1+1
								break		
	num[uid1]=mnr
	#id1=id1+1
	return num,tzone,mn,mrt,duser


#print(" Enter S to Take the input from new user "+" Enter Z to stope"+"\n")
def storing_newuser_input():
	new_mv_rt={}
	new_user={}
	#global id1
	for k5 in range(611,621):
		print("Enter S for new user input. After Entering S at least once Enter Z to show the Recommended movies for the new user"+"\n")
		j=str(input())
		if j=='S':	
				new_u_p,tzone,mn,mrt,duser=new_user_input(k5)
				up_n_user_pr={}
				mtr={}
				for i in new_u_p:
					for j in new_u_p[i]:
						hj=str(tzone[j])
						#for t in j.values():
						print(i,mn[j],new_u_p[i][j],hj)
						new_mv_rt[j]=new_u_p[i][j]
					new_user[i]=new_mv_rt
					#with open('ratings.csv','a') as f:
						##f.write(str(i)+","+str(j)+","+str(new_u_p[i][j])+","+str(hj)+"\n") 
		elif j=='Z':
			return new_user,duser,mrt,mn
			#sys.exit()
			
def find_similar_user_recommend_movie():
	n,o,mrt,mn=storing_newuser_input()
	print(n)
	new_user_id=611
	#print(o)
	#sys.exit()
	nm=[]
	om=[]
	mm=[]
	c=0
	oum={}
	omm={}
	nuser={}
	nn={}
	recoomen_mv1=[]
	recoomen_mv2=[]
	for i in n:
		for j in n[i]:
			if float(n[i][j])>=4.0:
				nn[j]=float(n[i][j])
		nuser[i]=nn
			#if j  not in nm:
				#nm.append(j)
	for j in o:
		for kk in o[j]:
			if float(o[j][kk])>=3.0:
				omm[kk]=float(o[j][kk])
		oum[j]=omm
			#if kk not in om:
				#om.append(kk)
	oldu={}
	nem={}
	smu=[]
	smm={}
	smid=[]
	for tt in oum:
		for hj in oum[tt]:
			if hj not in om:
				om.append(hj)
		oldu[tt]=om
	for tt in nuser:
		for hj in nuser[tt]:
			if hj not in nm:
				nm.append(hj)
		nem[tt]=nm
	for e in oldu:
		for tt in oldu[e]:
			for w in nem:
				if  tt in nem[w]:
					c+=1
			if c>=abs(len(nem[w])*0.75):
				smu.append(e)

	for ii in smu:
		for rt in oldu:
			if ii==rt:
				smm[ii]=oldu[rt]
	for hh in smm:
		for tt in smm[hh]:
			for y in nem:
				if tt not in nem[y]:
					smid.append(tt)

	
	random.shuffle(smid)
	print("Recommended movies for the new user:"+str(new_user_id)+"\n")
	#new_user_id+=1
	for t in range(0,5):#Recomending first 5 movies
		for tt in mn:
			if tt==smid[t]:
				print(mn[tt])
				#print("\n")
	




find_similar_user_recommend_movie()