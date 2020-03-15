from django.contrib import admin
import logging
from .models import Rankinglist,Player,Ranking,Match

logger = logging.getLogger(__name__)

# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
class MatchAdmin(admin.ModelAdmin):
    ordering = ['-playedat']  

    fields = ('rankinglist', 'playerone','playertwo','playedat','status',('set1playerone','set1playertwo'),('set2playerone','set2playertwo'),('set3playerone','set3playertwo'))

    list_display = ('rankinglist','status', 'playerone','playertwo','playedat','set1','set2','set3')

    list_display_links = ('status',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # change ranking position
        ranking_playerone = Ranking.objects.filter(rankinglist=obj.rankinglist,player=obj.playerone).first()
        ranking_playertwo = Ranking.objects.filter(rankinglist=obj.rankinglist,player=obj.playertwo).first()
        if ( ranking_playerone.position > ranking_playertwo.position):
            posplayerone_old = ranking_playerone.position
            ranking_playerone.position = ranking_playertwo.position
            ranking_playertwo.position = posplayerone_old
            ranking_playerone.save()
            ranking_playertwo.save()

class RankingAdmin(admin.ModelAdmin):
    fields = ('rankinglist', ('position','player'))

    list_display = ('rankinglist','position', 'player')

    list_display_links = ('position',)


# Register your models here.
admin.site.register(Rankinglist)
# admin.site.register(Player)
admin.site.register(Ranking,RankingAdmin)
admin.site.register(Match,MatchAdmin)