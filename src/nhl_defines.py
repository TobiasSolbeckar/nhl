''' Pre defined variables '''
# @TODO: Maybe move the separate defines to the files where they are used?

# Links to team information from CapFriendly
CF_TEAM_LINKS = {
    "ANA": "https://www.capfriendly.com/teams/ducks",
    "ARI": "https://www.capfriendly.com/teams/coyotes",
    "BOS": "https://www.capfriendly.com/teams/bruins",
    "BUF": "https://www.capfriendly.com/teams/sabres",
    "CGY": "https://www.capfriendly.com/teams/flames",
    "CAR": "https://www.capfriendly.com/teams/hurricanes",
    "CHI": "https://www.capfriendly.com/teams/blackhawks",
    "COL": "https://www.capfriendly.com/teams/avalanche",
    "CBJ": "https://www.capfriendly.com/teams/bluejackets",
    "DAL": "https://www.capfriendly.com/teams/stars",
    "DET": "https://www.capfriendly.com/teams/redwings",
    "EDM": "https://www.capfriendly.com/teams/oilers",
    "FLA": "https://www.capfriendly.com/teams/panthers",
    "LAK": "https://www.capfriendly.com/teams/kings",
    "MIN": "https://www.capfriendly.com/teams/wild",
    "MTL": "https://www.capfriendly.com/teams/canadiens",
    "NSH": "https://www.capfriendly.com/teams/predators",
    "NJD": "https://www.capfriendly.com/teams/devils",
    "NYI": "https://www.capfriendly.com/teams/islanders",
    "NYR": "https://www.capfriendly.com/teams/rangers",
    "OTT": "https://www.capfriendly.com/teams/senators",
    "PHI": "https://www.capfriendly.com/teams/flyers",
    "PIT": "https://www.capfriendly.com/teams/penguins",
    "SJS": "https://www.capfriendly.com/teams/sharks",
    "SEA": "https://www.capfriendly.com/teams/kraken",
    "STL": "https://www.capfriendly.com/teams/blues",
    "TBL": "https://www.capfriendly.com/teams/lightning",
    "TOR": "https://www.capfriendly.com/teams/mapleleafs",
    "VAN": "https://www.capfriendly.com/teams/canucks",
    "VGK": "https://www.capfriendly.com/teams/goldenknights",
    "WSH": "https://www.capfriendly.com/teams/capitals",
    "WPG": "https://www.capfriendly.com/teams/jets"
}

AGE_COEFF = {
    16: 4.372,
    17: 3.676,
    18:	2.98,
    19:	2.284,
    20:	2.018,
    21:	1.179,
    22:	1.107,
    23:	1.056,
    24:	1.025,
    25:	1,
    26:	1,
    27:	1,
    28:	1,
    29:	1
}

MONTH_LOOKUP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}

LEAGUE_COEFF = {"NHL": 1,
                "AHL": 0.389,
                "ALLSVENSKAN": 0.351,
                "BCHL": 0.080,
                "CZECH": 0.583,
                "CZECH2": 0.240,
                "DENMARK": 0.190,
                "ECHL": 0.147,
                "HOCKEYALLSVENSKAN": 0.285,
                "HOCKEYETTAN": 0.109,
                "J18 ELIT": 0.045,
                "J18 ALLSVENSKAN": 0.067,
                "J18 DIV 1": 0.02,
                "J18 DIV 2": 0.01,
                "J20 SUPERELIT": 0.091,
                "KHL": 0.772,
                "LIIGA": 0.441,
                "MHL": 0.143,
                "NCAA": 0.194,
                "NLA": 0.459,
                "NORWAY": 0.173,
                "OHL": 0.144,
                "QMJHL": 0.113,
                "SHL": 0.566,
                "SL": 0.137,
                "SLOVAKIA": 0.295,
                "USDP": 0.121,
                "USHL": 0.143,
                "USHS-PREP": 0.028,
                "VHL": 0.328,
                "WHL": 0.141
                }

