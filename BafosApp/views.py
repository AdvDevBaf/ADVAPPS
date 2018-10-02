from django.shortcuts import render
from .models import BlogPost,Category
from django.shortcuts import get_object_or_404, render_to_response
# Create your views here.

def index(request):
    entries = BlogPost.objects.published()
    return render_to_response('BafosApp/index.html', {'entries': entries})

def category(request, id, slug):
    category = get_object_or_404(Category, id=id, slug=slug)
    entries = category.entries.published()
    return render_to_response('BafosApp/index.html', {'entries': entries})


def archive_year(request, year):
    entries = BlogPost.objects.filter(draft=False,
                                      published_date__year=year)
    return render_to_response('BafosApp/index.html', {'entries': entries})


def archive_month(request, year, month):
    entries = BlogPost.objects.filter(draft=False,
                                      published_date__year=year,
                                      published_date__month=month)
    return render_to_response('BafosApp/index.html', {'entries': entries})


def archive_day(request, year, month, day):
    entries = BlogPost.objects.filter(draft=False,
                                      published_date__year=year,
                                      published_date__month=month,
                                      published_date__day=day)
    return render_to_response('BafosApp/index.html', {'entries': entries})


def details(request):
    entry = get_object_or_404(BlogPost)

    return render_to_response('BafosApp/details.html', {'entry': entry})


