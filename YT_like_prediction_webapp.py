import pickle
import pandas as pd
import streamlit as st
import requests
import sklearn

# load model
model = pickle.load(open('YT_likes_model.pkl', 'rb'))

# create function to turn cat_id into cat name for later
def cat_id_to_name(x):
    if x == 1:
        x = 'Film_and_Animation'
    elif x == 2:
        x = 'Autos_and_Vehicles'
    elif x == 10:
        x = 'Music'
    elif x == 15:
        x = 'Pets_and_Animals'
    elif x == 17:
        x = 'Sports'
    elif x == 18:
        x = 'Short_Movies'
    elif x == 19:
        x = 'Travel_and_Events'
    elif x == 20:
        x = 'Gaming'
    elif x == 21:
        x = 'Videoblogging'
    elif x == 22:
        x = 'People_and_Blogs'
    elif x == 23:
        x = 'Comedy'
    elif x == 24:
        x = 'Entertainment'
    elif x == 25:
        x = 'News_and_Politics'
    elif x == 26:
        x = 'Howto_and_Style'
    elif x == 27:
        x = 'Education'
    elif x == 28:
        x = 'Science_and_Technology'
    elif x == 29:
        x ='Nonprofits_and_Activism'
    elif x == 30:
        x = 'Movies'
    elif x == 31:
        x = 'Anime/Animation_Movie'
    elif x == 32:
        x = 'Action/Adventure_Movie'
    elif x == 33:
        x = 'Classics_Movie'
    elif x == 34:
        x = 'Comedy_Movie'
    elif x == 35:
        x = 'Documentary_Movie'
    elif x == 36:
        x = 'Drama_Movie'
    elif x == 37:
        x = 'Family_Movie'
    elif x == 38:
        x = 'Foreign_Movie'
    elif x == 39:
        x = 'Horror_Movie'
    elif x == 40:
        x = 'Sci-Fi/Fantasy_Movie'
    elif x ==41:
        x = 'Thriller_Movie'
    elif x == 42:
        x = 'Shorts'
    elif x == 43:
        x = 'Shows'
    elif x == 44:
        x = 'Trailers'
    return x

# create function to convert vid duration from ISO 8601 to mins for later
def vid_duration_to_min(x):
    if 'H' in x:
        hours = x.split('T')[1].split('H')[0]
        mins = (lambda x: x.split('H')[1].split('M')[0] if 'M' in x else 0)(x)
        secs = (lambda x: x.split('M')[1].split('S')[0] if 'S' and 'M' in x else (x.split('H')[1].split('S')[0] if 'S' in x else 0))(x)
    elif 'M' in x:
        hours = 0
        mins = x.split('T')[1].split('M')[0]
        secs = (lambda x: x.split('M')[1].split('S')[0] if 'S' in x else 0)(x)
    elif 'S' in x:
        hours = 0
        mins = 0
        secs = x.split('T')[1].split('S')[0]
    else:
        hours = 0
        mins = 0
        secs = 0
    mins_tot = (3600*int(hours)+60*int(mins)+int(secs))/60
    return mins_tot
# defign main function
def main():
    st.title('Youtube Expected Like Estimation')
    
    # youtube video id input
    video_id = st.text_input('Video ID')
    
    #create button to make prediction from video id
    if st.button('Predict'):
        
        # collect input variables from youtube api using video id
        API_key = "AIzaSyB-ytg0iOp83p4bxEK2l8SrYeigAMOhQRk"
        url = "https://www.googleapis.com/youtube/v3/videos?key="+API_key+"&id="+video_id+"&part=snippet,contentDetails,statistics"
        response = requests.get(url).json()
        for item in response['items']:
            desc  = item['snippet']['description']
            cat_id = item['snippet']['categoryId']
            vid_duration = item['contentDetails']['duration']
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
        
        # convert cat_id from number to name
        cat_id = cat_id_to_name(int(cat_id))
        
        # convert vid duration from ISO 8601 to mins
        vid_duration = vid_duration_to_min(vid_duration)
        
        # create desc_length var
        desc_length = len(str(desc))
        
        # create df with dummy var to give to model
        data = {'vid_duration': vid_duration, 'comments': comments, 'veiws': veiws, 'desc_length': desc_length,
                'cat_id_Autos_and_Vehicles': 0, 'cat_id_Comedy': 0, 'cat_id_Education': 0,
                'cat_id_Entertainment': 0, 'cat_id_Film_and_Animation': 0, 'cat_id_Gaming': 0,
                'cat_id_Howto_and_Style': 0, 'cat_id_Music': 0, 'cat_id_News_and_Politics': 0,
                'cat_id_Nonprofits_and_Activism': 0, 'cat_id_People_and_Blogs': 0, 'cat_id_Pets_and_Animals': 0,
                'cat_id_Science_and_Technology': 0, 'cat_id_Sports': 0, 'cat_id_Travel_and_Events': 0,
                'definition_hd': 0, 'definition_sd': 0}
        
        # change cat_id dummy vars to correct values
        for item in data:
            if cat_id == item.replace('cat_id_', ''):
                data[item] = 1
        
        # change definition dummy vars to correct values
        if definition == 'hd':
            data['definition_hd'] = 1
        else:
            data['definition_sd'] = 1
        df = pd.DataFrame(data, index=[0])
        # use model to make prediction
        prediction = model.predict(df)
        output = round(prediction[0], 0)
        st.success('The model estimates that your video should have about {} likes'.format(output))
        
if __name__ == '__main__':
            main()