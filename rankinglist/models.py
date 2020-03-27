from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    #TODO  logo + address + google map

    def __str__(self):
        return self.name
    

class Rankinglist(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Rangliste"
        verbose_name_plural = "Ranglisten"

class Player(models.Model):    
    # if deleted set ranking and matches to a "deleted" user
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)
    leistungsklasse = models.IntegerField(default=0)

    @receiver(post_save, sender=User,dispatch_uid="player_create")
    def create_save_user_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User,dispatch_uid="player_save")
    def save_user_player(sender, instance, **kwargs):
        instance.player.save()

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def nameshort(self):
        return "%s %s." % (self.user.first_name, self.user.last_name[:1])
    
    class Meta:    
        verbose_name = "Spieler"
        verbose_name_plural = "Spieler"

class Ranking(models.Model):
    position = models.IntegerField(default=0)
    rankinglist = models.ForeignKey(Rankinglist, on_delete=models.CASCADE, related_name="rankings")
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s: %s %s" % (self.rankinglist, self.position, self.player)

    class Meta:
        ordering = ["position"]
        verbose_name = "Position"
        verbose_name_plural = "Positionen"
        
class Match(models.Model):
    GEPLANT='geplant'
    GESPIELT='gespielt'
    ABGEBROCHEN='abgebrochen'
    MATCHSTATUS_CHOICES = (
    (GEPLANT,'geplant'),
    (GESPIELT,'gespielt'),
    (ABGEBROCHEN,'abgebrochen'),
    )

    rankinglist = models.ForeignKey(Rankinglist, on_delete=models.CASCADE,verbose_name='Rangliste')
    playerone = models.ForeignKey(User, related_name='playerone', on_delete=models.CASCADE,verbose_name='Spieler 1 (Sieger)')
    playertwo = models.ForeignKey(User, related_name='playertwo', on_delete=models.CASCADE,verbose_name='Spieler 2')
    playedat = models.DateTimeField(verbose_name='Spieldatum')
    set1playerone = models.IntegerField(default=0,verbose_name='Satz1 - Spieler 1')
    set1playertwo = models.IntegerField(default=0,verbose_name='Satz1 - Spieler 2')
    set2playerone = models.IntegerField(default=0,verbose_name='Satz2 - Spieler 1')
    set2playertwo = models.IntegerField(default=0,verbose_name='Satz2 - Spieler 2')
    set3playerone = models.IntegerField(default=0,verbose_name='Satz3 - Spieler 1')
    set3playertwo = models.IntegerField(default=0,verbose_name='Satz3 - Spieler 2')
    status = models.CharField(max_length=20, choices=MATCHSTATUS_CHOICES, default=GEPLANT)
    
    def __str__(self):
        return "%s: %s vs %s - %s" % (self.rankinglist,self.playerone,self.playertwo,self.playedat)

    def set1(self):
        return "%s : %s" % (self.set1playerone,self.set1playertwo)
    
    def set2(self):
        return "%s : %s" % (self.set2playerone,self.set2playertwo)

    def set3(self):
        if self.set3playerone != 0 and self.set3playertwo != 0:
            return "%s : %s" % (self.set2playerone,self.set2playertwo)
        else:
            return ""
    class Meta:
         verbose_name = "Spiel"
         verbose_name_plural = "Spiele"
