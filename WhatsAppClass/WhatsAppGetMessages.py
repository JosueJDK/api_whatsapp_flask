class WhatsAppGetMessages(object):

    def preprocess(self, data):
        return data["entry"][0]["changes"][0]["value"]
    
    def get_mobile(self, data):
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]

    def get_name(self, data):
        contact = self.preprocess(data)
        if contact:
            return contact["contacts"][0]["profile"]["name"]
    
    def get_message(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["text"]["body"]

    def get_message_id(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["id"]

    def get_message_timestamp(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["timestamp"]

    def get_interactive_response(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "interactive" in data["messages"][0]:
                return data["messages"][0]["interactive"]
    
    def get_location(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "location" in data["messages"][0]:
                return data["messages"][0]["location"]
    
    def get_image(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "image" in data["messages"][0]:
                return data["messages"][0]["image"]
               
    def get_document(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "document" in data["messages"][0]:
                return data["messages"][0]["document"]

    def get_audio(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "audio" in data["messages"][0]:
                return data["messages"][0]["audio"]

    def get_video(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "video" in data["messages"][0]:
                return data["messages"][0]["video"]

    def get_message_type(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["type"]

    def get_delivery(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["status"]

    def changed_field(self, data):
        return data["entry"][0]["changes"][0]["field"]
