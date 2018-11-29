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
		midm={}
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
		mty1=[]
		ss=set(mty)
		for t in ss:
			mty1.append(t)
		for kk in range(0,len(ttl)):
			mname[mid[kk]]=ttl[kk]
		for kk in range(0,len(ttl)):
			midm[ttl[kk]]=mid[kk]
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
		return dmv,mid,uniq_user,mname,mvtzm,mrt,duser,type_m,mty1,midm
def new_user_input(m3):
	dm2,m2,u,mn,tzone,mrt,duser,type_m,mty1,midm=reading_file()
	ty_m_v={}
	
	for i in mty1:
		mb=[]
		for j1 in type_m:
				if str(i)==str(type_m[j1]):
					if mn[j1] not in mb:
							#print(mn[j1])
							mb.append(mn[j1])
		ty_m_v[i]=mb
	
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
	#print("Enter the choice for the following types of movie that you will rate to get Recommended movies for you:"+"\n")
	cc=0
	n_m={}
	for tt in mty1:
		if cc<len(mty1):
			cc=cc+1
			print(str(cc)+" "+str(tt)+"\n")
			n_m[cc]=tt
	print("Your Choice:")
	hh=int(input())
	mv_tc=[]
	for i in n_m:
		if int(i)==int(hh):
			#print(i,hh)
			for tz in ty_m_v:
				if tz==n_m[i]:
					#print(tz,n_m[i])
					#sys.exit()
					for t12 in ty_m_v[tz]:
						mv_tc.append(t12)
	#print(len(mv_tc),mv_tc)
	#sys.exit()
	for c1 in range(0,len(mv_tc)):
			L=[]
			#p=0
			#j=0
			#global cm
			#L.append(mvid)
			#random.shuffle(m2)
			#mv1=m2[mvid]
			#if mv1 not in L:
				#L.append(int(mv1))
			#for tt in L:
				#tz=tzone[tt]
			#for tt in L:
				#for tt1 in mv_tc:
					#if str(mn[tt])==str(tt1):
			print(str(mv_tc[c1])+"\n")
			print("Enter the rating of the movie within the range from 1 to 5:"+"\n")
			i=float(input())
			#
			#for rt in midm:
						#if int(rt)!=mvid:
						#if rt==mv_tc[c1]:
			mnr[midm[mv_tc[c1]]]=str(i)
							#print("hgfhfyfftff")
							#if mn[rt]==mv_tc[c1]:
										#print(mn[rt],mv_tc[c1])
										
										
										#mvid=mvid1#random.randint(mvid1,9741)
										#c1=c1+1
										#break		
	num[uid1]=mnr
	#id1=id1+1
	return num,tzone,mn,mrt,duser,type_m


#print(" Enter S to Take the input from new user "+" Enter Z to stope"+"\n")
def storing_newuser_input():
	new_mv_rt={}
	new_user={}
	#global id1
	for k5 in range(611,711):
		print("Enter S for new user input. After Entering S at least once Enter Z to show the Recommended movies for the new user.After Pressing S you will ge the choice options for the movies.Enter the choice for the following types of movie that you will rate to get Recommended movies for you:"+"\n")
		j=str(input())
		if j=='S':	
				new_u_p,tzone,mn,mrt,duser,type_m=new_user_input(k5)
				up_n_user_pr={}
				mtr={}
				for i in new_u_p:
					for j in new_u_p[i]:
						#hj=str(tzone[j])
						#for t in j.values():
						print(k5,mn[j],new_u_p[i][j],type_m[j])
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
		u_1=np.array(v)#np.ma.masked_equal(v,0)#np.array(v)
		u_2=np.array(v1)#np.ma.masked_equal(v1,0)#np.array(v1)
		dot_product = np.dot(u_1, u_2)
		norm_user1 = np.linalg.norm(u_1)
		norm_user2= np.linalg.norm(u_2)
		simi=dot_product/(norm_user1 * norm_user2)
		#print(simi)
		if float(simi)>=0:
			#print(simi)
			u_s_id.append(i)
			#su_t[j]=float(o[i][j])
			#smu.append(j)
	same_u={}
	for y in u_s_id:
		for ty in o:
			if y==ty:
				for j in o[ty]:
					if float(o[ty][j])>=3.0:
						smu.append(j)
		same_u[y]=smu

	#print(su_t)
	#dd=sorted(su_t.items(),key=operator.itemgetter(1),reverse=True)
	#for t in dd:
		#smu.append(t[0])
	#print(mn)
	print("Recommended movies for the new user:"+"\n")
	g=0
	flist=[]
	for e in same_u:
		for i in same_u[e]:
			if type_m[i] in nuser_mt:
				for k in mn:
				#print(i,k)
					if str(i)==str(k):
					#if g<10:
							#kk=str(mn[k])+":"+str(o[e][i])+":"+str(type_m[i])
							kk1=str(mn[k])+":"+str(type_m[i])
							if kk1 not in flist:
								flist.append(kk1)
						#g=g+1
	for rt in range(0,len(flist)):
		print(flist[rt])
						

		



find_similar_user_recommend_movie()