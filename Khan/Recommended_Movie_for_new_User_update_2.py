import numpy as np
import random
import pandas as pd 
import sys
import operator

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
		mty=[]
		type_m={}
		for tt in f2.movieId:
			mid.append(tt)
		for tt in f2.title:
			ttl.append(tt)
		for tt in f2.genres:
				mty.append(tt)
		for kk in range(0,len(ttl)):
			mname[mid[kk]]=ttl[kk]
		for kk in range(0,len(mty)):
			type_m[mid[kk]]=mty[kk]
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
		return dmv,mid,uniq_user,mname,mvtzm,mrt,duser,type_m
def new_user_input(m3):
	dm2,m2,u,mn,tzone,mrt,duser,type_m=reading_file()
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
	
	while c1<25:
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
	return num,tzone,mn,mrt,duser,type_m


#print(" Enter S to Take the input from new user "+" Enter Z to stope"+"\n")
def storing_newuser_input():
	new_mv_rt={}
	new_user={}
	#global id1
	for k5 in range(611,711):
		print("Enter S for new user input. After Entering S at least once Enter Z to show the Recommended movies for the new user"+"\n")
		j=str(input())
		if j=='S':	
				new_u_p,tzone,mn,mrt,duser,type_m=new_user_input(k5)
				up_n_user_pr={}
				mtr={}
				for i in new_u_p:
					for j in new_u_p[i]:
						hj=str(tzone[j])
						#for t in j.values():
						print(i,mn[j],new_u_p[i][j],type_m[j],hj)
						new_mv_rt[j]=new_u_p[i][j]
					new_user[i]=new_mv_rt
					#with open('ratings.csv','a') as f:
						##f.write(str(i)+","+str(j)+","+str(new_u_p[i][j])+","+str(hj)+"\n") 
		elif j=='Z':
			return new_user,duser,mrt,mn,type_m
			#sys.exit()
			
def find_similar_user_recommend_movie():
	n,o,mrt,mn,type_m=storing_newuser_input()
	movid=[]                     
	mv_rt=[]
	nuser_mt=[]
	for i in n:
		for j in n[i]:
			for k in type_m:
				if j==k:
					if float(mrt[j])>=3.0:
						nuser_mt.append(type_m[k])
	for i in mrt:
		movid.append(i)
		mv_rt.append(float(mrt[i]))
	n23=len(movid)
	v=[0]*n23
	smu=[]
	su_t={}

	for i in n:
		for j in n[i]:
			for t in range(0,len(movid)):
				if movid[t]==j:
					v[t]=float(mv_rt[t])
	u_s_id=[]
	for i in o:
		v1=[0]*n23
		for j in o[i]:
			for t in range(0,len(movid)):
				if movid[t]==j:
					v1[t]=float(mv_rt[t])
		u_1=np.ma.masked_equal(v,0)#np.array(v)
		u_2=np.ma.masked_equal(v1,0)#np.array(v1)
		dot_product = np.dot(u_1, u_2)
		norm_user1 = np.linalg.norm(u_1)
		norm_user2= np.linalg.norm(u_2)
		simi=dot_product / (norm_user1 * norm_user2)
		#print(simi)
		if float(simi)>=0.1:
			#print(simi)
			u_s_id.append(i)
			#su_t[j]=float(o[i][j])
			#smu.append(j)
	for y in u_s_id:
		for ty in o:
			if y==ty:
				for j in o[ty]:
					if float(o[ty][j])>=3.0:
						smu.append(j)

	#print(su_t)
	#dd=sorted(su_t.items(),key=operator.itemgetter(1),reverse=True)
	#for t in dd:
		#smu.append(t[0])
	#print(mn)
	print("Recommended movies for the new user:"+"\n")
	g=0
	for i in smu:
		if type_m[i] in nuser_mt:
			for k in mn:
				#print(i,k)
				if str(i)==str(k):
					if g<5:
						print(str(mn[k])+":"+str(mrt[i])+":"+str(type_m[i])+"\n")
						g=g+1
						

		



find_similar_user_recommend_movie()