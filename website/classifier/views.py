from django.shortcuts import render

def classify(request):
	context = {'a': 1}
	return render(request, 'classifier/classifier.html', context)

def predict_image(request):
	print(request)
	print(request.GET.dict())
	print (request.POST.dict())
	fileObj=request.FILES['filePath']
	fs=FileSystemStorage()
	filePathName=fs.save(fileObj.name,fileObj)
	filePathName=fs.url(filePathName)
	testimage='.'+filePathName
	return render(request, 'classifier/classifier.html', context) 
