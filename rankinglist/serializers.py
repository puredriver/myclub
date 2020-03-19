from rest_framework import serializers  
from .models import Match, Rankinglist, Player, Ranking

class RankinglistSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Rankinglist
        exclude = ['active','admin']

class PlayerSerializer(serializers.ModelSerializer):
    nameshort = serializers.SerializerMethodField('get_nameshort')

    class Meta:
        model = Player
        fields = ['id','nameshort']

    def get_nameshort(self, obj):
        return "%s %s." % (obj.first_name, obj.last_name[:1])

class RankingSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = Ranking
        fields = ['id', 'position','player' ]
        depth = 1

class MatchSerializer(serializers.ModelSerializer):
    playerone = PlayerSerializer()
    playertwo = PlayerSerializer()
    rankinglist = RankinglistSerializer()

    class Meta:
        model = Match
        fields = ['id', 'status', 'playedat', 'rankinglist', 'playerone','playertwo','set1playerone','set1playertwo', 'set2playerone', 'set2playertwo', 'set3playerone','set3playertwo']
        depth = 1