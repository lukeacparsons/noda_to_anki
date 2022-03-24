import csv
import random

fields = ['Uuid','Title','ImageURL','FromUuid','ToUuid']
fields_mapped = {}


class NodaItem:
    def __init__(self):
        self._uuid = None
        self._title = None 
        self._image_url = None 
        self._from_uuid = None 
        self._to_uuid = None 
        self._child_nodes = [] 

    def setUUID(self, uuid):
        self._uuid = uuid

    def setTitle(self, title):
        self._title = title

    def setImageUrl(self, image_url):
        self._image_url = image_url

    def setFromUUID(self, from_uuid):
        self._from_uuid = from_uuid

    def setToUUID(self, to_uuid):
        self._to_uuid = to_uuid

    def getUUID(self):
        return self._uuid 

    def getTitle(self):
        return self._title 

    def getImageUrl(self):
        return self._image_url

    def getFromUUID(self):
        return self._from_uuid

    def getToUUID(self):
        return self._to_uuid 

    def getChildNodes(self):
        return self._child_nodes

    def addChildNode(self, NodaItem):
        if NodaItem.getFromUUID() == self.getUUID():
            self._child_nodes.append(NodaItem.getToUUID())


class AnkiItem:
    def __init__(self):
        self._title = None
        self._image_urls = []
        self._front_html = ''
        self._back_html = ''

    def getTitle(self): 
        return self._title

    def setTitle(self, title): 
        self._title = title
        self.buildFrontHTML()

    def getImageURLS(self):
        return self._image_urls

    def addImageURL(self, image_url): 
        self._image_urls.append(image_url) 
        self.buildBackHTML()

    def getFrontHTML(self):
        return self.front_html

    def buildFrontHTML(self):
        self.front_html = '<html>'+self.getTitle()+"</html>"

    def getBackHTML(self):
        return self.back_html

    def buildBackHTML(self):
        self.back_html = '<html>'
        for img_url in self.getImageURLS():
            self.back_html += '<img src='+img_url+'></img><br>'
        self.back_html += '</html>'

    def printCard(self):
        return self.getFrontHTML() + ',' + self.getBackHTML()

    def printReverseCard(self):
        return self.getBackHTML() + ',' + self.getFrontHTML()



def getNodeByUUID(uuid, nodaItems):
    for node in nodaItems:
        if node.getUUID() == uuid:
            return node
        else:
            pass


# Parse the Noda Export File and Create the NodaItems
nodaItems = []
with open('noda_export.csv', 'r') as noda_file:
    reader = csv.reader(noda_file)
    for idx, row in enumerate(reader):
        if idx == 0:
            for field in fields:
                fields_mapped[field] = row.index(field)
        else:
            nodaItem = NodaItem()
            for field in fields_mapped:
                #print(row[fields_mapped.get(field)])
                if field == 'Uuid':
                    try: nodaItem.setUUID(row[fields_mapped.get(field)])
                    except: pass
                if field == 'Title':
                    try: nodaItem.setTitle(row[fields_mapped.get(field)])
                    except: pass
                if field == 'ImageURL':
                    try: nodaItem.setImageUrl(row[fields_mapped.get(field)])
                    except: pass
                if field == 'FromUuid':
                    try: nodaItem.setFromUUID(row[fields_mapped.get(field)])
                    except: pass
                if field == 'ToUuid':
                    try: nodaItem.setToUUID(row[fields_mapped.get(field)])
                    except: pass
            nodaItems.append(nodaItem) 


# Add the NodaItem Child Nodes
for node_to_add_child in nodaItems:
    for node_to_check_child in nodaItems:
        node_to_add_child.addChildNode(node_to_check_child)


# Create the AnkiItems
ankiItems = []
for node in nodaItems:
    if node.getTitle() != '' and len(node.getChildNodes()) != 0:
        ankiItem = AnkiItem()
        ankiItem.setTitle(node.getTitle())
        for child_node_uuid in node.getChildNodes():
            child_node = getNodeByUUID(child_node_uuid, nodaItems)
            ankiItem.addImageURL(child_node.getImageUrl())
        ankiItems.append(ankiItem)


# Print the Anki Items to a File
outputfilename = "noda_anki_deck.csv"
out = open(outputfilename, "w")
for ankiItem in ankiItems:
    out.write(ankiItem.printCard()+"\n")
    out.write(ankiItem.printReverseCard()+"\n")
out.close()


# Shuffle the Cards in the File
lines = open(outputfilename).readlines()
random.shuffle(lines)
open(outputfilename, 'w').writelines(lines)
