# Libraries Included:
from rdflib import Graph, URIRef, BNode, Literal, XSD, Namespace, RDF, RDFS
import json
import datetime
import string
import jsonlines
import time
from datetime import datetime


class GameKG:
    def __init__(self):
        self.my_kg = Graph()

    def define_namespaces(self):
        # Namespaces:
        self.FOAF = Namespace('http://xmlns.com/foaf/0.1/')
        self.MGNS = Namespace('http://inf558.org/games#')
        self.SCHEMA = Namespace('http://schema.org/')

        self.my_kg.bind('mgns', self.MGNS)
        self.my_kg.bind('foaf', self.FOAF)
        self.my_kg.bind('schema', self.SCHEMA)

    def define_classes(self):
        ## Enterpise Class ##
        self.enterprise_global = URIRef(self.MGNS['Enterprise'])
        self.my_kg.add((self.enterprise_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.enterprise_global, RDFS.subClassOf, self.SCHEMA["Organisation"]))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.enterprise_global, self.MGNS['ratingValue'], XSD.decimal))
        self.my_kg.add((self.enterprise_global, self.MGNS['ratingCount'], XSD.integer))
        self.my_kg.add((self.enterprise_global, self.MGNS['bestRating'], XSD.decimal))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['logo'], self.SCHEMA['URL']))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['url'], self.SCHEMA['URL']))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['foundingDate'], XSD.date))
        self.my_kg.add((self.enterprise_global, self.SCHEMA['foundingLocation'], self.SCHEMA['Place']))

        ## Seller Class ##
        self.seller_global = URIRef(self.MGNS['Seller'])
        self.my_kg.add((self.seller_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.seller_global, RDFS.subClassOf, self.SCHEMA["seller"]))
        self.my_kg.add((self.seller_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.seller_global, self.MGNS['ratingValue'], XSD.decimal))
        self.my_kg.add((self.seller_global, self.MGNS['bestRating'], XSD.decimal))

        ## Platform Class ##
        self.platform_global = URIRef(self.MGNS['Platform'])
        self.my_kg.add((self.platform_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.platform_global, self.MGNS['platformName'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['platformType'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['operatingSystem'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['memory'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['cpu'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['storage'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.MGNS['supportedResolution'], self.SCHEMA['Text']))
        self.my_kg.add((self.platform_global, self.SCHEMA['url'], self.SCHEMA['URL']))

        ## Processor Class ##
        self.processor_global = URIRef(self.MGNS["Processor"])
        self.my_kg.add((self.processor_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.processor_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['numCore1'], XSD.integer))
        self.my_kg.add((self.processor_global, self.MGNS['numCore2'], XSD.integer))
        self.my_kg.add((self.processor_global, self.MGNS['lowerClockSpeedghz'], XSD.decimal))
        self.my_kg.add((self.processor_global, self.MGNS['higherClockSpeedghz'], XSD.decimal))
        self.my_kg.add((self.processor_global, self.MGNS['l3CacheMB'], XSD.integer))
        self.my_kg.add((self.processor_global, self.MGNS['socket'], self.SCHEMA['Text']))
        self.my_kg.add((self.processor_global, self.MGNS['process_nm'], XSD.integer))
        self.my_kg.add((self.processor_global, self.MGNS['hasCPUMark'], XSD.decimal))

        ## Graphics Class ##
        self.graphics_global = URIRef(self.MGNS["Graphics"])
        self.my_kg.add((self.graphics_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.graphics_global, self.SCHEMA['name'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuChip'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['bus'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.SCHEMA['datePublished'], self.SCHEMA['date']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemorySize_MB'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemoryType'], self.SCHEMA['Text']))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuMemoryBits'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['gpuClockSpeed_MHz'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['memoryClockSpeed_MHz'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['shader_1'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['shader_2'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['TMUs'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.MGNS['ROPs'], XSD.integer))
        self.my_kg.add((self.graphics_global, self.SCHEMA['url'], self.SCHEMA['URL']))
        self.my_kg.add((self.graphics_global, self.MGNS['g3dMark'], XSD.integer))


        ## Minimum Supporting Device Class ##
        self.msd_global = URIRef(self.MGNS["MSD"])
        self.my_kg.add((self.msd_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.msd_global, self.MGNS['processor'], self.processor_global))
        self.my_kg.add((self.msd_global, self.MGNS['graphics'], self.graphics_global))
        self.my_kg.add((self.msd_global, self.MGNS['memory_MB'], self.SCHEMA['Text']))
        self.my_kg.add((self.msd_global, self.MGNS['diskSpace_MB'], self.SCHEMA['Text']))

        ### Additional Classes ###
        self.game_mode_global = URIRef(self.MGNS['GameMode'])
        self.my_kg.add((self.game_mode_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.game_mode_global, RDFS.label, Literal("Game Mode")))

        self.genre_global = URIRef(self.MGNS["Genre"])
        self.my_kg.add((self.genre_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.genre_global, RDFS.label, Literal("Genre")))

        self.theme_global = URIRef(self.MGNS["Theme"])
        self.my_kg.add((self.theme_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.theme_global, RDFS.label, Literal("Theme")))

        ## Game Class ##
        self.game_global = URIRef(self.MGNS["Game"])
        self.my_kg.add((self.game_global, RDF.type, RDFS.Class))
        self.my_kg.add((self.game_global, RDFS.subClassOf, self.SCHEMA["Game"]))
        self.my_kg.add((self.game_global, self.SCHEMA["name"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.SCHEMA["description"], self.SCHEMA["Text"]))
        self.my_kg.add((self.game_global, self.SCHEMA["url"], self.SCHEMA["URL"]))
        self.my_kg.add((self.game_global, self.SCHEMA["datePublished"], self.SCHEMA["date"]))
        self.my_kg.add((self.game_global, self.MGNS["supportedPlatform"], self.platform_global))
        self.my_kg.add((self.game_global, self.MGNS["hasMSD"], self.msd_global))
        self.my_kg.add((self.game_global, self.MGNS["developedBy"], self.enterprise_global))
        self.my_kg.add((self.game_global, self.MGNS["publishedBy"], self.enterprise_global))
        self.my_kg.add((self.game_global, self.MGNS["hasGameMode"], self.game_mode_global))
        self.my_kg.add((self.game_global, self.MGNS["hasGenre"], self.genre_global))
        self.my_kg.add((self.game_global, self.MGNS["hasTheme"], self.theme_global))
        self.my_kg.add((self.game_global, self.MGNS["ratingValue"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["ratingCount"], XSD.integer))
        self.my_kg.add((self.game_global, self.MGNS["bestRating"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["soldBy"], self.seller_global))
        self.my_kg.add((self.game_global, self.MGNS["price_USD"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["oldPrice_USD"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["discount_percent"], XSD.decimal))
        self.my_kg.add((self.game_global, self.MGNS["sellerFeedback"], XSD.integer))
        self.my_kg.add((self.game_global, self.MGNS["sellerUrl"], self.SCHEMA["Text"]))

    '''def define_properties(self):
        ## Properties ##
        self.supported_platform_global = URIRef(self.MGNS["supportedPlatform"])
        self.my_kg.add((self.supported_platform_global, RDF.type, RDF.Property))
        self.my_kg.add((self.supported_platform_global, RDFS.label, Literal("Supported Platform", lang="en")))
        self.my_kg.add((self.supported_platform_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.supported_platform_global, RDFS.range, self.MGNS['Platform']))

        self.msd_global = URIRef(self.MGNS["hasMSD"])
        self.my_kg.add((self.msd_global, RDF.type, RDF.Property))
        self.my_kg.add((self.msd_global, RDFS.label, Literal("Minimum Supporting Device", lang="en")))
        self.my_kg.add((self.msd_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.msd_global, RDFS.range, self.MGNS['MSD']))

        self.developed_by_global = URIRef(self.MGNS["developedBy"])
        self.my_kg.add((self.developed_by_global, RDF.type, RDF.Property))
        self.my_kg.add((self.developed_by_global, RDFS.label, Literal("Developed By", lang="en")))
        self.my_kg.add((self.developed_by_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.developed_by_global, RDFS.range, self.MGNS['Enterprise']))

        self.published_by_global = URIRef(self.MGNS["publishedBy"])
        self.my_kg.add((self.published_by_global, RDF.type, RDF.Property))
        self.my_kg.add((self.published_by_global, RDFS.label, Literal("Published By", lang="en")))
        self.my_kg.add((self.published_by_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.published_by_global, RDFS.range, self.MGNS['Enterprise']))

        self.has_game_mode_global = URIRef(self.MGNS["hasGameMode"])
        self.my_kg.add((self.has_game_mode_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_game_mode_global, RDFS.label, Literal("Has Game", lang="en")))
        self.my_kg.add((self.has_game_mode_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.has_game_mode_global, RDFS.range, self.MGNS['GameMode']))

        self.has_genre_global = URIRef(self.MGNS["hasGenre"])
        self.my_kg.add((self.has_genre_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_genre_global, RDFS.label, Literal("Has Genre", lang="en")))
        self.my_kg.add((self.has_genre_global, RDFS.domain, self.MGNS['Game']))
        self.my_kg.add((self.has_genre_global, RDFS.range, self.MGNS['Genre']))

        self.has_theme_global = URIRef(self.MGNS["hasTheme"])
        self.my_kg.add((self.has_theme_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_theme_global, RDFS.label, Literal("Has Theme", lang="en")))
        self.my_kg.add((self.has_theme_global, RDFS.domain, self.MGNS['Theme']))
        self.my_kg.add((self.has_theme_global, RDFS.range, self.MGNS['Genre']))

        self.has_theme_global = URIRef(self.MGNS["hasTheme"])
        self.my_kg.add((self.has_theme_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_theme_global, RDFS.label, Literal("Has Theme", lang="en")))
        self.my_kg.add((self.has_theme_global, RDFS.domain, self.MGNS['Theme']))
        self.my_kg.add((self.has_theme_global, RDFS.range, self.MGNS['Genre']))

        self.rating_value_global = URIRef(self.MGNS["ratingValue"])
        self.my_kg.add((self.has_theme_global, RDF.type, RDF.Property))
        self.my_kg.add((self.has_theme_global, RDFS.label, Literal("Rating Value", lang="en")))
        self.my_kg.add((self.has_theme_global, RDFS.domain, self.MGNS['Enterprise']))
        self.my_kg.add((self.has_theme_global, RDFS.range, XSD.integer))'''

    def define_ontology(self):
        self.define_classes()
        #self.define_properties()

    def storeKG(self, kg_file_name):
        self.my_kg.serialize(kg_file_name, format="turtle")

    def __convertSizeToMB(self, cur_size):
        cur_size = cur_size.lower()
        cur_val = ""
        for cur_char in cur_size:
            if cur_char.isdigit():
                cur_val += cur_char
            else:
                break

        cur_val = int(cur_val)
        cur_unit = cur_size

        if "kb" in cur_unit:
            cur_val /= 1024
        elif "gb" in cur_unit:
            cur_val *= 1024
        elif "tb" in cur_unit:
            cur_val *= (1024 * 1024)

        return cur_val

    def __generateShortURI(self, input_uri):
        cur_list = input_uri.split("_")
        short_uri = ""
        for cur_val in cur_list[:-1]:
            short_uri += cur_val[0]
        short_uri += "_" + cur_list[-1]
        return short_uri

    def __generateURIfromString(self, input_string):
        input_string = input_string.lower()
        for cur_punc in string.punctuation:
            input_string = input_string.replace(cur_punc, " ")
        cur_uri = "_".join(input_string.split())
        return cur_uri

    def addEnterpriseInstance(self, enterprise_instance):
        cur_uri = self.__generateShortURI(list(enterprise_instance.keys())[0])
        cur_uri = URIRef(self.MGNS[cur_uri])
        cur_val = list(enterprise_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.enterprise_global))
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val["company_name"], lang="en")))

        try:
            self.my_kg.add((cur_uri, self.MGNS['ratingValue'], Literal(float(cur_val["rating_value"]))))
        except:
            pass

        try:
            self.my_kg.add((cur_uri, self.MGNS['ratingCount'], Literal(int(cur_val["num_ratings"]))))
        except:
            pass

        try:
            self.my_kg.add((cur_uri, self.MGNS['bestRating'], Literal(float(cur_val["best_rating"]))))
        except:
            pass

        if len(cur_val["logo_url"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['logo'], Literal(cur_val["logo_url"], lang="en")))

        if len(cur_val["url"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['url'], Literal(cur_val["url"], lang="en")))

        if len(cur_val["founding_date"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['foundingDate'], Literal(cur_val["founding_date"], lang="en")))

        if len(cur_val["founding_country"]) != 0:
            self.my_kg.add((cur_uri, self.SCHEMA['foundingLocation'], Literal(cur_val["founding_country"], lang="en")))

    def addSellerInstance(self, seller_instance):
        cur_val = list(seller_instance.values())[0]
        try:
            cur_uri = URIRef(self.MGNS[self.__generateURIfromString(cur_val['seller_name'])])
            self.my_kg.add((cur_uri, RDF.type, self.seller_global))
            self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val['seller_name'], lang='en')))
            self.my_kg.add(
                (cur_uri, self.MGNS['ratingValue'], Literal(cur_val['seller_rating'][:-1], datatype=XSD.integer)))
            self.my_kg.add((cur_uri, self.MGNS['bestRating'], Literal(100, datatype=XSD.integer)))
        except:
            pass

    def addPlatformInstance(self, platform_instance):
        cur_uri = self.__generateShortURI(list(platform_instance.keys())[0])
        cur_uri = URIRef(self.MGNS[cur_uri])
        cur_val = list(platform_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.platform_global))
        self.my_kg.add((cur_uri, self.MGNS['platformName'], Literal(cur_val['platform_name'], lang="en")))

        try:
            if len(cur_val['PLATFORM TYPE:']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['platformType'], Literal(cur_val['PLATFORM TYPE:'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Operating System']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['operatingSystem'], Literal(cur_val['Operating System'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Memory']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['memory'], Literal(cur_val['Memory'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['CPU']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['CPU'], Literal(cur_val['CPU'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Storage']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['storage'], Literal(cur_val['Storage'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['Supported Resolutions']) != 0:
                self.my_kg.add(
                    (cur_uri, self.MGNS['supportedResolution'], Literal(cur_val['Supported Resolutions'], lang="en")))
        except:
            pass

    def addProcessorInstance(self, processor_instance):
        cur_uri = self.__generateShortURI(list(processor_instance.keys())[0])
        cur_uri = URIRef(self.MGNS[cur_uri])
        cur_val = list(processor_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.processor_global))
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val["name"], lang="en")))

        try:
            if cur_val['core_1'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['numCore1'], Literal(cur_val['core_1'], datatype=XSD.integer)))
        except:
            pass

        try:
            if cur_val['core_2'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['numCore2'], Literal(cur_val['core_2'], datatype=XSD.integer)))
        except:
            pass

        try:
            if cur_val['lower_clock_speed_ghz'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['lowerClockSpeedghz'],
                                Literal(cur_val['lower_clock_speed_ghz'], datatype=XSD.decimal)))
        except:
            pass

        try:
            if cur_val['higher_clock_speed_ghz'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['higherClockSpeedghz'],
                                Literal(cur_val['higher_clock_speed_ghz'], datatype=XSD.decimal)))
        except:
            pass

        try:
            if cur_val(['l3_cache']) != -1:
                self.my_kg.add((cur_uri, self.MGNS['l3CacheMB'], Literal(cur_val['l3_cache'], datatype=XSD.integer)))
        except:
            pass

        try:
            if len(cur_val['Socket']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['socket'], Literal(cur_val['Socket'], lang="en")))
        except:
            pass

        try:
            if cur_val['process'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['process_nm'], Literal(cur_val['process'], datatype=XSD.integer)))
        except:
            pass

        try:
            self.my_kg.add((cur_uri, self.MGNS['hasCPUMark'], Literal(cur_val['cpu_mark'], datatype = XSD.decimal)))
        except:
            pass

    def addGraphicsInstance(self, graphics_instance):
        cur_uri = self.__generateShortURI(list(graphics_instance.keys())[0])
        cur_uri = URIRef(self.MGNS[cur_uri])
        cur_val = list(graphics_instance.values())[0]
        self.my_kg.add((cur_uri, RDF.type, self.graphics_global))
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(cur_val["product_name"], lang="en")))
        self.my_kg.add((cur_uri, self.SCHEMA['url'], Literal(cur_val["product_url"], lang="en")))
        self.my_kg.add((cur_uri, self.MGNS['g3dMark'], Literal(cur_val["g3d_mark"], datatype=XSD.integer)))

        try:
            if len(cur_val['gpu_chip']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['gpuChip'], Literal(cur_val['gpu_chip'], lang="en")))
        except:
            pass

        try:
            if len(cur_val['bus_info']) != 0:
                self.my_kg.add((cur_uri, self.MGNS['bus'], Literal(cur_val['bus_info'], lang="en")))
        except:
            pass

        try:
            if cur_val['released_year'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['datePublished'], Literal(cur_val['released_year'])))
        except:
            pass

        try:
            if cur_val['memory_val_mb'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['gpuMemorySize_MB'], Literal(cur_val['memory_val_mb'])))

            if len(cur_val["memory_type"]) != 0:
                self.my_kg.add((cur_uri, self.MGNS['gpuMemoryType'], Literal(cur_val["memory_type"], lang="en")))

            if cur_val['memory_bits'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['gpuMemoryBits'], Literal(cur_val['memory_bits'])))
        except:
            pass

        try:
            if cur_val['gpu_clock_mhz'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['gpuClockSpeed_MHz'], Literal(cur_val['gpu_clock_mhz'])))
        except:
            pass

        try:
            if cur_val['memory_clock_mhz'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['memoryClockSpeed_MHz'], Literal(cur_val['memory_clock_mhz'])))
        except:
            pass

        try:
            if cur_val['shader_1'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['shader_1'], Literal(cur_val['shader_1'])))
        except:
            pass

        try:
            if cur_val['shader_2'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['shader_2'], Literal(cur_val['shader_2'])))
        except:
            pass

        try:
            if cur_val['tmus'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['TMUs'], Literal(cur_val['tmus'])))
        except:
            pass

        try:
            if cur_val['rops'] != -1:
                self.my_kg.add((cur_uri, self.MGNS['ROPs'], Literal(cur_val['rops'])))
        except:
            pass

    def addMSDInstance(self, cur_cpu_uri, cur_gpu_uri, memory_val, disk_space_val):
        cur_msd_node = BNode()
        cur_cpu_uri = self.__generateShortURI(cur_cpu_uri)
        cur_gpu_uri = self.__generateShortURI(cur_gpu_uri)
        self.my_kg.add((cur_msd_node, RDF.type, self.msd_global))
        self.my_kg.add((cur_msd_node, self.MGNS['processor'], URIRef(self.MGNS[cur_cpu_uri])))
        self.my_kg.add((cur_msd_node, self.MGNS['graphics'], URIRef(self.MGNS[cur_gpu_uri])))
        self.my_kg.add((cur_msd_node, self.MGNS['memory_MB'], Literal(memory_val)))
        self.my_kg.add((cur_msd_node, self.MGNS['diskSpace_MB'], Literal(disk_space_val)))
        return cur_msd_node

    def addGameModeInstance(self, game_mode_instance):
        # cur_uri = URIRef(self.MGNS[list(enterprise_instance.keys())[0]])
        # should we create a single uri
        cur_val = list(game_mode_instance.values())[0]
        try:
            for mode in cur_val['game_modes']:
                cur_uri = URIRef(self.MGNS[self.__generateURIfromString(mode)])
                self.my_kg.add((cur_uri, RDF.type, self.game_mode_global))
                self.my_kg.add((cur_uri, RDFS.label, Literal(mode, lang="en")))
        except:
            pass

    def addGenreInstance(self, genre_instance):
        cur_val = list(genre_instance.values())[0]
        try:
            for genre in cur_val['genre']:
                cur_uri = URIRef(self.MGNS[self.__generateURIfromString(genre)])
                self.my_kg.add((cur_uri, RDF.type, self.genre_global))
                self.my_kg.add((cur_uri, RDFS.label, Literal(genre, lang='en')))
        except:
            pass

    def addThemeInstance(self, theme_instance):
        cur_val = list(theme_instance.values())[0]
        try:
            for theme in cur_val['themes']:
                cur_uri = URIRef(self.MGNS[self.__generateURIfromString(theme)])
                self.my_kg.add((cur_uri, RDF.type, self.theme_global))
                self.my_kg.add((cur_uri, RDFS.label, Literal(theme, lang='en')))
        except:
            pass

    def addGameInstance(self, igdb_game_id, igdb_game, g2a_game, gpu_list, cpu_list, er_platform, er_publisher,
                        er_developer):
        cur_uri = self.__generateShortURI(igdb_game_id)
        cur_uri = URIRef(self.MGNS[cur_uri])
        self.my_kg.add((cur_uri, RDF.type, self.game_global))
        # add game name
        self.my_kg.add((cur_uri, self.SCHEMA['name'], Literal(igdb_game['game_name'], lang='en')))
        try:
            # add game summary
            if len(igdb_game['game_summary']) != 0:
                self.my_kg.add((cur_uri, self.SCHEMA['description'], Literal(igdb_game['game_summary'], lang='en')))
        except:
            pass

        try:
            # add game url
            self.my_kg.add((cur_uri, self.SCHEMA['url'], Literal(igdb_game['url'])))
        except:
            pass

        try:
            # add release date
            self.my_kg.add((cur_uri, self.SCHEMA['datePublished'], Literal(int(igdb_game['release_date'][:4]), datatype=XSD.integer)))
        except:
            pass

        try:
            if len(er_platform) != 0:
                for platform in er_platform:
                    platform = self.__generateShortURI(platform)
                    self.my_kg.add((cur_uri, self.MGNS['supportedPlatform'], URIRef(self.MGNS[platform])))
        except:
            pass

        try:
            # Link Developer
            for comp in er_developer:
                comp = self.__generateShortURI(comp)
                self.my_kg.add((cur_uri, self.MGNS['developedBy'], URIRef(self.MGNS[comp])))

        except:
            pass

        try:
            # Link publisher
            for comp in er_publisher:
                comp = self.__generateShortURI(comp)
                self.my_kg.add((cur_uri, self.MGNS['publishedBy'], URIRef(self.MGNS[comp])))
        except:
            pass

        try:
            # game mode
            for game_mode in igdb_game['game_modes']:
                self.my_kg.add(
                    (cur_uri, self.MGNS['hasGameMode'], URIRef(self.MGNS[self.__generateURIfromString(game_mode)])))
        except:
            pass

        try:
            # game genre
            for genre in igdb_game['genre']:
                self.my_kg.add((cur_uri, self.MGNS['hasGenre'], URIRef(self.MGNS[self.__generateURIfromString(genre)])))
        except:
            pass

        try:
            # link game theme
            for theme in igdb_game['themes']:
                self.my_kg.add((cur_uri, self.MGNS['hasTheme'], URIRef(self.MGNS[self.__generateURIfromString(theme)])))
        except:
            pass

        try:
            # Rating Value
            try:
                rating_val = float(igdb_game['game_rating'])
            except:
                rating_val = -1
            self.my_kg.add((cur_uri, self.MGNS['ratingValue'], Literal(rating_val, datatype=XSD.decimal)))
        except:
            pass

        try:
            # Rating Count
            try:
                rating_cnt = int(igdb_game['num_rating_counts'])
            except:
                rating_cnt = -1
            self.my_kg.add(
                (cur_uri, self.MGNS['ratingCount'], Literal(rating_cnt, datatype=XSD.integer)))
        except:
            pass

        try:
            # Best Rating
            self.my_kg.add((cur_uri, self.MGNS['bestRating'], Literal(100, datatype=XSD.decimal)))
        except:
            pass

        try:
            # Seller
            self.my_kg.add(
                (cur_uri, self.MGNS['soldBy'], URIRef(self.MGNS[self.__generateURIfromString(g2a_game['seller_name'])])))
        except:
            pass
        try:
            # Link game best price
            cur_price = float(g2a_game['seller_price'].split()[0])
            self.my_kg.add((cur_uri, self.MGNS['price_USD'], Literal(cur_price, datatype=XSD.decimal)))
        except:
            pass

        try:
            # Link game old price
            cur_price = float(g2a_game['seller_old_price'].split()[0])
            self.my_kg.add((cur_uri, self.MGNS['old_price_USD'], Literal(cur_price, datatype=XSD.decimal)))
        except:
            pass

        try:
            # Link discount provided
            cur_discount = float(g2a_game['seller_discount'].split("%")[0])
            self.my_kg.add((cur_uri, self.MGNS['discount_percent'], Literal(cur_discount, datatype=XSD.decimal)))
        except:
            pass

        try:
            # Seller Feedback message
            cur_feedback = g2a_game['seller_feedback_msg']
            if cur_feedback is None:
                cur_feedback_val = 0
            elif cur_feedback == "Positive feedback":
                cur_feedback_val = 1

            self.my_kg.add((cur_uri, self.MGNS['sellerFeedback'], Literal(cur_feedback_val, datatype=XSD.integer)))
        except:
            pass

        try:
            # Seller URL
            self.my_kg.add((cur_uri, self.MGNS['sellerURL'], Literal(g2a_game['url'])))
        except:
            pass

        try:
            disk_space = g2a_game["min_requirements"]["Disk space"]
            disk_space_val = self.__convertSizeToMB(disk_space)
            memory = g2a_game["min_requirements"]["Memory"]
            memory_val = self.__convertSizeToMB(memory)

            for cur_cpu_uri in cpu_list:
                for cur_gpu_uri in gpu_list:
                    cur_msd_node = self.addMSDInstance(cur_cpu_uri, cur_gpu_uri, memory_val, disk_space_val)
                    self.my_kg.add((cur_uri, self.MGNS["hasMSD"], cur_msd_node))
        except:
            pass