EP_TEAM_LINKS = {
    "ANA": "https://www.eliteprospects.com/team/1580/anaheim-ducks",
    "ARI": "https://www.eliteprospects.com/team/72/arizona-coyotes",
    "BOS": "https://www.eliteprospects.com/team/52/boston-bruins",
    "BUF": "https://www.eliteprospects.com/team/53/buffalo-sabres",
    "CGY": "https://www.eliteprospects.com/team/54/calgary-flames",
    "CAR": "https://www.eliteprospects.com/team/55/carolina-hurricanes",
    "CHI": "https://www.eliteprospects.com/team/56/chicago-blackhawks",
    "COL": "https://www.eliteprospects.com/team/57/colorado-avalanche",
    "CBJ": "https://www.eliteprospects.com/team/58/columbus-blue-jackets",
    "DAL": "https://www.eliteprospects.com/team/59/dallas-stars",
    "DET": "https://www.eliteprospects.com/team/60/detroit-red-wings",
    "EDM": "https://www.eliteprospects.com/team/61/edmonton-oilers",
    "FLA": "https://www.eliteprospects.com/team/62/florida-panthers",
    "LAK": "https://www.eliteprospects.com/team/79/los-angeles-kings",
    "MIN": "https://www.eliteprospects.com/team/63/minnesota-wild",
    "MTL": "https://www.eliteprospects.com/team/64/montreal-canadiens",
    "NSH": "https://www.eliteprospects.com/team/65/nashville-predators",
    "NJD": "https://www.eliteprospects.com/team/66/new-jersey-devils",
    "NYI": "https://www.eliteprospects.com/team/67/new-york-islanders",
    "NYR": "https://www.eliteprospects.com/team/68/new-york-rangers",
    "OTT": "https://www.eliteprospects.com/team/69/ottawa-senators",
    "PHI": "https://www.eliteprospects.com/team/70/philadelphia-flyers",
    "PIT": "https://www.eliteprospects.com/team/71/pittsburgh-penguins",
    "SJS": "https://www.eliteprospects.com/team/73/san-jose-sharks",
    "SEA": "https://www.eliteprospects.com/team/27336/seattle-kraken",
    "STL": "https://www.eliteprospects.com/team/74/st.-louis-blues",
    "TBL": "https://www.eliteprospects.com/team/75/tampa-bay-lightning",
    "TOR": "https://www.eliteprospects.com/team/76/toronto-maple-leafs",
    "VAN": "https://www.eliteprospects.com/team/77/vancouver-canucks",
    "VGK": "https://www.eliteprospects.com/team/22211/vegas-golden-knights",
    "WPG": "https://www.eliteprospects.com/team/9966/winnipeg-jets",
    "WSH": "https://www.eliteprospects.com/team/78/washington-capitals"
}

TOTAL_POINTS_PER_GAME = 2.1066089693154995
TOTAL_GOALS_PER_GAME = 5.209284028324154
TOTAL_GOALS_PER_GAME_ES = 0
TOTAL_GOALS_PER_GAME_PP = 0
TOTAL_GOALS_PER_GAME_PK = 0
SCF_SF_FACTOR = 4.292072174177282
PROBABILITY_FOR_OT = 0.10660896931549961
CURRENT_TEAM = ['ht', 'at']
OPPONENT_TEAM = ['at', 'ht']
SIMULATION_LIGHT = 0
SIMULATION_EXT = 1
HT_ADVANTAGE = 1.1878
AT_ADVANTAGE = 1/HT_ADVANTAGE
WS_DEF = [1, 0.75, 0.15]
WS_CEN = [1, 1, 0.5]
WS_WNG = [0.75, 1, 1]
WS_FWD = [1.25, 1.25, 0.5]
GAMEPLAY_ES = 0
GAMEPLAY_PP_HT = 1
GAMEPLAY_PP_AT = 2
GAMEPLAY_PK_HT = 2
GAMEPLAY_PK_AT = 1
NO_GOALIE_HT = 3
NO_GOALIE_AT = 4
NUMBER_OF_PERIODS = 3

PLAYFORMS = ['es', 'pp', 'pk']
'''
STAT_ES = 0
STAT_PP = 1
STAT_PK = 2
STAT_INDEX = [STAT_ES, STAT_PP, STAT_PK]
'''

# Scrape
SKATER_BIO_BIT = 0
SKATER_ES_BIT = 1
SKATER_PP_BIT = 2
SKATER_PK_BIT = 3
SKATER_ON_ICE_BIT = 4
SKATER_RELATIVE_BIT = 5
GOALIE_ES_BIT = 6
GOALIE_PP_BIT = 7
GOALIE_PK_BIT = 8
TEAM_ES_BIT = 9
TEAM_PP_BIT = 10
TEAM_PK_BIT = 11
TEAM_HOME_BIT = 12
TEAM_AWAY_BIT = 13
UNAVAILABLE_PLAYERS_BIT = 14
CONTRACT_EXPIRY_BIT = 15
DATABASE_ERROR_REGISTER = 16*[True]
DATABASE_WARNING_REGISTER = 16*[True]
CONNECTION_TIMEOUT = 60  # Connection will timeout after 60 seconds


ACTIVE_TEAMS = ['ANA', 'ARI', 'BOS', 'BUF', 'CAR', 'CBJ', 'CGY', 'CHI', 'COL',
                        'DAL', 'DET', 'EDM', 'FLA', 'LAK', 'MIN', 'MTL', 'NJD', 'NSH',
                        'NYI', 'NYR', 'OTT', 'PHI', 'PIT', 'SEA', 'SJS', 'STL', 'TBL',
                        'TOR', 'VAN', 'VGK', 'WPG', 'WSH']
