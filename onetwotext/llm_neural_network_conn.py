"""Module that expose functionality to call a LLM neural network from prompt to obtain response"""

from json import loads
from queue import Queue, Empty
from re import findall
from threading import Thread
from typing import Generator, Optional
from curl_cffi import requests
from fake_useragent import UserAgent

from onetwotext.config_data.ott_data import get_ott_data


class Completion:
    """Class to hold methods to create correct requests for a LLM API


    Methods
    -------
    * request:
        function to create correct request for a LLM Neural Network API

    * create:
        Function to create request with acceptance criteria for LLM API

    * handle_stream_response:
        The method that handle response from API

    """

    # experimental
    part1 = '{"role":"assistant","id":"chatcmpl'
    part2 = '"},"index":0,"finish_reason":null}]}}'
    regex = rf"{part1}(.*){part2}"

    timer = None
    message_queue = Queue()
    stream_completed = False
    last_msg_id = None

    @staticmethod
    def request(prompt: str, proxy: Optional[str] = None):
        """function to create correct request for a LLM Neural Network API

        Input:
        ------

         - prompt: str
           text body of the request.
         - proxy: str
           proxy to send request.
        """

        ott_data = get_ott_data()

        headers = {
            "authority": ott_data.links.authority,
            "content-type": "application/json",
            "origin": ott_data.links.origin,
            "user-agent": UserAgent().random,
        }

        proxies = (
            {"http": "http://" + proxy, "https": "http://" + proxy} if proxy else None
        )

        options = {}
        if Completion.last_msg_id:
            options["parentMessageId"] = Completion.last_msg_id

        requests.post(
            ott_data.links.api,
            headers=headers,
            proxies=proxies,
            content_callback=Completion.handle_stream_response,
            json={"prompt": prompt, "options": options},
        )

        Completion.stream_completed = True

    @staticmethod
    def create(prompt: str, proxy: Optional[str] = None) -> Generator[str, None, None]:
        """Function to create request with acceptance criteria for LLM API

        Input:
        ------

         - prompt: str
           text body of the request.
         - proxy: str
           proxy to send request.
        """

        Completion.stream_completed = False

        Thread(target=Completion.request, args=[prompt, proxy]).start()

        while not Completion.stream_completed or not Completion.message_queue.empty():
            try:
                message = Completion.message_queue.get(timeout=0.01)
                for message in findall(Completion.regex, message):
                    message_json = loads(Completion.part1 + message + Completion.part2)
                    Completion.last_msg_id = message_json["id"]
                    yield message_json["delta"]

            except Empty:
                pass

    @staticmethod
    def handle_stream_response(response):
        """The method that handle response from API"""

        Completion.message_queue.put(response.decode())
