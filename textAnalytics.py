import http.client, urllib.request, urllib.parse, urllib.error, base64, json

class TextAnalytics:

    def __init__(self):
        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': 'c00b9969c9c24f2796b66918ba0e856b',
        }
        self.params = urllib.parse.urlencode({})
        self.url = "westus.api.cognitive.microsoft.com"

    def getKeyPhrases(self, text):

        try:
            conn = http.client.HTTPSConnection(self.url)
            body = { "documents" : [{"language" : "en", "id" : "1", "text" : text}] }
            conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % self.params, json.dumps(body), self.headers)
            response = conn.getresponse()
            json_obj = json.loads(response.read().decode('utf-8'))
            # print(json_obj)
            return json_obj["documents"][0]["keyPhrases"]
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