'''
Skater Bio-DB from naturalstattrick.com
,"Player","Team","Position","Age","Date of Birth",
"Birth City","Birth State/Province","Birth Country",
"Nationality","Height (in)","Weight (lbs)","Draft Year",
"Draft Team","Draft Round","Round Pick","Overall Draft Position"
'''
SKATER_DB_BIO_NAME = 1
SKATER_DB_BIO_TEAM_ID = 2
SKATER_DB_BIO_POSITION = 3
SKATER_DB_BIO_AGE = 4
SKATER_DB_BIO_DOB = 5
SKATER_DB_BIO_HEIGHT = 10
SKATER_DB_BIO_WEIGHT = 11
SKATER_DB_BIO_DRAFT_YEAR = 12
SKATER_DB_BIO_DRAFT_TEAM = 13
SKATER_DB_BIO_DRAFT_ROUND = 14
SKATER_DB_BIO_ROUND_PICK = 15
SKATER_DB_BIO_TOTAL_DRAFT_POS = 16
SKATER_DB_BIO_LENGTH = 17

'''
Skater Individual-DB, ES, from naturalstattrick.com
'''
SKATER_DB_IND_TEAM_ID = 2
SKATER_DB_IND_TOI = 5
SKATER_DB_IND_GOALS = 6
SKATER_DB_IND_ASSIST = 7
SKATER_DB_IND_FIRST_ASSIST = 8
SKATER_DB_IND_SECOND_ASSIST = 9
SKATER_DB_IND_SF = 12
SKATER_DB_IND_SH_PCG = 13
SKATER_DB_IND_IXG = 14
SKATER_DB_IND_ICF = 15
SKATER_DB_IND_IFF = 16
SKATER_DB_IND_ISCF = 17
SKATER_DB_IND_IHDCF = 18
SKATER_DB_IND_RUSH_ATTEMPTS = 19
SKATER_DB_IND_REBOUNDS_CREATED = 20
SKATER_DB_IND_PIM = 21
SKATER_DB_IND_TOTAL_PENALTIES = 22
SKATER_DB_IND_MINOR = 23
SKATER_DB_IND_MAJOR = 24
SKATER_DB_IND_MISCONDUCT = 25
SKATER_DB_IND_PENALTIES_DRAWN = 26
SKATER_DB_IND_GIVEAWAYS = 27
SKATER_DB_IND_TAKEAWAYS = 28
SKATER_DB_IND_HITS = 29
SKATER_DB_IND_HITS_TAKEN = 30
SKATER_DB_IND_SHOTS_BLOCKED = 31
SKATER_DB_IND_FACEOFFS_WON = 32
SKATER_DB_IND_FACEOFFS_LOST = 33
SKATER_DB_IND_FACEOFFS_WON_PCG = 34
SKATER_DB_IND_LENGTH = 35

'''
Skater OnIce-DB from naturalstattrick.com
'''
SKATER_DB_ON_ICE_GP = 4
SKATER_DB_ON_ICE_TOI_UL = 5
SKATER_DB_ON_ICE_CF = 6
SKATER_DB_ON_ICE_CA = 7
SKATER_DB_ON_ICE_CF_PERCENT = 8
SKATER_DB_ON_ICE_FF = 9
SKATER_DB_ON_ICE_FA = 10
SKATER_DB_ON_ICE_FF_PERCENT = 11
SKATER_DB_ON_ICE_SF = 12
SKATER_DB_ON_ICE_SA = 13
SKATER_DB_ON_ICE_SF_PERCENT = 14
SKATER_DB_ON_ICE_GF = 15
SKATER_DB_ON_ICE_GA = 16
SKATER_DB_ON_ICE_GF_PERCENT = 17
SKATER_DB_ON_ICE_xGF = 18
SKATER_DB_ON_ICE_xGA = 19
SKATER_DB_ON_ICE_xGF_PERCENT = 20
SKATER_DB_ON_ICE_SCF = 21
SKATER_DB_ON_ICE_SCA = 22
SKATER_DB_ON_ICE_SCF_PERCENT = 23
SKATER_DB_ON_ICE_HDCF = 24
SKATER_DB_ON_ICE_HDCA = 25
SKATER_DB_ON_ICE_HDCF_PERCENT = 26
SKATER_DB_ON_ICE_OZS = 45
SKATER_DB_ON_ICE_NZS = 46
SKATER_DB_ON_ICE_DZS = 47
SKATER_DB_ON_ICE_OZS_PERCENT = 49
SKATER_DB_ON_ICE_OZFO = 50
SKATER_DB_ON_ICE_NZFO = 51
SKATER_DB_ON_ICE_DZFO = 52
SKATER_DB_ON_ICE_OZFO_PERCENT = 53
SKATER_DB_ON_ICE_LENGTH = 54

