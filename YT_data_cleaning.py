import pandas as pd

# import uncleaned data
df = pd.read_csv('YT_data_uncleaned.csv')

# Turn catigory id into catigory name
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
df['cat_id'] = df['cat_id'].apply(cat_id_to_name)

# convert vid duration from ISO 8601 to mins
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

df['vid_duration'] = df['vid_duration'].apply(vid_duration_to_min)

# Drop rows with Na values for likes comments and veiws
df = df[df.likes != 'Na']
df = df[df.comments != 'Na']
df = df[df.veiws != 'Na']

df = df.reset_index()
df = df.drop('index', axis=1)
# convert likes comments and veiw count from string to int
df['likes'] = df['likes'].apply(lambda x: int(x))
df['comments'] = df['comments'].apply(lambda x: int(x))
df['veiws'] = df['veiws'].apply(lambda x: int(x))

# add fetures
# add column with length of description
df['desc_length'] = df['desc'].apply(lambda x: len(str(x)))

# add like to veiw ratio
df['like_veiw_ratio'] = (df['likes'].apply(lambda x: x))/(df['veiws'].apply(lambda x: x))

# add comment to veiw ratio
df['comment_veiw_ratio'] = (df['comments'].apply(lambda x: x))/(df['veiws'].apply(lambda x: x))

# export cleaned data
df.to_csv('YT_data_cleaned.csv', index=False)