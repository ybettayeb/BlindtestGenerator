#!/usr/bin/env python
# coding: utf-8

# Processus de création de bl
# 
# #1 Parse une playlist (spotify/youtube)
# #2 telecharger les musiques
# #3 Randomiser les chansons 
# #4 découper les chansons
# #4 Modifier clips vidéos avec fond noir et ajouter la musique pendant 15 secondes puis ajouter la réponse en texte + image ? 
# #5 Combiner tout les clips en une vidéo

# In[216]:


import moviepy.editor as mp
import youtube_dl
from itertools import count
import os


# In[219]:


def downloadVid(uri):
    ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio/best'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([uri])

def downloadSound(uri):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'C:\\Users\\ybett\\Documents\\download\\%(title)s.%(ext)s.',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
            
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([uri])
        info_dict = ydl.extract_info(uri, download=False)
        return info_dict.get('title', None)
    
    
def getPlaylistURLS(uri):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
           result = ydl.extract_info(
               uri,
               download=False # We just want to extract the info
           )

    if 'entries' in result:
           # Can be a playlist or a list of videos
           return [row['webpage_url'] for row in result['entries']]


# In[54]:


# downloadVid('https://www.youtube.com/watch?v=j06DuMrn9n0')
downloadSound('https://www.youtube.com/watch?v=pRpeEdMmmQ0')


# In[44]:


video = mp.VideoFileClip("example.mp4")
audio = mp.AudioFileClip('example.mp3')


# In[45]:


audio = audio.subclip(10,30)

video = video.set_audio(audio)
video.subclip(0,20).ipython_display()


# In[220]:


class song:
    _ids = count(0)
    def __init__(self,uri):
        self.id = next(self._ids)
        self.name = downloadSound(uri)
        self.fileName = str(self.name)+".mp3"


# In[225]:


class blindtest:
    _ids = count(0)
    def __init__(self,playlistUri):
        self.playlistUri = playlistUri
        self.id = next(self._ids)
        self.videosURI = getPlaylistURLS(playlistUri) 
        self.tracklist = [] #List of URLs
        self.audioClips = [] #All the audios clips for editing
        for video in self.videosURI:
            self.tracklist.append(song(video))
        
    def createClips(self):
        cpt = 1
        for song in self.tracklist:
            print("getting audio clip of song " +  str(cpt) + "/" + str(len(self.tracklist)) )
            file = song.fileName
            name = song.name
            audioClip = mp.AudioFileClip('C:\\Users\\ybett\\Documents\\download\\'+str(file))
            self.audioClips.append([name,audioClip.subclip(10,30)])
            cpt+=1
    
    
    def generateVideo(self):
        guessingBlackScreen = mp.VideoFileClip('Example.mp4') #20 seconds of blackscreen
        answerBlackScreen = mp.VideoFileClip('Example.mp4').subclip(0,5)
        EditedClips= []

        for clip in self.audioClips:
            txt = mp.TextClip(clip[0], font='Amiri-regular',  color='white',fontsize=24)
            guessAudio = clip[1].subclip(10,30)
            answerAudio = clip[1].subclip(30,35)
            
            guessingClip = guessingBlackScreen.set_audio(guessAudio)
            AnswerClip = answerBlackScreen.set_audio(answerAudio)
            AnswerClipWithText = mp.CompositeVideoClip([AnswerClip,txt]).set_duration(7)
            FinalGuessAnswerClip = mp.concatenate_videoclips([guessingClip,AnswerClipWithText])
            EditedClips.append(FinalGuessAnswerClip)

        
        
        Final = mp.concatenate_videoclips(EditedClips)
        Final.write_videofile("OUTPUT.MP4")            


# In[226]:


blindT = blindtest("https://www.youtube.com/playlist?list=PLJKMzc-mCb5gmoyR28abNNLZlxu5yvd72")


# In[227]:


blindT.createClips()


# In[218]:





# In[228]:


blindT.generateVideo()