def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict


def createMAPforGPU(json_lines_file):
    score_threshold = 0.60
    result_dict = {}
    count = 0
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = cur_dict["g2a_games_id"]
            val = []

            gpu1 = cur_dict["tpowerup_gpu1"]
            gpu2 = cur_dict["tpowerup_gpu2"]
            flag = 0
            if bool(gpu1):
                if gpu1["max_score"] >= score_threshold:
                    val.append(gpu1["max_match_id"])
                    flag = 1

            if bool(gpu2):
                if gpu2["max_score"] >= score_threshold:
                    val.append(gpu2["max_match_id"])
                    flag = 1

            if flag == 1:
                count += 1
            result_dict[key] = val

    print("Num matches for GPU = ", count)
    return result_dict


def createMAPforCPU(json_lines_file):
    score_threshold = 1.2
    result_dict = {}
    count = 0
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = cur_dict["g2_games_id"]
            val = []

            cpu1 = cur_dict["tpowerup_cpu1"]
            cpu2 = cur_dict["tpowerup_cpu2"]
            flag = 0
            if bool(cpu1):
                if cpu1["max_match_score"] >= score_threshold:
                    val.append(cpu1["max_match_id"])
                    flag = 1

            if bool(cpu2):
                if cpu2["max_match_score"] >= score_threshold:
                    val.append(cpu2["max_match_id"])
                    flag = 1

            if flag == 1:
                count += 1
            result_dict[key] = val

    print("Num matches for CPU = ", count)
    # print(result_dict)
    return result_dict


