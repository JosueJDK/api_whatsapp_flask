from WhatsAppClass.WhatsApp import WhatsApp
from typing import Dict, Any, List

class WhatsAppMessage(WhatsApp):
    def __init__(self, token, phone_number_id):
        super().__init__(token, phone_number_id)
    
    def send_message_text(self, message, recipient_id, recipient_type="individual", preview_url=True):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        return super().send_message(recipient_id, 'Text', data)
    
    def send_message_location(self, lat, long, name, address, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "location",
            "location": {
                "latitude": lat,
                "longitude": long,
                "name": name,
                "address": address,
            },
        }
        return super().send_message(recipient_id, 'Location', data)
    
    def send_message_image(self, image, recipient_id, recipient_type="individual", caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": image, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"id": image, "caption": caption},
            }
        return super().send_message(recipient_id, 'Image', data)
    
    def send_message_audio(self, audio, recipient_id, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"link": audio},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"id": audio},
            }
        return super().send_message(recipient_id, 'Audio', data)
    
    def send_message_video(self, video, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"link": video, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"id": video, "caption": caption},
            }
        return super().send_message(recipient_id, 'Video', data)
    
    def send_message_document(self, document, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"link": document, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"id": document, "caption": caption},
            }
        return super().send_message(recipient_id, 'Document', data)
    
    def send_message_contact(self, contacts: List[Dict[Any, Any]], recipient_id: str):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "contacts",
            "contacts": contacts,
        }
        return super().send_message(recipient_id, 'Contact', data)
    
    def send_message_template(self, template, recipient_id, lang="en_US", components={}):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template,
                "language": {"code": lang},
                "components": components,
            },
        }
        return super().send_message(recipient_id, 'Template', data)
    
    def send_message_templatev2(self, template, recipient_id, components, lang="en_US"):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template,
                "language": {"code": lang},
                "components": components,
            },
        }
        return super().send_message(recipient_id, 'Template V2.', data)

    def send_message_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button(button),
        }
        return super().send_message(recipient_id, 'Button', data)
    
    def send_reply_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": button,
        }
        return super().send_message(recipient_id, 'Reply Button', data)