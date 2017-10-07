import json
import unittest

import app


class DownloaderTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.headers = {
            "Authorization": "Basic VVNFUk5BTUU6UEFTU1dPUkQ=",
            "Content-Type": "application/json"
        }

    def test_general_download(self):
        tmp = self.app.post("/", data=json.dumps(dict(
            url="https://mrose.org/cc/png-test.png",
            name="test png",
            category="test"
        )), headers=self.headers)
        assert tmp.status_code == 200

    def test_download_without_auth(self):
        tmp = self.app.post("/", data=json.dumps(dict(
            url="https://mrose.org/cc/png-test.png"
        )), headers={
            "Content-Type": "application/json"
        })
        assert tmp.status_code == 401

    def wrong_download(self, headers):
        return self.app.post("/", data=json.dumps(dict(
            url="https://mrose.org/cc/png-test.png"
        )), headers=headers)

    def test_download_with_wrong_auth(self):
        tmp = self.wrong_download(headers={
            "Authorization": "Basic VVNFUk5BTUUyOlBBU1NXT1JEMg==",
            "Content-Type": "application/json"
        })
        assert tmp.status_code == 401

    def test_download_without_content_type(self):
        tmp = self.wrong_download(headers={
            "Authorization": "Basic VVNFUk5BTUU6UEFTU1dPUkQ="
        })
        assert tmp.status_code == 500

    def download_youtube(self):
        return self.app.post("/", data=json.dumps(dict(
            url="https://www.youtube.com/watch?v=Pfq8f59u3kk"
        )), headers=self.headers)

    def test_youtubedl_crash(self):
        ydl_tmp = app.ydl
        app.ydl = None
        tmp = self.download_youtube()
        assert tmp.status_code == 500
        app.ydl = ydl_tmp

    def test_youtubedl(self):
        tmp = self.download_youtube()
        assert tmp.status_code == 200

    def test_pushbullet_crash(self):
        oldKey = app.conf["users"][0]["pushbullet_token"]
        app.conf["users"][0]["pushbullet_token"] = "Invalid"
        tmp = app.on_complete("USERNAME", "test")
        assert tmp is False
        app.conf["users"][0]["pushbullet_token"] = oldKey

    def test_pushbullet(self):
        tmp = app.on_complete("USERNAME", "test")
        assert tmp is True


if __name__ == "__main__":
    unittest.main()
