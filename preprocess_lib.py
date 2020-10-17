from nltk.corpus import stopwords
from nltk import word_tokenize
import string

class PreProcess(object):
	def __init__(self):
		super(PreProcess, self).__init__()
		stoplist = set([]).union(set({',','`','!',';',"'s","``","''","the",'_','.','\'re',':'}))
		self.stop_words = set(stopwords.words('english'))
		self.punctuations = {}
		for i in stoplist:
			self.punctuations[i]=1

	def run_on(self, line):
		temp = line.split(' ')

		# merge continues same tags and convert to lower
		res = []
		flag=-1
		for index in range(len(temp)):
			if(temp[index]=='</PERSON>' and temp[index+1]=='<PERSON>' and index+1<len(temp)):
				flag=1
				continue
			if(temp[index]=='</LOCATION>' and temp[index+1]=='<LOCATION>' and index+1<len(temp)):
				flag=1
				continue
			if(temp[index]=='</ORGANIZATION>' and temp[index+1]=='<ORGANIZATION>' and index+1<len(temp)):
				flag=1
				continue
			if(flag==1):
				flag=-1
			else:
				res.append(temp[index].lower())
		
		# Joins the full name, organization or location to:
		# loc_new_york, org_abc_news, person_donald_trump
		res_1 = []
		index_1 = 0
		while(index_1<len(res)-2):
			if('<person>' in res[index_1]):
				index_2 = index_1
				while('</person>' not in res[index_2] and index_2<len(res)-1):
					index_2+=1
				res_1.append('person_'+'_'.join(res[index_1+1:index_2]))
				index_1=index_2
			elif ('<organization>' in res[index_1]):
				index_2 = index_1
				while('</organization>' not in res[index_2] and index_2<len(res)-1):
					index_2+=1
				res_1.append('org_'+'_'.join(res[index_1+1:index_2]))
				index_1=index_2
			elif ('<location>' in res[index_1]):
				index_2 = index_1
				while('</location>' not in res[index_2] and index_2<len(res)-1):
					index_2+=1
				res_1.append('loc_'+'_'.join(res[index_1+1:index_2]))
				index_1=index_2
			else:
				if(res[index_1] not in self.punctuations and res[index_1].isdigit()==False):
					res_1.append(res[index_1])
			index_1+=1

		# Now I can safely use word_tokenize to remove joined punctuations
		temp = word_tokenize(' '.join(res_1))
		res_1 = []
		for i in (temp):
			# removing punctuations and stop_words
			if(i not in self.punctuations and i not in self.stop_words):
				res_1.append(i)

		# Removing all punctuations now
		return ' '.join(res_1)

