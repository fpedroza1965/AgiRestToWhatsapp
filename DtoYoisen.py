from DtoModel import *


class DtoYoisen(DtoModel):

    def get_model_hsm_without_buttons_and_tags(self,
                          serviceId=None,
                          phoneNumber=None,
                          text=None,
                          hsmElementName=None,
                          hsmNamespace=None,
                          hsmLanguage=None,
                          hsmHeader=None,
                          hsmBodyParam1=None,
                          hsmBodyParam2=None):

        return json.dumps( { 
            "serviceId": serviceId, 
            "phoneNumber": phoneNumber, 
            "text": text, 
            "hsm": { 
                "elementName": hsmElementName, 
                "namespace": hsmNamespace, 
                "language": hsmLanguage, 
                "header": hsmHeader, 
                "body": { "1": hsmBodyParam1, "2": hsmBodyParam2}
                }
            })

    def get_headers(self, contentType=None):

        return json.dumps({
            "Content-Type": contentType
        })