def youtube(request):
    #entry = get_object_or_404(BlogPost)
    import requests
    import pandas as pd
    from tkinter.filedialog import askdirectory

    if 'text' in request.GET and request.GET['text']:
        text = request.GET.get('text', '')
        data = request.GET.get('data', '')

        request_text = text
        video_name = []
        url_video = []
        description = []
        view_count = []
        vids = []
        if data == "video":
            response = requests.get('https://www.googleapis.com/youtube/v3/search?type=video'
                                '&key=AIzaSyACxrnyfBEZgUBNCwzCp7urOlORSzlZsHU&maxResults=50&'
                                'part=snippet&q=' + str(request_text))
            search_results = response.json()

            try:
                for i in range(len(search_results['items'])):
                    print(search_results['items'][i]['snippet']['title'])
                    print(search_results['items'][i]['id']['videoId'])
                    print(search_results['items'][i]['snippet']['description'])
                    video_name.append(search_results['items'][i]['snippet']['title'])
                    url_video.append('https://www.youtube.com/watch?v=' + search_results['items'][i]['id']['videoId'])
                    description.append(search_results['items'][i]['snippet']['description'])
                    vids.append(search_results['items'][i]['id']['videoId'])
                    print('ne token')
                    if 'nextPageToken' in search_results:
                        try:
                            for i in range((int(search_results['pageInfo']['totalResults']) // 50) + 1):
                                print('s is ' + str(search_results['pageInfo']['totalResults']))
                                if 'nextPageToken' in search_results:
                                    print(i)
                                    print('token?')
                                    response = requests.get('https://www.googleapis.com/youtube/v3/search?type=video'
                                                        '&key=AIzaSyACxrnyfBEZgUBNCwzCp7urOlORSzlZsHU&maxResults=50&'
                                                        '&part=snippet&pageToken=' + str(
                                        search_results['nextPageToken'])
                                                        + '&q=' + str(request_text))
                                    search_results = response.json()
                                    print(search_results)
                                    for j in range(len(search_results['items'])):
                                        print('token')
                                        print(search_results['items'][j]['snippet']['title'])
                                        print(search_results['items'][j]['id']['videoId'])
                                        print(search_results['items'][j]['snippet']['description'])
                                        video_name.append(search_results['items'][j]['snippet']['title'])
                                        url_video.append(
                                        'https://www.youtube.com/watch?v=' + search_results['items'][j]['id'][
                                            'videoId'])
                                        description.append(search_results['items'][j]['snippet']['description'])
                                        vids.append(search_results['items'][j]['id']['videoId'])
                        except:
                            print(i)
                            print('Something goes wrong. oops...')
            except:
                print('Видео не существует, или проблемы с сетью')
        else:
            print('')

        if text != "":
            for vid in vids:
                try:
                    video_response = requests.get('https://www.googleapis.com/youtube/v3/videos?part=statistics'
                                          '&key=AIzaSyACxrnyfBEZgUBNCwzCp7urOlORSzlZsHU&id=' + str(vid))
                    video_search_results = video_response.json()
                    print(video_search_results)
                    print(video_search_results['items'][0]['statistics']['viewCount'])
                    view_count.append(video_search_results['items'][0]['statistics']['viewCount'])
                except:
                    view_count.append('N/A')

            table = pd.DataFrame({'Название видеоролика': video_name, 'Описание': description,
                                  'Количество просмотров': view_count, 'Url видеоролика': url_video})
            path_to = askdirectory()

            if text!="":
                table.to_csv(str(path_to) + '/' + str("Поиск") + '.csv', sep=';', index=False,
                             encoding='utf-8-sig')
            else:
                table.to_csv(str(path_to) + '/' + 'Поиск' + '.csv', sep=';', index=False,
                             encoding='utf-8-sig')
            import ctypes
            message = 'Готово!'
            ctypes.windll.user32.MessageBoxW(0, message, 'Результаты поиска', 0)
            print('ok')

    text='tratata'
    data='kek'
    context = {
        'text': "CCHORT",
        'data': "DIRT",
    }

    if text and data:
        print('Text: {}\nData: {}'.format("CCHORT", "DIRT"))

    return render_to_response('BafosApp/youtube.html')

def youtube_data_view(request):
    import requests
    text = request.GET.get('text','')
    data = request.GET.get('data','')

    request_text = text
    video_name = []
    url_video = []
    description = []
    view_count = []
    vids = []
    if 2 == 2:
        response = requests.get('https://www.googleapis.com/youtube/v3/search?type=video'
                                '&key=AIzaSyACxrnyfBEZgUBNCwzCp7urOlORSzlZsHU&maxResults=50&'
                                'part=snippet&q=' + str(request_text))
        search_results = response.json()

        try:
            for i in range(len(search_results['items'])):
                print(search_results['items'][i]['snippet']['title'])
                print(search_results['items'][i]['id']['videoId'])
                print(search_results['items'][i]['snippet']['description'])
                video_name.append(search_results['items'][i]['snippet']['title'])
                url_video.append('https://www.youtube.com/watch?v=' + search_results['items'][i]['id']['videoId'])
                description.append(search_results['items'][i]['snippet']['description'])
                vids.append(search_results['items'][i]['id']['videoId'])
                print('ne token')
                if 'nextPageToken' in search_results:
                    try:
                        for i in range((int(search_results['pageInfo']['totalResults']) // 50) + 1):
                            print('s is ' + str(search_results['pageInfo']['totalResults']))
                            if 'nextPageToken' in search_results:
                                print(i)
                                print('token?')
                                response = requests.get('https://www.googleapis.com/youtube/v3/search?type=video'
                                                        '&key=AIzaSyACxrnyfBEZgUBNCwzCp7urOlORSzlZsHU&maxResults=50&'
                                                        '&part=snippet&pageToken=' + str(
                                    search_results['nextPageToken'])
                                                        + '&q=' + str(request_text))
                                search_results = response.json()
                                print(search_results)
                                for j in range(len(search_results['items'])):
                                    print('token')
                                    print(search_results['items'][j]['snippet']['title'])
                                    print(search_results['items'][j]['id']['videoId'])
                                    print(search_results['items'][j]['snippet']['description'])
                                    video_name.append(search_results['items'][j]['snippet']['title'])
                                    url_video.append(
                                        'https://www.youtube.com/watch?v=' + search_results['items'][j]['id'][
                                            'videoId'])
                                    description.append(search_results['items'][j]['snippet']['description'])
                                    vids.append(search_results['items'][j]['id']['videoId'])
                    except:
                        print(i)
                        print('Something goes wrong. oops...')
        except:
            print('Видео не существует, или проблемы с сетью')
    else:
        print('')

    for vid in vids:
        try:
            video_response = requests.get('https://www.googleapis.com/youtube/v3/videos?part=statistics'
                                          '&key=AIzaSyACxrnyfBEZgUBNCwzCp7urOlORSzlZsHU&id=' + str(vid))
            video_search_results = video_response.json()
            print(video_search_results)
            print(video_search_results['items'][0]['statistics']['viewCount'])
            view_count.append(video_search_results['items'][0]['statistics']['viewCount'])
        except:
            view_count.append('N/A')

    context = {
        'text': "CCHORT",
        'data': "DIRT",
    }

    if text and data:

        print('Text: {}\nData: {}'.format("CCHORT","DIRT"))

    return render_to_response(request,'BafosApp/youtube.html',context)