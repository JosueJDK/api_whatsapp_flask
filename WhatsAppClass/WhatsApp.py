import os
import requests
import logging
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder

class WhatsApp(object):
    
    def __init__(self, token, phone_number_id):
        self._token = token
        self._phone_number_id = phone_number_id
        self._base_url = "https://graph.facebook.com/v14.0"
        self._url = f"{self._base_url}/{self._phone_number_id}/messages"
        self._headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self._token),
            }    
    
    def send_message(self, recipient_id, type_message, data):
        logging.info(f"Sending Message {type_message} to {recipient_id}")
        response = requests.post(self._url, headers=self._headers, json=data)
        if response.status_code == 200:
            logging.info(f"Message sent to {recipient_id}")
            return response.json()
        logging.info(f"Message not sent to {recipient_id}")
        logging.info(f"Status code: {response.status_code}")
        logging.error(response.json())
        return response.json()

    def reply_to_message(self, message_id: str, recipient_id: str, message: str, preview_url: bool = True):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "text",
            "context": {"message_id": message_id},
            "text": {"preview_url": preview_url, "body": message},
        }

        logging.info(f"Replying to {message_id}")
        response = requests.post(f"{self._url}", headers=self._headers, json=data)
        if response.status_code == 200:
            logging.info(f"Message sent to {recipient_id}")
            return response.json()
        logging.info(f"Message not sent to {recipient_id}")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.json()}")
        return response.json()
    
    def updaload_media(self, media: str):
        form_data = {
            "file": (
                media,
                open(os.path.realpath(media), "rb"),
                mimetypes.guess_type(media)[0],
            ),
            "messaging_product": "whatsapp",
            "type": mimetypes.guess_type(media)[0],
        }
        form_data = MultipartEncoder(fields=form_data)
        headers = self._headers.copy()
        headers["Content-Type"] = form_data.content_type
        logging.info(f"Content-Type: {form_data.content_type}")
        logging.info(f"Uploading media {media}")
        response = requests.post(
            f"{self._base_url}/{self._phone_number_id}/media",
            headers=self._headers,
            data=form_data,
        )
        if response.status_code == 200:
            logging.info(f"Media {media} uploaded")
            return response.json()
        logging.info(f"Error uploading media {media}")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.json()}")
        return None
    
    def delete_media(self, media_id: str):
        logging.info(f"Deleting media {media_id}")
        response = requests.delete(f"{self._base_url}/{media_id}", headers=self.headers)
        if response.status_code == 200:
            logging.info(f"Media {media_id} deleted")
            return response.json()
        logging.info(f"Error deleting media {media_id}")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.json()}")
        return None
    
    def query_media_url(self, media_id: str):
        logging.info(f"Querying media url for {media_id}")
        response = requests.get(f"{self._base_url}/{media_id}", headers=self._headers)
        if response.status_code == 200:
            logging.info(f"Media url queried for {media_id}")
            return response.json()["url"]
        logging.info(f"Media url not queried for {media_id}")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.json()}")
        return None
    
    def download_media(self, media_url: str, mime_type: str, file_path: str = "temp"):
        response = requests.get(media_url, headers=self._headers)
        content = response.content
        extension = mime_type.split("/")[1]
        # create a temporary file
        try:

            save_file_here = (
                f"{file_path}.{extension}" if file_path else f"temp.{extension}"
            )
            with open(save_file_here, "wb") as f:
                f.write(content)
            logging.info(f"Media downloaded to {save_file_here}")
            return f.name
        except Exception as e:
            print(e)
            logging.info(f"Error downloading media to {save_file_here}")
            return None