'''
Relative stats from naturalstattrick.com
'''
SKATER_DB_RELATIVE_NAME = 1
SKATER_DB_RELATIVE_TEAM_ID = 2
SKATER_DB_RELATIVE_CF_PER_60 = 7
SKATER_DB_RELATIVE_CA_PER_60 = 8
SKATER_DB_RELATIVE_CF_PCG = 9
SKATER_DB_RELATIVE_FF_PER_60 = 10
SKATER_DB_RELATIVE_FA_PER_60 = 11
SKATER_DB_RELATIVE_FF_PCG = 12
SKATER_DB_RELATIVE_SF_PER_60 = 13
SKATER_DB_RELATIVE_SA_PER_60 = 14
SKATER_DB_RELATIVE_SF_PCG = 15
SKATER_DB_RELATIVE_GF_PER_60 = 16
SKATER_DB_RELATIVE_GA_PER_60 = 17
SKATER_DB_RELATIVE_GF_PCG = 18
SKATER_DB_RELATIVE_xGF_PER_60 = 19
SKATER_DB_RELATIVE_XGA_PER_60 = 20
SKATER_DB_RELATIVE_xGF_PCG = 21
SKATER_DB_RELATIVE_SCF_PER_60 = 22
SKATER_DB_RELATIVE_SCA_PER_60 = 23
SKATER_DB_RELATIVE_SCF_PCG = 24

'''
Goalie-DB from naturalstattrick.com
'''
GOALIE_DB_NAME = 1
GOALIE_DB_TEAM_ID = 2
GOALIE_DB_GP = 3
GOALIE_DB_TOI = 4
GOALIE_DB_SA = 5
GOALIE_DB_SV = 6
GOALIE_DB_GA = 7
GOALIE_DB_SV_PCG = 8
GOALIE_DB_GAA = 9
GOALIE_DB_GSAA = 10
GOALIE_DB_XGA = 11
GOALIE_DB_AVG_SHOT_DIST = 30
GOALIE_DB_AVG_GOAL_DIST = 31
GOALIE_DB_LENGTH = 32

'''
Team-DB from naturalstattrick.com
Columns:
0-10:  0,"Team","GP","TOI","W","L","OTL","ROW","Points","Point %","CF",
11-20: "CA","CF%","FF","FA","FF%","SF","SA","SF%","GF","GA",
21-30: "GF%","xGF","xGA","xGF%","SCF","SCA","SCF%","SCSF","SCSA","SCSF%",
31-40: "SCGF","SCGA","SCGF%","SCSH%","SCSV%","HDCF","HDCA","HDCF%","HDSF","HDSA",
41-50: "HDSF%","HDGF","HDGA","HDGF%","HDSH%","HDSV%","MDCF","MDCA","MDCF%","MDSF",
51-60: "MDSA","MDSF%","MDGF","MDGA","MDGF%","MDSH%","MDSV%","LDCF","LDCA","LDCF%",
61-70: "LDSF","LDSA","LDSF%","LDGF","LDGA","LDGF%","LDSH%","LDSV%","SH%","SV%",
71-80: "PDO"
'''
TEAM_DB_NAME_COL = 1
TEAM_DB_GP_COL = 2
TEAM_DB_TOI_COL = 3
TEAM_DB_W_COL = 4
TEAM_DB_L_COL = 5
TEAM_DB_OTL_COL = 6
TEAM_DB_ROW_COL = 7
TEAM_DB_P_COL = 8
TEAM_DB_P_PCG_COL = 9
TEAM_DB_CF_COL = 10
TEAM_DB_CA_COL = 11
TEAM_DB_CF_PCG_COL = 12
TEAM_DB_FF_COL = 13
TEAM_DB_FA_COL = 14
TEAM_DB_FF_PCG_COL = 15
TEAM_DB_SF_COL = 16
TEAM_DB_SA_COL = 17
TEAM_DB_SF_PCG_COL = 18
TEAM_DB_GF_COL = 19
TEAM_DB_GA_COL = 20
TEAM_DB_GF_PCG_COL = 21
TEAM_DB_xGF_COL = 22
TEAM_DB_xGA_COL = 23
TEAM_DB_xGF_PCG_COL = 24
TEAM_DB_SCF_COL = 25
TEAM_DB_SCA_COL = 26
TEAM_DB_SCF_PCG_COL = 27
TEAM_DB_HDCF_COL = 36
TEAM_DB_HDCA_COL = 37
TEAM_DB_HDCF_PCG_COL = 38
TEAM_DB_SV_PCG_COL = 70
TEAM_DB_PDO_COL = 71
TEAM_DB_LENGTH = 72
P_PCG_FACTOR = 0.25  # This sets how much/little the point% of the season should be weighted in to the rating.


if __name__ == '__main__':
    pass