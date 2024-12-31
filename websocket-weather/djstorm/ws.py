# from devtools import debug
import json

from django_ws import WebSocketHandler

from djstorm.models import WeatherPoint


class WeatherSocket(WebSocketHandler):
    async def on_open(self):
        self.current_location = None
        self.start_ping()

    async def on_message(self, data):
        print(data)
        if "location" in data:
            if "send_weather" in self.tasks:
                self.tasks["send_weather"].cancel()

            self.current_location = "{},{}".format(*data["location"])
            # print(f"current_location {self.current_location}")
            self.start_task("send_weather", self.send_weather)

        else:
            print("Unknown message:", data)

    async def on_close(self):
        print("Connection Closed, Tasks Cancelled")

    async def on_error(self, error):
        print("ERROR", error)

    async def _send_weather(self):
        if self.current_location:
            wp = await WeatherPoint.objects.filter(point=self.current_location).afirst()
            if wp:
                print("SENDING", wp.weather_data["current"])
                await self.send({"weather": wp.weather_data["current"]})

    async def send_weather(self):
        await self._send_weather()
        await self.sleep_loop(self._send_weather, 60 * 1)


class WeatherSocket2(WebSocketHandler):
    async def on_open(self):
        self.current_location = None
        self.start_ping()

    async def on_message(self, data):
        print(data)
        print(type(data))
        print("location" in data)
        if "location" in data:
            print("location in data...")
            if "send_weather" in self.tasks:
                print("lsend_weather in tasks...")
                self.tasks["send_weather"].cancel()

            # self.current_location = "{},{}".format(*data["location"])
            self.current_location = data["location"]
            print(f"current_location --> {self.current_location}")
            self.start_task("send_weather", self.send_weather)

        else:
            print("Unknown message:", data)

    async def on_close(self):
        print("Connection Closed, Tasks Cancelled")

    async def on_error(self, error):
        print("ERROR", error)

    async def send(self, data):
        if isinstance(data, str):
            to_send = {"type": "websocket.send", "text": data}
        else:
            to_send = {"type": "websocket.send", "text": json.dumps(data)}
        print("SEND...", to_send)
        await self._send(to_send)

    async def _send_weather(self):
        print("__send_weather... 1")
        print(f"__send_weather... current_location: {self.current_location}")
        if self.current_location:
            print("__send_weather... 2")
            print(f"__send_weather... 3 current_location --> {self.current_location}")
            wp = await WeatherPoint.objects.filter(point=self.current_location).afirst()
            print(f"_send_weather - wp: {wp}")
            if wp:
                print("SENDING", wp.weather_data["current"])
                content = """
                    <div hx-swap-oob="beforeend:#content">
                    <p>{weather}</p>
                    </div>
                """
                await self.send(content.format(weather=str(wp.weather_data["current"])))

    async def send_weather(self):
        print("send_weather.. 1")
        await self._send_weather()
        print("send_weather.. 2")
        await self.sleep_loop(self._send_weather, 60 * 1)
