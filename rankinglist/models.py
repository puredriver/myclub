from django.db import models

# Create your models here.


class Rankinglist(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)

    def nameshort(self):
        return "%s %s." % (self.firstname, self.lastname[:1])

class Ranking(models.Model):
    position = models.IntegerField(default=0)
    rankinglist = models.ForeignKey(Rankinglist, on_delete=models.CASCADE, related_name="rankings")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s: %s %s" % (self.rankinglist, self.position, self.player)
        
    class Meta:
        ordering = ["position"]
        
class Match(models.Model):
    rankinglist = models.ForeignKey(Rankinglist, on_delete=models.CASCADE)
    playerone = models.ForeignKey(Player, related_name='playerone', on_delete=models.CASCADE)
    playertwo = models.ForeignKey(Player, related_name='playertwo', on_delete=models.CASCADE)
    playedat = models.DateField()
    set1playerone = models.IntegerField(default=0)
    set1playertwo = models.IntegerField(default=0)
    set2playerone = models.IntegerField(default=0)
    set2playertwo = models.IntegerField(default=0)
    set3playerone = models.IntegerField(default=0)
    set3playertwo = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s: %s vs %s - %s" % (self.rankinglist,self.playerone,self.playertwo,self.playedat)

  
