from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.template import loader,RequestContext
from django.views.decorators.csrf import csrf_exempt
from random import randint
# Create your views here.
from models import VideoSnippetForm,WebMVideo
import json


def _stream_image(vid):
    data_count=0;
    while True:
        try:
            #data= q.get(block=True,timeout=10)
            vid_file =open('image_%s'%vid.id)
            
            data = vid_file.read()
            #print "got data %s"%data_count
            data_count+=1
            if data_count > 1:
                break
            #print "Got data len is %s"%(len(data))
            #yield data
            yield data.decode('base64')
        except Exception as e:
            print "Exception Occurred  "
            break
    print "End image queue data"
    
def _stream_data(vid):
    data_count=0;
    while True:
        try:
            #data= q.get(block=True,timeout=10)
            vid_file =open('video_%s'%vid.id)
            
            data = vid_file.read()
            print "got data %s"%data_count
            data_count+=1
            if data_count > 10:
                break
            #print "Got data %s len is %s"%(data,len(data))
            yield data
            #yield data.decode('base64')
        except Exception as e:
            print "Exception Occurred  "
            break
    print "End queue data"

def home_mobile(request):
    print "Hey htert"
    #template = loader.get_template('MediaSource/camera_capture.html')
    return render(request, 'MediaSource/camera_capture_mobile.html',{})

def home(request):
    print "Hey htert"
    #template = loader.get_template('MediaSource/camera_capture.html')
    return render(request, 'MediaSource/camera_capture.html',{})

@csrf_exempt
def get_random_videos(request,amount):
    print "show amount %s"%amount
    #print "Stream video by sorted list at index %s"%video_index
    videos = WebMVideo.objects.all()
    vid_ids=[]
    
    if len(videos) < int(amount):
        amount = len(videos)
    print "Now show %s"%amount
    for i in range(int(amount)-1):
        random_idx = randint(0,len(videos)-1)
        print "video len %s abd random idx %s"%(len(videos),random_idx)
        ids=videos[random_idx].id
        vid_ids.append(ids)
        
    
    return render(request,'MediaSource/json_video_list.json',{'data':vid_ids})
    
    


@csrf_exempt
def video_stream_count(request,video_index):
    #print "Stream video by sorted list at index %s"%video_index
    videos = WebMVideo.objects.all().order_by('vote_count').reverse()
    #print "Got sorted videos %s"%len(videos)
    if len(videos) > 0:
        #print "Length greater 0"
        if len(videos) < (int(video_index)-1):
            #print "index too high"
            video=videos[len(videos)-1]
            
            return HttpResponse(json.dumps({"error":False,"id":"%s"%video.id}))
        else:
            #print "index should exist"
            video=videos[int(video_index)-1];
            return HttpResponse(json.dumps({"error":False,"id":"%s"%video.id}))
            
    return HttpResponse(json.dumps({"error":True,"message":"no videos avail"}))

def get_image(request,video_id):
    print "Get Image ID"
    video = WebMVideo.objects.filter(pk=video_id)
    print "Got Image %s"%video
    if len(video) > 0:
        response = StreamingHttpResponse(_stream_image(video[0]),content_type='image/png')
        return response
        #print "Video Id is %s"%video[0].id
        #print "video Length is %s"%video[0].size
        #print "return image file image_%s"%video_id
        #try:
        #    with open("image_%s"%video_id, "rb") as f:
        #        print "Opened file , now write out image_%s"%video_id
        #        return HttpResponse(f.read(), content_type="image/png")
        #except IOError:
            #red = Image.new('RGBA', (1, 1), (255,0,0,0))
            #response = HttpResponse(mimetype="image/jpeg")
            #red.save(response, "JPEG")
            #return response
        #    print "Error Getting Image"
        #    return HttpResponse("Error");
    
def video_stream(request,video_id):
    print "Stream Video %s"%video_id
    video = WebMVideo.objects.filter(pk=video_id)
    print "Got video %s"%video
    if len(video) > 0:
        print "Video Id is %s"%video[0].id
        print "video Length is %s"%video[0].size
    #response = StreamingHttpResponse(v.stream_video(q,stream_id),content_type='video/webm;codecs="vp8,vorbis"')
        response = StreamingHttpResponse(_stream_data(video[0]),content_type='video/webm;codecs="vp8,vorbis"')
        return response
    else:
        return HttpResponse("Error Stream %s"%video_id)

def video_submit_vote(request,video_id,video_submit_vote):
    print "Got Vote %s"%video_submit_vote
    video = WebMVideo.objects.filter(id=video_id)
    if len(video) > 0:
        v_cnt=video[0].vote_count;
        if video_submit_vote == '1':
            v_cnt+=1
        else:
            v_cnt-=1
        video[0].vote_count=v_cnt
        video[0].save()
    return HttpResponse("got vote")
    
def video_vote(request):
    print "video vote page"
    data = {}
    webm = WebMVideo.objects.all()
    print "videos %s"%webm
    return render(request,'MediaSource/video_vote.html',{'data':webm})

def _handle_uploaded_file(f,name):
    #print "Try to open "
    with open('%s'%name, 'wb+') as destination:
        #print "for chuck in f "
        for chunk in f.chunks():
            #print "Writing chunk %s"%chunk
            destination.write(chunk)
            
@csrf_exempt
def video_snippet(request):
    if request.method == 'POST':
        print "Method is posting info"
        form = VideoSnippetForm(request.POST,request.FILES)
        #data = Document(docfile=request.FILES['docfile'])
        if form.is_valid():
            print "Form is Valid %s"%request.POST['metadata']
            print "Form message is %s"%request.POST['message']
            print "Files are %s"%request.FILES
            print "File is at data_blob %s"%request.FILES['data_blob']
            print "File size is %s"%len(request.FILES['data_blob'])
            print "File image size is %s"%len(request.FILES['image_blob'])
            newdoc = WebMVideo()
            
            newdoc.set_data(request.FILES['data_blob'],request.FILES['image_blob'],request.POST['metadata'],request.POST['action'],request.POST['message'])
            newdoc.save()
            print "Create File Name with %s"%newdoc.id
            _handle_uploaded_file(request.FILES['data_blob'],'video_%s'%newdoc.id)
            _handle_uploaded_file(request.FILES['image_blob'],'image_%s'%newdoc.id)
            
        else:
            print "Form is not Valid"
    else:
        print "method is get ... no good"
   
    return HttpResponse("Thanks for you video")