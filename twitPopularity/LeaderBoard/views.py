from django.shortcuts import render
from .models import Person
from django.shortcuts import redirect
from .forms import UserForm
from django.views.generic import View
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonSerializer

import argparse
from urllib.parse import urlparse 
import urllib
import csv
import tweepy
import sys
import requests
import urllib
from itertools import product

PopUsername='Mr/Mrs Popular'
PopScreenName='twitPop_star' 
Popfollowing=0
Popfollowers=0 
Popranking=0 
Popimage=''

YourName=''
YourScreenName=''
YourFollowers=0
YourFollowing=0
YourImage=''
rankCounter = 1
counter = 100

    
def index(request):

    global PopUsername, PopScreenName, Popfollowing, Popfollowers, Popranking, Popimage
    if(len(PopUsername) > 30 ):
        PopUsername = "UserName"
       
    return render(request, 'LeaderBoard/index.html', { 'Popusername': PopUsername, 'PopscreenName': PopScreenName,
                                                       'Popfollowing': Popfollowing, 'Popfollowers': Popfollowers,
                                                        'Popimage': Popimage, 'YourName': YourName, 'YourScreenName': YourScreenName,
                                                        'YourFollowing': YourFollowing, 'YourFollowers': YourFollowers, 
                                                        'YourImage': YourImage,'rankCounter': rankCounter, 'total': counter})

   
        