if __name__=='__main__':
	obj = PreProcess()
	raw_text = "The ripples from the <LOCATION> Iowa </LOCATION> precinct caucuses are spreading to <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION>, boosting winners and damaging losers in the final days before the nation's first primary, polls indicate. Vice President <PERSON> George </PERSON> <PERSON> Bush </PERSON>, who was slipping in <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION> even before his third-place <LOCATION> Iowa </LOCATION> finish, lost more ground in polls this week. Democratic third-place finisher <PERSON> Michael </PERSON> <PERSON> Dukakis </PERSON> also lost support, but not as much. <LOCATION> Iowa </LOCATION>, meanwhile, has boosted the candidacies of Rep. <PERSON> Richard </PERSON> <PERSON> Gephardt </PERSON> of <LOCATION> Missouri </LOCATION> and Sen. <PERSON> Bob </PERSON> <PERSON> Dole </PERSON> of <LOCATION> Kansas </LOCATION>, the Democratic and <ORGANIZATION> Republican </ORGANIZATION> winners, and has aided <PERSON> Pat </PERSON> <PERSON> Robertson </PERSON>, <LOCATION> Iowa </LOCATION>'s surprise second-place <ORGANIZATION> Republican </ORGANIZATION> finisher, the polls indicate As recently as two weeks ago, <PERSON> Bush </PERSON> commanded the <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION> GOP field. A <ORGANIZATION> CBS </ORGANIZATION> <ORGANIZATION> News-New </ORGANIZATION> <ORGANIZATION> York </ORGANIZATION> <ORGANIZATION> Times </ORGANIZATION> poll in the last week of January had him 22 percentage points over <PERSON> Dole </PERSON>, the same place he'd held in polls since November and earlier But a crack appeared last week, when an <ORGANIZATION> ABC </ORGANIZATION> <ORGANIZATION> News-Washington </ORGANIZATION> <ORGANIZATION> Post </ORGANIZATION> poll found <PERSON> Bush </PERSON>'s lead sharply diminished, to 7 percentage points. After <LOCATION> Iowa </LOCATION>'s vote Monday, <ORGANIZATION> ABC </ORGANIZATION> found the spread down to 4 percentage points: <PERSON> Bush </PERSON>, 33, <PERSON> Dole </PERSON>, 29. In a poll with an error margin of 6 percentage points, that amounted to a dead heat. Another survey, done for <ORGANIZATION> The </ORGANIZATION> <ORGANIZATION> Boston </ORGANIZATION> <ORGANIZATION> Globe </ORGANIZATION> this week by pollster <PERSON> Gary </PERSON> <PERSON> Orren </PERSON>, had essentially he same result: <PERSON> Bush </PERSON> 29, <PERSON> Dole </PERSON> 27. <ORGANIZATION> CBS </ORGANIZATION> on Thursday had it as <PERSON> Bush </PERSON> 35, <PERSON> Dole </PERSON> 27 _ still a big drop for the vice president. `` <PERSON> Dole </PERSON> got a very big kick out of <LOCATION> Iowa </LOCATION>; more than that, there is some reluctance in the support for <PERSON> Bush </PERSON>,'' <PERSON> Orren </PERSON> said Thursday. `` He's shown vulnerability, and that's sort of arousing doubts people have about him.'' `` The unanswered question is how far <PERSON> Bush </PERSON> will fall,'' <PERSON> Richard </PERSON> <PERSON> Morin </PERSON>, polling director for <ORGANIZATION> The </ORGANIZATION> <ORGANIZATION> Washington </ORGANIZATION> <ORGANIZATION> Post </ORGANIZATION>. `` The expectation is that he will continue to drop. That's been the clear direction.'' If voters were leaving <PERSON> Bush </PERSON> before <LOCATION> Iowa </LOCATION>, it was not clear where they were going, <PERSON> Morin </PERSON> said. This week the chief gainers turned out to be <PERSON> Dole </PERSON> and <PERSON> Robertson </PERSON>, whose support was up to 10 percent in the <ORGANIZATION> ABC </ORGANIZATION> and CBS polls, from 6 percent last week and 4 percent two weeks ago. Rep. <PERSON> Jack </PERSON> <PERSON> Kemp </PERSON> of <LOCATION> New </LOCATION> <LOCATION> York </LOCATION> held steady at 13 percent in the <ORGANIZATION> ABC </ORGANIZATION> poll, and fell from 16 percent to 12 percent in the <ORGANIZATION> CBS </ORGANIZATION> poll. Analysts said he now may be challenged by <PERSON> Robertson </PERSON> for third place in <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION>. `` <PERSON> Kemp </PERSON> was gaining last week. <LOCATION> Iowa </LOCATION> ended that,'' said <PERSON> Morin </PERSON>. <LOCATION> Iowa </LOCATION>'s effect on the Democratic race probably is in the battle for second place, not first, pollsters said. <LOCATION> Massachusetts </LOCATION> Gov. <PERSON> Dukakis </PERSON>, despite finishing third in <LOCATION> Iowa </LOCATION>, maintained a strong lead in <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION> _ but he no longer had the huge 49 percent support indicated in an <ORGANIZATION> NBC-Wall </ORGANIZATION> <ORGANIZATION> Street </ORGANIZATION> <ORGANIZATION> Journal </ORGANIZATION> poll in November. Three polls indicated a drop in support for <PERSON> Dukakis </PERSON>, to 36 percent in the <ORGANIZATION> ABC-Post </ORGANIZATION> survey this week from 41 percent last week; to 35 percent in the <ORGANIZATION> Globe </ORGANIZATION>'s survey, from 38 percent last week; and to 38 percent in the <ORGANIZATION> CBS </ORGANIZATION> poll, from 40 percent in late January. A fourth new poll, however _ done for <ORGANIZATION> WBZ-TV </ORGANIZATION> in <LOCATION> Boston </LOCATION>, <ORGANIZATION> WRC-TV </ORGANIZATION> in <LOCATION> Washington </LOCATION> and the <ORGANIZATION> Boston </ORGANIZATION> <ORGANIZATION> Herald </ORGANIZATION> _ said <PERSON> Dukakis </PERSON>' support had risen from 36 percent at the end of January to 44 percent this week. `` It's a big lead for <PERSON> Dukakis </PERSON> no matter whose poll you're looking at _ and a strong one, too,'' said <PERSON> Jeff </PERSON> <PERSON> Alderman </PERSON>, chief of polling for <ORGANIZATION> ABC </ORGANIZATION> <ORGANIZATION> News </ORGANIZATION> He said 58 percent of <PERSON> Dukakis </PERSON>' backers told <ORGANIZATION> ABC </ORGANIZATION> they supported him strongly. The win in <LOCATION> Iowa </LOCATION> transformed <PERSON> Gephardt </PERSON>, who had single-digit support in <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION> as recently as last month. The <ORGANIZATION> CBS </ORGANIZATION> poll had him at 19 percent, up from 7 percent in late January; <ORGANIZATION> ABC </ORGANIZATION>'s poll put him this week at 22 percent, up from 13 percent last week The Globe had him at 18 percent, up from 8, and the <ORGANIZATION> WBZ </ORGANIZATION> poll had him at 17, up from 8 last month. Poll results were more mixed on <PERSON> Gephardt </PERSON>'s chief rival, Sen. <PERSON> Paul </PERSON> <PERSON> Simon </PERSON> of <LOCATION> Illinois </LOCATION>, the second-place finisher in <LOCATION> Iowa </LOCATION>. He moved to 18 percent from 13 percent in <ORGANIZATION> ABC </ORGANIZATION>'s poll, to 13 from 11 in <ORGANIZATION> WBZ </ORGANIZATION>'s and fell in the <ORGANIZATION> Globe </ORGANIZATION>'s, to 12 from 17 He held about even in the <ORGANIZATION> CBS </ORGANIZATION> poll, at 15 percent this week. Movement is taking place at the bottom as well as the top of the pack. Former Sen. <PERSON> Gary </PERSON> <PERSON> Hart </PERSON> of <LOCATION> Colorado </LOCATION>, who had 11 percent in the <ORGANIZATION> WBZ </ORGANIZATION> and <ORGANIZATION> Globe </ORGANIZATION> polls last week, fell to single-digit support after winning just 1 percent in <LOCATION> Iowa </LOCATION>. <PERSON> Hart </PERSON> and former <LOCATION> Arizona </LOCATION> Gov. <PERSON> Bruce </PERSON> <PERSON> Babbitt </PERSON>, also a poor finisher in <LOCATION> Iowa </LOCATION>, went from 7 percent in <ORGANIZATION> ABC </ORGANIZATION>'s <LOCATION> New </LOCATION> <LOCATION> Hampshire </LOCATION> poll last week to 4 percent this week"
	refined_text = obj.run_on(raw_text)
	print(refined_text)
