import os
import logging
from WhatsAppClass.WhatsAppMessage import WhatsAppMessage
from WhatsAppClass.WhatsAppGetMessages import WhatsAppGetMessages
from dotenv import load_dotenv
from flask import Flask, request, make_response

# Initialize Flask App
app = Flask(__name__)

# Load .env file
load_dotenv()
send_messages = WhatsAppMessage(os.getenv("TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID"))
get_messages = WhatsAppGetMessages()

VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.route("/webhooks", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            logging.info("Verified webhook")
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        logging.error("Webhook Verification failed")
        return "Invalid verification token"

    # Handle Webhook Subscriptions
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    changed_field = get_messages.changed_field(data)
    if changed_field == "messages":
        new_message = get_messages.get_mobile(data)
        if new_message:
            mobile = get_messages.get_mobile(data)
            name = get_messages.get_name(data)
            message_type = get_messages.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = get_messages.get_message(data)
                name = get_messages.get_name(data)
                logging.info("Message: %s", message)
                send_messages.send_message_text(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                message_response = get_messages.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = get_messages.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                image = get_messages.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = send_messages.query_media_url(image_id)
                image_filename = send_messages.download_media(image_url, mime_type)
                print(f"{mobile} sent image {image_filename}")
                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "document":
                document = get_messages.get_document(data)
                document_id, mime_type = document["id"], document["mime_type"]
                document_url = send_messages.query_media_url(document_id)
                document_filename = send_messages.download_media(document_url, mime_type)
                print(f"{mobile} sent document {document_filename}")
                logging.info(f"{mobile} sent document {document_filename}")

            elif message_type == "video":
                video = get_messages.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = send_messages.query_media_url(video_id)
                video_filename = send_messages.download_media(video_url, mime_type)
                print(f"{mobile} sent video {video_filename}")
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = get_messages.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = send_messages.query_media_url(audio_id)
                audio_filename = send_messages.download_media(audio_url, mime_type)
                print(f"{mobile} sent audio {audio_filename}")
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "file":
                file = get_messages.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = send_messages.query_media_url(file_id)
                file_filename = send_messages.download_media(file_url, mime_type)
                print(f"{mobile} sent file {file_filename}")
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = get_messages.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"


if __name__ == "__main__":
    app.run(port=5000, debug=False)
