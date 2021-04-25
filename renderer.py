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
    
    def renderTemplate(self,template, cards, output):
        commit = self.getCurrentCommit()
        footer = Template(self.readfile('template/footer.j2'))
        footerString = footer.render(
            date=self.getCurrentTime(),
            commit=commit,
            shortcommit = self.getCurrentShortCommit()
        )
        pageTemplateString = template.render(
            CARDS=cards,
            footer = footerString
            )
        self.writeFile(output,pageTemplateString)
        
    def generateCards(self):
        data = self.loadYaml(self.config.get('resources'))
        data = data[::-1] ## Reverse the list
        cardtemplate = Template(self.readfile('template/card.j2'))
        collectiontemplate = Template(self.readfile('template/collection.j2'))

        renders = []
        renderTags={}
        colours = {
                'website' : 'purple',
                'person' : 'green',
                'organization' : 'blue' 
            }
        for card in data:
            
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

            __render = cardtemplate.render(
                title=card.get('name'),
                description = description,
                links= links,
                colour = colours.get(card.get('type'),'blue')
            )
            renders.append(__render)
            tags = card.get('tags','').split(',')
            for tag in tags:
                tag = tag.lower().strip().replace('\n','')
                if tag == '' or tag == None:
                    continue
                if tag not in renderTags:
                    renderTags[tag] = []
                renderTags[tag].append(__render)
        
        
        
        pageTemplate = Template(self.readfile('template/tags.j2'))

        collections = [
            { 'link' : '{}.html'.format(tag) ,
               'linktext' : tag.title().strip()
                }
            for tag in renderTags
        ]
        print(collections)
        renderString = collectiontemplate.render(links=collections,colour='blue')
        self.renderTemplate(pageTemplate,renderString,'public/index.html')
        for tag in renderTags:
            self.renderTemplate(pageTemplate,
                '\n'.join(renderTags[tag]),
                'public/{}.html'.format(tag)
                )
        


if __name__ == '__main__':
    card = Cards()