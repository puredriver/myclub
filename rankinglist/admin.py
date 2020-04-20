from django.contrib import admin
import logging
from .models import Rankinglist,Player,Ranking,Match
from django.contrib import messages
from .forms import MatchAdminForm

logger = logging.getLogger(__name__)


# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
class MatchAdmin(admin.ModelAdmin):
    ordering = ['-playedat']  
    fields = ('rankinglist', 'playerone','playertwo','playedat','status',('set1playerone','set1playertwo'),('set2playerone','set2playertwo'),('set3playerone','set3playertwo'))
    list_display = ('rankinglist','status', 'playerone','playertwo','playedat','set1','set2','set3')
    list_display_links = ('status',)

    form = MatchAdminForm

    def save_model(self, request, obj, form, change):
        # switch the ranking if needed
        ranking_playerone = Ranking.objects.filter(rankinglist=obj.rankinglist,player=obj.playerone).first()
        ranking_playertwo = Ranking.objects.filter(rankinglist=obj.rankinglist,player=obj.playertwo).first()
       
        if ( ranking_playerone.position > ranking_playertwo.position and (obj.status == Match.GESPIELT or obj.status == Match.ABGEBROCHEN)):            
            ranking_playerone.position, ranking_playertwo.position = ranking_playertwo.position, ranking_playerone.position
            ranking_playerone.save()
            ranking_playertwo.save()
        
        super().save_model(request, obj, form, change)
        # change ranking position automaticaly
        

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
    

# class RankingAdmin(admin.ModelAdmin):
#    fields = ('rankinglist', ('position','player'))
#    list_display = ('rankinglist','position', 'player')
#    list_display_links = ('position',)

class RankingInline(admin.TabularInline):
    model=Ranking

# Register your models here.
@admin.register(Rankinglist)
class RankinglistAdmin(admin.ModelAdmin):
    list_display = ('name','active', 'admin')
    list_display_links = ('name',)
    inlines = [RankingInline,]

# admin.site.register(Player)
# admin.site.register(Ranking,RankingAdmin)
admin.site.register(Match,MatchAdmin)
admin.site.site_header = 'Ranglisten Administration'
admin.site.index_title = 'Navigation'