def createMAPforplatform(json_lines_file):
    result_dict = {}
    with jsonlines.open(json_lines_file) as reader:
        for obj in reader:
            key, val = list(obj.items())[0][0], list(obj.items())[0][1]
            result_dict[key] = val
    return result_dict


def createMAPforpublisher_developer(json_lines_file):
    publisher_dict = {}
    developer_dict = {}
    with jsonlines.open(json_lines_file) as reader:
        for obj in reader:
            key, val = list(obj.items())[0][0], list(obj.items())[0][1]
            publisher_dict[key] = val['publisher']
            developer_dict[key] = val['developer']
    return publisher_dict, developer_dict


if __name__ == "__main__":
    my_game_kg = GameKG()
    my_game_kg.define_namespaces()
    my_game_kg.define_ontology()
    batch_size_timer = 1000

    start_time = time.time()
    count = 0
    igdb_companies_file = "../../data_with_ids/igdb_companies.jl"
    with open(igdb_companies_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addEnterpriseInstance(cur_dict)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("1. IGDB Companies - Seconds Elapsed = ", seconds_elapsed)

    count = 0
    igdb_platforms_file = "../../data_with_ids/igdb_platforms.jl"
    with open(igdb_platforms_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addPlatformInstance(cur_dict)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("2. IGDB Platforms - Seconds Elapsed = ", seconds_elapsed)

    count = 0
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs_cleaned_with_scores.jl"
    with open(techpowerup_gpu_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addGraphicsInstance(cur_dict)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("3. Techpowerup GPUs - Seconds Elapsed = ", seconds_elapsed)

    count = 0
    techpowerup_cpu_file = "../../data_with_ids/techpowerup_cpu_cleaned_along_with_benchmark_scores.jl"
    with open(techpowerup_cpu_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addProcessorInstance(cur_dict)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("4. Techpowerup CPUs - Seconds Elapsed = ", seconds_elapsed)

    # Adding Games:
    g2a_games_file = "../../data_with_ids/g2a_games_with_requirements.jl"
    igdb_games_file = "../../data_with_ids/igdb_games.jl"
    er_g2a_igdb_file = "../../data_er/ER_g2a_games_igdb_games.jl"
    er_g2a_gpu_file = "../../data_er/ER_g2a_games_gpus_and_techpowerup_gpus.jl"
    er_g2a_cpu_file = "../../data_er/ER_g2a_game_cpus_techpowerup_cpus.jl"
    platform_file = '../../data_er/ER_platforms.jl'
    companies_file = '../../data_er/ER_companies.jl'

    # Adding "game mode class", "genre class", "theme class"
    count = 0
    with open(igdb_games_file, 'r') as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addGameModeInstance(cur_dict)
            my_game_kg.addGenreInstance(cur_dict)
            my_game_kg.addThemeInstance(cur_dict)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("5. IGDB Game modes, Genres, Themes - Seconds Elapsed = ", seconds_elapsed)

    # Adding "seller class"
    count = 0
    with open(g2a_games_file, 'r') as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            my_game_kg.addSellerInstance(cur_dict)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("6. G2A Sellers - Seconds Elapsed = ", seconds_elapsed)

    g2a_games = constructDictfromJL(g2a_games_file)
    igdb_games = constructDictfromJL(igdb_games_file)
    er_g2a_gpu = createMAPforGPU(er_g2a_gpu_file)
    er_g2a_cpu = createMAPforCPU(er_g2a_cpu_file)
    er_platform = createMAPforplatform(platform_file)
    er_publisher, er_developer = createMAPforpublisher_developer(companies_file)

    count = 0
    with open(er_g2a_igdb_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)

            igdb_game_id = cur_dict["igdb_key"]
            igdb_game = igdb_games[igdb_game_id]

            try:
                g2a_game_id = cur_dict["similar_g2a_key"]
                g2a_game = g2a_games[g2a_game_id]
            except:
                g2a_game = {}

            try:
                gpu_list = er_g2a_gpu[g2a_game_id]
            except:
                gpu_list = []

            try:
                cpu_list = er_g2a_cpu[g2a_game_id]
            except:
                cpu_list = []

            try:
                platforms = er_platform[igdb_game_id]
            except:
                platforms = []

            try:
                publishers = er_publisher[igdb_game_id]
            except:
                publishers = []

            try:
                developers = er_developer[igdb_game_id]
            except:
                developers = []

            my_game_kg.addGameInstance(igdb_game_id, igdb_game, g2a_game, gpu_list, cpu_list, platforms,
                                       publishers, developers)
            count += 1
            if count % batch_size_timer == 0:
                print("Progress cnt = ", count)

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("7. IGDB Games - Seconds Elapsed = ", seconds_elapsed)

    my_game_kg.storeKG("Game_KG.ttl")
