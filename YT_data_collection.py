import requests
import pandas as pd

#Create API call to get list of random video ids
# Since i want 2000 vids loop code 40 times since api max results is 50
df = pd.DataFrame(columns=['video_id','title','desc','cat_id','vid_duration','dimension','definition','likes','comments','veiws'])
for n in range(40):
    API_key = "AIzaSyB-ytg0iOp83p4bxEK2l8SrYeigAMOhQRk"
    page_token = ""
    url = "https://www.googleapis.com/youtube/v3/search?key="+API_key+"&part=snippet,id&type=video&maxResults=50"+page_token
    response = requests.get(url).json()
    
    #Create for loop to colect Video Ids
    video_id_lst = []
    for vid in response['items']:
        video_id = vid['id']['videoId']
        video_id_lst.append(video_id)
    
    #Create second API call to git more data on specific vids and create our dataframe
    for vid in video_id_lst:
        url = "https://www.googleapis.com/youtube/v3/videos?key="+API_key+"&id="+vid+"&part=snippet,contentDetails,statistics"
        response = requests.get(url).json()
        #Create nested for loop to add data to df
        for item in response['items']:
            title = item['snippet']['title']
            desc  = item['snippet']['description']
            cat_id = item['snippet']['categoryId']
            vid_duration = item['contentDetails']['duration']
            dimension = item['contentDetails']['dimension']
            definition = item['contentDetails']['definition']
            if 'likeCount' in item['statistics']:
                likes = item['statistics']['likeCount']
            else:
                likes = 'Na'
            if 'commentCount' in item['statistics']:
                comments = item['statistics']['commentCount']
            else:
                comments = 'Na'
            if 'viewCount' in item['statistics']:
                veiws = item['statistics']['viewCount']
            else:
                veiws = 'Na'
            #Add data to df
            df = df.append({'video_id':vid,'title':title,'desc':desc,'cat_id':cat_id,
                            'vid_duration':vid_duration,'dimension':dimension,
                            'definition':definition,'likes':likes,
                            'comments':comments,'veiws':veiws}, ignore_index=True)
df.to_csv('YT_data_uncleaned.csv', index=False)