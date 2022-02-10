from keybert import KeyBERT
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import itertools
import re

df = pd.read_csv("fengineering.csv", header=0, index_col=None, sep=',')
del df['Unnamed: 0']

# default stopwords
stop_words = nltk.corpus.stopwords.words('english')
docs = []
# creating document from the series of articles(text)
for i in df['lemma_punc']:
    text = word_tokenize(str(i))
    sentence = []
    for words in text:
        if words not in stop_words:
            sentence.append(words)
    intern = ' '.join(sentence)
    docs.append(intern)

texts = []
# removing ’ from the text
for i in df['lemma_punc']:
    i = re.sub(r"[.’]", '', str(i))
    text = word_tokenize(str(i))
    texts.append(text)

# word counter in document
cnts = list(itertools.chain(*texts))
a = Counter(cnts)
print(cnts)

cnt = pd.DataFrame.from_dict(a, orient='index').reset_index()
cnt.rename(columns={'index': 'words', 0: 'counts'}, inplace=True)

# custom common stop words found during the process
new_stopwords = ["read", "dec", "family", "adventure", "new", "year", "wednesday", "monday", "fun", "run", "review",
                 "van", "hit", "find", "long", "plenty", "micheal", "birthday", "upcoming", "staff", "opportunity",
                 "british", "ute", "melissa", "car", "husband", "teacher", "city", "hope", "house", "thank", "you",
                 "zealand", "past", "leave", "local", "group", "right", "month", "update", "allow", "like", "ltd",
                 "december", "help", "hard", "soon", "share", "focus", "night", "award", "difference", "partner", "sun"
    , "day", "window", "winner", "town", "buy", "te", "acre","operation","naturesweet","eosda","agristakeholder",
                 "dehaat","thatoffer","fullstack","standardizes","epik","garuda","aerospace","adjacent","lighting",
                 "cloudbase","manual","solution","profound","digitize","israeli","spraying","mexico","experimentation",
                 "optimize","rethink","largescale","immediately","singapore","data","agtech","profitability","venture",
                 "center","technology","advanced","globally","farmland","joint","partnership","insight","trial",
                 "meister","crisis","platform","startup","expand","limit","online","introduce","productivity",
                 "grower","popular","worldwide","force","experience","farmer","region","tool","service",
                 "decision","build","science","condition","currently","digital","research","datum","benefit",
                 "start","media","cost","approach","environmental","india","current","set","add","market","provide",
                 "field","industry","farm","agricultural","crop","high","use","agriculture","rajasthan","page","team",
                 "agribusiness","yield","plant","ag","agro","farm","farmer","farmers","kumar","indiana","pradesh",
                 "produce","app","average","barn","farming","haryana","karnataka","tax","taxes","ministry","chattisgarh"
                 , "covid", "coronavirus", "pandemic", "flood","flooding","crisis","forecast","cup","eu", "farmland",
                 "agtech","agronomic","agricultural","agriculture", "packaging", "consumer", "labelling", "label","meat",
                 "company","production", "ingredient", "bakery", "euractiv", "poultry", "beverage", "beef", "champagne",
                 "starbucks", "ice", "foodmanufacture", "manufacturer", "foodstuff", "foodmanjobs", "milk" ,
                 "manufacturing", "regulation", "li", "toshiba", "lid", "rice", "balsamic" , "alcohol", "basmati"
                 ,"euipo", "cama", "foods", "revenue", "manufacture", "pig", "livestock", "fuller", "coffee", "pepsico",
                 "trends", "pharmaceutical", "africa", "tablet", "pulp", "bio", "jelly", "tobacco", "dpd", "hive",
                 "bosch", "agri", "factory", "kashmir", "sheep", "smoking", "pulp", "rasin", "olive", "pulpbased",
                 "wellness" , "pigging", "foodrelated" , "machinetomachine", "beekeeper", "freezer", "butcher",
                 "bakerytype" , "belgian", "transport", "agrifood", "climate", "sustainable" , "address", "soil",
                 "parliament", "cattle", "efsa","rural", "wheat", "amendment", "safety", "stakeholder", "management",
                 "legislation", "request", "researcher", "soybean", "germany", "irish", "regulatory", "ireland", "virus",
                 "funding" ,"fertiliser", "kauffman", "diet", "bayer", "reserve", "copacogeca", "iowa" , "grain",
                 "trend", "chicken", "conservative", "flower", "ethanol", "buffett", "fruit", "bee", "shortage", "pipe",
                 "legislative", "insect", "vegetable", "vegetarian", "veterinary", "river", "ecosystem", "oat",
                 "nutrition", "peat", "fish", "animals", "corn", "moy", "hong", "macron", "tuna", "macau", "bluefin",
                 "wool", "coalition", "leak", "influenza", "maize", "workforce", "supermarket", "hospital", "freeze",
                 "outbreak", "fuel", "transportation", "woolen", "metro", "planting", "mississippi", "barley", "gmfood"
                 ,"faribault", "oil", "policymaking", "fishing", "floodplain", "camp", "bumblebee", "inflation",
                 "neiffer", "recruitment", "oilseed", "prescriptiononly", "adelaide", "farmtofork", "plumber",
                 "fisheries", "minnesota", "staffing", "animaltransport", "barge", "crisislevel", "plumbing",
                 "farmersufcommunitiesufand", "nurse", "bovine", "agriculturerelated", "antrim", "foodlabelling",
                 "nutritiondeficient", "soyoil", "efsax", "policies", "oatup", "honeybee", "harvesting", "beesfrontier",
                 "graincorp", "coronaviruse", "eco", "starvation", "markets","nz", "health" , "dairy","nz","health",
                 "grow","water","sector","dose","tauranga","increase","police","council","environment", "crane",
                 "healthy","surf","port","challenge","event","programme","road","waikato","tree","plan","friday","grass"
    ,"sunlive","demand","vaccine","supply","crawler","christmas","export","saturday","turf","publication","booster","cow"
    ,"forestry","sunday","south","forest","competition","island","auckland","street","global","minister","feed","highway"
    ,"rd","testing","globalhq","thursday","northland","catchment","encourage","canterbury","fonterra","rain","lamb",
                 "weather","protest","groundswell","officer","katikati","wine","shane","nov","emergency","disease",
                 "training","news","pine","hawke","squash","caterpillar","yearold","holiday","shearin","herd","tamariki"
    ,"māori","southland","vaccination","zealanders	","otago","traffic","milking","ride","labour","facility","councillor"
    ,"waste","nature","tractor","employment","cybersecurity","shear","wellington","deer","capital","mackay","security",
                 "tournament","waka","maori","luxon","honey","manuka","workshop","vaccinate","ballance","christchurch",
                 "train","harbour","hemp","arrest","racecourse","rainfall","mayor","participate","plough","supplier",
                 "landowner","dairynz","teach","bulletin","paulin","landcare","epa","investigation","restoration",
                 "rangatahi","pump","weekend","kaimaumau","pacific	","hop","investor","horse","wetland","cyberattack",
                 "forester","kawerau","goosman","gap","cherry","boat","whanau","innovation","mandate","shareholder",
                 "bank","mānuka","fagan","drought","trap","explore","vaccinated","machinery","parkvale","cooperative",
                 "hurrell","laurie","garden","moth	","snow","kiwifruit","income","conference","kotahi	","ship",
                 "proposal","freight","stan","cycling","bovis","estate","golden","quarantine","firefighter",
                 "henderson","fiordland","helicopter","freshwater","auction","tg","consultation","nectar","shearer"
    ,"norwood","cougar","lifestyle","rust","symptom","seedling","breeder","murray","shears","altercation",
                 "ticket","tongariro","debris","housing","halal","whānau","injury","whakapapa","guide","woolhandling",
                 "myrtle","habitat","grandfather","commodity","alliance","disability","charitable","founder","earning",
                 "katuku","expert","kāpiti","relocation","myfarm","mentor","nation","waikirikir","thistle","ebike",
                 "cook","sunflower","neil","scenic","ploughing","creek","valencia","wellbee","pāpāmoa","selenium",
                 "hikurangi","indigenous","seasonal","campus","exporter","eradication","farms","elworthy","puro",
                 "euthanasia","dunedin","emissions","turbine","retailer","waters","kgms","harbourmaster","piripaua",
                 "berry","beatson","heifer","politician","bat","warming","beer","conifer","healthcare","ambulance",
                 "ipca","wilde","mortgage","envy","cyclone","fern","wharf","cetacean","waimata","runoff","waiouru",
                 "badcock","strawberry","grape","meal","slater","carcase","gardening","makaroro","unvaccinated",
                 "karapeeva","pond","participation","cop","bark","firebreak	","kuraawao","arborgen","provision",
                 "winegrowers","blaze","roading","napier","classroom","ātihauwhanganui","storm","catchmentscale",
                 "coastal","coop","bubble","fishery","craft","coal","sheepmeat","nzme","vineyard","uawa","amlaku",
                 "waikaka","cancer","waioeka","cultivation","georgia","contest","evacuate","running","nzx",
                 "restructuring",
                 "restructure","brewing","matawai","wynne","woolhandler","hutchings","butchery","tasman","pony",
                 "generator","grazing","rent","rubyred","arkwright","chairman","federation","bottlebrush","ruminant",
                 "mattress","paperwork","protests","gardener","festival","kate","kanakanaia","brewery","nzta",
                 "thamescoromandel","chemicals","commercialisation","annum","squashplaye","banking","beehive",
                 "coastguard","desmond","berth","toxicity","deficiency","seagrass","whale","cemetery","caterpillars",
                 "cyclist","cricket","waipuka	","cherries","burial","sgx","ashburton","pfi","pollution","tokoroa",
                 "mvm","wills","whanganui","fiona","triallist","speedway","ripen","xylella","shorttaile","tribe",
                 "wools","jan","winery","whinray","dunedinbase	","evacuation","reindeer","wakatipu","beekeeping",
                 "vicki","townhouse",
                 "halalcertifie","tapanui","summerfruit","lambing	","hereford","longtaile","farmhouse","waimumu",
                 "wines","flora","feedlot","forestation","floor","amhara","tribal","pipfruit","hunger","ethiopia",
                 "chef","larvae","mataura","seedle","predeparture","orcharding","susanne","plowman","postcovid",
                 "foodservice","snowfall","lactose","fireseason","funeral","fjord","plougher","indies","farmright",
                 "keats","zealandwide","mentorship","whaling","marshalling","seafarers","loved","ministers","trout",
                 "nzgsta","mowers","waiamarama","enviroschool","cairns","waikaretaheke","mealsmrs","merritt",
                 "woolweigh","icc","kaiwaka","fertilisers","wheatgrowers","keat","wnzbranded","hops","broker",
                 "biotech","dietary","unemployed","woolhandle","deforestation","ethiopian","meateate","agrifoodtech",
                 "sprout","woollen"]

