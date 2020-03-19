from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Match, Rankinglist, Ranking
from .serializers import MatchSerializer, RankinglistSerializer, RankingSerializer

import logging
logger = logging.getLogger('rankinglist')


class RankinglistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rankinglist.objects.filter(active=True)
    serializer_class = RankinglistSerializer

    #lookup_field = 'id'

    @action(detail=True,url_path='rankings', url_name='rankings')
    def get_rankings(self, request, pk=None):
        """
        Returns a list of all the rankings
        """
        rankinglist = self.get_object()
        logger.debug("in viewset -get_rankings-: " + rankinglist.name)
        queryset = Ranking.objects.filter(rankinglist=rankinglist)
        serializer = RankingSerializer(queryset, many=True)
        logger.debug(serializer.data)
        return Response(serializer.data)

    @action(detail=True,url_path='matchesp', url_name='matchesp')
    def get_matchesp(self,request,pk=None):
        rankinglist = self.get_object()
        logger.debug("in viewset -get_matchesp-: " + rankinglist.name)
        queryset = Match.objects.filter(rankinglist=rankinglist,status=Match.GEPLANT).order_by('playedat')
        serializer = MatchSerializer(queryset, many=True)
        logger.debug(serializer.data)
        return Response(serializer.data)

    @action(detail=True,url_path='matches', url_name='matches')
    def get_matches(self,request,pk=None):
        rankinglist = self.get_object()
        logger.debug("in viewset -get_matches-: " + rankinglist.name)
        queryset = Match.objects.all().filter(rankinglist=rankinglist).exclude(status=Match.GEPLANT).order_by('-playedat')
        serializer = MatchSerializer(queryset, many=True)
        logger.debug(serializer.data)
        return Response(serializer.data)