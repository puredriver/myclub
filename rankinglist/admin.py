from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Rankinglist,Player,Ranking,Match,Club
from django.contrib import messages
from .forms import MatchAdminForm

import logging
logger = logging.getLogger("rankinglist")


class ClubAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

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
    

class RankingAdmin(admin.ModelAdmin):
    fields = ('rankinglist', ('position','player'))
    list_display = ('rankinglist','position', 'player')
    list_display_links = ('position',)

class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    fields =('club','leistungsklasse')
    #verbose_name_plural = 'Spieler'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "club":
            if not request.user.is_superuser:
                kwargs["queryset"] = Club.objects.filter(name=request.user.player.club)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline,)
    list_display = ('get_club','username','first_name', 'last_name', 'email','is_active', 'is_staff','get_email_confirmed')
    list_display_links = ('username',)

    def get_club(self,instance):
        return instance.player.club
    get_club.short_description = 'Club'

    def get_email_confirmed(self,instance):
        return instance.player.email_confirmed

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        # is user is_staff and has role "ClubAdmin" he can edit user from his club               
        return qs.filter(player__club__exact=request.user.player.club)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff','groups')

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]

class RankingInline(admin.TabularInline):
    model=Ranking
    extra = 0

# Register your models here.
@admin.register(Rankinglist)
class RankinglistAdmin(admin.ModelAdmin):
    fields = (('name','active'), ('club','admin'))
    list_display = ('club','name','active', 'admin',)
    list_display_links = ('name',)
    inlines = [RankingInline,]

# Re-register UserAdmin to add player fields to admin scree
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Match,MatchAdmin)
admin.site.register(Club,ClubAdmin)
admin.site.site_header = 'Ranglisten Administration'
admin.site.index_title = 'Navigation'