# extending the stop word list with custom list
stop_words.extend(new_stopwords)
# initialising kbert for topic modelling
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(docs)
tfidf = []

# creating tdidf scores for the generated words
for i in keywords:
    print(i)
    y = [ele[0] for ele in i if ele[0] not in stop_words]
    mid = ' '.join(y)
    tfidf.append(mid)

tfIdfVectorizer = TfidfVectorizer(use_idf=True)
tfIdf = tfIdfVectorizer.fit_transform(tfidf)
df1 = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
df1 = df1.sort_values('TF-IDF', ascending=False)
df1['words'] = df1.index
df1.reset_index(drop=True, inplace=True)
print(df1)
print(cnt)


date_list = []
words_list = []

# finding all the occurence date for the keywords
for i in range(len(df)):
    tokens = word_tokenize(str(df.iloc[i]['lemma_punc']))
    date_list.append(df.iloc[i]['date'])
    words_list.append(tokens)
new_df = pd.DataFrame(list(zip(date_list, words_list)),columns=['date', 'words'])
print(new_df)
new_dict = dict(new_df.values)

sent_list = []
words_list = []

# finding all the sentiment scores for the keywords
for i in range(len(df)):
    tokens = word_tokenize(str(df.iloc[i]['lemma_punc']))
    sent_list.append(df.iloc[i]['positive_score'])
    words_list.append(tokens)
sent_df = pd.DataFrame(list(zip(sent_list, words_list)),columns=['positive_score', 'words'])
sent_dict = dict(sent_df.values)

# merging the new tdidf dataframe with the keywords
merge = pd.merge(df1, cnt, how="inner", on="words")
dates_list = []
for i in merge['words']:
    dates = []
    dates = [k for k,v in new_dict.items() if i in v]
    print(dates)
    dates_list.append(dates)

sent_list = []
for i in merge['words']:
    sents = []
    sents = [k for k,v in sent_dict.items() if i in v]
    print(sents)
    sent_list.append(sents)

# new columns for occurence and sentiment scores
merge['occurance'] = dates_list
merge['postive_sentiment'] = sent_list

# writing csv file
merge.to_csv('merge.csv', encoding='utf-8', header=True, sep=',')
print('csv file successfully generated')
