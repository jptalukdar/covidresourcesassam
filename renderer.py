import yaml
from jinja2 import Template
import time

import pytz
from datetime import datetime

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
        
    def generateCards(self):
        data = self.loadYaml(self.config.get('resources'))
        cardtemplate = Template(self.readfile('template/card.j2'))
        
        renders = []
        for card in data:
            colours = {
                'website' : 'purple',
                'person' : 'green'
            }
            renders.append(cardtemplate.render(
                title=card.get('name'),
                description = card.get('description'),
                link= card.get('link','#'),
                colour = colours.get(card.get('type'),'blue')
            ))
        
        renderString = '\n'.join(renders)

        pageTemplate = Template(self.readfile('template/index.j2'))
        pageTemplateString = pageTemplate.render(CARDS=renderString,date=self.getCurrentTime())

        self.writeFile('public/index.html',pageTemplateString)


if __name__ == '__main__':
    card = Cards()