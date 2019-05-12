from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
import csv
import operator
import os
# Create your views here.

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

		# with open('primary_index.csv','a',newline="") as myfile:
		# 	wr=csv.writer(myfile,dialect="excel")

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

