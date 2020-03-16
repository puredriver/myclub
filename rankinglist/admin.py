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
        # change ranking position automaticaly
        ranking_playerone = Ranking.objects.filter(rankinglist=obj.rankinglist,player=obj.playerone).first()
        ranking_playertwo = Ranking.objects.filter(rankinglist=obj.rankinglist,player=obj.playertwo).first()
        # TODO check rankings first if available
        # TODO validation - check match result if status GESPIELT
        # TODO show only players in dropdown who have a ranking for rankingadmin
        if ( ranking_playerone.position > ranking_playertwo.position and (obj.status == Match.GESPIELT or obj.status == Match.ABGEBROCHEN)):
            posplayerone_old = ranking_playerone.position
            ranking_playerone.position = ranking_playertwo.position
            ranking_playertwo.position = posplayerone_old
            ranking_playerone.save()
            ranking_playertwo.save()

    def get_queryset(self, request):
        qs = super(MatchAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        # is user admin of a rankinglist? than filter matches by rankinglist
        rankinglists = Rankinglist.objects.filter(admin=request.user)
        
        return qs.filter(rankinglist__in=rankinglists)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "rankinglist":
            if not request.user.is_superuser:
                kwargs["queryset"] = Rankinglist.objects.filter(admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class RankingAdmin(admin.ModelAdmin):
    fields = ('rankinglist', ('position','player'))

    list_display = ('rankinglist','position', 'player')

    list_display_links = ('position',)


# Register your models here.
admin.site.register(Rankinglist)
# admin.site.register(Player)
admin.site.register(Ranking,RankingAdmin)
admin.site.register(Match,MatchAdmin)