def AddUser(request):
    form = UserForm(request.POST or None, request.FILES or None )
 
    # URL CLEANUP
    def url_fix(s, charset='utf-8'):
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    # COMMAND PARSER
    def tw_parser():
        global qw, ge, l, t, c, d


    # Parse the command
        parser = argparse.ArgumentParser(description='Twitter Search')
        parser.add_argument(action='store', dest='query', help='Search term string')
        parser.add_argument('-g', action='store', dest='loca', help='Location (lo, nyl, nym, nyu, dc, sf, nb')
        parser.add_argument('-l', action='store', dest='l', help='Language (en = English, fr = French, etc...)')
        parser.add_argument('-t', action='store', dest='t', help='Search type: mixed, recent, or popular')
        parser.add_argument('-c', action='store', dest='c', help='Tweet count (must be <50)')
        args = parser.parse_args()

        qw = args.query   
        ge = ''
        l='en'



        # Tweet count
        if args.c:
            c = int(args.c)
            if (c > cmax):
                print ("Resetting count to ",cmax," (maximum allowed)")
                c = cmax
            if (not (c) or (c < 1)):
                c = 1
        if not(args.c):
            c = 1

    

    # AUTHENTICATION
    def tw_oauth(authfile):
        with open(authfile, "r") as f:
            ak = f.readlines()
        f.close()
        auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
        auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
        return tweepy.API(auth1)

    def tw_search_json(query, cnt=5):
        authfile = './auth.k'
        api = tw_oauth(authfile)
        results = {}
        meta = {
            'username': 'text',
            'usersince': 'date',
            'followers': 'numeric',
            'friends': 'numeric',
            'authorid': 'text',
            'authorloc': 'geo',
            'geoenable': 'boolean',
            'source': 'text'
        }
        data = []
        for tweet in tweepy.Cursor(api.search, q=query, count=cnt).items():
            dTwt = {}
            dTwt['username'] = tweet.author.name
            dTwt['usersince'] = tweet.author.created_at      #author/user profile creation date
            dTwt['followers'] = tweet.author.followers_count #number of author/user followers (inlink)
            dTwt['friends']   = tweet.author.friends_count   #number of author/user friends (outlink)
            dTwt['authorid']  = tweet.author.id              #author/user ID#
            dTwt['authorloc'] = tweet.author.location        #author/user location
            dTwt['geoenable'] = tweet.author.geo_enabled     #is author/user account geo enabled?
            dTwt['source']    = tweet.source                 #platform source for tweet
            data.append(dTwt)
        results['meta'] = meta
        results['data'] = data
        return results

  

   

    # TWEEPY SEARCH FUNCTION
    def tw_search(api):

        # Open/Create a file to append data
        csvFile = open('result.csv','w')
        #Use csv Writer
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["UserID","Name", "UserName", "followers", "friends","image"])
        
        for tweet in tweepy.Cursor(api.search,
                                    q = qw,
                                    g = ge,
                                    lang = l,
                                    count = c).items():

    
            #AUTHOR INFO
            username  = tweet.author.name            #author/user name
            UserName = str(username).encode("utf-8")
            usersince = tweet.author.created_at      #author/user profile creation date
            followers = tweet.author.followers_count #number of author/user followers (inlink)
            friends   = tweet.author.friends_count   #number of author/user friends (outlink)
            authorid  = tweet.author.id              #author/user ID#
            authorloc = tweet.author.location        #author/user location
            user = api.get_user(authorid)
            screenName = user.screen_name
        
            profile_image_url = 'https://twitter.com/%s/profile_image?size=original'
            r = requests.get(profile_image_url % screenName)
            url = r.url.startswith('https://twitter.com/') and '-' or r.url


            #TECHNOLOGY INFO
            geoenable = tweet.author.geo_enabled     #is author/user account geo enabled?
            source    = tweet.source                 #platform source for tweet

            global PopUsername, PopScreenName, Popfollowing, Popfollowers, Popranking, Popimage, rankCounter, counter
            
            if(YourName[0].islower()):
                OtherWord = YourName[0].upper()
                for i in range(1, len(YourName)):
                    OtherWord+=YourName[i]
            else:
                if(YourName[0].isupper()):
                    OtherWord = YourName[0].lower()
                    for i in range(1, len(YourName)):
                        OtherWord+=YourName[i]
                
            words =[YourName,OtherWord]
            for word in words:
                if (word in screenName):
                    csvWriter.writerow([UserName,screenName,followers, friends,url])
                    if(followers > Popfollowers):
                        PopUsername = UserName
                        PopScreenName = screenName
                        Popfollowing = friends
                        Popfollowers = followers
                        Popranking = 1
                        Popimage = url

                    if(followers > int(YourFollowers)):
                        rankCounter = rankCounter + 1
            
                    counter = counter +1
            if (counter == c):
                csvWriter.writerow(['PopUserName','PopscreenName','Popfollowers', 'Popfriends','Popurl'])
                csvWriter.writerow([PopUsername,PopScreenName,Popfollowers, Popfollowing,Popimage])
                csvFile.close()
                break
            






    # MAIN ROUTINE
    def main():

        global api, cmax, locords
        
        cmax = 20
        
        # OAuth key file
        authfile = './auth.k'

        tw_parser()
        api = tw_oauth(authfile)
        tw_search(api)

        global PopUsername, PopScreenName, Popfollowing, Popfollowers, Popranking, Popimage

        PopularPerson = Person()
        PopularPerson.Username = PopUsername
        PopularPerson.ScreenName = PopScreenName
        PopularPerson.followers = Popfollowers
        PopularPerson.following = Popfollowing
        PopularPerson.image = Popimage
        PopularPerson.save()

   
    if request.method == 'POST':
        global YourName, YourScreenName, YourFollowing, YourFollowers, YourImage
        
        if form.is_valid():
            YourName = request.POST.get('Username', None)
            YourScreenName = request.POST.get('ScreenName', None)
            YourFollowing = request.POST.get('following', None)
            YourFollowers = request.POST.get('followers', None)
            YourImage = request.session.get('image')
            sys.argv = [sys.argv[0], YourName, '-c', '20']
            main()
            return redirect('twitPopularity:index')
        else:
            return HttpResponse("Error")
    else:
        
        form = UserForm()
        

        context = {"form": form}   
        return render(request, 'LeaderBoard/person_form.html', context)


class PopularPerson(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    
 