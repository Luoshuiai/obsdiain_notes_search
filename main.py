# -*- coding: utf-8 -*-

import sys, os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
import webbrowser
from obs import obsidian


class HelloWorld(FlowLauncher):

    def query(self, query):
        ob1 = obsidian()
        results = []
        if query:
            notes = ob1.search_notes(query)
            for note in notes:
                results.append({
                    "Title": note.note_title,
                    "SubTitle": 'Vault:' + note.vault_name,
                    "IcoPath": "Images/icon.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": [f"{note.open_link}"],
                    }
                })
        return results

    def context_menu(self, data):
        return [
            {
                "Title": "Hello World Python's Context menu",
                "SubTitle": "Press enter to open Flow the plugin's repo in GitHub",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
                }
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    HelloWorld()
