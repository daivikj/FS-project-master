from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import csv
import operator
import os

def add(request):
	if request.method=="POST":
		post_title=request.POST.get('title')
		post_author=request.POST.get('author')
		post_category=request.POST.get('category')
		blog_post=request.POST.get('blog')

		blog_path=os.path.join('files','{}.txt'.format(post_title))

		with open(blog_path,'w+') as f:

			f.write(blog_post)
			f.close()

		primary_path=os.path.join('primary files','primary_index.csv')	

		with open(primary_path,'a',newline="") as myfile:
			wr=csv.writer(myfile,dialect="excel")
			wr.writerow([post_title,blog_path])

		with open(primary_path,'r') as myfile:
			rd=csv.reader(myfile,delimiter=',')
			sort=sorted(rd,key=operator.itemgetter(0))

			with open(primary_path,'w',newline="") as file:
				wr=csv.writer(file,dialect='excel')

				for eachline in sort:
					wr.writerow(eachline)

		secondary_path = os.path.join('secondary files','secondary_index.csv')

		with open(secondary_path, 'a', newline="") as myfile:
			wr = csv.writer(myfile, dialect='excel')
			wr.writerow([post_author, blog_path])

		with open(secondary_path ,'r') as myfile:
			rd = csv.reader(myfile,dialect="excel")
			sort = sorted(rd, key=operator.itemgetter(0))

			with open(secondary_path, 'w', newline="") as file:
				wr = csv.writer(file,dialect="excel")

				for eachline in sort:
					wr.writerow(eachline)

	return render(request,'add.html')	

def search(request):

	if request.method=="POST":
		post_title=request.POST.get('title')
		
		primary_path=os.path.join('primary files','primary_index.csv')

		with open(primary_path,'r') as myfile:
			rd=csv.reader(myfile,delimiter=",")
			
			title_list=[]
			path_list=[]
			for eachline in rd:
				title_list.append(eachline[0])
				path_list.append(eachline[1])

			lines = len(title_list)
			text_path = ''
			last = lines-1
			first = 0

			while text_path == '':
				mid = (first + last)//2

				if title_list[mid] == post_title:
					text_path = path_list[mid]

				elif post_title < title_list[mid]:
					last = mid-1

				else:
					first = mid+1					

		with open(text_path,'r+') as readfile:
			data=readfile.read()
			print(data)
			print(type(data))
			data=data.split()
			blogs=''
			for i in data:
				blogs=blogs+' '+i
				print(blogs)	

		titles=post_title		
		return render(request,'display_post.html',{"blogs":blogs,"titles":titles})
	return render(request,'search.html')

def delete(request):

	if request.method=="POST":
		post_title=request.POST.get('title')
		post_author=request.POST.get('author')
		
		primary_path=os.path.join('primary files','primary_index.csv')
		secondary_path=os.path.join('secondary files','secondary_index.csv')
		new_primary_path = os.path.join('primary files','new_primary_file.csv')
		new_secondary_path = os.path.join('secondary files','new_secondary_file.csv')

		with open(primary_path,'r') as myfile, open (new_primary_path,'w', newline='') as out:
			rd=csv.reader(myfile,delimiter=",")
			writer = csv.writer(out,dialect="excel")
			for row in rd:
				if row[0] != post_title:
					writer.writerow(row)

				else:
					file_path = row[1]

		with open(new_primary_path,'r') as myfile, open (primary_path,'w', newline='') as out:
			rd=csv.reader(myfile,delimiter=",")
			writer = csv.writer(out,dialect="excel")
			for row in rd:
				if row != '/n':
					writer.writerow(row)

		with open(secondary_path,'r') as myfile, open (new_secondary_path,'w', newline='') as out:
			rd=csv.reader(myfile,delimiter=",")
			writer = csv.writer(out,dialect="excel")
			for row in rd:
				if row[1] != file_path:
					writer.writerow(row)

		with open(new_secondary_path,'r') as myfile, open (secondary_path,'w', newline='') as out:
			rd=csv.reader(myfile,delimiter=",")
			writer = csv.writer(out,dialect="excel")
			for row in rd:
				if row != '/n':
					writer.writerow(row)

		os.remove(file_path)

		os.remove(primary_path)	
		primary_path=os.path.join('primary files','primary_index.csv')
		os.rename(new_primary_path, primary_path)

		os.remove(secondary_path)
		secondary_path = os.path.join('secondary files','secondary_index.csv')
		os.rename(new_secondary_path, secondary_path)		

	return render(request,'delete.html')

def signup(request):

	if request.method=="POST":
		email=request.POST.get('email')
		password1=request.POST.get('password1')
		password2=request.POST.get('password2')
		
		try:
			user=User.objects.get(username=email)
			return render(request,"signup.html",{"error":"user with this email already exists"})
		except:
			if password1==password2:
				user=User.objects.create_user(username=email,email=email,password=password1,is_staff=True)

				login(request,user)

				return redirect("/login/")

			else:
				return render(request,"signup.html",{"error":" the passwords do not match "})	

	return render(request,"signup.html")			

def signin(request):
	
	if request.method=="POST":
		email=request.POST.get('email')
		print(email)
		password=request.POST.get('password')
		print(password)
		user=authenticate(request,username=email,password=password) 
		print(user)
		if user is not None:
			login(request,user)

			return redirect("/home/")	
		else:
			print("User is None")
	return render(request,"login.html")

def signout(request):
	logout(request)
	return redirect('/signin/')