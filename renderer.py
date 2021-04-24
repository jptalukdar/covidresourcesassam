import yaml
from jinja2 import Template
import time
import subprocess
import pytz
from datetime import datetime
import requests
import json
class Cards():
    def __init__(self):
        self.config()
        self.generateCards()
    def loadYaml(self, path):
        with open(path,'r') as fp:
            data = yaml.safe_load(fp)
        return data

    def config(self):
        self.config = {
            'resources' : 'resources/resource-list.yml',
            'timezone' : 'Asia/Kolkata'
        }
    def readfile(self,filename):
        with open(filename,'r') as fp:
            data = fp.read()
        return data
    def getCurrentTime(self):
        tz = pytz.timezone(self.config.get('timezone'))

        return str(datetime.now(tz=tz).strftime('%m/%d/%Y, %H:%M:%S %Z'))

    def writeFile(self,filename,data):
        with open(filename,'w') as fp:
            fp.write(data)
    
    def getCurrentCommit(self):
        return str(subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8')).strip().replace('\n','')
    def getCurrentShortCommit(self):
        return str(subprocess.check_output(['git', 'rev-parse', '--short' ,'HEAD']).decode('utf-8')).strip().replace('\n','')
    def getTwitterCard(self,twitterurl):
        try:
            url = "https://publish.twitter.com/oembed?url={}".format(twitterurl)
            response = requests.get(url)
            data = json.loads(response.text)
            return data['html']
        except Exception:
            return ''
    def generateCards(self):
        data = self.loadYaml(self.config.get('resources'))
        data = data[::-1] ## Reverse the list
        cardtemplate = Template(self.readfile('template/card.j2'))
        
        renders = []
        for card in data:
            colours = {
                'website' : 'purple',
                'person' : 'green',
                'organization' : 'blue' 
            }
            link = '#'
            links = []
            if card.get('link') != None:
                links.append({
                    'link' : card.get('link')
                })
            if card.get('phone') != None:
                links.append({
                    'link' : 'tel:{}'.format(card.get('phone')),
                    'linktext' : 'Call'
                })
            if card.get('mail') != None:
                links.append({
                    'link' : 'mailto:{}'.format(card.get('mail')),
                    'linktext' : 'Mail'
                }) 
            description = card.get('description')
            if card.get('type') == 'twitter':
                description = description + '\n' + self.getTwitterCard(card.get('link'))
            renders.append(cardtemplate.render(
                title=card.get('name'),
                description = description,
                links= links,
                colour = colours.get(card.get('type'),'blue')
            ))
        
        renderString = '\n'.join(renders)

        pageTemplate = Template(self.readfile('template/index.j2'))
        commit = self.getCurrentCommit()
        pageTemplateString = pageTemplate.render(
            CARDS=renderString,
            date=self.getCurrentTime(),
            commit=commit,
            shortcommit = self.getCurrentShortCommit()
            )
        self.writeFile('public/index.html',pageTemplateString)


if __name__ == '__main__':
    card = Cards()