from django.test import TestCase
from django.test import Client
import datetime

# Create your tests here.

from .models import Rankinglist, Player, Match, Ranking

class ViewsTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        r = Rankinglist.objects.create(name="herren")
        boris = Player.objects.create(firstname="Boris",lastname="Becker")
        ivan = Player.objects.create(firstname="Ivan",lastname="Lendl")
        roger = Player.objects.create(firstname="Roger",lastname="Federer")

        Ranking.objects.create(position=1,rankinglist=r,player=boris)
        Ranking.objects.create(position=2,rankinglist=r,player=ivan)
        Ranking.objects.create(position=3,rankinglist=r,player=roger)

        Match.objects.create(rankinglist=r,playerone=boris,playertwo=ivan,playedat=datetime.datetime(2020, 5, 17))        
        Match.objects.create(rankinglist=r,playerone=boris,playertwo=roger,playedat=datetime.datetime(2020, 5, 16))
        Match.objects.create(rankinglist=r,playerone=boris,playertwo=ivan,playedat=datetime.datetime(2020, 5, 15))

    def test_rankingliststats(self):   
        r = Rankinglist.objects.get(name="herren")

        # Issue a GET request.
        response = self.client.get('/rankinglist/rankinglist/%s/stats' %(r.id))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertEqual(response.context['rankinglist'].name,"herren")
        self.assertEqual(len(response.context['players']),3)