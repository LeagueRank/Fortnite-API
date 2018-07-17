from datetime import datetime, timedelta

from leaguerank import settings
from leaguerank.utils import getJSON, postJSON, convert_iso_time

from . import Player, BattleRoyale, BattleRoyaleStats, Store, StoreFront, Leaderboard, News, PatchNotes

class FortniteClient(object):
    """
    Client for accessing the Fortnite API.
    """
    def __init__(self, fortnite_token, launcher_token, password, email):
        password_response = postJSON(settings.token, headers={'Authorization': 'basic {}'.format(launcher_token)},
                                          data={'grant_type': 'password', 'username': '{}'.format(email),
                                                'password': '{}'.format(password), 'includePerms': True})
        access_token = password_response.get('access_token')

        exchange_response = getJSON(settings.exchange,
                                         headers={'Authorization': 'bearer {}'.format(access_token)})
        code = exchange_response.get('code')

        token_response = postJSON(settings.token, headers={'Authorization': 'basic {}'.format(fortnite_token)},
                                       data={'grant_type': 'exchange_code', 'exchange_code': '{}'.format(code),
                                             'includePerms': True, 'token_type': 'egl'})

        access_token = token_response.get('access_token')
        refresh_token = token_response.get('refresh_token')
        expires_at = convert_iso_time(token_response.get('expires_at'))
        self.session = Session(access_token, refresh_token, expires_at, fortnite_token)

    def player(self, username):
        """Return object containing player name and id"""
        response = self.session.get(settings.player.format(username))
        return Player(response)

    def battle_royale_stats(self, username, platform):
        """Return object containing Battle Royale stats"""
        player_id = self.player(username).id
        response = self.session.get(settings.battle_royale.format(player_id))
        return BattleRoyale(response=response, platform=platform)

    def friends(self, username):
        """Return list of player ids. This method only works for the authenticated account."""
        player_id = self.player(username).id
        response = self.session.get(settings.friends.format(player_id))
        return [friend.get('accountId') for friend in response]

    def store(self, rw=-1):
        """Return current store items. This method only works for the authenticated account."""
        response = self.session.get(settings.store.format(rw))
        return Store(response)

    def leaderboard(self, count=50, platform=settings.Platform.pc, mode=settings.GameType.solo):
        """Return list of leaderboard objects. Object attributes include id, name, rank, and value."""
        params = {'ownertype': '1', 'itemsPerPage': count}
        leaderboard_response = self.session.post(endpoint=settings.leaderboard.format(platform, mode), params=params)
        for entry in leaderboard_response.get('entries'):
            for key, value in entry.items():
                if key == 'accountId':
                    entry[key] = value.replace('-', '')
        account_ids = '&accountId='.join([entry.get('accountId') for entry in leaderboard_response.get('entries')])
        account_response = self.session.get(endpoint=settings.account.format(account_ids))
        players = []
        for player in leaderboard_response.get('entries'):
            for account in account_response:
                if player.get('accountId') == account.get('id'):
                    players.append({'id': player.get('accountId'), 'name': account.get('displayName'),
                                    'value': player.get('value'), 'rank': player.get('rank')})
        return [Leaderboard(player) for player in players]

    @staticmethod
    def news():
        """Get the current news on fortnite."""
        response = Session.get_noauth(endpoint=settings.news, headers={'Accept-Language': 'en'})
        return News(response=response)

    @staticmethod
    def server_status():
        """Check the status of the Fortnite servers. Returns True if up and False if down."""
        response = Session.get_noauth(endpoint=settings.status)
        if response[0]['status'] == 'UP':
            return True
        else:
            return False

    @staticmethod
    def patch_notes(posts_per_page=5, offset=0, locale='en-US', category='patch notes'):
        """Get a list of recent patch notes for fortnite. Can return other blogs from epicgames.com"""
        params = {'category': category, 'postsPerPage': posts_per_page, 'offset': offset, 'locale': locale}
        response = Session.get_noauth(endpoint=settings.patch_notes, params=params)
        return PatchNotes(status=response.status_code, response=response)


class Session:
    def __init__(self, access_token, refresh_token, expires_at, fortnite_token):
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.fortnite_token = fortnite_token
        self.access_token = access_token

        self.check_token()

    def check_token(self):
        "Check if the token needs to be updated"
        now = datetime.utcnow()
        if self.expires_at < (now - timedelta(seconds=60)):
            print('Token Refresh')
            self.refresh()

    def refresh(self):
        response = postJSON(settings.token, 
            headers={
                'Authorization': 'basic {}'.format(self.fortnite_token),
            },
            data={
                'grant_type': 'refresh_token', 
                'refresh_token': '{}'.format(self.refresh_token),
                'includePerms': True
            })
        self.access_token = response.get('access_token')
        self.refresh_token = response.get('refresh_token')
        self.expires_at = convert_iso_time(response.get('expires_at'))

    def get(self, endpoint, params=None, headers=None):
        self.check_token()
        if headers is None:
            headers = {}
        headers['Authorization'] = 'bearer {}'.format(self.access_token)
        response = getJSON(endpoint, params=params, headers=headers)
        return response

    def post(self, endpoint, params=None, headers=None):
        self.check_token()
        if headers is None:
            headers = {}
        headers['Authorization'] = 'bearer {}'.format(self.access_token)
        response = postJSON(endpoint, data=params, headers=headers)
        return response

    @staticmethod
    def get_noauth(endpoint, params=None, headers=None):
        response = getJSON(endpoint, params=params, headers=headers)
        return response

    @staticmethod
    def post_noauth(endpoint, params=None, headers=None):
        response = postJSON(endpoint, data=params, headers=headers)
        return response

